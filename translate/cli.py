import click
from dataclasses import dataclass
from itertools import groupby
from operator import attrgetter
from pprint import pprint
from typing import Dict, Optional, List, Iterable, Tuple, Union


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
    genomic_pos: Union[int, str]
    _print_order = ["tx_name", "tx_pos", "chr", "genomic_pos"]

    def __repr__(self):
        """Create the line that will be printed based on the header fields."""
        return "{}\t{}\t{}\t{}".format(
            *[attrgetter(v)(self) for v in self._print_order]
        )


# Opname: (query op, ref op)
# https://samtools.github.io/hts-specs/SAMv1.pdf
CIGAR_OPS = {
    "M": (1, 1),
    "I": (1, 0),
    "D": (0, 1),
    "N": (0, 1),
    "S": (1, 0),
    "H": (0, 0),
    "P": (0, 0),
    "=": (1, 1),
    "X": (1, 1),
    "*": (0, 0),
}


def parse_cigar(cigar: str) -> Iterable[Tuple[int, str]]:
    """Iterate over the cigar string operations."""
    if cigar == "*":
        print("return star")
        yield 0, "*"
        return
    cigar_iterator = groupby(cigar, lambda x: x.isdigit())
    for _, group in cigar_iterator:
        yield int("".join(group)), "".join(next(cigar_iterator)[1])


def translate(query: Query, transcripts: Dict[str, Transcript]) -> Translation:
    """Translate the transcript coordinates into genomic coordinates.
    
    If a transcript name is in the transcripts, but the transcript pos form the
    query is outside the the tx as defined in the transcripts, the genomic pos will
    be set to '*', but the chromosome will be returned based on the matching transcript
    name.

    If the transcript name is not found in the transcripts, then the chr and genomic 
    pos will be set to '*'
    """
    # Assume the best for now, that a transcript exists
    tx: Optional[Transcript] = transcripts.get(query.tx_name, None)
    if tx == None:
        return Translation(query.tx_name, query.tx_pos, "*", "*")
    # Figure out where on the genome the tx coord is
    genomic_pos = tx.genomic_pos
    tx_pos = 0
    tx_found = False
    for number, op in parse_cigar(tx.cigar):
        query_op, ref_op = CIGAR_OPS[op]
        for i in range(number):
            if query.tx_pos == tx_pos:
                tx_found = True
                break
            genomic_pos += ref_op
            tx_pos += query_op
        if tx_found:
            break
    if tx_found:
        return Translation(query.tx_name, query.tx_pos, tx.chr, genomic_pos)
    else:
        return Translation(query.tx_name, query.tx_pos, tx.chr, "*")


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

    Both the transcript and query files are 0-based. When a value can't be determined
    it is set to '*'.

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
        if translation is not None:
            print(translation)
