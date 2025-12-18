.. SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
   SPDX-License-Identifier: CC-BY-4.0
   SPDX-FileContributor: David Pape

Library
=======

The reference implementation can also be used as a Python library for integration into
other tools.
E.g., to "parameterize" a graph which contains ``sc:Parameter`` objects, you can use the
following snippet:

.. code:: python
   :caption: Graph parameterization using the library.

   from rdflib import Graph
   from software_card_policies.data_model import parameterize_graph

   policy_graph = Graph()  # the graph containing policies with parameter placeholders
   config_parameters = {}  # the values to override the placeholders

   parameterized_graph = parameterize_graph(policy_graph, config_parameters)

The full validator implementation based on the library can be found in
``software_card_policies.__main__``.
