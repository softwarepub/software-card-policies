<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR), Forschungszentrum Jülich (FZJ)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
SPDX-FileContributor: Oliver Bertuch
-->

# Introduction

```{note}
This specification is a living document and will be updated as the Software CaRD project evolves.
Feedback and contributions are welcome via the [issue tracker](https://github.com/softwarepub/software-card-policies/issues).
The specification is licensed under [`CC-BY-4.0`](https://creativecommons.org/licenses/by/4.0/)
```

This documentation specifies how to write and configure machine-readable policies for validating research software metadata.
It defines a framework based on SHACL (Shapes Constraint Language) that enables organizations and communities to express their metadata requirements in a standardized, interoperable way.

The specification serves two audiences:

1. **Developers and technical writers** who create policy files containing validation rules
2. **Policy makers and other stakeholders** who need to understand the capabilities and limitations of this approach to define organizational requirements

## The Software CaRD Project

[Software CaRD](https://helmholtz-metadaten.de/en/inf-projects/softwarecard) (`ZT-I-PF-3-080`) is a project funded by the Initiative and Networking Fund of the Helmholtz Association in the framework of the Helmholtz Metadata Collaboration.
The project aims to improve the quality and FAIRness of research software metadata through automated validation and curation support.

## Motivation

In recent years, researchers and institutions have made substantial efforts to publish research software with rich metadata.
Guidelines and policies have been developed to help researchers make their publications more FAIR in accordance with the FAIR and FAIR4RS principles.
However, curation of software publications is still an arduous manual process.
Curators lack tooling that helps them automatically check publication metadata for common issues or pitfalls, or violations of organizational policies.
In order to prevent development of custom solutions, and to promote interoperability of tooling and machine-readable policies, a common framework for policy description and validation is required.

## Summary

This specification defines a framework for expressing software metadata validation policies using SHACL.
It enhances the capabilities of SHACL with a parameterization mechanism that allows policies to be configurable and reusable across different contexts.
The framework enables:

- **Declarative Policy Definition:** Policies are written as SHACL shapes in RDF format, making them machine-readable
- **Parameterization:** Policies can include configurable parameters that are resolved at validation time from configuration files, enabling the same policy template to be used with different constraints.
- **Standard Validation Reports:** Validation produces standard SHACL validation reports that can be processed by existing tooling or presented to users in various ways.
- **Web-based Distribution:** Policies can be published on the web and referenced by URL, facilitating sharing and reuse across organizations.

## Goals

- Provide a framework that enables automated validation of research software metadata against organizational policies
- Build on existing standards (SHACL, RDF, Schema.org, Codemeta) and tools rather than creating proprietary/custom solutions
- Enable policy sharing and reuse through web-based distribution and parameterization
- Produce machine-readable validation reports that can drive automated workflows
- Support both technical implementers and non-technical policy makers through clear documentation

```{todo}
The following paragraph was taken from down below.
Work it into this subsection.

This allows viewers of the report (e.g. curators) to understand which parameters were customized ~~from their defaults~~.
~~In the curation dashboard, this will allow curators to look at the provenance of automated hints.~~
```

```{todo}
Motivation, summary and goals are very similar.
Clearly differentiate!
```

## Conclusion

```{todo}
As this is a browsable website and not an article to be read front to back, we don't really need a conclusion.
Work this into the other sections on this page.
```

This specification provides a comprehensive framework for expressing and validating research software metadata policies using SHACL.
By building on established W3C standards and adding parameterization capabilities, it enables organizations to:

- Express their metadata requirements in a machine-readable, interoperable format
- Share and reuse policies across institutions
- Automate validation to reduce manual curation effort
- Support researchers in creating high-quality, FAIR software publications

The framework is designed to be accessible to both technical implementers and policy-making stakeholders, supporting the full lifecycle from policy definition to validation and reporting.
