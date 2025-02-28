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

TODO: What is this document?

TODO: What is Software CaRD?

[Software CaRD](https://helmholtz-metadaten.de/en/inf-projects/softwarecard) (`ZT-I-PF-3-080`) is funded by the Initiative and Networking Fund of the Helmholtz Association in the framework of the Helmholtz Metadata Collaboration.

### Problem description / Motivation

TODO

### Summary / Abstract

TODO

### Goals

TODO

### Glossary

TODO

### Conventions

All code examples are written in the following formats/languages:

- Policies and data: Turtle,
- Configuration: TOML,
- Program code: Python.

RDF examples use the following namespace prefixes which are omitted for brevity:

TODO: Remove the namespaces we don't need.

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

TODO: Mention here which features we expect the used SHACL impwlementation to have?

### Policy Description

**Input Data Format:**
The software publication metadata to be validated using Software CaRD policies must be provided as RDF, either as a file or as a resource on the web that is retrievable using the HTTP protocol.
Any of the established serialization formats for RDF (XML, JSON-LD, Turtle, ...) may be used.
The metadata should mainly be based on Codemeta.

TODO: SHACL shapes for CodeMeta software metadata

TODO: Parameterization mechanism

TODO: Software CaRD namespaces and what to put in them.

TODO: Explain explicitly which aspects of the SHACL and SHACL Advanced specs may be used (e.g. `owl:imports`, SPARQL, JavaScript, ...)

TODO: Output format? What kinds of violations (severities? messages?) are part of the validation report?

### Configuration

The configuration follows the structure defined in the JSON Schema below.
Configuration files may be written in any file format that can reproduce this schema (e.g. JSON, YAML, TOML, ...).

NOTE: A validator for a variety of formats can be found at <https://www.npmjs.com/package/pajv>

TODO: Add schema

TODO: Add an example policy configuration that uses some parameters. If possible, show how to configure a policy that was already given above.

### Example Policies and Configurations

TODO: Add examples for simple policies, parameterizable policies, and config files

### Example / Reference Implementation

An example implementation of a validator for Software CaRD policies can be found at <https://github.com/softwarepub/software-card-policies>.
It can be installed as a command line tool `sc-validate` using:

```bash
pipx install https://github.com/softwarepub/software-card-policies.git
```

## Considerations

- Security (SHACL-JS, ...)
- Privacy
- Accessibility
- Performance (e.g., we could suggest RDF files/policies to be cached rather than downloaded on every run)
- ...
