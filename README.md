# PEDSnet Data Archive Validator

[![Coverage Status](https://coveralls.io/repos/PEDSnet/data-archive-validator/badge.svg?branch=master&service=github)](https://coveralls.io/github/PEDSnet/data-archive-validator?branch=master)

Validate unpacked PEDSnet data archives.

## Command Line/Python

```sh
# Recommended: with activated virtualenv environment ...
git pull https://github.com/PEDSnet/data-archive-validator.git
cd data-archive-validator
python setup.py install

davd /my/data/archive/metadata.csv 2.0.0
```

Via Python API:

```python
from davd import validate

validate('/my/data/archive/metadata.csv', '2.0.0')
```

## Docker

Currently, the Dockerfile wraps the CLI script and not the (forthcoming) web service.

```sh
git pull https://github.com/PEDSnet/data-archive-validator.git
cd data-archive-validator
docker build -t davd . && docker run davd davd -v /my/archive:/data /data/metadata.csv 2.0.0
```

`/my/archive` is a directory containing the unpacked data archive on the 
Docker host, and `/data` is an arbitrary directory in the container.  On Mac or
Windows, use an absolute path in `/Users` or `C:\Users`, since those
directories are auto-shared with the VM host by `boot2docker`/`machine`.

## Web Service

TBD
