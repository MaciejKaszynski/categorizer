from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Tuple, Optional, List
from dataclasses import dataclass, field
from pypdf import DocumentInformation

@dataclass
class Data:
    images_file_path: Optional[List[Path]] = None
    ocr_text: Optional[List[str]] = None
    pdf_metadata: Optional[DocumentInformation] = None
    output_pfd: Optional[Path] = None


class Pipe(ABC):
    @abstractmethod
    def forward(self, data: Data) -> Data:
        raise NotImplementedError("Abstract Method")
