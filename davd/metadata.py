from __future__ import unicode_literals

import io
import os
import csv
import urllib2
import logging
from multiprocessing import Pool, cpu_count, Process

from davd import utils
from davd import model


class ValidationError(Exception):
    pass


logger = logging.getLogger(__name__)

DEFAULT_METADATA_FILE = 'metadata.csv'


# Set for testing against passed metadata keys
METADATA_FIELDS = set([
    'organization',
    'filename',
    'checksum',
    'cdm',
    'table',
    'etl',
])


def utf_dict_reader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, 'utf-8') for key, value in row.iteritems()}


def read(path):
    """Takes a path to a metadata file and returns a list of mapped records."""

    with open(path, 'rb') as f:
        records = list(utf_dict_reader(f))
        norm_records = []

        for record in records:
            norm_records.append({k.lower(): v for k, v in record.iteritems()})

        return norm_records


# TODO: version is a hack that should be removed when metadata includes it
def validate_record(record, archive_path, check_commit_url, version):
    errors = []

    file_name = record['filename']
    file_path = os.path.join(archive_path, os.path.relpath(file_name))

    logger.info('start validation', extra={
        'record': record,
    })

    header = None

    # Open the file and get the header row
    try:
        with io.open(file_path, encoding='utf_8_sig') as f:
            header = [x.lower() for x in next(csv.reader(f))]
    except IOError as e:
        errors.append('cannot open file: {}'.format(e))
    except StopIteration:
        errors.append('file is empty')
    else:
        logger.info('computing SHA-256', extra={
            'record': record,
        })

        sha256, valid_utf8 = utils.file_digest_and_utf8_check(file_path,
                                                              'sha256')

        if not valid_utf8:
            errors.append('data file encoding is not in the UTF-8 range')

        if sha256 != record['checksum'].lower():
            errors.append('local checksum does not match')

    data_model = record['cdm'].lower()
    data_table = record['table'].lower()

    table_valid = True
    try:
        cdm = model.Model(data_model, version)
    except ValueError, exc:
        errors.append(str(exc))
    else:
        try:
            table_fields = cdm.fields(data_table)
        except ValueError:
            table_valid = False
            errors.append('table `{}` not in model `{} v{}`'.format(data_table,
                                                                    data_model,
                                                                    version))

        if table_valid:
            if not header:
                errors.append('no header is present')

            else:
                invalid_fields = set(header) - set(table_fields)
                if invalid_fields:
                    tpl = 'header fields do not match table fields: {}'
                    errors.append(tpl.format(', '
                                             .join(sorted(invalid_fields))))

    if not record['etl']:
        errors.append('commit URL is not specified')
    elif check_commit_url:
        logger.info('validating commit URL', extra={
            'record': record,
        })

        try:
            urlf = urllib2.urlopen(record['etl'])

            if urlf.getcode() != 200:
                errors.append('commit URL "{}" did not return a '
                              '200 response (instead: {})'
                              .format(record['etl'], urlf.getcode()))
        except urllib2.URLError as e:
            errors.append('error checking commit URL: {}'.format(e.reason))

    logger.info('end validation', extra={
        'record': record,
    })

    return file_name, errors


def _validate_worker(*args, **kwargs):
    """Prevent the worker process from complaining."""
    try:
        return validate_record(*args, **kwargs)
    except (KeyboardInterrupt, SystemExit):
        pass


# TODO: should not need to pass in version; that should be in the metadata file
def validate(path, version, check_commit_url=True, processes=None):
    """Validates a metadata file.

    processes is the number of processes to use when computing checksums and
    verifying UTF-8 status.
    """
    if not utils.is_utf8(path):
        raise ValidationError('metadata file "{}" is not in the UTF-8 range'
                              .format(path))

    try:
        records = read(path)
    except Exception as e:
        raise ValidationError('unable to read metadata file "{}": {}'
                              .format(path, e))

    if set(records[0]) != METADATA_FIELDS:
        raise ValidationError(
            'metadata file "{f}" does not have the '
            'expected header fields: {exp} (actual fields: {act})'
            .format(f=path,
                    exp=', '.join(["'{}'".format(x) for x in
                                   METADATA_FIELDS]),
                    act=', '.join(["'{}'".format(x) for x in
                                   records[0]])))

    archive_path = os.path.dirname(path)

    if processes is None:
        processes = max(cpu_count() / 4, 1)
    else:
        processes = int(processes)
    pool = Pool(processes=processes)
    results = []

    try:
        for record in records:
            args = (record, archive_path, check_commit_url, version)
            results.append(pool.apply_async(_validate_worker, args))

        pool.close()

        errors = {}

        for result in results:
            file_name, error = result.get()

            if error:
                errors[file_name] = error

        if errors:
            raise ValidationError(errors)
    except (KeyboardInterrupt, SystemExit):
        pool.terminate()
        raise


def coverage_multiprocessing_process(): # pragma: no cover
    try:
        import coverage
    except:
        # give up monkey-patching if coverage not installed
        return

    from coverage.collector import Collector
    from coverage.control import coverage
    # detect if coverage was running in forked process
    if Collector._collectors:
        class Process_WithCoverage(Process):
            def _bootstrap(self):
                cov = coverage(data_suffix=True)
                cov.start()
                try:
                    return Process._bootstrap(self)
                finally:
                    cov.stop()
                    cov.save()
        return Process_WithCoverage

ProcessCoverage = coverage_multiprocessing_process()
if ProcessCoverage:
    Process = ProcessCoverage
