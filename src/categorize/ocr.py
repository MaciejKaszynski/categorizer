from categorize.pipe import Pipe, Data
from PIL import Image
from pytesseract import image_to_string
from sys import argv
from pathlib import Path

class OCR(Pipe):

    def forward(self, data: Data) -> Data:
        """

        precondition: `data.images_file_path` has to be a `List[Path]` where
                       each `Path` is a readable image.
        """
        assert bool(data.images_file_path), f"{__class__.__name__} precondition not met!"

        data.ocr_text = []
        for f in data.images_file_path:
            print(f"Processing {f}")
            data.ocr_text.append(image_to_string(Image.open(f)))


        return data

if __name__ == "__main__":
    o = OCR()
    data = o.forward(Data(images_file_path=[Path(argv[1])]))
    print(data)
