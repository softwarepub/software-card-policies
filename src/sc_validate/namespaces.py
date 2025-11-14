# SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

from rdflib.namespace import OWL, RDF, RDFS, SDO, SH, XSD, DefinedNamespace, Namespace
from rdflib.term import URIRef


class SC(DefinedNamespace):
    """The Software CaRD schema."""

    _NS = Namespace("https://schema.software-metadata.pub/software-card/2025-01-01/#")

    #: A "placeholder" parameter to be used in a policy
    Parameter: URIRef

    #: Represents the notion that a `sc:Parameter`` is a stand-in for a scalar (i.e.
    #: non-List/Seq/Bag/Alt) value
    Scalar: URIRef

    #: The "outer type" of a parameter. May be `rdf:List/Seq/Bag/Alt` or `sc:Scalar`.
    parameterOuterType: URIRef
    #: The "inner type" of a parameter. May be `rdfs:Resource` to refer to a complex
    #: type. Or, may be one of the following primitive data types:
    #: `xsd:integer/float/string/.../anyURI` to refer to a literal value.
    parameterInnerType: URIRef
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
    "sc": SC,
    "scex": SCEX,
    "scimpl": SCIMPL,
    "schema": SDO,
    "sh": SH,
    "xsd": XSD,
}
"""Default namespace prefix bindings."""
