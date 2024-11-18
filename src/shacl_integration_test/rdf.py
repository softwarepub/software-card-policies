# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import operator
import pathlib
from functools import reduce
from typing import Any, Dict, List, Tuple

from pyshacl import validate
from rdflib import Graph, Literal
from rdflib.namespace import RDF, Namespace

from shacl_integration_test.config import Policy

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


def read_rdf_file(file_path: pathlib.Path):
    graph = Graph()
    graph.parse(file_path)
    for prefix, iri in BINDINGS.items():
        graph.bind(prefix, iri)
    return graph


def parse_policies(policy_config: List[Policy]) -> Graph:
    policy_graphs = []
    for policy in policy_config:
        # TODO: Identifier should be a URI (or left out → BNode)
        graph = Graph(identifier=policy.name)
        graph.parse(policy.source)
        policy_graphs.append(graph)
    return reduce(operator.add, policy_graphs)  # Union of all graphs


# TODO: Is it safe to modify the graph while iterating over it?
def parametrize_graph(graph: Graph, config_parameters: Dict[str, Any]) -> Graph:
    # iterate over all declared parameters of type `sc:Parameter`
    for parameter, _, _ in graph.triples((None, RDF.type, SC.Parameter)):
        # get config name for the parameter
        parameter_name = None
        for _, _, o in graph.triples((parameter, SC.parameterName, None)):
            parameter_name = str(o)
            print(f"{parameter_name=}")

        # get default value for the parameter
        default_value = None
        for _, _, o in graph.triples((parameter, SC.parameterDefaultValue, None)):
            default_value = o
            print(f"{default_value=}")

        # load parameter from config by its name, using the default value as a fallback
        parameter_value = Literal(config_parameters.get(parameter_name, default_value))
        print(f"{parameter_value=}")

        # add replacements for all occurences of the parameter as an object
        for s, p, _o in graph.triples((None, None, parameter)):
            graph.add((s, p, parameter_value))

        # remove all references to the parameter from the graph
        # TODO: Keep all `(parameter, None, None)` for debugging reasons?
        graph.remove((parameter, None, None))
        graph.remove((None, None, parameter))

    return graph


# TODO: Create a report. Inspiration:
# https://github.com/RDFLib/pySHACL/blob/0d0d5d3adec13ce1dd405289223ba8fcefe8c148/pyshacl/cli.py#L328
def validate_graph(data_graph: Graph, shacl_graph: Graph) -> Tuple[bool, Graph]:
    conforms, validation_graph, _validation_text = validate(
        data_graph,
        shacl_graph=shacl_graph,
        ont_graph=None,
        inference="rdfs",
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        meta_shacl=False,
        advanced=False,
        js=False,
        debug=False,
    )
    return conforms, validation_graph
