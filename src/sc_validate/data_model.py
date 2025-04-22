# SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

from dataclasses import dataclass
from enum import Enum
from typing import List

from rdflib import Graph, Literal
from rdflib.namespace import SH
from rdflib.term import URIRef

from sc_validate.namespaces import SC

#################################### Software CaRD ####################################


@dataclass
class Parameter:
    """Model of a `sc:Parameter`."""

    uri: URIRef
    outer_type: URIRef
    inner_type: URIRef
    default_value: URIRef
    config_path: str

    @classmethod
    def from_graph(cls, uri: URIRef, graph: Graph):
        outer_type = graph.value(uri, SC.parameterOuterType, None)
        inner_type = graph.value(uri, SC.parameterInnerType, None)
        default_value = graph.value(uri, SC.parameterDefaultValue, None)
        config_path = str(graph.value(uri, SC.parameterConfigPath, None))

        return cls(
            uri=uri,
            outer_type=outer_type,
            inner_type=inner_type,
            default_value=default_value,
            config_path=config_path,
        )


# TODO: This only works for constraints of type NodeShape. Is this enough?
@dataclass
class Policy:
    """Model of a Software CaRD Policy."""

    name: str
    description: str

    @classmethod
    def from_graph(cls, reference: URIRef, graph: Graph):
        name = graph.value(reference, SH.name, None)
        description = graph.value(reference, SH.description, None)
        return cls(name=name, description=description)


######################################## SHACL ########################################


class Severity(Enum):
    """Model of `sh:Severity`."""

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
    """Model of a `sh:ValidationResult`."""

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
    """Model of a `sh:ValidationReport`."""

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
