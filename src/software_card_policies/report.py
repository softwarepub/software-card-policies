# SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

from rdflib import Graph
from rdflib.namespace import RDF, SH

from software_card_policies.data_model import ValidationReport


def create_report(validation_graph: Graph, debug=False) -> str:
    shacl_report, *_ = validation_graph.subjects(RDF.type, SH.ValidationReport)
    validation_report = ValidationReport.from_graph(shacl_report, validation_graph)

    if validation_report.conforms:
        return "Validation succeeded!"

    text = "Validation failed!\n"
    for validation_result in validation_report.results:
        text += "\n"
        text += f"{validation_result.severity}:\n"
        text += f"Breached policy: {validation_result.source_policy.name}\n"
        text += f"{validation_result.source_policy.description}\n"
        if debug:
            text += f"Debug: {validation_result.message}\n"

    return text
