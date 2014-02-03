import unittest

import colander
from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass
from voteit.core.models.interfaces import IAuthPlugin


class FacebookPluginTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.velruse.providers.facebook import FacebookAuth
        return FacebookAuth

    def test_verify_object(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        self.failUnless(verifyObject(IAuthPlugin, self._cut(context, request)))

    def test_verify_class(self):
        self.failUnless(verifyClass(IAuthPlugin, self._cut))


class GoogleOAuth2Tests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.velruse.providers.google_oauth2 import GoogleOAuth2
        return GoogleOAuth2

    def test_verify_object(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        self.failUnless(verifyObject(IAuthPlugin, self._cut(context, request)))

    def test_verify_class(self):
        self.failUnless(verifyClass(IAuthPlugin, self._cut))


class OpenIDAuthTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.velruse.providers.openid import OpenIDAuth
        return OpenIDAuth

    def test_verify_object(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        self.failUnless(verifyObject(IAuthPlugin, self._cut(context, request)))

    def test_verify_class(self):
        self.failUnless(verifyClass(IAuthPlugin, self._cut))


class TwitterAuthTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.velruse.providers.twitter import TwitterAuth
        return TwitterAuth

    def test_verify_object(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        self.failUnless(verifyObject(IAuthPlugin, self._cut(context, request)))

    def test_verify_class(self):
        self.failUnless(verifyClass(IAuthPlugin, self._cut))