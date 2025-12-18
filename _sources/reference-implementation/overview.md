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

A reference implementation of a validator for Software CaRD policies can be found at
<https://github.com/softwarepub/software-card-policies>.
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

To use the library in your own application, install it into your virtual environment
using:

```bash
pip install git+https://github.com/softwarepub/software-card-policies.git
```

Or add it as a dependency to your `pyproject.toml`, e.g.:

```toml
[project]
dependencies = [
  "software-card-policies @ git+https://github.com/softwarepub/software-card-policies.git",
]
```
