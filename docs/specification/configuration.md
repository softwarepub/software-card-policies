<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR), Forschungszentrum Jülich (FZJ)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
SPDX-FileContributor: Oliver Bertuch
-->

# Configuration Format

This chapter describes the configuration format used by the "Software CaRD Policies" project.
An implementation MAY choose to provide its own format which is more integrated into its associated application.
The shown reference configuration format is coupled to the specification of the [validation process](./validation.md).

```{todo}
"Coupled to" in which sense?
```

## Configuration File Format

Configuration files specify which policies to apply and what parameter values to use.
The configuration SHOULD follow the TOML format.
Other formats like JSON or YAML MAY also be supported by implementations.

**Basic Structure:**

```toml
[policies.<policy-name>]
source = "<URL or file path to policy>"

[policies.<policy-name>.parameters]
<parameter-config-key> = <value>
```

## Configuration Sections

**Policy Declaration:**

Each policy MUST be declared under `[policies.<policy-name>]`, where `<policy-name>` is a user-chosen identifier:

```toml
[policies.authors]
source = "https://example.org/policies/authors.ttl"
```


The `source` field specifies where to load the policy from.
It can be:

- An HTTPS URL pointing to a policy file on the web
- An HTTP URL (though HTTPS is recommended for security)
- A file:// URL for local files
- A relative or absolute file path

**Parameter Configuration:**

Parameters for a policy are specified under `[policies.<policy-name>.parameters]`:

```toml
[policies.licenses]
source = "https://example.org/policies/licenses-parameterizable.ttl"

[policies.licenses.parameters]
suggested_licenses = [
    "https://spdx.org/licenses/Apache-2.0",
    "https://spdx.org/licenses/GPL-3.0-or-later"
]
```

Parameters MAY also be specified inline using TOML's inline table syntax:

```toml
[policies.description]
source = "https://example.org/policies/description-parameterizable.ttl"
parameters = {description_min_length = 50, description_max_length = 5000}
```


**Parameter Value Types:**

TOML configuration values are mapped to RDF types:

- TOML string → `xsd:string`
- TOML integer → `xsd:integer`
- TOML float → `xsd:decimal`
- TOML boolean → `xsd:boolean`
- TOML array → `rdf:List` (or other collection type as specified)
- TOML datetime → `xsd:dateTime`

```{todo}
This contradicts the section on data type support.
```

## Complete Configuration Example

```toml
# Author requirements with affiliation checking
[policies.authors]
source = "https://software-metadata.pub/software-card-policies/policies/authors-affiliation.ttl"

# Description requirements with configurable length
[policies.description]
source = "https://software-metadata.pub/software-card-policies/policies/description-parameterizable.ttl"
parameters = {description_min_length = 100}

# License requirements with suggested options
[policies.licenses]
source = "https://software-metadata.pub/software-card-policies/policies/licenses-parameterizable.ttl"

[policies.licenses.parameters]
suggested_licenses = [
    "https://spdx.org/licenses/Apache-2.0",
    "https://spdx.org/licenses/GPL-3.0-or-later",
    "https://spdx.org/licenses/MIT"
]
```

## Configuration Validation

Implementations should validate configuration files before attempting to use them:

- Verify that all required fields (`source`) are present
- Check that URLs are well-formed
- Verify that file paths exist and are readable
- Ensure parameter values match the expected types from parameter definitions
- Warn about unknown configuration keys
