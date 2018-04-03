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
import argparse

import devopsloft.web


def create_parser():
    """Returns argparse parser."""

    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true',
                        dest="DEVOPSLOFT_DEBUG", help='Turn debug on')
    parser.add_argument('--conf', '-c', dest="DEVOPSLOFT_CONFIG_FILE",
                        help='devopsloft configuration file')
    parser.add_argument('--port', '-p', dest="DEVOPSLOFT_SERVER_PORT",
                        help='devopsloft server port')

    return parser


def launch_app(args=None):
    """Runs Web application."""
    web_server = devopsloft.web.Server(args)
    web_server.run()


def main():
    """Main entry for running the web server."""
    parser = create_parser()
    args = parser.parse_args()
    launch_app(args)
