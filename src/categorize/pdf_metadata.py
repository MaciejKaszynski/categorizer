from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class PdfMetadata(BaseModel):
    author: str
    producer: str
    title: str
    subject: str
    keywords: List[str]
    creation_date: Optional[str]
    mod_date: str = datetime.now().strftime("D\072%Y%m%d")

    creator: str

    def to_pdfdata(self):
        return {
            "/Author": self.author,
            "/Producer": self.producer,
            "/Title": self.title,
            "/Subject": self.subject,
            "/Keywords": ",".join(self.keywords),
            "/CreationDate": self.creation_date,
            "/ModDate": self.mod_date,
            "/Creator": self.creator,
        }
