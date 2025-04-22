# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import pathlib
from dataclasses import dataclass
from typing import Any, Dict, Tuple

from pyshacl import validate
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDF, RDFS, XSD

from sc_validate.namespaces import PREFIXES, SC


def read_rdf_resource(source: pathlib.Path | str) -> Graph:
    graph = Graph()
    graph.parse(source)
    for prefix, iri in PREFIXES.items():
        graph.bind(prefix, iri)
    return graph


@dataclass
class Parameter:
    reference: URIRef
    outer_type: URIRef
    inner_type: URIRef

    config_path: str

    @classmethod
    def from_graph(cls, reference: URIRef, graph: Graph):
        outer_type = graph.value(reference, SC.parameterOuterType, None)
        inner_type = graph.value(reference, SC.parameterInnerType, None)
        config_path = str(graph.value(reference, SC.parameterConfigPath, None))

        return cls(
            reference=reference,
            outer_type=outer_type,
            inner_type=inner_type,
            config_path=config_path,
        )


# TODO: Is it safe to modify the graph while iterating over it?
def parameterize_graph(graph: Graph, config_parameters: Dict[str, Any]) -> Graph:
    # iterate over all declared parameters of type `sc:Parameter`
    for parameter_ref in graph.subjects(RDF.type, SC.Parameter):
        parameter = Parameter.from_graph(parameter_ref, graph)

        inner_type_is_primitive = parameter.inner_type in (
            XSD.string,
            XSD.boolean,
            XSD.integer,
            XSD.int,
            XSD.decimal,
            XSD.float,
            XSD.double,
            XSD.anyURI,
        )

        if not inner_type_is_primitive and parameter.inner_type != RDFS.Resource:
            raise ValueError(
                f"Parameter '{parameter.reference}' has unknown inner type "
                f"'{parameter.inner_type}'"
            )

        # get default value for the parameter
        default_value = graph.value(parameter.reference, SC.parameterDefaultValue, None)

        if parameter.outer_type == RDF.List:
            assert (default_value, RDF.first, None) in graph
            assert (default_value, RDF.rest, None) in graph
            default_value = Collection(graph, default_value)

            # load parameter from config by its name
            parameter_value = config_parameters.get(parameter.config_path, [])
            assert isinstance(parameter_value, list)

            o = default_value.uri
            if parameter_value:
                parameter_value = Collection(
                    graph, BNode(), seq=[Literal(value) for value in parameter_value]
                )
                o = parameter_value.uri

                # empty the list of the unused default value while the variable is still
                # in scope
                default_value.clear()

        elif parameter.outer_type in (RDF.Seq, RDF.Bag, RDF.Alt):
            raise NotImplementedError(
                f"Parameter '{parameter.reference}' has outer type "
                f"'{parameter.outer_type}', the handling of which "
                "is currently not implemented"
            )

        elif parameter.outer_type == SC.Scalar:
            # load parameter from config by its name
            parameter_value = config_parameters.get(parameter.config_path)
            assert isinstance(parameter_value, (str, int, float, type(None)))
            o = Literal(parameter_value) if parameter_value else default_value

        else:
            raise ValueError(
                f"'Parameter {parameter.reference}' has unknown outer type "
                f"'{parameter.outer_type}'"
            )

        # add replacements for all occurences of the parameter
        for s, p in graph.subject_predicates(parameter.reference):
            graph.add((s, p, o))

        # remove all references to the parameter from the graph
        # TODO: Keep all `(parameter.reference, None, None)` for debugging purposes?
        graph.remove((parameter.reference, None, None))
        graph.remove((None, None, parameter.reference))

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
