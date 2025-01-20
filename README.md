<!--
SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
-->

# Software CaRD Policies

## `sc-validate`

Program that validates a given metadata file using a set of configurable policies.

The selection of policies to use can be configured via [`config.toml`](config.toml).
Policies can be loaded using any of the protocols supported by
[RDFlib's `Graph.parse` method](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.parse)
(e.g. local files, http, ...).
All of the given policies are loaded and merged into one RDF graph (union of all triples of the parts).

Policies can be implemented in a configurable fashion by defining an `sc:Parameter` and using it in place of a literal.
See [`description.ttl`](src/sc_validate/policies/description.ttl) as an example.
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
python -m http.server -b 127.0.0.1 -d src/sc_validate/
```

Then, run the program:

```bash
sc-validate data.ttl
```

This will validate [`data.ttl`](data.ttl) using the policies defined in [`config.toml`](config.toml) and print the
result to the screen.
A more detailed validation result and the combined and parametrized policies that were used can be found in the created
files `debug-validation.ttl` and `debug-shapes-processed.ttl`, respectively.
