<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR), Forschungszentrum Jülich (FZJ)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
SPDX-FileContributor: Oliver Bertuch
-->

# Parameterization

SHACL shapes are reusable, but fixed and unflexible constraints once written. // SHACL shapes are reusable but unchangeable once they are written.
One of the key features of the Software CaRD framework is the ability to enable parameterized SHACL shapes. // Software CaRD policies are parameterizable SHACL shapes.
This allows the creation of policy templates, to be reused with slightly different constraints configured for different contexts.
Parameters can define default values which can be overwritten using runtime configuration.

## Defining a Parameter

A parameter MUST be defined as an instance of `sc:Parameter`.

Example:
```turtle
scex:suggestedLicenses a sc:Parameter ;
    rdfs:comment """List of SPDX license identifiers that are recommended for use."""@en
    sc:parameterOuterType rdf:List ;
    sc:parameterInnerType xsd:anyURI ;
    sc:parameterConfigKey "suggested_licenses" ;
    sc:parameterDefaultValue (
        "https://spdx.org/licenses/Apache-2.0"
        "https://spdx.org/licenses/MIT"
    ) .
```

A parameter MUST define these attributes:
- `rdfs:comment`: A human readable description of the parameter
- `sc:parameterOuterType`: A container type (see below)
- `sc:parameterInnerType`: A data type (see below)
- `sc:parameterConfigKey`: A non-empty key that can be used to resolve the value at runtime from a configuration

The parameter MAY define a `sc:parameterDefaultValue`. When given, the parameter's value MAY be omitted in the configuration during the validation process. When not given, the parameter's value is REQUIRED.

For a formal definition of the Parameter class, see [](../appendices/ontology.md).

An implementation providing the parameter's value during runtime MAY use TOML ~~as a source for them~~.
In the following sections, any example assumes such a provision mechanism.
For the parameter example above, a configuration MAY look like this:

```toml
[policies.licenses.parameters]
suggested_licenses = [
    "https://spdx.org/licenses/BSD-3-Clause",
    "https://spdx.org/licenses/LGPL-3.0-or-later"
]
```

## Using a Parameter in a SHACL Shape

Parameters MAY be used in place of concrete values within SHACL constraints.

Example:
```turtle
scex:licenseRequirements a sh:NodeShape ;
    sh:targetClass schema:SoftwareSourceCode ;

    sh:property [
        sh:name "Suggested license" ;
        sh:description "A license from this list should be chosen." ;
        sh:severity sh:Warning ;

        sh:path schema:license ;
        sh:datatype xsd:string ;
        sh:in scex:suggestedLicenses ;  # Parameter reference
    ] .
```

```{note}
This shape description is not usable as is in any SHACL validator.
The parameters need runtime instantiation, which requires special implementation support.
```

## Parameter Type System

Parameters use a two-level type system to describe both the *structure* (outer type) and the *content* (inner type) of configurable values:

**Outer Type**: Describes the structure or cardinality of the parameter value

- Is it a single value or multiple values?
- If multiple, are they ordered, unordered, or alternatives?

**Inner Type**: Describes the datatype of the individual value(s)

- Are they strings, numbers, dates, or references to other resources?
- What are allowed value ranges?

```{todo}
We mention dates as an example here but disallow them later.
```

This separation allows the framework to correctly handle configurations like:

- A minimum character requirement for descriptions (outer: `sc:Scalar`, inner: `xsd:int`)
- A list of license URIs (outer: `rdf:List`, inner: `xsd:anyURI`)
- A set of organization names (outer: `rdf:Bag`, inner: `xsd:string`)


## `sc:parameterInnerType`

The inner type MUST be present and MUST specify what kind of data each value contains.

These types MUST be supported by implementations:


