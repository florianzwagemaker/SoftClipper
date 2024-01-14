import argparse

from ReadClipper import __prog__, __version__
from ReadClipper.cli_formatter import FlexibleArgFormatter, RichParser


class CLIparser:
    def __init__(self, input_args: list[str]) -> None:
        self.flags = self._get_args(input_args)

    def _get_args(self, input_args: list[str]) -> argparse.Namespace:
        parser: argparse.ArgumentParser = RichParser(
            prog=f"[bold]{__prog__}[/bold]",
            usage="%(prog)s \[required arguments] \[optional arguments]",
            description="%(prog)s: filter and clean sequencing reads based on alignment information. BAM -> FastQ",
            formatter_class=FlexibleArgFormatter,
            add_help=False,
        )

        parser.add_argument(
            "--input" "-i",
            metavar="File",
            help="BAM file containing the reads. sorted and indexed with SAMtools.",
            type=str,
            required=True,
        )

        parser.add_argument(
            "--output",
            "-o",
            metavar="File",
            help="File with cleaned fastq reads",
            type=argparse.FileType("w"),
            required=True,
        )
