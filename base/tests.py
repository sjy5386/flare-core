import os
import sys
import tempfile
from types import ModuleType
from unittest import mock

from django.test import SimpleTestCase

import base.newrelic as newrelic_bootstrap


class InitializeNewRelicTests(SimpleTestCase):
    ENV_KEYS = (
        'NEW_RELIC_LICENSE_KEY',
        'NEW_RELIC_CONFIG_FILE',
        'NEW_RELIC_APP_NAME',
        'NEW_RELIC_ENVIRONMENT',
        'NEW_RELIC_ENABLED',
        'SITE_NAME',
        'APPLICATION_TYPE',
    )

    def setUp(self):
        newrelic_bootstrap._initialized = False
        self._env_backup = {key: os.environ.get(key) for key in self.ENV_KEYS}
        self._modules_backup = {
            name: sys.modules.get(name) for name in ('newrelic', 'newrelic.agent')
        }
        for key in self.ENV_KEYS:
            os.environ.pop(key, None)

    def tearDown(self):
        newrelic_bootstrap._initialized = False
        for key, value in self._env_backup.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        for name, module in self._modules_backup.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module

    def _install_fake_newrelic(self):
        agent = ModuleType('newrelic.agent')
        agent.initialize = mock.Mock()
        package = ModuleType('newrelic')
        package.agent = agent
        sys.modules['newrelic'] = package
        sys.modules['newrelic.agent'] = agent
        return agent

    def test_skips_when_unconfigured(self):
        self.assertFalse(newrelic_bootstrap.initialize_newrelic())

    def test_skips_when_explicitly_disabled(self):
        os.environ['NEW_RELIC_LICENSE_KEY'] = '0' * 40
        os.environ['NEW_RELIC_ENABLED'] = 'false'
        agent = self._install_fake_newrelic()

        self.assertFalse(newrelic_bootstrap.initialize_newrelic())
        agent.initialize.assert_not_called()

    def test_skips_when_package_missing(self):
        os.environ['NEW_RELIC_LICENSE_KEY'] = '0' * 40
        sys.modules.pop('newrelic', None)
        sys.modules.pop('newrelic.agent', None)

        real_import = __import__

        def fake_import(name, *args, **kwargs):
            if name == 'newrelic' or name.startswith('newrelic.'):
                raise ImportError('simulated missing newrelic')
            return real_import(name, *args, **kwargs)

        with mock.patch('builtins.__import__', side_effect=fake_import):
            self.assertFalse(newrelic_bootstrap.initialize_newrelic())

    def test_initializes_from_license_key(self):
        os.environ['NEW_RELIC_LICENSE_KEY'] = '0' * 40
        os.environ['NEW_RELIC_APP_NAME'] = 'Flare Test'
        agent = self._install_fake_newrelic()

        self.assertTrue(newrelic_bootstrap.initialize_newrelic())
        agent.initialize.assert_called_once_with(None, None)
        self.assertTrue(newrelic_bootstrap._initialized)

        # Idempotent on subsequent calls.
        self.assertTrue(newrelic_bootstrap.initialize_newrelic())
        agent.initialize.assert_called_once()

    def test_invalid_config_file_falls_back_to_environment(self):
        """License key + missing CONFIG_FILE must still initialize successfully.

        Regression: the agent re-reads NEW_RELIC_CONFIG_FILE from the environment
        even when initialize(None) is passed, so the invalid path must be removed.
        """
        os.environ['NEW_RELIC_LICENSE_KEY'] = '0' * 40
        os.environ['NEW_RELIC_APP_NAME'] = 'Flare Test'
        os.environ['NEW_RELIC_CONFIG_FILE'] = '/nonexistent/path/newrelic.ini'
        agent = self._install_fake_newrelic()

        self.assertTrue(newrelic_bootstrap.initialize_newrelic())
        agent.initialize.assert_called_once_with(None, None)
        self.assertNotIn('NEW_RELIC_CONFIG_FILE', os.environ)

    def test_valid_config_file_is_passed_through(self):
        with tempfile.NamedTemporaryFile(suffix='.ini', delete=False) as handle:
            config_path = handle.name
            handle.write(b'[newrelic]\n')

        try:
            os.environ['NEW_RELIC_LICENSE_KEY'] = '0' * 40
            os.environ['NEW_RELIC_CONFIG_FILE'] = config_path
            os.environ['NEW_RELIC_ENVIRONMENT'] = 'production'
            agent = self._install_fake_newrelic()

            self.assertTrue(newrelic_bootstrap.initialize_newrelic())
            agent.initialize.assert_called_once_with(config_path, 'production')
            self.assertEqual(os.environ.get('NEW_RELIC_CONFIG_FILE'), config_path)
        finally:
            os.unlink(config_path)

    def test_default_app_name_from_site_and_application_type(self):
        os.environ['NEW_RELIC_LICENSE_KEY'] = '0' * 40
        os.environ['SITE_NAME'] = 'Acme'
        os.environ['APPLICATION_TYPE'] = 'API'
        agent = self._install_fake_newrelic()

        self.assertTrue(newrelic_bootstrap.initialize_newrelic())
        self.assertEqual(os.environ['NEW_RELIC_APP_NAME'], 'Acme API')
        agent.initialize.assert_called_once()
