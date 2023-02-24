# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# This file is autogenerated.
# To change this file you should edit assets/configuration/spec.yaml and then run the following commands:
#     ddev -x validate config -s <INTEGRATION_NAME>
#     ddev -x validate models -s <INTEGRATION_NAME>

from datadog_checks.base.utils.models.fields import get_default_field_value


def shared_custom_metrics(field, value):
    return get_default_field_value(field, value)


def shared_global_custom_queries(field, value):
    return get_default_field_value(field, value)


def shared_service(field, value):
    return get_default_field_value(field, value)


def instance_adoprovider(field, value):
    return 'SQLOLEDB'


def instance_ao_database(field, value):
    return get_default_field_value(field, value)


def instance_autodiscovery_db_service_check(field, value):
    return True


def instance_autodiscovery_exclude(field, value):
    return get_default_field_value(field, value)


def instance_autodiscovery_include(field, value):
    return get_default_field_value(field, value)


def instance_availability_group(field, value):
    return get_default_field_value(field, value)


def instance_aws(field, value):
    return get_default_field_value(field, value)


def instance_azure(field, value):
    return get_default_field_value(field, value)


def instance_command_timeout(field, value):
    return 5


def instance_connection_string(field, value):
    return get_default_field_value(field, value)


def instance_connector(field, value):
    return 'adodbapi'


def instance_custom_queries(field, value):
    return get_default_field_value(field, value)


def instance_database(field, value):
    return 'master'


def instance_database_autodiscovery(field, value):
    return False


def instance_database_autodiscovery_interval(field, value):
    return 3600


def instance_db_fragmentation_object_names(field, value):
    return get_default_field_value(field, value)


def instance_dbm(field, value):
    return False


def instance_disable_generic_tags(field, value):
    return False


def instance_driver(field, value):
    return 'SQL Server'


def instance_dsn(field, value):
    return get_default_field_value(field, value)


def instance_empty_default_hostname(field, value):
    return False


def instance_gcp(field, value):
    return get_default_field_value(field, value)


def instance_ignore_missing_database(field, value):
    return False


def instance_include_ao_metrics(field, value):
    return False


def instance_include_db_fragmentation_metrics(field, value):
    return False


def instance_include_fci_metrics(field, value):
    return False


def instance_include_instance_metrics(field, value):
    return True


def instance_include_master_files_metrics(field, value):
    return False


def instance_include_query_plan_cache_metrics(field, value):
    return False


def instance_include_task_scheduler_metrics(field, value):
    return False


def instance_log_unobfuscated_plans(field, value):
    return False


def instance_log_unobfuscated_queries(field, value):
    return False


def instance_metric_patterns(field, value):
    return get_default_field_value(field, value)


def instance_min_collection_interval(field, value):
    return 15


def instance_obfuscator_options(field, value):
    return get_default_field_value(field, value)


def instance_only_custom_queries(field, value):
    return False


def instance_only_emit_local(field, value):
    return False


def instance_password(field, value):
    return get_default_field_value(field, value)


def instance_proc_only_if(field, value):
    return get_default_field_value(field, value)


def instance_proc_only_if_database(field, value):
    return 'master'


def instance_query_activity(field, value):
    return get_default_field_value(field, value)


def instance_query_metrics(field, value):
    return get_default_field_value(field, value)


def instance_reported_hostname(field, value):
    return get_default_field_value(field, value)


def instance_server_version(field, value):
    return '2014'


def instance_service(field, value):
    return get_default_field_value(field, value)


def instance_stored_procedure(field, value):
    return get_default_field_value(field, value)


def instance_tags(field, value):
    return get_default_field_value(field, value)


def instance_use_global_custom_queries(field, value):
    return 'true'


def instance_username(field, value):
    return get_default_field_value(field, value)
