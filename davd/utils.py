import hashlib

CHUNK_SIZE = 8192


def file_digest_and_utf8_check(path, algo='sha256'):
    _hash = hashlib.new(algo)

    valid_utf = True

    with open(path, 'rb') as f:
        first_buffer = True
        while True:
            chunk = f.read(CHUNK_SIZE)

            if not chunk:
                break

            _hash.update(chunk)

            if valid_utf:
                try:
                    if first_buffer:
                        first_buffer = False
                        chunk.decode('utf_8_sig')
                    else:
                        chunk.decode('utf8')
                except UnicodeDecodeError:
                    valid_utf = False

    return _hash.hexdigest(), valid_utf


def is_utf8(path):
    with open(path, 'rU') as f:
        first_buffer = True
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            try:
                if first_buffer:
                    first_buffer = False
                    chunk.decode('utf_8_sig')
                else:
                    chunk.decode('utf8')
            except UnicodeDecodeError:
                return False

    return True