| Inner Type      | Meaning                | Example Values                    | Use Cases                           |
| --------------- | ---------------------- | --------------------------------- | ----------------------------------- |
| `xsd:string`    | Text string            | `"Apache-2.0"`, `"Hello"`         | Names, descriptions, identifiers    |
| `xsd:anyURI`    | URI/IRI                | `"https://spdx.org/licenses/MIT"` | License identifiers, URL references |
| `xsd:int`       | 32-bit integer         | `42`                              | Smaller integer values              |
| `xsd:long`      | 64-bit integer         | `10,000,000,000`                  | Large integer values                |
| `xsd:float`     | Single-precision float | `3.14`                            | Approximate numbers                 |
| `xsd:double`    | Double-precision float | `3.141592653589793`               | High-precision approximations       |
| `xsd:boolean`   | True/false             | `true`, `false`                   | Flags, enable/disable options       |
| `rdfs:Resource` | IRI reference          | `<https://example.org/org>`       | References to other RDF resources   |

```{todo}
Note on "normal" datetimes? ->
disallow and refer to string+regex to allow for more flexibility?
```

```{note}
`rdfs:Resource` is a special inner type, with the parameter value representing references to other RDF entities rather than literal values.
The validator MUST treat configured values as IRIs and MUST NOT attempt to parse or validate them as literals.
```

For simplicity of the implementation and to avoid edge cases, the following XSD types are NOT recommended for use:

- `xsd:integer`, `xsd:decimal`, `xsd:short`, `xsd:byte` - to avoid value representation issues in systems using fixed size integer and floating point values
- `xsd:duration`, `xsd:gYearMonth`, `xsd:gYear`, `xsd:gMonthDay`, `xsd:gDay`, `xsd:gMonth` - Partial date/time types that are rarely needed
- `xsd:hexBinary`, `xsd:base64Binary` - Binary data types not suitable for metadata validation
- `xsd:NOTATION` - Used only in XML schema definitions
- `xsd:QName` - Qualified names that require namespace context

Implementations MAY support these types but MUST warn users in case of interoperability issues.

Example:
```turtle
scex:requiredAffiliation a sc:Parameter ;
    sc:parameterOuterType sc:Scalar ;
    sc:parameterInnerType rdfs:Resource ;
    sc:parameterConfigPath "required_affiliation_iri" ;
    sc:parameterDefaultValue <https://ror.org/0281dp749> .  # Helmholtz' ROR identifier
```
Configuration:
```toml
[policies.affiliation.parameters]
required_affiliation_iri = "https://ror.org/01zy2cs03"  # Different organization's ROR
```

## `sc:parameterOuterType`

The outer type MUST be present and MUST specify how values are structured.

These types MUST be supported by implementations:

| Outer Type  | Meaning            | Use When                                     | Example                                    |
| ----------- | ------------------ | -------------------------------------------- | ------------------------------------------ |
| `sc:Scalar` | Single value       | Only one value is needed                     | Minimum description length, a boolean flag |
| `rdf:List`  | Ordered sequence   | Order matters and multiple values are needed | Priority-ordered list of licenses          |
| `rdf:Bag`   | Unordered sequence | Order does not matter for multiple values    | List of software dependencies              |

Ohter RDF collection types (like `rdf:Seq`, `rdf:Alt`) MAY be supported by a validation implementation.

## `sc:parameterConfigKey`

A string that identifies where in the configuration this parameter's value can be found.
This key is used to look up the configured value.
Details such as hierarchy/nesting within an application's configuration file are at the implementation's discretion.
However, for simplicity of the implementation, the string itself MUST NOT encode such structure (cf. JSONPath, XPath).

Example:

```turtle
sc:parameterConfigKey "min_length" ;
```

Configuration:

```toml
[policies.description.parameters]
min_length = 100
```

## `sc:parameterDefaultValue`

The value to use when no configured value is provided.
The default value MUST match the specified outer and inner types.
Adding a default value to a parameter is optional, and, if omitted, MUST make the implementation require a configuration value.

```{note}
The default value serves as both a fallback and documentation:

- Policy users can see what value will be used if they don't configure it
- Policy authors can provide sensible defaults for common use cases
- The default demonstrates the expected format and type
```

**Example: Type Matching**

