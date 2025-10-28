<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR), Forschungszentrum Jülich (FZJ)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
SPDX-FileContributor: Oliver Bertuch
-->

# Considerations

## Security

**SHACL Feature Restrictions:**
This specification deliberately excludes SHACL-SPARQL and SHACL-JS features to prevent arbitrary code execution.
Policies can only use declarative SHACL Core features, which can be safely evaluated without security risks.

**Web Resource Loading:** When loading policies from the web, implementations should:
- Use HTTPS when possible to prevent tampering
- Implement timeouts to prevent denial-of-service
- Validate that loaded resources are well-formed RDF before processing
- Consider caching mechanisms to reduce network dependencies

**Configuration Validation:** Configuration files should be validated before use to prevent injection attacks or misconfigurations.

## Privacy

Validation reports may contain sensitive information from the metadata being validated (such as author names, email addresses, affiliations).
When presenting or storing reports:

- Consider whether personal data needs to be redacted
- Implement appropriate access controls for reports
- Comply with applicable data protection regulations (GDPR, etc.)

## Accessibility

Validation report presentations should be accessible:

- Use semantic HTML with appropriate ARIA labels
- Ensure sufficient color contrast in visual presentations
- Provide text alternatives for graphical representations
- Support keyboard navigation in interactive presentations

```{todo}
This is specific to HTML.
Can we find a more generic way of phrasing this?
Suggestions on HTML may be kept as an exmaple.
```

## Performance

**Caching:** Implementations should cache loaded policy files to avoid repeated network requests:
- Cache policies fetched from the web
- Use standard HTTP caching headers (ETag, Last-Modified)
- Provide cache invalidation mechanisms

```{todo}
This might be difficult to achieve in the reference implementation.
I don't think pySHACL / rdflib support this use case very well.
```

**Validation Efficiency:** For large metadata graphs or complex policies:
- Consider streaming or incremental validation approaches
- Provide progress indicators for long-running validations
- Allow validation of individual policies or subsets

```{todo}
I don't think this will be an actual problem.
Implementing streaming would be worth the hassle for text files that will probably amount to less than a metabyte.
```

**Resource Limits:** Implementations should guard against resource exhaustion:
- Limit maximum graph size
- Implement timeouts for validation operations
- Provide clear error messages when limits are exceeded

## Extensibility

While this specification defines core features, implementations may extend functionality:

- Additional parameter types beyond those specified
- Custom report presentation formats
- Integration with metadata collection tools
- Batch validation of multiple metadata files
- Continuous integration hooks

Extensions should be clearly documented and should not break compatibility with the core specification.

## Versioning

As the Software CaRD framework evolves:

- Policy files should indicate which version of the specification they conform to
- Configuration files should support version specification
- Validators should clearly indicate which specification version they implement
- Backward compatibility should be maintained where possible
