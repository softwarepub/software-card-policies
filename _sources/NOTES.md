<!--
SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileContributor: David Pape
-->

# NOTES

```{todo}
Remove this file after moving all info to the appropriate places.
```

Notes from the research and development process.

## Resources

Specifications:

```{todo}
Link these in the policies spec
```

- [SHACL](https://www.w3.org/TR/shacl/)
- [SHACL JavaScript Extensions](https://www.w3.org/TR/shacl-js/)

Implementations:

```{todo}
These could be provided as extra information in an appendix.
```

- [pySHACL](https://github.com/RDFLib/pySHACL)
- ~~[shacl-js](https://github.com/TopQuadrant/shacl-js)~~ (unmaintained)
- [rdf-validate-shacl](https://github.com/zazuko/rdf-validate-shacl)
- [shacl-engine](https://github.com/rdf-ext/shacl-engine) (also JavaScript)

Other:

```{todo}
Some of these might be good to put into the SHACL guide for policy writers.
```

- [SHACL playground](https://shacl.org/playground/) (no SPARQL support)
- [rdf-validate-shacl playground](https://shacl-playground.zazuko.com/)
- [SHACL Play!](https://shacl-play.sparna.fr/play/)
- [Book: Validating RDF Data](https://book.validatingrdf.com)

## pySHACL Usage

[pySHACL](https://github.com/RDFLib/pySHACL/) can be installed from PyPI:

```bash
pip install 'pyshacl[js]'
# or
pipx install 'pyshacl[js]'
```

It can be used to validate a data graph `data.ttl` against a SHACL shapes graph `shapes.ttl` like so:

```bash
pyshacl --metashacl --imports --js -s shapes.ttl data.ttl
```

The `--metashacl` flag validates the shapes graph, first.
The `--imports` flag is required in order for pySHACL to resolve `owl:imports` properties.
The `--js` flag enables JavaScript functionality.

pySHACL can also be used as a library.
