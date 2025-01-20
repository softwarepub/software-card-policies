# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import pathlib
import sys

from sc_validate.config import Settings
from sc_validate.rdf import (
    parametrize_graph,
    parse_policies,
    read_rdf_resource,
    validate_graph,
)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} DATA_FILE", file=sys.stderr)
        sys.exit(2)

    try:
        settings = Settings()
    except ValueError as e:
        print("Failed to parse configuration file", str(e), sep="\n\n", file=sys.stderr)
        sys.exit(2)

    data_file = pathlib.Path(sys.argv[1])
    if not data_file.exists():
        print("Data file does not exist:", data_file, file=sys.stderr)

    data_graph = read_rdf_resource(data_file)
    shapes_graph = parse_policies(settings.policies)
    shapes_graph = parametrize_graph(shapes_graph, settings.parameters)

    # Serialize to file for manual debugging.
    shapes_graph.serialize("debug-shapes-processed.ttl", "turtle")

    print("Validating ...", end=" ", flush=True)
    conforms, validation_graph = validate_graph(data_graph, shapes_graph)
    print("✓" if conforms else "✗")

    # Serialize to file for manual debugging.
    validation_graph.serialize("debug-validation.ttl", "turtle")

    if not conforms:
        sys.exit(1)


if __name__ == "__main__":
    main()
