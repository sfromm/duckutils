#!/usr/bin/python

import unittest
import os

import duckutils
import duckutils.constants as C
import duckutils.sendemail

SMTP_SENDER = os.environ.get('DUCKUTILS_SMTP_SENDER', 'nobody@localhost')
SMTP_RECIPIENT = os.environ.get('DUCKUTILS_SMTP_RECIPIENT', 'root@localhost')
SMTP_SUBJECT = os.environ.get('DUCKUTILS_SMTP_SUBJECT', 'nose test')
SMTP_TEXT = 'This is a test message'
YAML_FILE = 'test.yml'

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.basedir = os.path.dirname(__file__)

    def test_email(self):
        r = duckutils.sendemail.send_email(SMTP_TEXT,
                SMTP_SENDER, SMTP_RECIPIENT,
                SMTP_SUBJECT, server=C.DEFAULT_SMTP_SERVER)
        assert r is True

    def test_yaml(self):
        r = duckutils.parse_yaml_from_file(os.path.join(self.basedir, YAML_FILE))
        assert r is not None
