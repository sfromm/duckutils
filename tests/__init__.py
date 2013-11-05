#!/usr/bin/python

import unittest
import os
import tempfile

import duckutils
import duckutils.constants as C
import duckutils.sendemail

SMTP_SENDER = os.environ.get('DUCKUTILS_SMTP_SENDER', 'nobody@localhost')
SMTP_RECIPIENT = os.environ.get('DUCKUTILS_SMTP_RECIPIENT', 'root@localhost')
SMTP_SUBJECT = os.environ.get('DUCKUTILS_SMTP_SUBJECT', 'nose test')
SMTP_TEXT = 'This is a test message'
YAML_FILE = 'test.yml'
JSON_FILE = 'test.json'

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.basedir = os.path.dirname(__file__)
        self.cmd_success = '/bin/true'
        self.cmd_fail = '/bin/false'

    def test_email(self):
        r = duckutils.sendemail.send_email(SMTP_TEXT,
                SMTP_SENDER, SMTP_RECIPIENT,
                SMTP_SUBJECT, server=C.DEFAULT_SMTP_SERVER)
        assert r is True

    def test_command(self):
        (rc, out, err) = duckutils.run_command(self.cmd_success)
        assert rc == 0
        (rc, out, err) = duckutils.run_command(self.cmd_fail)
        assert rc == 1
        (rc, out, err) = duckutils.run_command('/usr/bin/this-does-not-exist')
        assert rc == 127

    def test_yaml(self):
        r = duckutils.parse_yaml_from_file(os.path.join(self.basedir, YAML_FILE))
        assert r is not None

    def test_json(self):
        r = duckutils.parse_json_from_file(os.path.join(self.basedir, JSON_FILE))
        assert r is not None
        r = duckutils.json_dumps(r)
        assert isinstance(r, str)

    def test_flock(self):
        fd = file(os.path.join(self.basedir, JSON_FILE))
        duckutils.flock_file(fd)
        duckutils.unflock_file(fd)

    def test_nb_flock(self):
        fd1 = file(os.path.join(self.basedir, JSON_FILE))
        fd2 = file(os.path.join(self.basedir, JSON_FILE))
        duckutils.flock_file(fd1)
        r = duckutils.nb_flock_file(fd2)
        assert r is False
        duckutils.unflock_file(fd1)

    def test_touch(self):
        (fh, path) = tempfile.mkstemp()
        path2 = '%s.tmp2' % path
        duckutils.touch_file(path)
        duckutils.touch_file(path2)
        os.unlink(path)
        os.unlink(path2)
