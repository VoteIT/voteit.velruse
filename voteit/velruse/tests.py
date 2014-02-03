import unittest

import colander
from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass
from voteit.core.models.interfaces import IAuthPlugin


class BaseOAuth2PluginTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.velruse.models import BaseOAuth2Plugin
        return BaseOAuth2Plugin

    def test_verify_object(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        self.failUnless(verifyObject(IAuthPlugin, self._cut(context, request)))

    def test_verify_class(self):
        self.failUnless(verifyClass(IAuthPlugin, self._cut))
