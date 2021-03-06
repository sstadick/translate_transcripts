from translate.cli import parse_cigar, translate, Transcript, Query, Translation

cigars = [
    ("100M", [(100, "M")]),
    (
        "8M7D6M2I2M11D7M",
        [(8, "M"), (7, "D"), (6, "M"), (2, "I"), (2, "M"), (11, "D"), (7, "M")],
    ),
    ("*", [(0, "*")]),
]
transcripts = {
    "TR1": Transcript(
        tx_name="TR1", chr="CHR1", genomic_pos=3, cigar="8M7D6M2I2M11D7M"
    ),
    "TR2": Transcript(tx_name="TR2", chr="CHR2", genomic_pos=10, cigar="20M"),
    "TR3": Transcript(
        tx_name="TR3", chr="CHR2", genomic_pos=10, cigar="10M", strand="-"
    ),
    "TR4": Transcript(tx_name="TR4", chr="CHR3", genomic_pos=100, cigar="20M5D"),
    "TR5": Transcript(tx_name="TR5", chr="CHR5", genomic_pos=100, cigar="5I20M")
}
queries = [
    Query(tx_name="TR1", tx_pos=4),
    Query(tx_name="TR2", tx_pos=0),
    Query(tx_name="TR1", tx_pos=13),
    Query(tx_name="TR2", tx_pos=10),
    Query(tx_name="TR3", tx_pos=6),
    Query(tx_name="TR3", tx_pos=11),  # Verify that we can't go over chromosome edge
    Query(
        tx_name="TR7", tx_pos=2
    ),  # Test for a transcript name that isn't in transcripts
    Query(
        tx_name="TR4", tx_pos=100
    ),  # Test for a transcript position that is outside of the transcript
    Query(
        tx_name="TR5", tx_pos=4
    )  # Test that insertions are handled correctly when tx pos falls within one
]
translations = [
    Translation(tx_name="TR1", tx_pos=4, chr="CHR1", genomic_pos=7),
    Translation(tx_name="TR2", tx_pos=0, chr="CHR2", genomic_pos=10),
    Translation(tx_name="TR1", tx_pos=13, chr="CHR1", genomic_pos=23),
    Translation(tx_name="TR2", tx_pos=10, chr="CHR2", genomic_pos=20),
    Translation(tx_name="TR3", tx_pos=6, chr="CHR2", genomic_pos=4),
    Translation(tx_name="TR3", tx_pos=11, chr="CHR2", genomic_pos="*"),
    Translation(tx_name="TR7", tx_pos=2, chr="*", genomic_pos="*"),
    Translation(tx_name="TR4", tx_pos=100, chr="CHR3", genomic_pos="*"),
    Translation(tx_name="TR5", tx_pos=4, chr="CHR5", genomic_pos=100)
]


def test_parse_cigar():
    for cigar in cigars:
        assert list(parse_cigar(cigar[0])) == cigar[1]


def test_translate():
    for i, query in enumerate(queries):
        tx = translate(query, transcripts)
        assert tx == translations[i]
