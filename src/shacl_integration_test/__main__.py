# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import pathlib
import sys

from pydantic import ValidationError

from shacl_integration_test.config import Settings
from shacl_integration_test.rdf import (
    SC,
    SCEX,
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
    except ValidationError as e:
        print("Failed to parse configuration file", str(e), sep="\n\n", file=sys.stderr)
        sys.exit(2)

    print(f"Data file: {data_file}")
    data_graph = read_rdf_file(data_file)
    shacl_graph = parse_policies(settings.policies)

    # ----------------------------------------------------------------------------------

    # Get default value for scex:longDescriptionMinLength.
    default_value = None
    for _, _, o in shacl_graph.triples(
        (SCEX.longDescriptionMinLength, SC.defaultValue, None)
    ):
        default_value = o

    # Get all triples where scex:longDescriptionMinLength is the object. Add the same
    # triple but with the default value as the object.
    for s, p, _o in shacl_graph.triples((None, None, SCEX.longDescriptionMinLength)):
        shacl_graph.add((s, p, default_value))

    # Remove all references to the parameter from the graph.
    shacl_graph.remove((SCEX.longDescriptionMinLength, None, None))
    shacl_graph.remove((None, None, SCEX.longDescriptionMinLength))

    # Serialize to file for manual debugging.
    shacl_graph.serialize("debug-shapes-processed.ttl", "turtle")

    # ----------------------------------------------------------------------------------

    print("Validating ...", end=" ")
    conforms, validation_graph = validate_graph(data_graph, shacl_graph)
    print("✓" if conforms else "✗")

    # Serialize to file for manual debugging.
    validation_graph.serialize("debug-validation.ttl", "turtle")

    if not conforms:
        sys.exit(1)


if __name__ == "__main__":
    main()
