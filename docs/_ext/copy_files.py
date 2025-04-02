# SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

from pathlib import Path

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.console import colorize
from sphinx.util.docutils import SphinxDirective
from sphinx.util.fileutil import copy_asset
from sphinx.util.typing import ExtensionMetadata

logger = logging.getLogger(__name__)


def log_message(text: str, detail: str = None) -> None:
    message = colorize("bold", "[Copy Files]") + " " + text
    if detail is not None:
        message += " " + colorize("darkgreen", detail)
    logger.info(message)


class CopyExampleFilesDirective(SphinxDirective):
    required_arguments = 1

    def run(self) -> list[nodes.Node]:
        filename = Path(self.get_source_info()[0])  # currently processed file
        directory = filename.parent

        source_file_or_directory = (directory / self.arguments[0]).resolve()

        # output directory of the builder
        output_directory = Path(self.state.document.settings.env.app.outdir)

        # output directory of the currently processed file
        current_output_directory = (
            output_directory / self.state.document.settings.env.docname
        ).parent

        log_message(
            "Copying files",
            f"from: {source_file_or_directory} to {current_output_directory}",
        )
        copy_asset(source_file_or_directory, current_output_directory, force=True)

        note = nodes.note()
        text = nodes.paragraph(text="Files were automatically added to this directory.")
        note.append(text)
        return [note]


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive("copy-files", CopyExampleFilesDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
