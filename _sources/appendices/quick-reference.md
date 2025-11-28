<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR), Forschungszentrum Jülich (FZJ)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
SPDX-FileContributor: Oliver Bertuch
-->

# Quick Reference

```{todo}
Move this reference into "SHACL Guide for Policy Writers"?
```

## SHACL Constraint Components

| Component                       | Purpose            | Example                       |
| ------------------------------- | ------------------ | ----------------------------- |
| `sh:minCount` / `sh:maxCount`   | Cardinality        | At least 1 author, at most 10 |
| `sh:datatype`                   | Literal type       | Must be a string              |
| `sh:class`                      | Instance type      | Must be a Person              |
| `sh:nodeKind`                   | Node kind          | Must be IRI, not blank node   |
| `sh:hasValue`                   | Specific value     | Must be "Apache-2.0"          |
| `sh:in`                         | Value set          | Must be one of listed options |
| `sh:minLength` / `sh:maxLength` | String length      | Description at least 50 chars |
| `sh:pattern`                    | Regular expression | Email must match pattern      |
| `sh:qualifiedValueShape`        | Counted sub-shape  | At least 1 author from HZDR   |
| `sh:not` / `sh:and` / `sh:or`   | Logic              | Must not be a bot             |

## Parameter Types

These types must be supported by implementations. More types may be available.

**Outer Types:**
- `sc:Scalar` - Single value
- `rdf:List` - Ordered list

**Inner Types:**
- `xsd:string`, `xsd:anyURI`, `xsd:boolean`
- `xsd:integer`, `xsd:int`, `xsd:decimal`, `xsd:float`, `xsd:double`
- `rdfs:Resource`

**Configuration Type Mapping:**
- TOML or JSON string → `xsd:string`, `xsd:anyURI`, `rdfs:Resource`
- TOML or JSON integer → `xsd:integer`, `xsd:int`, `xsd:decimal`
- TOML or JSON float → `xsd:decimal`, `xsd:float`, `xsd:double`
- TOML or JSON boolean → `xsd:boolean`

## Parameter Definition Template

```turtle
<parameter-name> a sc:Parameter ;
    sc:parameterOuterType <scalar-or-collection-type> ;
    sc:parameterInnerType <datatype> ;
    sc:parameterConfigPath "<config-key>" ;
    sc:parameterDefaultValue <default-value> .
```

## Configuration Template

```toml
[policies.<policy-id>]
source = "<policy-url-or-path>"

[policies.<policy-id>.parameters]
<config-key> = <value>
```
