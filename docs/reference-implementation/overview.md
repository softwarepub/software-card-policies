<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR), Forschungszentrum Jülich (FZJ)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
SPDX-FileContributor: Oliver Bertuch
-->

# Overview

```{todo}
Completely rework this section.
```

A reference implementation of a validator for Software CaRD policies can be found at <https://github.com/softwarepub/software-card-policies>.
This implementation demonstrates how to:

- Load and parse SHACL policy files from the web or filesystem
- Resolve parameters from TOML configuration files
- Execute SHACL validation using a standard validator
- Generate and present validation reports

## Installation

The reference implementation can be installed as a command-line tool using:

```bash
pipx install git+https://github.com/softwarepub/software-card-policies.git
```


## Usage

Basic usage:

```bash
software-card-validate --config config.toml --data metadata.ttl
```


This will:
1. Load policies specified in `config.toml`
2. Resolve any parameters from the configuration
3. Validate the metadata in `metadata.ttl`
4. Print a validation report

## Integration

The reference implementation can also be used as a Python library for integration into other tools:

```{todo}
This code example doesn't work.
```

```python
from software_card_policies import validate

report = validate(
    config_path="config.toml",
    data_path="metadata.ttl"
)

if report.conforms:
    print("Validation passed!")
else:
    for result in report.results:
        print(f"Issue: {result.message}")
```
