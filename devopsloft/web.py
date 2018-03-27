# Copyright 2018 DevOpsLoft
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os

import devopsloft.views

LOG = logging.getLogger(__name__)
app = Flask(__name__, template_folder='templates')

views = (
    (devopsloft.views.home, ''),
)


class Server(object):
    """DevOpsLoft Server"""

    def __init__(self, args=None):

        self.setup_logging()
        self.load_config(args)
        self._register_blueprints()

    def _register_blueprints(self):
        """Registers Flask blueprints."""

        for view, prefix in views:
            app.register_blueprint(view, url_prefix=prefix)

    def load_config(self, args):
        """Load configuration from different sources"""

        self.load_config_from_env()
        self.load_config_from_parser(args)

    def load_config_from_env(self):
        """Loads configuration from environment variables."""
        DEVOPSLOFT_envs = filter(
            lambda s: s.startswith('DEVOPSLOFT_'), os.environ.keys())
        for env_key in DEVOPSLOFT_envs:
            if os.environ[env_key]:
                app.config[env_key] = os.environ[env_key]

    def load_config_from_parser(self, args):
        """Loads configuration based on provided arguments by the user."""
        for k, v in vars(args).items():
            if v:
                app.config[k] = v

    def setup_logging(self):
        """Setup logging level and format."""
        format = '[%(asctime)s] %(levelname)s %(module)s: %(message)s'
        level = logging.INFO
        logging.basicConfig(level=level, format=format)
        handler = RotatingFileHandler('DEVOPSLOFT.log', maxBytes=2000000,
                                      backupCount=10)
        logging.getLogger().addHandler(handler)

    def run(self):
        """Runs the web server."""
        LOG.info("Running DEVOPSLOFT web server")

        app.run(threaded=True, host='0.0.0.0', port=5000)
