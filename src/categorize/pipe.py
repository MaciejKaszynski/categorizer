from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Tuple, Optional, List
from dataclasses import dataclass, field
from typing import Callable, Dict
from PIL.Image import Image

from categorize.pdf_metadata import PdfMetadata


@dataclass
class Data:
    output_dir: Path

    debug_dir: Optional[Path] = None
    """The path to the debug artifacts.
    """

    images: List[Image] = field(default_factory=list)
    """A list of images of the scanned document.
    """

    ocr_text: Optional[List[str]] = None
    """Text from the document.

    @note: This is mapped such that index of `images_file_path` match here.
    """

    llm_model: str = "None"
    """Model to use

    @note "None" skips the LLM categorization pipe.
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
    def forward(self, data: Data) -> Data:
        """Common method for all Pipes."""
        raise NotImplementedError("Abstract Method")
