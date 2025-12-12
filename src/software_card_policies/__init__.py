# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

try:
    from software_card_policies._version import version, version_tuple
except ImportError:
    version = "0.0.0"
    version_tuple = (0, 0, 0)

__version__ = version
__version_tuple__ = version_tuple
