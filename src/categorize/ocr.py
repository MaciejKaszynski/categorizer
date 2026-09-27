from categorize.pipe import Pipe, Data
from PIL import Image
from pytesseract import image_to_string
from sys import argv
from pathlib import Path


import logging


logger = logging.getLogger("OCR")


class OCR(Pipe):

    @Pipe.precondition(lambda d: bool(d.images), "OCR needs images_file_path")
    def forward(self, data: Data) -> Data:
        """Given the `images_file_path` runs OCR on all images and appends all
        data into `ocr_text`.

        precondition: `data.images_file_path` has to be a `List[Path]` where
                       each `Path` is a readable image.
        """
        logger.info("OCR started")

        # not needed but lsp is fucked otherwise :)
        assert bool(data.images)

        data.ocr_text = []

        for i, image in enumerate(data.images):
            logger.info(f"Processing image {i}")
            current_page_text = image_to_string(image, lang="pol")
            data.ocr_text.append(current_page_text)

            if data.debug_dir:
                with (data.debug_dir / f"{i}.ocr.txt").open('w') as f:
                    f.write(current_page_text)

        logger.info("OCR done")
        return data
