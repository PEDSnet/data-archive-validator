import hashlib
import re

CHUNK_SIZE = 8192


def file_digest_and_utf8_check(path, algo='sha256'):
    _hash = hashlib.new(algo)

    valid_utf = True

    with open(path, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)

            if not chunk:
                break

            _hash.update(chunk)

            if valid_utf:
                try:
                    chunk.decode('utf8')
                except UnicodeDecodeError:
                    valid_utf = False

    return _hash.hexdigest(), valid_utf


def is_utf8(path):
    with open(path, 'rU') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            try:
                chunk.decode('utf8')
            except UnicodeDecodeError:
                return False

    return True
