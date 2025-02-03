# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import operator
import pathlib
import sys
from argparse import ArgumentParser, ArgumentTypeError
from functools import reduce
from typing import Dict
from urllib.parse import urlparse

from sc_validate import __version__ as version
from sc_validate.config import Policy, Settings
from sc_validate.rdf import (
    parameterize_graph,
    read_rdf_resource,
    validate_graph,
)


def path_or_url(path: str) -> pathlib.Path | str:
    if (path_obj := pathlib.Path(path)).exists():
        return path_obj
    result = urlparse(path)
    if result.scheme and result.netloc:
        return path
    raise ArgumentTypeError(f"Argument '{path}' is neither an existing file nor a URL")


def policies_to_shacl(policies: Dict[str, Policy]):
    shacl_graphs = []
    # TODO: We're only using the values. What to do with the keys?
    for policy in policies.values():
        policy_graph = read_rdf_resource(policy.source)
        shacl_graph = parameterize_graph(policy_graph, policy.parameters)
        shacl_graphs.append(shacl_graph)
    return reduce(operator.add, shacl_graphs)


def main():
    parser = ArgumentParser(
        prog="sc-validate",
        description="Validate publication metadata using Software CaRD policies.",
    )
    parser.add_argument(
        "metadata_file",
        help=(
            "file containing Codemeta-based software publication metadata "
            "(as a file path or URL)"
        ),
        type=path_or_url,
        metavar="METADATA_FILE",
    )
    parser.add_argument("--debug", help="run in debug mode", action="store_true")
    parser.add_argument("--version", action="version", version=f"%(prog)s {version}")
    arguments = parser.parse_args()

    try:
        settings = Settings()
    except ValueError as e:
        print("Failed to parse configuration file", str(e), sep="\n\n", file=sys.stderr)
        sys.exit(2)

    data_graph = read_rdf_resource(arguments.metadata_file)
    shapes_graph = policies_to_shacl(settings.policies)

    if arguments.debug:
        data_graph.serialize("debug-input-data.ttl", "turtle")
        shapes_graph.serialize("debug-shapes-processed.ttl", "turtle")

    conforms, validation_graph = validate_graph(data_graph, shapes_graph)

    if arguments.debug:
        validation_graph.serialize("debug-validation-report.ttl", "turtle")

    if not conforms:
        print("validation failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
