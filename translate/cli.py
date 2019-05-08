import click
from dataclasses import dataclass
from typing import Dict, Optional, List


@dataclass
class Query(object):
    """Quick and query class."""

    tx_name: str
    tx_pos: int


@dataclass
class Transcript(object):
    """Quick and dirty transcript class."""

    tx_name: str
    chr: str
    genomic_pos: int
    cigar: str


@dataclass
class Translation(object):
    """Quick and dirty translation class."""

    tx_name: str
    tx_pos: int
    chr: str
    genomic_pos: int


def translate(
    query: Query, transcripts: Dict[str, Transcript]
) -> Optional[Translation]:
    """Translate the transcript coordinates into genomic coordinates"""
    # Assume the best for now, that a transcript exists
    tx: Optional[Transcript] = transcripts.get(query.tx_name, None)
    if tx:
        # Figure out where on the genome the tx coord is
        pass
    else:
        return None
    return None


def parse_queries(query_path: str) -> List[Query]:
    """Parse the queries out of the query file."""
    queries: List[Query] = []
    with open(query_path, "r") as query_fh:
        for line in query_fh:
            vals = line.rstrip("\n").split("\t")
            queries.append(Query(vals[0], int(vals[1])))
    return queries


def parse_transcripts(transcript_path: str) -> Dict[str, Transcript]:
    """Parse the transcripts out of the transcript file."""
    transcripts: Dict[str, Transcript] = {}
    with open(transcript_path, "r") as trans_fh:
        for line in trans_fh:
            vals = line.rstrip("\n").split("\t")
            transcripts[vals[0]] = Transcript(vals[0], vals[1], int(vals[2]), vals[3])
    return transcripts


@click.command()
@click.option(
    "-t", "--transcript_file", type=click.Path(), help="Path to the transcripts file"
)
@click.option("-q", "--query_file", type=click.Path(), help="Path to the query file")
def main(transcript_file: str, query_file: str):
    """Locate the genomic coordinates of queries based on the transcript file.

    Both the transcript and query files are 0-based.

    Assumtions:

    \b
        - Transcript names are unique in the transcript file
        - Transcript names are not unique in the query file
        - Transcript files are of the form: transcript_name chromosome position cigar
        - Query files are of the form: transcript_name transcript_pos
        - Output is of the form: transcript_name query_pos chromosome genomic_pos
    """
    transcripts: Dict[str, Transcript] = parse_transcripts(transcript_file)
    queries: List[Query] = parse_queries(query_file)
    for query in queries:
        translation = translate(query, transcripts)
    print(transcripts)
    print(queries)

