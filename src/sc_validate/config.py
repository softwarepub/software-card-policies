# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum Dresden - Rossendorf (HZDR)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: David Pape

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

import toml


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
class Config:
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


def make_config(*, config_file: Path = None, config_dict: dict = None) -> Config:
    if config_file is None and config_dict is None:
        raise ValueError("Neither config_file nor config_dict were given")
    if config_file is not None and config_dict is not None:
        raise ValueError("Only one of config_file and config_dict may be given")
    if config_dict is None:
        if not config_file.exists():
            raise FileNotFoundError(f"Config file '{config_file}' does not exist")
        if not config_file.is_file():
            raise TypeError(f"Config file '{config_file}' is not a regular file")
        try:
            config_dict = toml.load(config_file)
        except toml.TomlDecodeError:
            raise ValueError(f"Config file '{config_file}' could not be parsed")
    return Config.from_dict(config_dict)
