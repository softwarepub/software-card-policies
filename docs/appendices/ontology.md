<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR), Forschungszentrum Jülich (FZJ)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
SPDX-FileContributor: Oliver Bertuch
-->

# Parameter Ontology & SHACL Shapes

```{todo}
"Parameter Ontology" is quite the narrow scope.
We should phrase this more vaguely to we don't need to change everything later, should we decide to add more concepts.
```

```{todo}
Put this as a file somewhere so that it can be embedded here, but downloaded by a client, too.
```

```{todo}
The formatting used in these code blocks is not supported by the code highlighter, causing warnings when compiling the documentation.
See: <https://github.com/pygments/pygments/pull/2980>
```

Formal OWL definition:

```{todo}
There are loads of errors in this.
```

```turtle
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sc: <https://schema.software-metadata.pub/software-card/2025-01/#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# ============================================================================
# Software CaRD Parameter Ontology (OWL)
# ============================================================================
#
# This file defines the semantic model for Software CaRD parameters using OWL.
# It specifies:
# - Class definitions and their relationships
# - Property definitions with domains and ranges
# - Basic cardinality constraints
# - Enumerated sets of allowed values
#
# NOTE: This OWL ontology is complemented by a SHACL shapes file
# (sc-parameter-shacl.ttl) that provides additional validation constraints
# that cannot be expressed in OWL, such as:
# - Minimum string length requirements
# - Specific literal datatype enforcement
# - Additional validation rules
#
# Both files work together to provide complete semantic definition and
# validation for Software CaRD parameters.
# ============================================================================

<https://schema.software-metadata.pub/software-card/2025-01/Parameter>
    a owl:Ontology ;
    rdfs:label "Software CaRD Parameter Ontology"@en ;
    rdfs:comment """OWL ontology defining the semantic model for configurable parameters
                    in Software CaRD policies."""@en ;
    owl:versionInfo "0.1" ;
    rdfs:seeAlso <https://schema.software-metadata.pub/software-card/2025-01/Parameter> .

# Define allowed inner types as an enumerated class
sc:AllowedInnerType a owl:Class ;
    rdfs:label "Allowed Inner Type"@en ;
    rdfs:comment """The set of datatypes that may be used as inner types for parameters.
                    This includes common XSD datatypes for literals and rdfs:Resource for
                    IRI references."""@en ;
    owl:oneOf (
        xsd:string
        xsd:boolean
        xsd:integer
        xsd:int
        xsd:decimal
        xsd:float
        xsd:double
        xsd:anyURI
        rdfs:Resource
    ) ;
    rdfs:isDefinedBy <https://schema.software-metadata.pub/software-card/2025-01/#> .

# Define allowed outer types as an enumerated class
sc:AllowedOuterType a owl:Class ;
    rdfs:label "Allowed Outer Type"@en ;
    rdfs:comment """The set of container types that may be used as outer types for parameters.
                    This includes scalar (single value), ordered lists, and unordered bags."""@en ;
    owl:oneOf ( sc:Scalar rdf:List rdf:Bag ) ;
    rdfs:isDefinedBy <https://schema.software-metadata.pub/software-card/2025-01/#> .

# Class Definition with cardinality restrictions
sc:Parameter a owl:Class ;
    rdfs:label "Parameter"@en ;
    rdfs:comment """A configurable placeholder in a Software CaRD policy that can be
                    assigned different values through a configuration file. Parameters
                    enable policy reuse across different contexts by allowing specific
                    constraints to be customized without modifying the policy itself.

                    Each parameter must specify:
                    - An outer type (container structure: scalar, list, or bag)
                    - An inner type (datatype of values)
                    - A configuration key (where to find the value in config)
                    - A description (via rdfs:comment)
                    - Optionally, a default value (if omitted, parameter is required)"""@en ;
    rdfs:subClassOf [
        a owl:Restriction ;
        owl:onProperty rdfs:comment ;
        owl:cardinality 1 ;
        rdfs:comment "Every parameter must have exactly one description."@en
    ] ;
    rdfs:subClassOf [
        a owl:Restriction ;
        owl:onProperty sc:parameterOuterType ;
        owl:cardinality 1 ;
        rdfs:comment "Every parameter must have exactly one outer type."@en
    ] ;
    rdfs:subClassOf [
        a owl:Restriction ;
        owl:onProperty sc:parameterInnerType ;
        owl:cardinality 1 ;
        rdfs:comment "Every parameter must have exactly one inner type."@en
    ] ;
    rdfs:subClassOf [
        a owl:Restriction ;
        owl:onProperty sc:parameterConfigKey ;
        owl:cardinality 1 ;
        rdfs:comment "Every parameter must have exactly one configuration key."@en
    ] ;
    rdfs:subClassOf [
        a owl:Restriction ;
        owl:onProperty sc:parameterDefaultValue ;
        owl:maxCardinality 1 ;
        rdfs:comment "A parameter may have at most one default value. If omitted, the parameter is required."@en
    ] ;
    rdfs:isDefinedBy <https://schema.software-metadata.pub/software-card/2025-01/#> .

# Properties

sc:parameterOuterType a owl:ObjectProperty ;
    rdfs:label "parameter outer type"@en ;
    rdfs:comment """Specifies the container/cardinality type of the parameter value.
                    Determines whether the parameter represents a single value (sc:Scalar),
                    an ordered collection (rdf:List), or an unordered collection (rdf:Bag)."""@en ;
    rdfs:domain sc:Parameter ;
    rdfs:range sc:AllowedOuterType ;
    rdfs:isDefinedBy <https://schema.software-metadata.pub/software-card/2025-01/#> .

sc:parameterInnerType a owl:ObjectProperty ;
    rdfs:label "parameter inner type"@en ;
    rdfs:comment """Specifies the datatype of the individual value(s) in the parameter.
                    Must be one of the supported XSD datatypes or rdfs:Resource for IRI references."""@en ;
    rdfs:domain sc:Parameter ;
    rdfs:range sc:AllowedInnerType ;
    rdfs:isDefinedBy <https://schema.software-metadata.pub/software-card/2025-01/#> .

sc:parameterConfigKey a owl:DatatypeProperty ;
    rdfs:label "parameter configuration key"@en ;
    rdfs:comment """A string that identifies the configuration key for this parameter.
                    Used to look up the configured value in the configuration file during
                    parameter resolution. Must be a non-empty string."""@en ;
    rdfs:domain sc:Parameter ;
    rdfs:range xsd:string ;
    rdfs:isDefinedBy <https://schema.software-metadata.pub/software-card/2025-01/#> .

sc:parameterDefaultValue a rdf:Property ;
    rdfs:label "parameter default value"@en ;
    rdfs:comment """The value to use when no configured value is provided. If omitted, the
                    parameter becomes required and must be provided in the configuration file.
                    When present, the default value must match the parameter's declared outer
                    and inner types. For scalar parameters, this is a single literal or resource.
                    For list or bag parameters, this is an rdf:List or rdf:Bag."""@en ;
    rdfs:domain sc:Parameter ;
    rdfs:isDefinedBy <https://schema.software-metadata.pub/software-card/2025-01/#> .

# Scalar Type Definition
sc:Scalar a rdfs:Datatype ;
    rdfs:label "Scalar"@en ;
    rdfs:comment """Represents a single value (as opposed to a collection). Used as the
                    outer type for parameters that accept exactly one value."""@en ;
    rdfs:isDefinedBy <https://schema.software-metadata.pub/software-card/2025-01/#> .
```

