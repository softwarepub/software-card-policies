<!--
SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
-->

# Software CaRD Policies

This repository contains the `software_card_policies` Python library as well as the associated command line program
`sc-validate` and example policies.
The software was written as part of the [Software CaRD](https://helmholtz-metadaten.de/en/inf-projects/softwarecard)
project.

## `sc-validate`

A command line program that validates a given metadata file using a set of configurable policies.

The selection of policies can be configured via [`config.toml`](config.toml).
Policies can be loaded using any of the protocols supported by
[RDFlib's `Graph.parse` method](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse)
(e.g. local files, http, ...).
All of the given policies are loaded and unioned into one RDF graph.

Policies can be implemented in a configurable fashion by defining an `sc:Parameter` and using it in place of a literal
or list.
See [`description-parameterizable.ttl`](examples/policies/description-parameterizable.ttl) and
[`licenses-parameterizable.ttl`](examples/policies/licenses-parameterizable.ttl) as examples.
The string specified as `sc:parameterConfigPath` is used to look up the desired value for the parameter in the config
file.

### Installation

```bash
python -m venv venv
source venv/bin/activate
python -m pip install -e .
```

### Run

Start a webserver hosting the example policy files (run it in the background or use a separate terminal window):

```bash
python -m http.server -b 127.0.0.1 -d examples/
```

Then, run the program:

```bash
sc-validate examples/data/hermes.ttl
```

This will validate [`hermes.ttl`](examples/data/hermes.ttl) using the policies defined in [`config.toml`](config.toml)
and print a validation report to the screen.
If run in debug mode (with `--debug`), the report is more verbose, and the following files are written to the current
working directory:

- `debug-input-data.ttl`: the input data
- `debug-shapes-processed.ttl`: the parameterized and combined policies
- `debug-validation-report.ttl`: the detailed SHACL validation report (`sh:ValidationReport`)

## Conventions

All examples in this repository use the following namespace prefix bindings:

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

For Software CaRD, the prefixes
[`sc:`](https://schema.software-metadata.pub/software-card/2025-01-01/#),
[`scex:`](https://schema.software-metadata.pub/software-card/2025-01-01/examples/#), and
[`scimpl:`](https://schema.software-metadata.pub/software-card/2025-01-01/implementation/#)
were established and are used for the following purposes:

- `sc:` contains terms exposed to users
- `scex:` contains example uses of `sc:` and `sh:` terms
- `scimpl:` contains internal implementation details

The associated IRIs currently don't exist.
A [search on prefix.cc](https://prefix.cc/sc) reveals prior usage of the prefix `sc:` by projects which seem to be
defunct.

## Acknowledgments

[Software CaRD](https://helmholtz-metadaten.de/en/inf-projects/softwarecard) (`ZT-I-PF-3-080`) is funded by the
Initiative and Networking Fund of the Helmholtz Association in the framework of the Helmholtz Metadata Collaboration.
