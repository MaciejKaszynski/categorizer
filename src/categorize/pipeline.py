from categorize.scanner import Scanner
from categorize.ocr import OCR
from categorize.llm import LLM
from categorize.pipe import Data
from categorize.pdf_creator import PDFCreator

"""
Scanner -> OCR -> LLM -> PDF Writer -> Uploader
"""


class Pipeline:
    def __init__(self):

        self.pipeline = [Scanner(), OCR(), LLM(), PDFCreator()]
        # self.pipeline = [Scanner(scanner), OCR(), PDFCreator()]

    def run(self, data: Data):

        for p in self.pipeline:
            data = p.forward(data)
