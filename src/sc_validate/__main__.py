# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

import sys
from argparse import ArgumentError, ArgumentParser, ArgumentTypeError
from pathlib import Path
from urllib.parse import urlparse

from sc_validate import __version__ as version
from sc_validate.config import make_config
from sc_validate.data_model import (
    make_shacl_graph,
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


def make_argument_parser() -> ArgumentParser:
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
        help="configuration file (the default is config.toml)",
        type=_path,
        default="config.toml",
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
    return parser


def main():
    parser = make_argument_parser()
    arguments = parser.parse_args()

    try:
        config = make_config(config_file=arguments.config)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    data_graph = read_rdf_resource(arguments.metadata_file)
    shapes_graph = make_shacl_graph(config)

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