Formal SHACL definition:

```{todo}
There are loads of errors in this.
```

```turtle
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sc: <https://schema.software-metadata.pub/software-card/2025-01/#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

# ============================================================================
# Software CaRD Parameter Validation Shapes (SHACL)
# ============================================================================
#
# This file defines SHACL validation constraints for Software CaRD parameters.
# It specifies detailed validation rules that complement the OWL ontology,
# including:
# - String length requirements
# - Explicit datatype constraints on literals
# - Value enumeration validation
# - Additional structural constraints
#
# NOTE: This SHACL shapes file works together with the OWL ontology file
# (sc-parameter-owl.ttl) to provide complete validation. The OWL file defines
# the semantic model while this file provides detailed validation rules that
# cannot be expressed in OWL alone.
#
# Use this file with a SHACL validator to check whether parameter definitions
# conform to the Software CaRD specification.
# ============================================================================

<https://schema.software-metadata.pub/software-card/2025-01/Parameter>
    a owl:Ontology ;
    rdfs:label "Software CaRD Parameter Validation Shapes"@en ;
    rdfs:comment """SHACL shapes for validating Software CaRD parameter definitions."""@en ;
    owl:versionInfo "0.1" ;
    owl:imports <https://schema.software-metadata.pub/software-card/2025-01/Parameter> ;
    rdfs:seeAlso <https://schema.software-metadata.pub/software-card/2025-01/Parameter> .

# Constraints expressed as SHACL shapes
sc:ParameterShape a sh:NodeShape ;
    sh:targetClass sc:Parameter ;
    rdfs:label "Parameter Shape"@en ;
    rdfs:comment """SHACL shape defining validation constraints on sc:Parameter instances.
                    This shape enforces structural and datatype requirements that complement
                    the OWL ontology definition."""@en ;

    # Must have exactly one outer type from allowed set
    sh:property [
        sh:path sc:parameterOuterType ;
        sh:name "Outer Type"@en ;
        sh:description "The container/cardinality type of the parameter."@en ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:in ( sc:Scalar rdf:List rdf:Bag ) ;
        sh:message "Parameter must have exactly one outer type: sc:Scalar, rdf:List, or rdf:Bag."@en ;
    ] ;

    # Must have exactly one inner type from allowed set
    sh:property [
        sh:path sc:parameterInnerType ;
        sh:name "Inner Type"@en ;
        sh:description "The datatype of the individual value(s)."@en ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:in (
            xsd:string
            xsd:boolean
            xsd:integer
            xsd:int
            xsd:decimal
            xsd:float
            xsd:double
            xsd:anyURI
            rdfs:Resource
        ) ;
        sh:message "Parameter must have exactly one inner type from the supported list."@en ;
    ] ;

    # Must have exactly one non-empty config key
    sh:property [
        sh:path sc:parameterConfigKey ;
        sh:name "Configuration Key"@en ;
        sh:description "The key used to look up this parameter's value in the configuration file."@en ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
        sh:minLength 1 ;
        sh:message "Parameter must have exactly one non-empty configuration key string."@en ;
    ] ;

    # Must have exactly one description of sufficient length
    sh:property [
        sh:path rdfs:comment ;
        sh:name "Description"@en ;
        sh:description "Human-readable description of the parameter's purpose and usage."@en ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
        sh:minLength 10 ;
        sh:message "Parameter must have exactly one rdfs:comment description of at least 10 characters."@en ;
    ] ;

    # May have at most one default value (optional - if omitted, parameter is required)
    sh:property [
        sh:path sc:parameterDefaultValue ;
        sh:name "Default Value"@en ;
        sh:description "Optional default value used when no configured value is provided."@en ;
        sh:maxCount 1 ;
        sh:message "Parameter may have at most one default value. If omitted, the parameter is required."@en ;
    ] ;

    rdfs:isDefinedBy <https://schema.software-metadata.pub/software-card/2025-01/#> .
```
