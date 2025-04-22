# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import pathlib
from dataclasses import dataclass
from typing import Any, Dict, Tuple

from pyshacl import validate
from rdflib import BNode, Graph, Literal, Node, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDF, RDFS, XSD

from sc_validate.namespaces import PREFIXES, SC

# TODO: Add debug messages to all asserts.
# TODO: Register sc:Parameter as custom class in rdflib?


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


@dataclass
class Parameter:
    uri: URIRef
    outer_type: URIRef
    inner_type: URIRef
    default_value: URIRef
    config_path: str

    @classmethod
    def from_graph(cls, uri: URIRef, graph: Graph):
        outer_type = graph.value(uri, SC.parameterOuterType, None)
        inner_type = graph.value(uri, SC.parameterInnerType, None)
        default_value = graph.value(uri, SC.parameterDefaultValue, None)
        config_path = str(graph.value(uri, SC.parameterConfigPath, None))

        return cls(
            uri=uri,
            outer_type=outer_type,
            inner_type=inner_type,
            default_value=default_value,
            config_path=config_path,
        )


def _handle_rdf_list(parameter: Parameter, graph: Graph, config_parameter: Any) -> Node:
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


def _handle_sc_scalar(
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
            o = _handle_rdf_list(parameter, graph, config_parameter)

        elif parameter.outer_type in (RDF.Seq, RDF.Bag, RDF.Alt):
            raise NotImplementedError(
                f"Parameter '{parameter.uri}' has outer type "
                f"'{parameter.outer_type}', the handling of which "
                "is currently not implemented"
            )

        elif parameter.outer_type == SC.Scalar:
            o = _handle_sc_scalar(parameter, graph, config_parameter)

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
    return conforms, validation_graph
