import pysam
import argparse
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
        "--version",
        action="version",
        version=__version__,
        help="Show the SoftClipper version and exit",
    )

    flags = arg.parse_args()

    bamfile = pysam.AlignmentFile(flags.input, "rb", threads=flags.threads)

    with flags.output as fileout:
        for read in bamfile:

            read_start = read.query_alignment_start
            read_end = read.query_alignment_end

            trimmed_seq = read.query_alignment_sequence
            trimmed_qual = read.qual[read_start:read_end]

            if read.is_reverse == True:
                complement = {"A": "T", "C": "G", "G": "C", "T": "A"}
                bases = list(trimmed_seq)
                bases = [complement[base] for base in bases]
                trimmed_seq = "".join(bases)
                trimmed_seq = trimmed_seq[::-1]
                trimmed_qual = trimmed_qual[::-1]

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
