from categorize.scanner.iscanner import Scanner
from categorize.ocr import OCR
from categorize.llm import LLM
from categorize.pipe import Data
from categorize.pdf_creator import PDFCreator
from argparse import Namespace

"""
Scanner -> OCR -> LLM -> PDF Writer -> Uploader
"""


class Pipeline:
    def __init__(self, args: Namespace):

        self.pipeline = [Scanner(args), OCR(args), LLM(args), PDFCreator(args)]
        # self.pipeline = [Scanner(scanner), OCR(), PDFCreator()]

    def run(self, data: Data):

        for p in self.pipeline:
            data = p.forward(data)
