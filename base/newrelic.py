"""Optional New Relic APM agent bootstrap.

The agent is enabled only when configuration is present *and* the
``newrelic`` package is installed. Missing package, missing license key,
or initialization failure must never prevent the application from starting.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

_initialized = False


def _is_explicitly_disabled() -> bool:
    value = os.environ.get('NEW_RELIC_ENABLED', 'true').strip().lower()
    return value in {'0', 'false', 'no', 'off'}


def _has_configuration() -> bool:
    if os.environ.get('NEW_RELIC_LICENSE_KEY', '').strip():
        return True
    config_file = os.environ.get('NEW_RELIC_CONFIG_FILE', '').strip()
    return bool(config_file and os.path.isfile(config_file))


def _default_app_name() -> str:
    site_name = os.environ.get('SITE_NAME', 'Flare').strip() or 'Flare'
    application_type = os.environ.get('APPLICATION_TYPE', 'API').strip() or 'API'
    return f'{site_name} {application_type}'


def initialize_newrelic() -> bool:
    """Initialize the New Relic agent when configured.

    Returns:
        True if the agent was initialized successfully, otherwise False.
    """
    global _initialized
    if _initialized:
        return True

    if _is_explicitly_disabled():
        return False

    if not _has_configuration():
        return False

    try:
        import newrelic.agent
    except ImportError:
        logger.warning(
            'New Relic is configured but the newrelic package is not installed; '
            'skipping agent initialization.'
        )
        return False

    # Prefer an explicit app name; otherwise derive one from existing env vars.
    if not os.environ.get('NEW_RELIC_APP_NAME', '').strip():
        os.environ['NEW_RELIC_APP_NAME'] = _default_app_name()

    config_file = os.environ.get('NEW_RELIC_CONFIG_FILE', '').strip() or None
    if config_file and not os.path.isfile(config_file):
        logger.warning(
            'NEW_RELIC_CONFIG_FILE=%s does not exist; '
            'initializing New Relic from environment variables only.',
            config_file,
        )
        config_file = None

    environment = os.environ.get('NEW_RELIC_ENVIRONMENT', '').strip() or None

    try:
        newrelic.agent.initialize(config_file, environment)
    except Exception:
        logger.exception(
            'Failed to initialize the New Relic agent; continuing without it.'
        )
        return False

    _initialized = True
    logger.info(
        'New Relic agent initialized (app_name=%s).',
        os.environ.get('NEW_RELIC_APP_NAME'),
    )
    return True
