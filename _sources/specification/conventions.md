<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR), Forschungszentrum Jülich (FZJ)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
SPDX-FileContributor: Oliver Bertuch
-->

# Conventions

All code examples are written in the following formats/languages:

- Policies and data: Turtle (RDF serialization format)
- Configuration: TOML
- Source code: Python

RDF examples use the following namespace prefixes (this declaration is omitted for brevity in code examples):

```turtle
@prefix codemeta: <https://doi.org/10.5063/schema/codemeta-2.0#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sc: <https://schema.software-metadata.pub/software-card/2025-01/#> .
@prefix scex: <https://schema.software-metadata.pub/software-card/2025-01/examples/#> .
@prefix scimpl: <https://schema.software-metadata.pub/software-card/2025-01/implementation/#> .
@prefix schema: <https://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

For Software CaRD, these prefixes were established:

- [`sc:`](https://schema.software-metadata.pub/software-card/2025-01/#) - Core Software CaRD vocabulary exposed to the users
- [`scex:`](https://schema.software-metadata.pub/software-card/2025-01/examples/#) - Example policies and data
- [`scimpl:`](https://schema.software-metadata.pub/software-card/2025-01/implementation/#) - Implementation details

## Glossary

```{todo}
Differentiate between general explanations and terms "invented" for Software CaRD.
```

**Policy:**
A _policy_ in this specification refers to a document that contains one or more _policy items_ along with associated metadata such as authorship information and descriptions.
_Policies_ may group _policy items_ thematically (e.g., an "affiliation policy" which checks explicitly given affiliations of software authors and implicitly stated affiliations in email address domains).
Alternatively, _policies_ may group by the aspect of metadata they validate (e.g., an "author policy" which checks all attributes an author might have).
_Policies_ are written in RDF.

**Policy Item:**
A _policy item_ is a single machine-readable validation rule within a _policy_, expressed as a SHACL constraint.
It can be used to _validate_ a given set of metadata.
For example, an "author and contributor policy" might have a _policy item_ that ensures each person has an ORCID identifier.
In addition, a second _policy item_ may ensure at least one person among the contributors has the role of author.

**Validation:**
_Validation_ is the process of determining whether given metadata adheres to all _policy items_ specified in the _policies_.
Validation is performed by a SHACL validator that compares the metadata (_data graph_) against the policy shapes (_shapes graph_).

**Parameter:**
A _parameter_ is a configurable placeholder within a policy that can be assigned different values through a configuration file.
Parameters enable policy reuse across different contexts by allowing specific constraints (such as allowed license values or minimum description length) to be customized without modifying the policy itself.

**Data Graph:**
The RDF graph containing the software metadata to be validated.

**Shapes Graph:**
The RDF graph containing the SHACL shapes that define the validation constraints (i.e., the policies).

**Validation Report:**
The structured output of the validation process, conforming to the SHACL validation report format, which describes any violations found and their severity.

**Shapes Constraint Language (SHACL):**
A [W3C standard](https://www.w3.org/TR/shacl/) for validating RDF graphs.
An introduction to SHACL for policy writers can be found [here](../appendices/shacl-introduction.md).

## Environment

Implementers and providers of policies SHOULD make them accessible on the web in a way that allows direct access to the raw files via the HTTP protocol (this requires provision of the files via a web server).
Static page infrastructures such as "Pages" provided by code forges (e.g., GitHub Pages, GitLab Pages) MAY be used for this purpose.

Content negotiation MAY be offered but is not required.
Policies SHOULD be served with appropriate MIME types for RDF formats (e.g., `text/turtle` for Turtle format).

If provision on the web is not possible or desired, local files MAY be used instead.

## Input Data Format

The software publication metadata to be validated using policies MUST be provided as RDF, either as a file or as a web resource retrievable using the HTTP protocol.
Any of the established serialization formats for RDF MAY be used, including:

- Turtle (`.ttl`)
- RDF/XML (`.rdf`, `.xml`)
- JSON-LD (`.jsonld`)
- N-Triples (`.nt`)

The metadata SHOULD primarily be based on the [Codemeta](https://codemeta.github.io/) vocabulary, which extends [Schema.org](https://schema.org/) with software-specific terms.
The root entity SHOULD be an instance of `schema:SoftwareSourceCode`.
When used for software publications, this MAY be enforced by the validation process.
Metadata MAY be extended following custom schemas and ontologies.
