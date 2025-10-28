<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR), Forschungszentrum Jülich (FZJ)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
SPDX-FileContributor: Oliver Bertuch
-->

# Validation Process

The validation process MUST involve the following steps:

1. *Policy Loading* - Load one or more policy files specified in the configuration
2. *Parameter Resolution* - Replace parameter placeholders with configured values
3. *Shapes Graph Construction* - Combine all loaded and resolved policies into a single shapes graph
4. *Data Graph Loading* - Load the software metadata to be validated
5. *SHACL Validation* - Execute SHACL validation of the data graph against the shapes graph
6. *Report Generation* - Produce a validation report conforming to SHACL standards

## Policy Loading

```{todo}
Extend this subsection.
```

When multiple policies are specified in the configuration, they are all loaded and merged into a single shapes graph.
Each policy file may contribute one or more shapes, and all shapes are evaluated during validation.
This allows modular composition of policies.

## Parameter Resolution

If a policy contains parameters, implementations MUST resolve them before validation:

1. *Identify Parameters* - Scan the policy for all instances of `sc:Parameter`
2. *Lookup Configuration* - For each parameter, use its `sc:parameterConfigKey` to look up a  value in the configuration
3. *Apply Value or Default* - If a configured value is found, use it; otherwise, use the `sc:parameterDefaultValue`. If no value was found and no default was given, produce an error.
4. *Type Validation* - Verify that the provided value matches the parameter's `sc:parameterOuterType` and `sc:parameterInnerType`. If not, produce an error.
5. *Graph Substitution** - Replace all references to the parameter IRI with the resolved value(s) in the shapes graph

**Resolution Example:**

```{todo}
Here we tell SHACL that we want a string.
But then, the parameter is of type `anyURI`!
```

Assume the following policy snippet:
```turtle
sh:property [
    sh:path schema:license ;
    sh:datatype xsd:string ;
    sh:in scex:suggestedLicenses ;  # Parameter reference
] .
```

Given parameter definition:
```turtle
scex:suggestedLicenses a sc:Parameter ;
    sc:parameterOuterType rdf:List ;
    sc:parameterInnerType xsd:anyURI ;
    sc:parameterConfigKey "suggested_licenses" ;
    sc:parameterDefaultValue ( "https://spdx.org/licenses/Apache-2.0" ) .
```


And a configuration in TOML (implementation specific):
```toml
[policies.licenses.parameters]
suggested_licenses = [
    "https://spdx.org/licenses/GPL-3.0-or-later",
    "https://spdx.org/licenses/MIT"
]
```


The resolved shapes graph will have:
```turtle
sh:property [
    sh:path schema:license ;
    sh:datatype xsd:string ;
    sh:in (
        "https://spdx.org/licenses/GPL-3.0-or-later"
        "https://spdx.org/licenses/MIT"
    ) ;
] .
```

### Type Validation

Implementations MUST validate that configured parameter values match the declared inner and outer types before performing parameter resolution. This includes:

1. **Outer Type Validation:**
   - `sc:Scalar`: parameters MUST receive a single value (not an array/list)
   - `rdf:List`: parameters MUST receive an (ordered) array/list of values
   - `rdf:Bag`: parameters MUST receive an (unorderd) array/list of values

2. **Inner Type Validation:**
   - Values MUST be compatible with the declared XSD datatype
   - Type coercion SHOULD follow standard XSD conversion rules where appropriate
   - Type handling MUST comply with the specification in [`sc:parameterInnerType`].

```{todo}
What are the "standard XSD conversion rules"?
Where are they defined?
```

1. **Configuration-to-RDF Type Mapping:**

Implementations MUST map configuration file types to RDF datatypes (`sc:parameterInnerType`) according to the following rules:

| Configuration Format | Config Type       | `sc:parameterInnerType`    | Validation             |
| -------------------- | ----------------- | -------------------------- | ---------------------- |
| TOML                 | String            | `xsd:string`, `xsd:anyURI` | Accept as-is           |
| TOML                 | Integer           | `xsd:int`, `xsd:long`      | Accept as-is           |
| TOML                 | Float             | `xsd:float`, `xsd:double`  | Accept as-is           |
| TOML                 | Integer           | `xsd:float`, `xsd:double`  | Accept with conversion |
| TOML                 | Boolean           | `xsd:boolean`              | Accept as-is           |
| TOML                 | String (URI-like) | `rdfs:Resource`            | Accept if valid IRI    |

Implementations using JSON or YAML as their configuration file formats MUST apply equivalent logic.
More specific datatypes MAY be used if allowed by the used configuration format.

