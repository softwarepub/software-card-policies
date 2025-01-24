# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import operator
import pathlib
from functools import reduce
from typing import Any, Dict, List, Tuple

from pyshacl import validate
from rdflib import BNode, Graph, Literal
from rdflib.collection import Collection
from rdflib.namespace import RDF, Namespace

from sc_validate.config import Policy

# Just for better readability of serialized linked data.
BINDINGS = {
    "codemeta": "https://doi.org/10.5063/schema/codemeta-2.0#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "sc": "https://software-metadata.pub/software-card#",
    "scex": "https://software-metadata.pub/software-card-examples#",
    "scimpl": "https://software-metadata.pub/software-card-implementation#",
    "schema": "https://schema.org/",
    "sh": "http://www.w3.org/ns/shacl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}

SC = Namespace("https://software-metadata.pub/software-card#")


def read_rdf_resource(source: pathlib.Path | str) -> Graph:
    graph = Graph()
    graph.parse(source)
    for prefix, iri in BINDINGS.items():
        graph.bind(prefix, iri)
    return graph


def parse_policies(policy_config: List[Policy]) -> Graph:
    policy_graphs = [read_rdf_resource(policy.source) for policy in policy_config]
    return reduce(operator.add, policy_graphs)  # Union of all graphs


# TODO: Is it safe to modify the graph while iterating over it?
def parameterize_graph(graph: Graph, config_parameters: Dict[str, Any]) -> Graph:
    # iterate over all declared parameters of type `sc:Parameter`
    for parameter in graph.subjects(RDF.type, SC.Parameter):
        # get config name for the parameter
        parameter_name = str(graph.value(parameter, SC.parameterConfigPath, None))
        is_list = graph.value(parameter, SC.parameterType, None) == RDF.List

        # get default value for the parameter
        default_value = graph.value(parameter, SC.parameterDefaultValue, None)

        if is_list:
            assert (default_value, RDF.first, None) in graph
            assert (default_value, RDF.rest, None) in graph
            default_value = Collection(graph, default_value)

            # load parameter from config by its name
            parameter_value = config_parameters.get(parameter_name, [])
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

        else:
            # load parameter from config by its name
            parameter_value = config_parameters.get(parameter_name)
            assert isinstance(parameter_value, (str, int, float, type(None)))
            o = Literal(parameter_value) if parameter_value else default_value

        # add replacements for all occurences of the parameter
        for s, p in graph.subject_predicates(parameter):
            graph.add((s, p, o))

        # remove all references to the parameter from the graph
        # TODO: Keep all `(parameter, None, None)` for debugging purposes?
        graph.remove((parameter, None, None))
        graph.remove((None, None, parameter))

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
