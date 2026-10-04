from pypdf import PdfReader, PdfWriter, PageObject

from categorize.pipe import Pipe, Data
from PIL import Image
from pytesseract import image_to_pdf_or_hocr
from io import BytesIO
import logging

logger = logging.getLogger("PDFCreator")

class PDFCreator(Pipe):

    def __init__(self, args):
        self.__out_dir = args.output_dir

    @Pipe.precondition(lambda d: len(d.images) != 0, "No images to make PDF from")
    def forward(self, data: Data) -> Data:

        writer = PdfWriter()

        for i, image in enumerate(data.images):
            pdf_bytes = image_to_pdf_or_hocr(image, extension="pdf", lang="eng")

            assert isinstance(pdf_bytes, bytes)

            tmp_pdf = PdfReader(BytesIO(pdf_bytes))
            
            writer.add_page(tmp_pdf.pages[0])

        logger.debug(f"metadata {data.pdf_metadata}")
        if data.pdf_metadata:
            logger.debug("Writing metadata!")
            writer.add_metadata(data.pdf_metadata.to_pdfdata())

        with (self.__out_dir / f"{data.pdf_metadata.title}.pdf").open('wb') as f:
            writer.write(f)

        return data
