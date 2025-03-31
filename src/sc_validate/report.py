# SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

from dataclasses import dataclass
from enum import Enum
from typing import List

from jinja2 import Environment, PackageLoader, select_autoescape
from rdflib import Graph, Literal
from rdflib.namespace import RDF, SH
from rdflib.term import URIRef


# TODO: This only works for constraints of type NodeShape. Is this enough?
@dataclass
class Policy:
    name: str
    description: str

    @classmethod
    def from_graph(cls, reference: URIRef, graph: Graph):
        name = graph.value(reference, SH.name, None)
        description = graph.value(reference, SH.description, None)
        return cls(name=name, description=description)


class Severity(Enum):
    INFO = 1
    WARNING = 2
    VIOLATION = 3
    OTHER = 4

    def __str__(self):
        return self.name.title()

    @classmethod
    def from_graph(cls, reference: URIRef, graph: Graph):
        if reference == SH.Info:
            return cls.INFO
        if reference == SH.Warning:
            return cls.WARNING
        if reference == SH.Violation:
            return cls.VIOLATION
        return cls.OTHER


@dataclass
class ValidationResult:
    severity: Severity
    message: str
    source_policy: Policy

    @classmethod
    def from_graph(cls, reference: URIRef, graph: Graph):
        severity = graph.value(reference, SH.resultSeverity, None)
        message = graph.value(reference, SH.resultMessage, None)
        source_policy = graph.value(reference, SH.sourceShape, None)
        return cls(
            severity=Severity.from_graph(severity, graph),
            message=message,
            source_policy=Policy.from_graph(source_policy, graph),
        )


@dataclass
class ValidationReport:
    conforms: bool
    results: List[ValidationResult]

    @classmethod
    def from_graph(cls, reference: URIRef, graph: Graph):
        conforms = (reference, SH.conforms, Literal(True)) in graph
        results = graph.objects(reference, SH.result)
        return cls(
            conforms=conforms,
            results=[ValidationResult.from_graph(result, graph) for result in results],
        )


def create_report(validation_graph: Graph, debug=False) -> str:
    shacl_report, *_ = validation_graph.subjects(RDF.type, SH.ValidationReport)
    validation_report = ValidationReport.from_graph(shacl_report, validation_graph)
    environment = Environment(
        loader=PackageLoader("sc_validate"), autoescape=select_autoescape()
    )
    template = environment.get_template("report.j2")
    return template.render(validation_report=validation_report, debug=debug)
