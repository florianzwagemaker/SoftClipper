import pysam
import argparse
import re
from .version import __version__

def main():
    arg = argparse.ArgumentParser()

    arg.add_argument(
        "--input",
        metavar="File",
        help="BAM file of the first minimap2 alignment run, sorted and indexed.",
        type=str,
        required=True,
    )

    arg.add_argument(
        "--output",
        metavar="File",
        help="File with cleaned fastq reads",
        type=argparse.FileType("w"),
        required=True,
    )

    arg.add_argument(
        "--threads",
        metavar="Number",
        help="Number of threads that can be used for decompressing/compressing the BAM file",
        default=1,
        type=int,
        required=False,
    )

    arg.add_argument(
        '--version',
        action='version',
        version=__version__,
        help="Show the SoftClipper version and exit"
        )

    flags = arg.parse_args()
    
    
    bamfile = pysam.AlignmentFile(flags.input, "rb", threads=flags.threads)
    
    
    with flags.output as fileout:
        for read in bamfile:
            try:
                s_clipped_left = re.match("^(\d*S)", read.cigarstring).group().split("S")[0]
            except:
                s_clipped_left = "0"

            try:
                s_clipped_right = (
                    re.search("(\d*S)$", read.cigarstring).group().split("S")[0]
                )
            except:
                s_clipped_right = "0"

            trim_seq_left = read.seq[int(s_clipped_left) :]
            trim_seq_right = trim_seq_left[: -int(s_clipped_right)]

            trimmed_seq = trim_seq_right

            trim_qual_left = read.qual[int(s_clipped_left) :]
            trim_qual_right = trim_qual_left[: -int(s_clipped_right)]

            trimmed_qual = trim_qual_right

            fileout.write(
                "@"
                + str(read.query_name)
                + "\n"
                + str(trimmed_seq)
                + "\n"
                + "+"
                + "\n"
                + str(trimmed_qual)
                + "\n"
            )

    fileout.close()
    
    
if __name__ == "__main__":
    main()