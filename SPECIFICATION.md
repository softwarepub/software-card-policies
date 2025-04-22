<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
-->

# Software CaRD Policy Specification (Draft)

| &nbsp;         | &nbsp;                                                                                                                       |
| -------------- | -----------------------------------------------------------------------------------------------------------------------------|
| **Version**    | 0.0                                                                                                                          |
| **Date**       | 202X-XX-XX                                                                                                                   |
| **Authors**    | [David Pape](https://orcid.org/0000-0002-3145-9880), [Helmholtz-Zentrum Dresden - Rossendorf (HZDR)](https://www.hzdr.de)    |
|                | ...                                                                                                                          |
|                | ...                                                                                                                          |
|                | ...                                                                                                                          |
| **Repository** | <https://github.com/softwarepub/software-card-policies>                                                                      |
| **Issues**     | <https://github.com/softwarepub/software-card-policies/issues>                                                               |
| **License**    | [`CC-BY-4.0`](https://creativecommons.org/licenses/by/4.0/)                                                                  |

## Introduction

**TODO:** What is this document?

**TODO:** What is Software CaRD?

[Software CaRD](https://helmholtz-metadaten.de/en/inf-projects/softwarecard) (`ZT-I-PF-3-080`) is funded by the Initiative and Networking Fund of the Helmholtz Association in the framework of the Helmholtz Metadata Collaboration.

### Problem description / Motivation

**TODO**

### Summary / Abstract

**TODO**

### Goals

**TODO**

### Glossary

**TODO**

### Conventions

All code examples are written in the following formats/languages:

- Policies and data: Turtle,
- Configuration: TOML,
- Source code: Python.

RDF examples use the following namespace prefixes which are omitted for brevity:

**TODO:** Remove the namespaces we don't need.

```turtle
@prefix codemeta: <https://doi.org/10.5063/schema/codemeta-2.0#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sc: <https://schema.software-metadata.pub/software-card/2025-01-01/#> .
@prefix scex: <https://schema.software-metadata.pub/software-card/2025-01-01/examples/#> .
@prefix scimpl: <https://schema.software-metadata.pub/software-card/2025-01-01/implementation/#> .
@prefix schema: <https://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

## Specification

### Environment

**Prerequisites:**
Implementers/providers of policies should make them accessible on the web, in a way that allows user agents direct access to the raw files via the HTTP protocol.
This requires provision of the files via a web server.
Static page infrastructures such as "pages" provided by code forges may be used for this purpose.
Content negotiation may be offered but is not required.
If provision on the web is not possible or desired, files may be used instead.

**SHACL Features:**
**TODO:** Mention here which features we expect the used SHACL implementation to have? (`owl:imports`, SPARQL, JavaScript, Custom Constraint Components, ...)

### Policy Description

**Input Data Format:**
The software publication metadata to be validated using Software CaRD policies must be provided as RDF, either as a file or as a resource on the web that is retrievable using the HTTP protocol.
Any of the established serialization formats for RDF (XML, JSON-LD, Turtle, ...) may be used.
The metadata should mainly be based on Codemeta.

**Namespaces:**
The `sc:` namespace is used to provide essential Software CaRD features.
Examples (e.g. policies, data) may be provided in `scex:`.
`scimpl:` is reserved for implementation details and may only be used in the internal data model of the validator.

**Policies:**
Policies may consist of one or more SHACL shapes.
Any object (i.e. the third value in a triple) in their description may be replaced by a `sc:Parameter`.

**Parameterization Placeholders:**
Instances of `sc:Parameter` describe placeholders for configurable values.
A `sc:Parameter` describes the value it represents by its inner and outer type as shown in the example below.
The outer type (akin to cardinality/container) may be `sc:Scalar` if the placeholder represent a single value, or one of `rdf:List`, `rdf:Seq`, `rdf:Bag`, `rdf:Alt`, if it represents a container.
The inner type may be `rdfs:Resource`, or any [primitive data type from `xsd:`](https://www.w3.org/TR/xmlschema-2/#built-in-primitive-datatypes) (such as `xsd:decimal`, `xsd:boolean`, `xsd:string`, ...).
If it is `rdfs:Resource`, any associated values are assumed to be references.
If it is a primitive data type, the values are assumed to be literals of that type.
`sc:parameterConfigPath` is a string that specifies where in the config file the configured value for this placeholder can be found.
`sc:parameterDefaultValue` specifies a default value to be used when no value is configured.
The default value has to match the inner and outer type of the parameter.

**TODO:** **All** primitive datatypes is probably a bit much. Which ones do we want to allow?
`xsd:string`, `xsd:boolean`, `xsd:decimal`, `xsd:float`, `xsd:double`, `xsd:dateTime`, `xsd:time`, `xsd:date`, `xsd:anyURI`,
but not `xsd:duration`, `xsd:gYearMonth`, `xsd:gYear`, `xsd:gMonthDay`, `xsd:gDay`, `xsd:gMonth`, `xsd:hexBinary`, `xsd:base64Binary`, `xsd:NOTATION`?
What about `xsd:QName`?

```turtle
scex:licenses a sc:Parameter ;
    sc:parameterOuterType rdf:List ;
    sc:parameterInnerType xsd:string ;
    sc:parameterConfigPath "suggested_licenses" ;
    sc:parameterDefaultValue ( "https://spdx.org/licenses/Apache-2.0" "https://spdx.org/licenses/MIT" ) .
```

### Validation Process

**TODO:** Parameterization placeholder replacements mechanism

**TODO:** Explain explicitly which aspects of the SHACL and SHACL Advanced specs may be used (e.g. `owl:imports`, SPARQL, JavaScript, Custom Constraint Components, ...)

### Report Generation

**Report Output Format:**
Reports must be valid SHACL validation reports (`sh:ValidationReport`).
**TODO:** If a default value of a policy is overridden, this must be added to the report as `sc:DefaultValueOverridden???`

**Report Presentation:**
The validation report may be presented to the user in a friendlier way, e.g. (formatted or plain) text, markup (HTML, Markdown), graphical visualization, etc.

### Configuration

The configuration follows the structure of the example below.
Configuration files may be written in any file format that can reproduce this schema (e.g. JSON, YAML, TOML, ...).

```toml
[policies.authors]
source = "https://software-metadata.pub/software-card-policies/example-policies/policies/authors-affiliation.ttl"

[policies.description]
source = "https://software-metadata.pub/software-card-policies/example-policies/policies/description-parameterizable.ttl"
parameters = {description_min_length = 10}

[policies.licenses]
source = "https://software-metadata.pub/software-card-policies/example-policies/policies/licenses-parameterizable.ttl"

[policies.licenses.parameters]
suggested_licenses = [
    "https://spdx.org/licenses/Apache-2.0",
    "https://spdx.org/licenses/GPL-3.0-or-later"
]
```

The key of each entry in the `policies` table/dictionary/map may be used to indicate problems to the user.

**TODO:** Provide a JSON Schema? A validator for a variety of formats can be found at <https://www.npmjs.com/package/pajv>

## Example Policies and Configurations

**TODO:** Add examples for simple policies, parameterizable policies, and config files

## Example Implementation

**TODO:** Call this "Example" or "Reference"?

An example implementation of a validator for Software CaRD policies can be found at <https://github.com/softwarepub/software-card-policies>.
Its latest version can be installed as a command line tool `sc-validate` using:

```bash
pipx install git+https://github.com/softwarepub/software-card-policies.git
```

## Considerations

- Security (SHACL-JS, ...)
- Privacy
- Accessibility
- Performance (e.g., we could suggest RDF files/policies to be cached rather than downloaded on every run)
- ...
