<!--
SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
-->

# Software CaRD Policies

This repository contains example policies developed as part of the Software CaRD project, as well as a validator tool.

## Conventions

All examples in this repository use the following namespace prefix bindings:

```ttl
@prefix codemeta: <https://doi.org/10.5063/schema/codemeta-2.0#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sc: <https://software-metadata.pub/software-card#> .
@prefix scex: <https://software-metadata.pub/software-card-examples#> .
@prefix scimpl: <https://software-metadata.pub/software-card-implementation#> .
@prefix schema: <https://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

For Software CaRD, the prefixes
[`sc:`](https://software-metadata.pub/software-card#),
[`scex:`](https://software-metadata.pub/software-card-examples#), and
[`scimpl:`](https://software-metadata.pub/software-card-implementation#)
were established and are used for the following purposes:

- `sc:` contains terms exposed to users
- `scex:` contains example uses of `sc:` and `sh:` terms
- `scimpl:` contains internal implementation details

The associated IRIs currently don't exist.
A [search on prefix.cc](https://prefix.cc/sc) reveals prior usage of the prefix `sc:` by projects which seem to be
defunct.

## `sc-validate`

A program that validates a given metadata file using a set of configurable policies.

The selection of policies to use can be configured via [`config.toml`](config.toml).
Policies can be loaded using any of the protocols supported by
[RDFlib's `Graph.parse` method](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse)
(e.g. local files, http, ...).
All of the given policies are loaded and merged into one RDF graph (union of all triples of the parts).

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

Start a webserver hosting the policy files (run it in the background or use a separate terminal window):

```bash
python -m http.server -b 127.0.0.1 -d examples/
```

Then, run the program:

```bash
sc-validate examples/data/hermes.ttl
```

This will validate [`hermes.ttl`](examples/data/hermes.ttl) using the policies defined in [`config.toml`](config.toml)
and print the result to the screen.
If run in debug mode (with `--debug`), a more detailed validation result and the combined and parameterized policies
that were used will be written to the files `debug-validation.ttl` and `debug-shapes-processed.ttl`, respectively.

## Acknowledgements

[Software CaRD](https://helmholtz-metadaten.de/en/inf-projects/softwarecard) (`ZT-I-PF-3-080`) is funded by the
Initiative and Networking Fund of the Helmholtz Association in the framework of the Helmholtz Metadata Collaboration.
