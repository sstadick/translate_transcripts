# Translate Transcripts

Translate transcript coordinates to genomic coordinates.

## Install

```bash
# Assumes you are in source dir
python3.6 -m venv ./venv
source ./venv/bin/activate
pip install .
```

## Run Tests

```bash
pip install pytest
pytest
```

## Running

```bash
$ translate --help 
Usage: translate [OPTIONS]

  Locate the genomic coordinates of queries based on the transcript file.

  Both the transcript and query files are 0-based. When a value can't be
  determined it is set to '*'.

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

## Discussion

### Design Choices

### Bells and Whistles

1. Handle transcripts mapping with reverse orientation:
2. Map genomic coordinates onto transcript coordinates:
3. Map transcript range onto a genomic range (or reverse). Transcript CIGAR onto a genomic CIGAR (or reverse):
4. Where to get transcripts:
