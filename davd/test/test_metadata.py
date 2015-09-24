import os
import unittest

from davd.metadata import ValidationError
from davd.main import main


def f(fname):
    return os.path.join(os.path.dirname(__file__), fname)


class TestEverything(unittest.TestCase):

    def setUp(self):
        self.cwd = os.path.dirname(__file__)

    def test_canonical(self):
        main([f('metadata.csv'), '2.0.0'])

    def test_bad_version(self):
        self.assertRaises(ValidationError, main, [f('metadata.csv'), 'x'])

    def test_bad_checksum(self):
        self.assertRaises(ValidationError, main, [f('metadata_bad_checksum.csv'), '2.0.0'])

    def test_bad_filename(self):
        self.assertRaises(ValidationError, main, [f('metadata_bad_filename.csv'), '2.0.0'])

    def test_bad_header(self):
        self.assertRaises(ValidationError, main, [f('metadata_bad_header.csv'), '2.0.0'])

    def test_bad_model(self):
        self.assertRaises(ValidationError, main, [f('metadata_bad_model.csv'), '2.0.0'])

    def test_bad_table(self):
        self.assertRaises(ValidationError, main, [f('metadata_bad_table.csv'), '2.0.0'])

    def test_bad_url(self):
        self.assertRaises(Exception, main, [f('metadata_bad_url.csv'), '2.0.0'])

    def test_suppressed_bad_url(self):
        main([f('metadata_bad_url.csv'), '2.0.0', '--no-check-urls'])

    def test_extra_column(self):
        self.assertRaises(ValidationError, main, [f('metadata_extra_column.csv'), '2.0.0'])

    def test_i2b2(self):
        self.assertRaises(ValidationError, main, [f('metadata_i2b2.csv'), '2.0.0'])

    def test_no_quoting(self):
        main([f('metadata_no_quoting.csv'), '2.0.0'])

    def test_not_utf8(self):
        self.assertRaises(ValidationError, main, [f('metadata_not_utf8.csv'), '2.0.0'])

    def test_with_bom(self):
        ValidationError, main, [f('metadata_with_bom.csv'), '2.0.0']

    def test_with_non_utf8_files(self):
        self.assertRaises(ValidationError, main, [f('metadata_with_non_utf8_files.csv'), 'x'])
