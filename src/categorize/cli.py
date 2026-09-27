"""Command-line interface for categorize."""

import argparse
import sys

from PIL import Image

from . import __version__
from categorize.scanner import Scanner
from categorize.pipeline import Pipeline
from categorize.pipe import Data
import logging
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="categorize",
        description="A CLI tool to categorize things.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
    )
    parser.add_argument("--use-image", type=Path)
    parser.add_argument("--model", type=str)
    parser.add_argument("--list-scanners", action="store_true")
    return parser


def setup_logs():
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("pytesseract").setLevel(logging.WARNING)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    data = Data(Path().resolve())
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("!!!Debug logging enabled!!!")
        data.debug_dir = Path("/tmp/categorize").resolve()
        data.debug_dir.mkdir(exist_ok=True)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info(f"Outputting to {data.output_dir}")

    setup_logs()

    if args.use_image:
        logging.info(f"Using {args.use_image}")
        data.images.append(Image.open(args.use_image.resolve()))

    if args.model:
        data.llm_model = args.model

    pipeline = Pipeline()
    pipeline.run(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
