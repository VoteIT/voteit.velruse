import unittest

import colander
from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass
from voteit.core.models.interfaces import IProfileImage


class FacebookProfileImagePluginTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from .facebook import FacebookProfileImagePlugin
        return FacebookProfileImagePlugin

    def test_verify_object(self):
        context = testing.DummyResource()
        self.failUnless(verifyObject(IProfileImage, self._cut(context)))

    def test_verify_class(self):
        self.failUnless(verifyClass(IProfileImage, self._cut))


class GoogleProfileImagePluginTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from .google import GoogleProfileImagePlugin
        return GoogleProfileImagePlugin

    def test_verify_object(self):
        context = testing.DummyResource()
        self.failUnless(verifyObject(IProfileImage, self._cut(context)))

    def test_verify_class(self):
        self.failUnless(verifyClass(IProfileImage, self._cut))
