
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from pypdf import PdfReader, PdfWriter
from pathlib import Path

 
@dataclass
class PDFMetadata:

    title: Optional[str] = None
    """Document title"""

    author: Optional[str] = None
    """Author or sender name/company"""

    subject: Optional[str] = None
    """Category / document type"""

    keywords: Optional[list[str]] = field(default_factory=list)
    """Tags"""

    creator: Optional[str] = None
    """Application that created the original doc"""

    producer: Optional[str] = None
    """PDF producer/converter application"""

    creation_date: Optional[datetime] = None
    """Date on the document"""

    mod_date: Optional[datetime] = None
    """Last modified date"""

 
    def write_to_pdf(self, input_path: Path, output_path: Path) -> None:
        """Open a PDF, apply all metadata, and save to output_path."""
        pass
 
