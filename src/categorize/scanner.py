from categorize.pipe import Pipe, Data
import pyinsane2
from typing import List
import logging
from PIL import Image


logger = logging.getLogger("Scanner")


class Scanner(Pipe):
    def __init__(self):
        pyinsane2.init()

        # setup scanner later incase it can be skipped
        self.__scanner = None

    def __dell__(self):
        pyinsane2.exit()

    def _get_scanners(self) -> None:
        logger.info("Getting scanners list")
        out = pyinsane2.get_devices()

        for i, d in enumerate(out):
            print(f"{i} - {d.name}")

        choice = int(input("> "))
        self.__scanner = out[choice]

        self.__set_scanner_opts()

    def __set_scanner_opts(self) -> None:
        """Sets the options for the scanner"""
        pyinsane2.set_scanner_opt(self.__scanner, "resolution", [300])
        pyinsane2.set_scanner_opt(self.__scanner, "mode", ["Color"])
        pyinsane2.maximize_scan_area(self.__scanner)

    def __scan_page(self) -> Image.Image:
        assert self.__scanner is not None
        scanning_session = self.__scanner.scan()
        try:
            while scanning_session.scan.is_scanning:
                scanning_session.scan.read()
        except EOFError:
            pass

        logger.info("Scanned")

        return scanning_session.images[-1]

    def __get_input(self, message: str, choice: List[str]) -> str:

        final_message = f"{message}\n{'/'.join(choice)}"
        lowered_choices = [c.lower() for c in choice]

        while True:
            res = input(final_message)
            if res not in lowered_choices:
                continue

            return res.lower()

    @Pipe.skip_if(lambda d: len(d.images) != 0)
    def forward(self, data: Data) -> Data:
        logger.info("Running Scanner")

        if self.__scanner is None:
            self._get_scanners()

        # document_finised: bool = False
        # while not document_finised:
        data.images.append(self.__scan_page())
            # document_finised = "y" == self.__get_input(
            #     "Would you like to scan another page", ["Y", "N"]
            # )

        if data.debug_dir:
            for i, image in enumerate(data.images):
                out_img = data.debug_dir / f"{i}.jpg"
                logger.debug(f"Saving to {out_img}")
                image.save(out_img)

        return data
