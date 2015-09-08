# PEDSnet Data Archive Validator

Validate unpacked PEDSnet data archives.

## Command Line/Python

```sh
# Recommended: with activated virtualenv environment ...
git pull https://github.com/PEDSnet/data-archive-validator.git
cd data-archive-validator
python setup.py install

davd /my/data/archive/metadata.csv 2.0.0
```

In Python:

```python
from davd import validate

validate('/my/data/archive/metadata.csv', '2.0.0')
```

## Docker

TBD

## Web Service

TBD
