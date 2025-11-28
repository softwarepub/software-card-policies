# SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import pathlib
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Tuple

from pyshacl import validate
from rdflib import BNode, Graph, Literal, Node
from rdflib.collection import Collection
from rdflib.namespace import RDF, RDFS, SH, XSD
from rdflib.term import URIRef

from sc_validate.namespaces import PREFIXES, SC
from sc_validate.rdf_helpers import get_language_tagged_literal

#################################### Software CaRD ####################################


@dataclass
class Parameter:
    """Model of a `sc:Parameter`."""

    uri: URIRef
    outer_type: URIRef
    inner_type: URIRef
    default_value: URIRef
    config_path: str

    @classmethod
    def from_graph(cls, reference: URIRef, graph: Graph):
        return cls(
            uri=reference,
            outer_type=graph.value(reference, SC.parameterOuterType, None),
            inner_type=graph.value(reference, SC.parameterInnerType, None),
            default_value=graph.value(reference, SC.parameterDefaultValue, None),
            config_path=str(graph.value(reference, SC.parameterConfigPath, None)),
        )


# TODO: This only works for constraints of type NodeShape. Is this enough?
@dataclass
class Policy:
    """Model of a Software CaRD Policy."""

    name: str
    description: str

    @classmethod
    def from_graph(cls, reference: URIRef, graph: Graph):
        return cls(
            name=get_language_tagged_literal(graph, reference, SH.name),
            description=get_language_tagged_literal(graph, reference, SH.description),
        )


######################################## SHACL ########################################


class SeverityLevel(Enum):
    """Model for severity levels."""

    INFO = 1
    WARNING = 2
    VIOLATION = 3
    OTHER = 4

    def __str__(self):
        return self.name.title()

    @classmethod
    def from_graph(cls, reference: URIRef, graph: Graph):
        if reference == SH.Info:
            return cls.INFO
        if reference == SH.Warning:
            return cls.WARNING
        if reference == SH.Violation:
            return cls.VIOLATION
        return cls.OTHER


@dataclass
class Severity:
    """Model of `sh:Severity`."""

    label: str
    comment: str
    level: SeverityLevel

    # TODO: ``rdfs:label`` is ``None`` for SHACL's builtin severities. They exist in the
    # SHACL source but the validator doesn't put them into the graph. Should we do it?
    def __str__(self):
        return self.label if self.label else str(self.level)

    @classmethod
    def from_graph(cls, reference: URIRef, graph: Graph):
        return cls(
            label=get_language_tagged_literal(graph, reference, RDFS.label),
            comment=get_language_tagged_literal(graph, reference, RDFS.comment),
            level=SeverityLevel.from_graph(reference, graph),
        )


@dataclass
class ValidationResult:
    """Model of a `sh:ValidationResult`."""

    severity: Severity
    message: str
    source_policy: Policy

    @classmethod
    def from_graph(cls, reference: URIRef, graph: Graph):
        severity = graph.value(reference, SH.resultSeverity, None)
        source_policy = graph.value(reference, SH.sourceShape, None)
        return cls(
            severity=Severity.from_graph(severity, graph),
            message=get_language_tagged_literal(graph, reference, SH.resultMessage),
            source_policy=Policy.from_graph(source_policy, graph),
        )


@dataclass
class ValidationReport:
    """Model of a `sh:ValidationReport`."""

    conforms: bool
    results: List[ValidationResult]

    @classmethod
    def from_graph(cls, reference: URIRef, graph: Graph):
        results = graph.objects(reference, SH.result)
        return cls(
            conforms=(reference, SH.conforms, Literal(True)) in graph,
            results=[ValidationResult.from_graph(result, graph) for result in results],
        )


################################## Graph Interaction ##################################

# TODO: Add debug messages to all asserts.
# TODO: Check allowed inner and outer types.

_ALLOWED_INNER_TYPES = (
    XSD.string,
    XSD.boolean,
    XSD.integer,
    XSD.int,
    XSD.decimal,
    XSD.float,
    XSD.double,
    XSD.anyURI,
)


def read_rdf_resource(source: pathlib.Path | str) -> Graph:
    graph = Graph()
    graph.parse(source)
    for prefix, iri in PREFIXES.items():
        graph.bind(prefix, iri)
    return graph


def _create_rdf_list_parameter(
    parameter: Parameter, graph: Graph, config_parameter: Any
) -> Node:
    assert parameter.outer_type == RDF.List
    # assert (parameter.default_value, RDF.type, RDF.List) in graph
    assert (parameter.default_value, RDF.first, None) in graph
    assert (parameter.default_value, RDF.rest, None) in graph

    if config_parameter is None:
        return Collection(graph, parameter.default_value).uri

    # TODO: What happens if `parameter_value` is empty list?
    assert isinstance(config_parameter, list)
    return Collection(
        graph, BNode(), seq=[Literal(value) for value in config_parameter]
    ).uri


def _create_sc_scalar_parameter(
    parameter: Parameter, graph: Graph, config_parameter: Any
) -> Node:
    assert parameter.outer_type == SC.Scalar

    assert isinstance(config_parameter, (str, int, float, type(None)))

    if config_parameter:
        return Literal(config_parameter)

    return graph.value(parameter.uri, SC.parameterDefaultValue, None)


# TODO: Is it safe to modify the graph while iterating over it?
def parameterize_graph(graph: Graph, config_parameters: Dict[str, Any]) -> Graph:
    # iterate over all declared parameters of type `sc:Parameter`
    for parameter_ref in graph.subjects(RDF.type, SC.Parameter):
        parameter = Parameter.from_graph(parameter_ref, graph)

        inner_type_is_primitive = parameter.inner_type in _ALLOWED_INNER_TYPES

        config_parameter = config_parameters.get(parameter.config_path)

        if not inner_type_is_primitive and parameter.inner_type != RDFS.Resource:
            raise ValueError(
                f"Parameter '{parameter.uri}' has unknown inner type "
                f"'{parameter.inner_type}'"
            )

        if parameter.outer_type == RDF.List:
            o = _create_rdf_list_parameter(parameter, graph, config_parameter)

        elif parameter.outer_type in (RDF.Seq, RDF.Bag, RDF.Alt):
            raise NotImplementedError(
                f"Parameter '{parameter.uri}' has outer type "
                f"'{parameter.outer_type}', the handling of which "
                "is currently not implemented"
            )

        elif parameter.outer_type == SC.Scalar:
            o = _create_sc_scalar_parameter(parameter, graph, config_parameter)

        else:
            raise ValueError(
                f"'Parameter {parameter.uri}' has unknown outer type "
                f"'{parameter.outer_type}'"
            )

        # add replacements for all occurences of the parameter
        for s, p in graph.subject_predicates(parameter.uri):
            graph.add((s, p, o))

        # remove all references to the parameter from the graph
        # TODO: Keep all `(parameter.uri, None, None)` for debugging purposes?
        graph.remove((parameter.uri, None, None))
        graph.remove((None, None, parameter.uri))

    return graph


def validate_graph(data_graph: Graph, shacl_graph: Graph) -> Tuple[bool, Graph]:
    conforms, validation_graph, _validation_text = validate(
        data_graph,
        shacl_graph=shacl_graph,
        advanced=True,
        inference="rdfs",
        meta_shacl=True,
        do_owl_imports=True,
        js=True,
    )
    # TODO: Is this required? Or are the bindings transferred from the data graph?
    for prefix, iri in PREFIXES.items():
        validation_graph.bind(prefix, iri)
    return conforms, validation_graph
