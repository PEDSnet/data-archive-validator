from davd import metadata, __version__


def main(argv=None):
    usage = """Validate PEDSnet data archive metadata.csv
    Usage: davd [-p PROCS] [-n] <METADATA_CSV_FILE> <DATA_MODEL_VERSION>

    Options:
    -p PROCS, --processes=PROCS   Number of processes to use.  Default is
                                  the greater of one-quarter the number
                                  of CPU cores and 1.
    -n, --no-check-urls           Do not check URLs

    DATA_MODEL_VERSION is a hack at the moment since metadata.csv
    files do not contain the data model version (e.g. '2.0.0', perhaps for
    the 'pedsnet' data model).
    """  # noqa

    from docopt import docopt

    args = docopt(usage, argv, version=__version__)

    metadata.validate(args['<METADATA_CSV_FILE>'],
                      args['<DATA_MODEL_VERSION>'],
                      processes=args['--processes'],
                      check_commit_url=not args['--no-check-urls'])


if __name__ == '__main__':
    main()
