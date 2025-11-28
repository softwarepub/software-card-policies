<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR), Forschungszentrum Jülich (FZJ)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
SPDX-FileContributor: Oliver Bertuch
-->

# Policy Creation

Policies MUST be written as SHACL shapes.

The basic anatomy of any SHACL Shape MUST follow this pattern:

1. **Target Declaration** - Specifies which nodes in the data graph this shape applies to
2. **Constraints** - Define what properties must exist, what values are allowed, cardinality restrictions, etc.
3. **Metadata** - Human-readable names and descriptions for validation messages

Example: _Simple License Policy_
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
- Targets all nodes of type `schema:SoftwareSourceCode` (the software being validated)
- Requires that the `schema:license` property has the specific value `"https://spdx.org/licenses/Apache-2.0"`
- Provides human-readable name and description for use in error messages

## Organizing Multiple Shapes

A policy file MUST contain at least one, ~~or~~ and MAY contain multiple shape definitions. ~~that specify constraints on the metadata.~~
//
A _policy_ MUST contain at least one _policy item_.
Each _policy item_ constitutes a shape definition.

Example:
```turtle
# Shape targeting the software itself
scex:softwareRequirements a sh:NodeShape ;
    sh:targetClass schema:SoftwareSourceCode ;
    sh:property [
        sh:path schema:author ;
        sh:minCount 1 ;
    ] .

# Shape targeting each author
scex:authorRequirements a sh:NodeShape ;
    sh:targetObjectsOf schema:author ;
    sh:class schema:Person ;
    sh:property [
        sh:path schema:givenName ;
        sh:minCount 1 ;
    ] .
```

Multiple shapes in a single policy file SHOULD be ~~somehow~~ related.
Related shapes MAY validate different aspects of the metadata in a coordinated way.

## SHACL Feature Restrictions

For security, simplicity, and portability, this specification restricts which SHACL features MAY be used in policies.

Any implementation SHOULD follow these restrictions:

**Allowed Core SHACL Features:**
- All core SHACL constraint components (property shapes, node shapes, value constraints, cardinality constraints, etc.)
- Logical constraint components (`sh:and`, `sh:or`, `sh:not`, `sh:xone`)
- Shape-based constraint components (`sh:node`, `sh:qualifiedValueShape`)
- Property path syntax for navigation
- Severity levels
- Human-readable metadata (`sh:name`, `sh:description`, `sh:message`, `rdfs:comment`)
- Custom constraint components defined with `sh:ConstraintComponent`

**JavaScript Execution:**

SHACL-JS (JavaScript-based constraints) support is **optional** and MUST be configurable in implementations. SHACL-JS enables more sophisticated validation scenarios such as:

- Checking values against external controlled vocabularies via SKOS APIs
- Complex string transformations and pattern matching
- Custom validation logic not expressible in core SHACL (e.g. validating identifier checksums)

However, JavaScript execution poses significant **security risks**:
- *Arbitrary code execution:* Malicious policies could execute harmful code
- *Data exfiltration:* JavaScript code could transmit sensitive metadata to external servers
- *Resource exhaustion:* Infinite loops or memory-intensive operations could cause denial of service
- *Privilege escalation:* In certain environments, JavaScript might access system resources

**Security Requirements for Implementations:**

Implementations that support SHACL-JS MUST:
1. *Provide a configuration option* to enable or disable JavaScript execution (RECOMMENDED: disabled by default)
2. *Clearly document* whether JavaScript execution is enabled and to what extent
3. *Warn users* when validating with JavaScript-enabled policies from untrusted sources

Implementations that support SHACL-JS SHOULD implement additional security measures such as:
- *Process isolation:* Execute validation in sandboxed processes or containers
- *Timeouts:* Enforce maximum execution time for validation operations
- *Resource limits:* Restrict memory usage, CPU time, and network access
- *Network isolation:* Block or restrict network access during validation
- *Input sanitization:* Validate and sanitize all data before JavaScript processing
- *Audit logging:* Log all JavaScript execution events for security monitoring

Organizations using validation tools SHOULD:
- Only load policies from trusted, verified sources
- Use HTTPS for policy retrieval to guarantee data integrity
- Consider maintaining an internal policy repository with security review processes
- Disable JavaScript execution unless specifically required for their use cases

**Disallowed Advanced (SHACL) Features:**
- OWL imports (`owl:imports`) - Avoid loading constraints not vetted by the implementation
- SHACL-SPARQL features (`sh:sparql`) - SPARQL queries pose similar security risks to JavaScript
- `sh:rule` (SHACL Rules for inferencing) - Rules can modify data and may have unintended side effects

These restrictions ensure that policies using only core features can be safely executed and validated using standard SHACL Core validators.

