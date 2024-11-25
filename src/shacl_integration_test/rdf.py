# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import operator
import pathlib
from functools import reduce
from typing import Any, Dict, List, Optional, Tuple

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


# TODO: Identifier should actually be a URI (or `None` → BNode)
def read_rdf_resource(source: pathlib.Path | str, identifier: Optional[str] = None):
    graph = Graph(identifier=identifier)
    graph.parse(source)
    for prefix, iri in BINDINGS.items():
        graph.bind(prefix, iri)
    return graph


def parse_policies(policy_config: List[Policy]) -> Graph:
    policy_graphs = [
        read_rdf_resource(policy.source, identifier=policy.name)
        for policy in policy_config
    ]
    return reduce(operator.add, policy_graphs)  # Union of all graphs


# TODO: Need special case to handle parameters of type `rdf:List`
# TODO: Is it safe to modify the graph while iterating over it?
def parametrize_graph(graph: Graph, config_parameters: Dict[str, Any]) -> Graph:
    # iterate over all declared parameters of type `sc:Parameter`
    for parameter in graph.subjects(RDF.type, SC.Parameter):
        # get config name for the parameter
        parameter_name = str(graph.value(parameter, SC.parameterConfigPath, None))

        # get default value for the parameter
        default_value = graph.value(parameter, SC.parameterDefaultValue, None)

        # load parameter from config by its name, using the default value as a fallback
        parameter_value = Literal(config_parameters.get(parameter_name, default_value))

        # add replacements for all occurences of the parameter as an object
        for s, p in graph.subject_predicates(parameter):
            graph.add((s, p, parameter_value))

        # remove all references to the parameter from the graph
        # TODO: Keep all `(parameter, None, None)` for debugging purposes?
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
