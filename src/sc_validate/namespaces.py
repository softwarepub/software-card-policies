# SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

from rdflib.namespace import OWL, RDF, RDFS, SDO, SH, XSD, DefinedNamespace, Namespace
from rdflib.term import URIRef


class SC(DefinedNamespace):
    """The Software CaRD schema."""

    _NS = Namespace("https://schema.software-metadata.pub/software-card/2025-01-01/#")

    Parameter: URIRef

    parameterType: URIRef
    parameterConfigPath: URIRef
    parameterDefaultValue: URIRef


class SCIMPL(DefinedNamespace):
    """Software CaRD implementation details."""

    _NS = Namespace(
        "https://schema.software-metadata.pub/software-card/2025-01-01/implementation/#"
    )


class SCEX(DefinedNamespace):
    """Software CaRD example components."""

    _NS = Namespace(
        "https://schema.software-metadata.pub/software-card/2025-01-01/examples/#"
    )


CODEMETA = Namespace("https://doi.org/10.5063/schema/codemeta-2.0#")
"""The Codemeta schema. See: https://codemeta.github.io/"""


PREFIXES = {
    "codemeta": CODEMETA,
    "owl": OWL,
    "rdf": RDF,
    "rdfs": RDFS,
    "sc": SH,
    "scex": SCEX,
    "scimpl": SCIMPL,
    "schema": SDO,
    "sh": SH,
    "xsd": XSD,
}
"""Default namespace prefix bindings."""
