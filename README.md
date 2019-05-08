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

  Assumptions:

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

I have chosen to implement this as a Python command line application with the whole nine yards of python project boilerplate. I'm not sure this is totally warranted, and my choice to do this would depend on the environment that this would be deployed into. Deploying virtual environments can be a pain in a pipeline environment. Python3 also may not be available. This script could easily be refactored down to a lower version of Python if needed. 

The use of Dataclasses and Typing could also be questioned. I have found both to be extremely useful in getting back up to speed after not touch a project for a while, and they don't affect the performance of the program that much. If performance were a priority, there are steps that could be taken, such as using __slots__, or downgrading to dicts / tuples.

### Bells and Whistles

1. Handle transcripts mapping with reverse orientation:

    This has been implemented. Strandedness could be taken into account by adding a column to the transcripts file with a + or -. If the transcript is on the - strand, then the genomic pos would be incremented by -1, and the tx_pos would be incremented by +1. The extra column is optional and defaults to '+' when not present. This assumes that the genomic position in the transcripts file refers to the the '+' strand. 

2. Map genomic coordinates onto transcript coordinates:

    Not implemented. This could be done using much the same framework that I have here. Outside of the code for accepting a different type of query file, the main difference would be the condition that breaks the loop inside the `translate` function. It would return once the genomic coordinate was reached.

3. Map transcript range onto a genomic range (or reverse). Transcript CIGAR onto a genomic CIGAR (or reverse):

    Not implemented. Some syntax and conventions would need to be written down for parsing ranges, but at its core we could probably just use the same `translate` function, run it twice, once for the start of the range, and once for the end of the range. 

    Regarding the cigar mappings, that should just be tracking the operations that are performed between the start and end of the ranges. This might get tricky. Off the top of my head I would do something like the `translate` function, walk the cigar, and pass in a start_record and end_record values to indicate what coordinates I want the recording to start and end at. 

4. Where to get transcripts:

    I am not aware of any transcript databases that contain alignments as well as transcript information. I would try to ask around for this as I am not an expert in all things transcript related. However, if it came down to it, my DIY solution would be to pull a transcript database uscs's [knownGeneMrna](http://hgdownload.soe.ucsc.edu/goldenPath/hg18/database/knownGeneMrna.txt.gz) that contains the mrna sequences. I would convert these to fastq format and align with a long read aligner such as STAR, or minimap2. This would provide me with a cigar string for each transcript against my reference of choice.
