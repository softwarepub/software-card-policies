# SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

from jinja2 import Environment, PackageLoader, select_autoescape
from rdflib import Graph
from rdflib.namespace import RDF, SH

from software_card_policies.data_model import ValidationReport


def create_report(validation_graph: Graph, debug=False) -> str:
    shacl_report, *_ = validation_graph.subjects(RDF.type, SH.ValidationReport)
    validation_report = ValidationReport.from_graph(shacl_report, validation_graph)
    environment = Environment(
        loader=PackageLoader("software_card_policies"), autoescape=select_autoescape()
    )
    template = environment.get_template("report.j2")
    return template.render(validation_report=validation_report, debug=debug)
