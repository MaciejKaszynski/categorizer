from categorize.pipe import Pipe, Data
from categorize.pdf_metadata import PdfMetadata
from sys import argv
from pathlib import Path
from ollama import Client
from typing import List
import json
from dataclasses import dataclass
import logging

logger = logging.getLogger("LLM")

SYSTEM_PROMPT = """
You are a document metadata extractor. 
You will be given raw OCR text from a scanned document.
Your job is to extract structured fields and return ONLY a valid JSON object,
no explanation, no markdown, no backticks.

Extract these fields:
- producer: (Can be a company name, or null)
- author: same as producer
- title: this should be something like {creation_date} - {producer} - {subject}
- subject: The type of document (e.g. invoice, contract, letter, receipt, bank_statement, other)
- keywords: (list of 3-5 relevant tags)
- creation_date: (YYYY-MM-DD, or null)
- reference_number: (invoice no, contract id, or null)
- creator: same as producer

If a field cannot be determined, use null.
"""


class LLM(Pipe):
    def __init__(self, args):
        self.message = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]
        self.client = Client()
        self.__model = args.model

    @Pipe.precondition(lambda d: bool(d.ocr_text), "LLM needs ocr_text")
    def forward(self, data: Data) -> Data:
        logger.info("Running LLM")

        assert bool(data.ocr_text)

        current_message = self.message
        current_message.append(
            {"role": "user", "content": " ".join(data.ocr_text)},
        )

        logger.info("Asking Jarvis")
        result = self.client.chat(self.__model, messages=current_message)
        logger.info("Got Response")

        logger.debug(f": {result.message.content}")

        # possible that llm output is not json parsable
        json_data = None
        retry_counter = 0

        while json_data is None:
            try:
                json_data = PdfMetadata.model_validate_json(str(result.message.content))
                logger.info("Parsed data!")
                logger.debug(json_data)
                data.pdf_metadata = json_data
                return data

            except json.JSONDecodeError as e:
                logger.error(f"LLM gave invalid json: {e.msg}")
                retry_counter += 1

            if retry_counter > 3:
                logger.error("Couldn't get LLM to produce valid json for scan")
                return data

            # append message to give proper output
            if len(current_message) == 1:
                current_message.append({"role": "assistant", "content": str(result)})
                current_message.append(
                    {
                        "role": "user",
                        "content": "That was not valid JSON. Return only a raw JSON object, no markdown, no backticks, no explanation.",
                    }
                )
            result = self.client.chat(self.__model, messages=current_message)

        return data
