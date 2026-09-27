from abc import ABC, abstractmethod
from argparse import Namespace
from platform import system
from categorize.pipe import Pipe, Data
import sane
import logging
from typing import Any, Optional
from PIL.Image import Image


logger = logging.getLogger("Scanner")

class iScanner(ABC):

    pass

class WinScanner(iScanner):
    pass


class LinuxScanner(iScanner, Pipe):

    def __configure_device(self) -> None:
        SETTINGS = {
                "mode": "color",
                "depth": 8,
                "resolution": 600
        }

        def try_set(data: dict[str, str]) -> None:
            for key, value in data.items():
                if key not in self.__scanner.opt:
                    logger.warning(f"Unknown scanner option: {key}")
                    continue

                try:
                    setattr(self.__scanner, key, value)
                except AttributeError as e:
                    logger.warning(f"Could not set {key}={value!r}: {e}")

        try_set(SETTINGS)

    def __del__(self):
        self.__scanner.close()
        sane.exit()


    def __init__(self, args: Namespace):
        version = sane.init()
        logger.debug(f"sane version: {version}")

        scanner_id: Optional[str] = args.scanner

        if not scanner_id:
            devices = sane.get_devices()
            for i, (device_name, _, model, _) in enumerate(devices):
                print(f"{i} - {model} {device_name}")

            choice = int(input(">"))
            scanner_id = devices[choice][0]
        self.__scanner = sane.open(scanner_id)

        self.__configure_device()
        params = self.__scanner.get_parameters()
        print("Device parameters:")
        print(f"Format: {params[0]}")
        print(f"Pixels per line: {params[2][0]}")
        print(f"Lines: {params[2][1]}")
        print(f"Depth: {params[3]}")
        print(f"Bytes per line: {params[4]}")

    def scan_page(self, data):
        self.__scanner.start()
        data.images.append(self.__scanner.snap())

    def forward(self, data) -> Data:
        self.scan_page(data)
        return data

class MacScanner(iScanner):
    pass

class Scanner:

  def __new__(cls, *args, **kwargs) -> "iScanner":
      match system():
          case "Windows":
              return WinScanner(*args, **kwargs)

          case "Linux":
              return LinuxScanner(*args, **kwargs)

          case "Darwin":
              return MacScanner(*args, **kwargs)

          case _:
              raise RuntimeError("Unknown OS!")