**Type Validation Errors:**

Implementations MUST reject configurations and produce clear error messages when:
- A scalar parameter receives a list/array
- A list parameter receives a single value (non-array)
- A value cannot be converted to the declared inner type (e.g., string `"hello"` for `xsd:int`)
- A resource parameter receives a value that is not a valid IRI

**Example Type Validation:**

Valid configuration:
```toml
[policies.description.parameters]
min_length = 100  # Integer for xsd:int parameter ✓
```


Invalid configurations:
```toml
[policies.description.parameters]
min_length = "100"  # String for xsd:int parameter ✗
min_length = [100, 200]  # List for scalar parameter ✗
```


```{note}
While this specification defines the type system, implementations MUST enforce type safety.
Implementations SHOULD provide detailed error messages indicating:

- Which parameter failed validation
- What type was expected (outer and inner)
- What type/value was actually received
- The location in the configuration file where the error occurred

Both "Integer" and "Float" config types are under the limitations of the configuration file format specification and its implementations.
In most cases, these libraries implicitely provide support for 64 bit internal types, but the implementation MUST take potential compatibility issues into consideration.
```

## Report Generation

Validation reports MUST be valid SHACL validation reports as defined in the SHACL specification.
A validation report is an RDF graph with a root node of type `sh:ValidationReport`.

**Report Structure:**

```turtle
[] a sh:ValidationReport ;
    sh:conforms false ;  # true if no violations, false if any violations
    sh:result [
        a sh:ValidationResult ;
        sh:resultSeverity sh:Violation ;
        sh:focusNode _:b1 ;
        sh:resultPath schema:license ;
        sh:value "https://spdx.org/licenses/Unknown-License" ;
        sh:resultMessage "A license from this list must be chosen." ;
        sh:sourceConstraintComponent sh:InConstraintComponent ;
        sh:sourceShape _:b2 ;
    ] .
```


**Key Report Properties:**

- `sh:conforms` - Boolean indicating whether validation passed
- `sh:result` - Zero or more validation results (one for each constraint violation)
- `sh:resultSeverity` - The severity level (Violation, Warning, Info, custom)
- `sh:focusNode` - The node that failed validation
- `sh:resultPath` - The property path where the issue was found
- `sh:value` - The actual value that caused the violation (if applicable)
- `sh:resultMessage` - Human-readable description of the issue
- `sh:sourceConstraintComponent` - Which SHACL constraint was violated
- `sh:sourceShape` - Which shape contained the violated constraint

### Reporting Parameter Overrides

When a parameter's default value is overridden by configuration, this SHOULD be recorded in the validation report for transparency.
The Software CaRD framework extends the standard SHACL report with:

```turtle
[] a sh:ValidationReport ;
    sh:conforms true ;
    sc:parameterOverride [
        sc:overrideParameter scex:suggestedLicenses ;
        sc:overrideConfiguredValue ( "https://spdx.org/licenses/GPL-3.0-or-later" ) ;
        sc:overrideDefaultValue ( "https://spdx.org/licenses/Apache-2.0" ) ;
    ] .
```

```{todo}
Make sure that this is the best way to solve this.

Also check again here:
[ValidationReport](https://www.w3.org/TR/shacl/#results-validation-report),
[ValidationResult](https://www.w3.org/TR/shacl/#results-validation-result).
It's important that a validation report may only have `conforms: true` if there are no validation results.
This means we can not put information on overridden defaults into the validation reports without making it `conforms: false`.

"The result of a validation process is an RDF graph with exactly one SHACL instance of sh:ValidationReport.
The RDF graph MAY contain additional information such as provenance metadata."

This suggests that it we should put the override information outside of the validation.
Or is inside also ok?
Just not inside the validation results.

Personally, I think putting this information into the validation results and haveing `conforms: false` would be fine, as long as the software clearly communicates to the user what this means and that it might not be a bad thing.
Warnings also cause `conforms: false` anyway.
```

### Report Presentation

While the canonical report format is RDF, implementations MAY present validation results to users in more accessible formats:

- **Plain Text** - Simple list of issues with line-by-line descriptions
- **Markdown** - Formatted text with headers, lists, and emphasis
- **HTML** - Rich web presentation with styling and interactivity
- **JSON** - Structured format for programmatic processing
- **CSV** - Tabular format for spreadsheet import

The presentation format SHOULD preserve key information:

- Whether validation passed or failed overall
- For each issue: severity, location (focus node and path), description, actual vs. expected values

It MAY be enrichted with additional information such as:

- Summary statistics (e.g. number of violations by severity)