Correct - outer type and inner type match:
```turtle
scex:minLength a sc:Parameter ;
    sc:parameterOuterType sc:Scalar ;
    sc:parameterInnerType xsd:int ;
    sc:parameterConfigKey "example" ;
    sc:parameterDefaultValue 50 .  # Single integer in the 32-bit range ✓
```
Correct - list of URIs:
```turtle
scex:licenses a sc:Parameter ;
    sc:parameterOuterType rdf:List ;
    sc:parameterInnerType xsd:anyURI ;
    sc:parameterConfigKey "example" ;
    sc:parameterDefaultValue (
        "https://spdx.org/licenses/Apache-2.0"
        "https://spdx.org/licenses/MIT"
    ) .  # List of URIs ✓
```
Incorrect - type mismatch:
```turtle
scex:minLength a sc:Parameter ;
    sc:parameterOuterType sc:Scalar ;
    sc:parameterInnerType xsd:int ;
    sc:parameterConfigKey "example" ;
    sc:parameterDefaultValue "50" .  # String instead of integer ✗
```
Incorrect - structure mismatch:
```turtle
scex:minLength a sc:Parameter ;
    sc:parameterOuterType sc:Scalar ;
    sc:parameterInnerType xsd:int ;
    sc:parameterConfigKey "example" ;
    sc:parameterDefaultValue ( 50 100 ) .  # List instead of scalar ✗
```

## Comprehensive Parameter Examples by Type Combination:

```{todo}
Is it necessary to have a comprehensive list?
What does comprehensive mean in this case?
Is it exhaustive (i.e. contains all possible combinations)?
Maybe these should be moved to the examples sections (and just referenced here).
```

**Scalar String (Single Text Value):**
```turtle
scex:organizationName a sc:Parameter ;
    sc:parameterOuterType sc:Scalar ;
    sc:parameterInnerType xsd:string ;
    sc:parameterConfigKey "organization_name" ;
    sc:parameterDefaultValue "Helmholtz-Zentrum Dresden-Rossendorf (HZDR)" .
```

Configuration:
```toml
[policies.affiliation.parameters]
organization_name = "German Aerospace Center (DLR)"
```

**Scalar Integer (Single Number):**
```turtle
scex:minDescriptionLength a sc:Parameter ;
    sc:parameterOuterType sc:Scalar ;
    sc:parameterInnerType xsd:integer ;
    sc:parameterConfigKey "description_min_length" ;
    sc:parameterDefaultValue 50 .
```

Configuration:
```toml
[policies.description.parameters]
description_min_length = 100
```

**Scalar Boolean (Flag):**
```turtle
scex:requireOrcid a sc:Parameter ;
    sc:parameterOuterType sc:Scalar ;
    sc:parameterInnerType xsd:boolean ;
    sc:parameterConfigKey "require_orcid" ;
    sc:parameterDefaultValue true .
```

Configuration:
```toml
[policies.authors.parameters]
require_orcid = false
```

**List of URIs (Ordered Collection of References):**
```turtle
scex:allowedLicenses a sc:Parameter ;
    sc:parameterOuterType rdf:List ;
    sc:parameterInnerType xsd:anyURI ;
    sc:parameterConfigKey "allowed_licenses" ;
    sc:parameterDefaultValue (
        "https://spdx.org/licenses/Apache-2.0"
        "https://spdx.org/licenses/MIT"
        "https://spdx.org/licenses/GPL-3.0-or-later"
    ) .
```

Configuration:
```toml
[policies.licenses.parameters]
allowed_licenses = [
    "https://spdx.org/licenses/BSD-3-Clause",
    "https://spdx.org/licenses/LGPL-3.0-or-later"
]
```

**List of Strings (Ordered Collection of Text):**
```turtle
scex:requiredKeywords a sc:Parameter ;
    sc:parameterOuterType rdf:List ;
    sc:parameterInnerType xsd:string ;
    sc:parameterConfigKey "required_keywords" ;
    sc:parameterDefaultValue ( "research-software" "open-source" ) .
```

Configuration:
```toml
[policies.keywords.parameters]
required_keywords = ["fair-software", "reproducible-research", "scientific-computing"]
```

**Bag of Strings (Unordered Collection):**
```turtle
scex:allowedLanguages a sc:Parameter ;
    sc:parameterOuterType rdf:Bag ;
    sc:parameterInnerType xsd:string ;
    sc:parameterConfigKey "allowed_programming_languages" ;
    sc:parameterDefaultValue ( "Python" "Java" "C++" ) .
```
