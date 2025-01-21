# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import pathlib
import sys
from argparse import ArgumentParser

from sc_validate.config import Settings
from sc_validate.rdf import (
    parametrize_graph,
    parse_policies,
    read_rdf_resource,
    validate_graph,
)


def main():
    parser = ArgumentParser(
        prog="sc-validate",
        description="Validate publication metadata using Software CaRD policies.",
    )
    parser.add_argument(
        "metadata_file",
        help="file containing Codemeta-based software publication metadata",
        metavar="METADATA_FILE",
    )
    parser.add_argument("-d", "--debug", help="run in debug mode", action="store_true")
    arguments = parser.parse_args()

    try:
        settings = Settings()
    except ValueError as e:
        print("Failed to parse configuration file", str(e), sep="\n\n", file=sys.stderr)
        sys.exit(2)

    data_file = pathlib.Path(arguments.metadata_file)
    if not data_file.exists():
        print("Data file does not exist:", data_file, file=sys.stderr)

    data_graph = read_rdf_resource(data_file)
    shapes_graph = parse_policies(settings.policies)
    shapes_graph = parametrize_graph(shapes_graph, settings.parameters)

    if arguments.debug:
        shapes_graph.serialize("debug-shapes-processed.ttl", "turtle")

    conforms, validation_graph = validate_graph(data_graph, shapes_graph)

    if arguments.debug:
        validation_graph.serialize("debug-validation.ttl", "turtle")

    if not conforms:
        print("validation failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
