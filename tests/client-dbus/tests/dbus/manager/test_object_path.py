# Copyright 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Test object path methods.
"""
import unittest

import dbus

from dbus_python_client_gen import DPClientInvocationError

from stratisd_client_dbus import Manager
from stratisd_client_dbus import ObjectManager
from stratisd_client_dbus import get_object

from .._misc import _device_list
from .._misc import Service

_DEVICE_STRATEGY = _device_list(0)


class GetObjectTestCase(unittest.TestCase):
    """
    Test get_object method.
    """

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testNonExisting(self):
        """
        A proxy object is returned from a non-existant path.
        """
        proxy = get_object('/this/is/not/an/object/path')
        self.assertIsNotNone(proxy)

        with self.assertRaises(DPClientInvocationError) as context:
            ObjectManager.Methods.GetManagedObjects(proxy, {})
        cause = context.exception.__cause__
        self.assertIsInstance(cause, dbus.exceptions.DBusException)
        self.assertEqual(cause.get_dbus_name(),
                         'org.freedesktop.DBus.Error.UnknownMethod')

        with self.assertRaises(DPClientInvocationError) as context:
            Manager.Properties.Version.Get(proxy)
        cause = context.exception.__cause__
        self.assertIsInstance(cause, dbus.exceptions.DBusException)
        self.assertEqual(cause.get_dbus_name(),
                         'org.freedesktop.DBus.Error.UnknownMethod')

    def testInvalid(self):
        """
        An invalid path causes an exception to be raised.
        """
        with self.assertRaises(ValueError):
            get_object('abc')
