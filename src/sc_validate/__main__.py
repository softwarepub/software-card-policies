# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import operator
import sys
from argparse import ArgumentError, ArgumentParser, ArgumentTypeError
from functools import reduce
from pathlib import Path
from typing import Dict
from urllib.parse import urlparse

from sc_validate import __version__ as version
from sc_validate.config import Policy, make_config
from sc_validate.data_model import (
    parameterize_graph,
    read_rdf_resource,
    validate_graph,
)
from sc_validate.report import create_report


def _path_or_url(path: str) -> Path | str:
    if (path_obj := Path(path)).exists():
        return path_obj
    result = urlparse(path)
    if result.scheme and result.netloc:
        return path
    raise ArgumentTypeError(f"Argument '{path}' is neither an existing file nor a URL")


def _path(path: str) -> Path:
    path_obj = Path(path)
    if path_obj.exists():
        return path_obj
    raise ArgumentError(f"Argument '{path}' is not an existing file")


# TODO: Move this function somewhere more useful
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
        type=_path_or_url,
        metavar="METADATA_FILE",
    )
    parser.add_argument(
        "-c",
        "--config",
        help="configuration file",
        type=_path,
        metavar="CONFIG_FILE",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="run in debug mode",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {version}",
    )
    arguments = parser.parse_args()

    try:
        config = make_config(config_file=arguments.config)
    # TODO: Catch more specific errors
    except Exception as e:
        print("Failed to parse configuration file:", str(e), file=sys.stderr)
        sys.exit(2)

    data_graph = read_rdf_resource(arguments.metadata_file)
    shapes_graph = policies_to_shacl(config.policies)

    if arguments.debug:
        data_graph.serialize("debug-input-data.ttl", "turtle")
        shapes_graph.serialize("debug-shapes-processed.ttl", "turtle")

    conforms, validation_graph = validate_graph(data_graph, shapes_graph)

    if arguments.debug:
        validation_graph.serialize("debug-validation-report.ttl", "turtle")

    report = create_report(validation_graph, debug=arguments.debug)
    print(report)

    if not conforms:
        sys.exit(1)


if __name__ == "__main__":
    main()
