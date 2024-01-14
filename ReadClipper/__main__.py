import argparse
import sys

import pandas as pd
import pysam

from ReadClipper import __prog__, __version__

# from ReadClipper.arg_parser import CLIparser


bamfile = pysam.AlignmentFile(sys.argv[1], "rb", threads=1)
data = {}
for read in bamfile:
    data[read.query_name] = {
        'refname': read.reference_name,
        'refstart': read.reference_start,
        'refend': read.reference_end,
        "querystart": read.query_alignment_start,
        "queryend": read.query_alignment_end,
        "querylength": read.query_length,
        "cigar": read.cigarstring,
        "cigartuples": read.cigartuples,
        "read_sequence": read.query_sequence,
        "read_qualities_int": read.query_qualities, # be sure to convert this to an ascii string before writing to file
        "read_is_reverse": read.is_reverse,
        "read_is_unmapped": read.is_unmapped,
        "read_is_secondary": read.is_secondary,
        "read_is_supplementary": read.is_supplementary,
        "read_tags": read.get_tags(),
    }


df = pd.DataFrame.from_dict(data, orient='index')

# Create a separate dataframe that contains the read names of reads to exclude
exclude_df = pd.DataFrame()

# Exclude reads that are unmapped
exclude_df = df[df['read_is_reverse'] == True]


print(exclude_df)

# remove reads in df that are in exclude_df
df = df[~df.index.isin(exclude_df.index)]


print(df)