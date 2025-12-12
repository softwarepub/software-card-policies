# SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

from rdflib import Graph, Literal, Node
from rdflib.term import URIRef


def get_language_tagged_literal(
    graph: Graph, subject: Node, predicate: URIRef, language=None
) -> Literal:
    """Try to get a literal of a given language."""
    literals_by_language = {}
    for obj in graph.objects(subject, predicate):
        assert isinstance(obj, Literal)
        literals_by_language[obj.language] = obj.value

    if not literals_by_language:
        return None

    return (
        literals_by_language.get(language)
        or literals_by_language.get("en")
        or literals_by_language.get("de")
        or next(iter(literals_by_language.values()))
    )
