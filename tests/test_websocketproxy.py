# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright(c)2013 NTT corp. All Rights Reserved.
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

""" Unit tests for websocketproxy """
import unittest
import time
import subprocess
import stubout
import select

from websockify import websocketproxy


class MockSocket(object):
    def __init__(*args, **kwargs):
        pass

    def shutdown(*args):
        pass

    def close(*args):
        pass


class WebSocketProxyTest(unittest.TestCase):

    def setUp(self):
        """Called automatically before each test."""
        super(WebSocketProxyTest, self).setUp()

        self.soc = ''
        self.stubs = stubout.StubOutForTesting()

    def tearDown(self):
        """Called automatically after each test."""
        self.stubs.UnsetAll()
        super(WebSocketProxyTest, self).tearDown()

    def test_run_wrap_cmd(self):
        web_socket_proxy = websocketproxy.WebSocketProxy()
        web_socket_proxy.__dict__["wrap_cmd"] = "wrap_cmd"

        def mock_Popen(*args, **kwargs):
            return '_mock_cmd'

        self.stubs.Set(subprocess, 'Popen', mock_Popen)
        web_socket_proxy.run_wrap_cmd()
        self.assertEquals(web_socket_proxy.spawn_message, True)

    def test_started(self):
        web_socket_proxy = websocketproxy.WebSocketProxy()
        web_socket_proxy.__dict__["spawn_message"] = False
        web_socket_proxy.__dict__["wrap_cmd"] = "wrap_cmd"

        def mock_run_wrap_cmd(*args, **kwargs):
            web_socket_proxy.__dict__["spawn_message"] = True

        self.stubs.Set(web_socket_proxy, 'run_wrap_cmd', mock_run_wrap_cmd)
        web_socket_proxy.started()
        self.assertEquals(web_socket_proxy.__dict__["spawn_message"], True)

    def test_poll(self):
        web_socket_proxy = websocketproxy.WebSocketProxy()
        web_socket_proxy.__dict__["wrap_cmd"] = "wrap_cmd"
        web_socket_proxy.__dict__["wrap_mode"] = "respawn"
        web_socket_proxy.__dict__["wrap_times"] = [99999999]
        web_socket_proxy.__dict__["spawn_message"] = True
        web_socket_proxy.__dict__["cmd"] = None
        self.stubs.Set(time, 'time', lambda: 100000000.000)
        web_socket_proxy.poll()
        self.assertEquals(web_socket_proxy.spawn_message, False)

    def test_new_client(self):
        web_socket_proxy = websocketproxy.WebSocketProxy()
        web_socket_proxy.__dict__["verbose"] = "verbose"
        web_socket_proxy.__dict__["daemon"] = None
        web_socket_proxy.__dict__["client"] = "client"

        self.stubs.Set(web_socket_proxy, 'socket', MockSocket)

        def mock_select(*args, **kwargs):
            ins = None
            outs = None
            excepts = "excepts"
            return ins, outs, excepts

        self.stubs.Set(select, 'select', mock_select)
        self.assertRaises(Exception, web_socket_proxy.new_client)
