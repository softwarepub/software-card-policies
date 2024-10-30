# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import operator
import pathlib
import sys
import tomllib
from functools import reduce
from typing import List

from pyshacl import validate
from rdflib import Graph


def read_config_file(file_path: pathlib.Path) -> dict:
    match file_path.suffix:
        case ".toml":
            with open(file_path, "rb") as f:
                config = tomllib.load(f)
            if "software-card" in config:
                return config["software-card"]
            return config
        case other:
            raise NotImplementedError(
                f"Cannot read config file with extension '{other}'."
            )


def read_rdf_file(file_path: pathlib.Path):
    graph = Graph()
    graph.parse(file_path)
    return graph


def parse_policies(policy_config: List[dict]):
    policy_graphs = []
    for policy in policy_config:
        name = policy.get("name")
        if name is None:
            raise ValueError("Could not parse rule due to missing name.")
        source = policy.get("source")
        if source is None:
            raise ValueError("Could not parse rule due to missing source.")
        graph = Graph(identifier=name)
        graph.parse(source)
        policy_graphs.append(graph)
    return policy_graphs


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} CONFIG_FILE DATA_FILE", file=sys.stderr)
        sys.exit(2)

    config_file = pathlib.Path(sys.argv[1])
    data_file = pathlib.Path(sys.argv[2])

    print(f"Config file: {config_file}")
    config = read_config_file(config_file)
    print(f"Data file: {data_file}")
    data_graph = read_rdf_file(data_file)

    policy_config = config["policies"]
    policy_graphs = parse_policies(policy_config)

    print("Validating ... ", end="")
    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=reduce(operator.add, policy_graphs),  # Union of all graphs
        ont_graph=Graph(),
        inference="rdfs",
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        meta_shacl=False,
        advanced=False,
        js=False,
        debug=False,
    )

    print("✓" if conforms else "✗")
    if not conforms:
        sys.exit(1)


if __name__ == "__main__":
    main()
