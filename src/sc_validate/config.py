# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

from dataclasses import dataclass, field
from typing import Any, Dict

CONFIG_FILE_NAME = "config.toml"


@dataclass
class Policy:
    source: str
    parameters: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, policy: dict):
        assert isinstance(policy, dict)
        source = policy.get("source")
        parameters = policy.get("parameters")
        assert source is not None
        assert isinstance(parameters, (dict, type(None)))
        return cls(source=source, parameters=parameters or {})


@dataclass
class Settings:
    policies: Dict[str, Policy]

    @classmethod
    def from_dict(cls, settings: dict):
        assert isinstance(settings, dict)
        assert "policies" in settings
        policies: dict = settings["policies"]
        assert all(isinstance(key, str) for key in policies.keys())
        return cls(
            policies={
                policy_name: Policy.from_dict(policy_settings)
                for policy_name, policy_settings in policies.items()
            }
        )
