from davd import metadata, __version__


def main():
    usage = """Validate PEDSnet data archive metadata.csv
    Usage: davd [-p PROCS] <METADATA_CSV_FILE> <DATA_MODEL_VERSION>

    Options:
    -p PROCS, --processes=PROCS   Number of processes to use.  Default is
                                  the greater of one-quarter the number
                                  of CPU cores and 1.

    DATA_MODEL_VERSION is a hack at the moment since metadata.csv
    files do not contain the data model version (e.g. '2.0.0', perhaps for
    the 'pedsnet' data model).
    """  # noqa

    from docopt import docopt

    args = docopt(usage, version=__version__)

    metadata.validate(args['<METADATA_CSV_FILE>'],
                      args['<DATA_MODEL_VERSION>'],
                      processes=args['--processes'])


if __name__ == '__main__':
    main()
