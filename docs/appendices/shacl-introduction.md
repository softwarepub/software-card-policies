<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR), Forschungszentrum Jülich (FZJ)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
SPDX-FileContributor: Oliver Bertuch
-->

# Introduction to SHACL for Policy Writers

The Shapes Constraint Language (SHACL) can be used to formulate constraints on (meta)data.
Constraints are expressed in terms of "shapes".
Each SHACL shape contains the following parts:

1. **[Target Declaration](https://www.w3.org/TR/shacl/#targets)**: Specifies which nodes in the data graph this shape applies to.
2. **Constraints**: Define which properties must exist, which values are allowed, what restrictions apply to cardinality (i.e. counts of properties), etc.
3. **Metadata**: Human-readable names and descriptions of the shape that can be used in validation messages.

**Example: Simple License Policy**

```turtle
scex:licenseRequirements a sh:NodeShape ;
    sh:targetClass schema:SoftwareSourceCode ;

    sh:property [
        sh:name "Apache-2.0 license" ;
        sh:description "Apache-2.0 license must be used" ;

        sh:path schema:license ;
        sh:datatype xsd:string ;
        sh:hasValue "https://spdx.org/licenses/Apache-2.0" ;
    ] .
```

This policy:

- targets all nodes of type `schema:SoftwareSourceCode`, i.e. the software(s) being validated
- requires that the property at the path `schema:license` has the value `"https://spdx.org/licenses/Apache-2.0"`
- provides human-readable name (`sh:name`) and description (`sh:description`) for error messages

## Targeting Strategies

SHACL provides multiple ways to specify which nodes a shape validates.
The choice of targeting strategy depends on what aspect of the metadata you want to validate.

**1. Target by Class (`sh:targetClass`)**

Use this when validating properties of entities of a specific type.

```turtle
scex:softwareRequirements a sh:NodeShape ;
    sh:targetClass schema:SoftwareSourceCode ;

    sh:property [
        sh:path schema:description ;
        sh:minLength 10 ;
    ] .
```


This validates all instances of `schema:SoftwareSourceCode`.

**2. Target by Relationship (`sh:targetObjectsOf`)**

Use this when validating entities that are referenced by a specific property.

```turtle
scex:authorRequirements a sh:NodeShape ;
    sh:targetObjectsOf schema:author ;

    sh:class schema:Person ;
    sh:property [
        sh:path schema:givenName ;
        sh:minCount 1 ;
    ] .
```


This validates all entities that appear as values of the `schema:author` property (i.e., all authors).

**3. Target by Node (`sh:targetNode`)**

Use this when validating a specific, known entity by its IRI.

```turtle
scex:specificSoftwareRequirements a sh:NodeShape ;
    sh:targetNode <https://example.org/my-software> ;

    sh:property [
        sh:path schema:version ;
        sh:minCount 1 ;
    ] .
```


## Common Constraint Patterns

**1. Cardinality Constraints**

Control how many values a property must or may have:

```turtle
sh:property [
    sh:path schema:author ;
    sh:minCount 1 ;        # At least one author required
    sh:maxCount 10 ;       # At most 10 authors allowed
] .
```


**2. Value Type Constraints**

Specify what type of value is allowed:

```turtle
sh:property [
    sh:path schema:license ;
    sh:datatype xsd:string ;     # Must be a string literal
] .

sh:property [
    sh:path schema:author ;
    sh:class schema:Person ;     # Must be an instance of schema:Person
    sh:nodeKind sh:IRI ;         # Must be identified by an IRI (not a blank node)
] .
```


**3. Value Range Constraints**

Restrict values to specific options or ranges:

```turtle
sh:property [
    sh:path schema:license ;
    sh:in (
        "https://spdx.org/licenses/Apache-2.0"
        "https://spdx.org/licenses/MIT"
        "https://spdx.org/licenses/GPL-3.0-or-later"
    ) ;
] .

sh:property [
    sh:path schema:datePublished ;
    sh:minInclusive "2020-01-01"^^xsd:date ;
] .
```


**String Constraints**

Validate string length or patterns:

```turtle
sh:property [
    sh:path schema:description ;
    sh:minLength 50 ;
    sh:maxLength 5000 ;
] .

sh:property [
    sh:path schema:email ;
    sh:pattern "^[^@]+@[^@]+\\.[^@]+$" ;  # Simple email pattern
] .
```

```{todo}
REGEXs for email addresses are notoriously hard.
Note here that this is just an example and that this pattern might not work for every email address out there.
```

**Path Navigation**

Navigate through multiple properties to check nested values:

```turtle
sh:property [
    sh:path ( schema:author schema:affiliation schema:legalName ) ;
    sh:hasValue "Helmholtz-Zentrum Dresden-Rossendorf (HZDR)" ;
] .
```


This checks that at least one author has an affiliation with the specified legal name.

**Qualified Value Shapes**

Count how many values of a property match a specific sub-shape:

```turtle
sh:property [
    sh:path schema:author ;
    sh:qualifiedValueShape [
        sh:path ( schema:affiliation schema:legalName ) ;
        sh:hasValue "Helmholtz-Zentrum Dresden-Rossendorf (HZDR)" ;
    ] ;
    sh:qualifiedMinCount 1 ;  # At least one author must be from HZDR
] .
```


**Logical Constraints**

Use boolean logic to express complex requirements:

```turtle
# Negative constraint: HIFIS Bot should not be an author
sh:not [
    sh:or (
        [ sh:property [ sh:path schema:givenName ; sh:hasValue "HIFIS Bot" ] ]
        [ sh:property [ sh:path schema:email ; sh:hasValue "gitlab-admin@hzdr.de" ] ]
    ) ;
] .
```


## Severity Levels

SHACL supports different severity levels for validation results:

```turtle
sh:property [
    sh:path schema:license ;
    sh:in ( "https://spdx.org/licenses/Apache-2.0" "https://spdx.org/licenses/MIT" ) ;
    sh:severity sh:Warning ;  # This is a recommendation, not a strict requirement
] .
```


List of severity levels:
- `sh:Violation` (default) - A hard requirement that must be met
- `sh:Warning` - A recommendation that should be followed
- `sh:Info` - Informational message
- Custom severity levels - The meaning is defined by the application
