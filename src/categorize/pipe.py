from abc import ABC, abstractmethod
from argparse import Namespace
from dataclasses import dataclass, field
from pathlib import Path
from PIL.Image import Image
from typing import Any, Tuple, Optional, List, Callable, Dict

from categorize.pdf_metadata import PdfMetadata


@dataclass
class Data:
    images: List[Image] = field(default_factory=list)
    """A list of images of the scanned document.
    """

    ocr_text: Optional[List[str]] = None
    """Text from the document.

    @note: This is mapped such that index of `images_file_path` match here.
    """

    pdf_metadata: Optional[PdfMetadata] = None
    """PDF metadata.
    """

    output_pfd: Optional[Path] = None
    """Path to the output PDF.
    """


class Pipe(ABC):
    @staticmethod
    def precondition(condition: Callable[[Data], bool], message: str):
        """Decorator to verify preconditions on the pipeline."""

        def _inner(function):
            def _innerer(*args, **kwargs):
                if not condition(args[1]):
                    __tracebackhide__ = True
                    raise AssertionError(f"Error! Precondition failed!{message}")
                res = function(*args, **kwargs)
                return res

            return _innerer

        return _inner

    @staticmethod
    def skip_if(condition: Callable[[Data], bool]):
        """Decorator check if the pipeline step can be skipped."""

        def _inner(function):
            def _innerer(*args, **kwargs):
                if condition(args[1]):
                    print("Skipping pipe")
                    return args[1]
                else:
                    print("Not Skipping")
                    res = function(*args, **kwargs)
                    return res

            return _innerer

        return _inner

    @abstractmethod
    def __init__(self, ars: Namespace):
        raise NotImplementedError("Abstract Method")

    @abstractmethod
    def forward(self, data: Data) -> Data:
        """Common method for all Pipes."""
        raise NotImplementedError("Abstract Method")
