<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR), Forschungszentrum Jülich (FZJ)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
SPDX-FileContributor: Oliver Bertuch
-->

# Examples

This section provides annotated examples for policy authors and policy makers to understand common patterns.

## Example 1: Fixed License Requirement

**Use Case:** An organization requires all software to be licensed under Apache-2.0.

**Policy (license-fixed.ttl):**

```turtle
scex:licenseRequirements a sh:NodeShape ;
    sh:targetClass schema:SoftwareSourceCode ;

    sh:property [
        sh:name "Apache-2.0 license required" ;
        sh:description "All software must be licensed under Apache-2.0." ;

        sh:path schema:license ;
        sh:minCount 1 ;
        sh:hasValue "https://spdx.org/licenses/Apache-2.0" ;
    ] .
```


**Configuration:**

```toml
[policies.licenses]
source = "https://example.org/policies/license-fixed.ttl"
```


**What it validates:**
- The software must have at least one `schema:license` property
- The value must exactly match the Apache-2.0 SPDX identifier

## Example 2: Suggested Licenses (Parameterizable)

**Use Case:** An organization recommends certain licenses but doesn't strictly require them.

**Policy (licenses-suggested.ttl):**

```turtle
scex:suggestedLicenses a sc:Parameter ;
    sc:parameterOuterType rdf:List ;
    sc:parameterInnerType xsd:anyURI ;
    sc:parameterConfigPath "suggested_licenses" ;
    sc:parameterDefaultValue (
        "https://spdx.org/licenses/Apache-2.0"
        "https://spdx.org/licenses/MIT"
    ) .

scex:licenseRequirements a sh:NodeShape ;
    sh:targetClass schema:SoftwareSourceCode ;

    sh:property [
        sh:name "Suggested license" ;
        sh:description "A license from the organization's recommended list should be chosen." ;
        sh:severity sh:Warning ;

        sh:path schema:license ;
        sh:in scex:suggestedLicenses ;
    ] .
```


**Configuration:**

```toml
[policies.licenses]
source = "https://example.org/policies/licenses-suggested.ttl"

[policies.licenses.parameters]
suggested_licenses = [
    "https://spdx.org/licenses/GPL-3.0-or-later",
    "https://spdx.org/licenses/LGPL-3.0-or-later",
    "https://spdx.org/licenses/MIT"
]
```


**What it validates:**
- If a license is specified, it should be one from the configured list
- Uses Warning severity, so non-compliant licenses generate warnings rather than violations
- Different organizations can use the same policy with their own preferred license lists

## Example 3: Author Affiliation Requirements

**Use Case:** Ensure at least one author is affiliated with a specific organization.

**Policy (authors-affiliation.ttl):**

```turtle
scex:requireHZDR a sc:Parameter ;
    sc:parameterOuterType sc:Scalar ;
    sc:parameterInnerType xsd:string ;
    sc:parameterConfigPath "required_affiliation" ;
    sc:parameterDefaultValue "Helmholtz-Zentrum Dresden-Rossendorf (HZDR)" .

scex:authorsRequirements a sh:NodeShape ;
    sh:targetClass schema:SoftwareSourceCode ;

    sh:property [
        sh:name "Required affiliation" ;
        sh:description "At least one author must be affiliated with the specified organization." ;

        sh:path schema:author ;
        sh:qualifiedValueShape [
            sh:path ( schema:affiliation schema:legalName ) ;
            sh:hasValue scex:requireHZDR ;
        ] ;
        sh:qualifiedMinCount 1 ;
    ] .
```


**Configuration:**

```toml
[policies.authors]
source = "https://example.org/policies/authors-affiliation.ttl"
parameters = {required_affiliation = "German Aerospace Center (DLR)"}
```


**What it validates:**
- The software must have at least one author whose affiliation's legal name matches the configured value
- Uses property path navigation to reach the affiliation's name
- Different organizations can reuse the policy with their own affiliation name

## Example 4: Description Length Requirements

**Use Case:** Ensure software descriptions are sufficiently detailed.

**Policy (description-length.ttl):**

```turtle
scex:minDescriptionLength a sc:Parameter ;
    sc:parameterOuterType sc:Scalar ;
    sc:parameterInnerType xsd:integer ;
    sc:parameterConfigPath "description_min_length" ;
    sc:parameterDefaultValue 50 .

scex:descriptionRequirements a sh:NodeShape ;
    sh:targetClass schema:SoftwareSourceCode ;

    sh:property [
        sh:name "Minimum description length" ;
        sh:description "The description must be sufficiently detailed." ;

        sh:path schema:description ;
        sh:minCount 1 ;
        sh:minLength scex:minDescriptionLength ;
    ] .
```


**Configuration:**

```toml
[policies.description]
source = "https://example.org/policies/description-length.ttl"
parameters = {description_min_length = 100}
```


**What it validates:**
- The software must have a description
- The description must be at least the configured number of characters long

## Example 5: Author Person Type and ORCID

**Use Case:** Ensure all authors are persons (not organizations) and have ORCID identifiers.

**Policy (authors-person-orcid.ttl):**

```turtle
scex:authorRequirements a sh:NodeShape ;
    sh:targetObjectsOf schema:author ;

    # Authors must be persons, not organizations
    sh:class schema:Person ;

    # Authors must be identified by IRI (ORCID)
    sh:nodeKind sh:IRI ;

    sh:property [
        sh:name "Given name required" ;
        sh:path schema:givenName ;
        sh:minCount 1 ;
    ] ;

    sh:property [
        sh:name "Family name required" ;
        sh:path schema:familyName ;
        sh:minCount 1 ;
    ] .
```


**Configuration:**

```toml
[policies.authors]
source = "https://example.org/policies/authors-person-orcid.ttl"
```


**What it validates:**
- Each entity listed as an author must be of type `schema:Person`
- Each author must be identified by an IRI (typically an ORCID like `https://orcid.org/0000-0002-1234-5678`)
- Each author must have both a given name and family name

## Example 6: Exclusion Pattern (Negative Constraint)

**Use Case:** Prevent automated bot accounts from being listed as authors.

**Policy (authors-no-bots.ttl):**

```turtle
scex:authorRequirements a sh:NodeShape ;
    sh:targetObjectsOf schema:author ;

    sh:not [
        sh:or (
            [ sh:property [ sh:path schema:givenName ; sh:hasValue "HIFIS Bot" ] ]
            [ sh:property [ sh:path schema:email ; sh:hasValue "gitlab-admin@hzdr.de" ] ]
            [ sh:property [ sh:path schema:email ; sh:hasValue "gitlab-admin+bot@hzdr.de" ] ]
        ) ;
    ] .
```


**Configuration:**

```toml
[policies.authors]
source = "https://example.org/policies/authors-no-bots.ttl"
```

**What it validates:**
- No author may have the given name "HIFIS Bot"
- No author may have certain bot-associated email addresses
- Uses logical negation (`sh:not`) and disjunction (`sh:or`) to express the exclusion
