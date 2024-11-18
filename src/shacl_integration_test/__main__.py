# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import pathlib
import sys

from shacl_integration_test.config import Settings
from shacl_integration_test.rdf import (
    parametrize_graph,
    parse_policies,
    read_rdf_file,
    validate_graph,
)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} CONFIG_FILE DATA_FILE", file=sys.stderr)
        sys.exit(2)

    config_file = pathlib.Path(sys.argv[1])
    data_file = pathlib.Path(sys.argv[2])

    print(f"Config file: {config_file}")
    try:
        settings = Settings()
    except ValueError as e:
        print("Failed to parse configuration file", str(e), sep="\n\n", file=sys.stderr)
        sys.exit(2)

    print(f"Data file: {data_file}")
    data_graph = read_rdf_file(data_file)
    shapes_graph = parse_policies(settings.policies)
    shapes_graph = parametrize_graph(shapes_graph, settings.parameters)

    print("Validating ...", end=" ")
    conforms, validation_graph = validate_graph(data_graph, shapes_graph)
    print("✓" if conforms else "✗")

    # Serialize to file for manual debugging.
    shapes_graph.serialize("debug-shapes-processed.ttl", "turtle")
    validation_graph.serialize("debug-validation.ttl", "turtle")

    if not conforms:
        sys.exit(1)


if __name__ == "__main__":
    main()
