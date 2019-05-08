# Translate Transcripts

Translate transcript coordinates to genomic coordinates.

## Install

```bash
# Assumes you are in source dir
python3.6 -m venv ./venv
source ./venv/bin/activate
pip install .
```

## Running

```bash
$ translate --help
Usage: translate [OPTIONS]

  Locate the genomic coordinates of queries based on the transcript file.

  Both the transcript and query files are 0-based.

  Assumtions:

      - Transcript names are unique in the transcript file
      - Transcript names are not unique in the query file
      - Transcript files are of the form: transcript_name chromosome position cigar
      - Query files are of the form: transcript_name transcript_pos
      - Output is of the form: transcript_name query_pos chromosome genomic_pos

Options:
  -t, --transcript_file PATH  Path to the transcripts file
  -q, --query_file PATH       Path to the query file
  --help                      Show this message and exit.
```


## TODO

- add pytest for translation
- add cigar string parsing methods and tests
