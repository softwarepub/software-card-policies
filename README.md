<!--
SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
-->

# shacl-integration-test

Test integrating shacl in a configurable tool written in Python.

## Installation

```bash
python -m venv venv
source venv/bin/activate
python -m pip install -e .
```

## Run

Start a webserver hosting the policy files (run it in the background or use a separate terminal window):

```bash
python -m http.server -b 127.0.0.1 -d src/shacl_integration_test/
```

Then, run the program:

```bash
shacl-integration-test config.toml data.ttl
```
