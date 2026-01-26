# SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import operator
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from pathlib import Path
from types import NoneType
from typing import Any, Dict, List, Tuple

from pyshacl import validate
from rdflib import BNode, Graph, Literal, Node
from rdflib.collection import Collection
from rdflib.namespace import RDF, RDFS, SH, XSD
from rdflib.term import URIRef

from software_card_policies.config import Config
from software_card_policies.namespaces import PREFIXES, SC
from software_card_policies.rdf_helpers import get_language_tagged_literal

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

_ALLOWED_OUTER_TYPES = (
    SC.Scalar,
    RDF.List,
)

_ALLOWED_INNER_TYPES = (
    XSD.string,
    XSD.boolean,
    XSD.integer,
    XSD.int,
    XSD.decimal,
    XSD.float,
    XSD.double,
    XSD.anyURI,
    RDFS.Resource,
)


def read_rdf_resource(
    source: Path | None = None,
    format: str | None = None,
    data: str | bytes | None = None,
) -> Graph:
    """Read in an RDF resource.

    Either ``source``, or ``format`` and ``data`` must be given.
    """
    assert (
        source is not None
        and format is None
        and data is None
        or source is None
        and format is not None
        and data is not None
    )
    graph = Graph()
    graph.parse(source=source, format=format, data=data)
    for prefix, iri in PREFIXES.items():
        graph.bind(prefix, iri, replace=True)
    return graph


def _create_list_parameter(
    parameter: Parameter, graph: Graph, config_parameter: Any
) -> Node:
    assert parameter.outer_type == RDF.List
    assert (parameter.default_value, RDF.first, None) in graph
    assert (parameter.default_value, RDF.rest, None) in graph

    if config_parameter is None:
        return Collection(graph, parameter.default_value).uri

    # TODO: What happens if `parameter_value` is empty list?
    assert isinstance(config_parameter, list)
    return Collection(
        graph, BNode(), seq=[Literal(value) for value in config_parameter]
    ).uri


def _create_scalar_parameter(
    parameter: Parameter, graph: Graph, config_parameter: Any
) -> Node:
    assert parameter.outer_type == SC.Scalar
    assert isinstance(config_parameter, (str, int, float, NoneType))

    if config_parameter:
        return Literal(config_parameter)

    return graph.value(parameter.uri, SC.parameterDefaultValue, None)


def parameterize_graph(graph: Graph, config_parameters: Dict[str, Any]) -> Graph:
    """Parameterize the ``graph`` using the ``config_parameters``."""

    # Extract references into a list so we don't have to iterate over the graph we want
    # to modify!
    parameter_refs = list(graph.subjects(RDF.type, SC.Parameter))

    for parameter_ref in parameter_refs:
        parameter = Parameter.from_graph(parameter_ref, graph)

        config_parameter = config_parameters.get(parameter.config_path)

        if parameter.outer_type not in _ALLOWED_OUTER_TYPES:
            raise ValueError(
                f"'Parameter {parameter.uri}' has unknown outer type "
                f"'{parameter.outer_type}'"
            )

        if parameter.inner_type not in _ALLOWED_INNER_TYPES:
            raise ValueError(
                f"Parameter '{parameter.uri}' has unknown inner type "
                f"'{parameter.inner_type}'"
            )

        if parameter.outer_type == SC.Scalar:
            o = _create_scalar_parameter(parameter, graph, config_parameter)

        else:
            o = _create_list_parameter(parameter, graph, config_parameter)

        # Add replacements for all occurences of the parameter. Again, extract
        # occurences before modifying the graph!
        occurences = list(graph.subject_predicates(parameter.uri))
        for s, p in occurences:
            graph.add((s, p, o))

        # remove all references to the parameter from the graph
        graph.remove((parameter.uri, None, None))
        graph.remove((None, None, parameter.uri))
        if parameter.outer_type != SC.Scalar:
            Collection(graph, parameter.default_value).clear()

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

    # Read the whole SHACL vocabulary into the graph so that we can use additional info
    # such as labels and descriptions.
    validation_graph.parse(SH._NS)

    # Bind namespace prefixes for better readability. These _should_ already be bound;
    # we're just making sure.
    for prefix, iri in PREFIXES.items():
        validation_graph.bind(prefix, iri, replace=True)

    return conforms, validation_graph


def make_shacl_graph(config: Config) -> Graph:
    shacl_graphs = []
    # TODO: We're only using the values. Make use of the keys which contain the config
    # names of the policies.
    for policy in config.policies.values():
        policy_graph = read_rdf_resource(policy.source)
        shacl_graph = parameterize_graph(policy_graph, policy.parameters)
        shacl_graphs.append(shacl_graph)
    return reduce(operator.add, shacl_graphs, Graph())
