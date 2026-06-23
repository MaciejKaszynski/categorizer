from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Tuple, Optional, List
from dataclasses import dataclass, field
from pypdf import DocumentInformation
from typing import Callable

@dataclass
class Data:
    images_file_path: Optional[List[Path]] = None
    ocr_text: Optional[List[str]] = None
    pdf_metadata: Optional[DocumentInformation] = None
    output_pfd: Optional[Path] = None


class Pipe(ABC):

    @staticmethod
    def precondition(condition: Callable[[Data], bool], message: str):
        def _inner(function):
            def _innerer(*args, **kwargs):
                if not condition(args[1]):
                    __tracebackhide__ = True
                    raise AssertionError("Error! Precondition failed!"
                                        f"{message}")
                res = function(*args, **kwargs)
                return res
            return _innerer
        return _inner


    @abstractmethod
    def forward(self, data: Data) -> Data:
        raise NotImplementedError("Abstract Method")
