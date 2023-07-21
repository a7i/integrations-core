# (C) Datadog, Inc. 2022-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# This file is autogenerated.
# To change this file you should edit assets/configuration/spec.yaml and then run the following commands:
#     ddev -x validate config -s <INTEGRATION_NAME>
#     ddev -x validate models -s <INTEGRATION_NAME>

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence, Union

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from datadog_checks.base.utils.functions import identity
from datadog_checks.base.utils.models import validation

from . import defaults, validators


class TargetMetric(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    label_to_match: Optional[str] = None
    labels_to_get: Optional[Sequence[str]] = None


class LabelJoins(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    target_metric: Optional[TargetMetric] = None


class InstanceConfig(BaseModel):
    model_config = ConfigDict(
        validate_default=True,
        frozen=True,
    )
    exclude_labels: Optional[Sequence[str]] = None
    health_service_check: Optional[bool] = None
    label_joins: Optional[LabelJoins] = None
    label_to_hostname: Optional[str] = None
    labels_mapper: Optional[Mapping[str, Any]] = None
    max_returned_metrics: Optional[int] = None
    metrics: Sequence[Union[Mapping[str, str], str]]
    namespace: str
    prometheus_metrics_prefix: Optional[str] = None
    prometheus_timeout: Optional[int] = None
    prometheus_url: str
    send_histograms_buckets: Optional[bool] = None
    send_monotonic_counter: Optional[bool] = None
    ssl_ca_cert: Optional[str] = None
    ssl_cert: Optional[str] = None
    ssl_private_key: Optional[str] = None
    type_overrides: Optional[Mapping[str, Any]] = None

    @model_validator(mode='before')
    def _initial_validation(cls, values):
        return validation.core.initialize_config(getattr(validators, 'initialize_instance', identity)(values))

    @field_validator('*', mode='before')
    def _ensure_defaults(cls, value, info):
        field = cls.model_fields[info.field_name]
        field_name = field.alias or info.field_name
        if field_name in info.context['configured_fields']:
            return value

        return getattr(defaults, f'instance_{info.field_name}', lambda: value)()

    @field_validator('*')
    def _run_validations(cls, value, info):
        field = cls.model_fields[info.field_name]
        field_name = field.alias or info.field_name
        if field_name not in info.context['configured_fields']:
            return value

        return getattr(validators, f'instance_{info.field_name}', identity)(value, field=field)

    @field_validator('*', mode='after')
    def _make_immutable(cls, value):
        return validation.utils.make_immutable(value)

    @model_validator(mode='after')
    def _final_validation(cls, model):
        return validation.core.check_model(getattr(validators, 'check_instance', identity)(model))
