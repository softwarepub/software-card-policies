.. SPDX-FileCopyrightText: 2025 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
   SPDX-License-Identifier: CC-BY-4.0
   SPDX-FileContributor: David Pape

Validator
=========

The validator can be run using the ``software-card-validate`` command which is
equivalent to ``python -m software_card_policies``.

.. code:: bash
   :caption: Basic usage.

   software-card-validate --config config.toml metadata.ttl

This example will:

1. Load policies specified in ``config.toml``
2. Resolve any parameters from the configuration
3. Validate the metadata in ``metadata.ttl`` using the given policies
4. Print a validation report
