from categorize.pipe import Pipe, Data
from sys import argv
from pathlib import Path
from ollama import Client
import json

DEFAULT_MODEL = "qwen3.6:latest"

SYSTEM_PROMPT = """
You are a document metadata extractor. 
You will be given raw OCR text from a scanned document.
Your job is to extract structured fields and return ONLY a valid JSON object — no explanation, no markdown, no backticks.

Extract these fields:
- document_type: (invoice, contract, letter, receipt, bank_statement, other)
- creation_date: (ISO format YYYY-MM-DD, or null)
- sender_name: (Can be a company name, or null)
- reference_number: (invoice no, contract id, or null)
- keywords: (list of 3-5 relevant tags)

If a field cannot be determined, use null.
"""

def LLM(Pipe):

    def __init__(self):
        self.messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                    },
            ]
        self.client = Client()

    def forward(self, data:Data) -> Data:
        assert data.ocr_text is not None, f"OCR needs to be filled out for {__name__}"

        current_message = self.message
        current_message.append(
            {
                "role": "user",
                "content": " ".join(data.ocr_text)
            },
        )

        result = self.client.chat(DEFAULT_MODEL, messages=current_message)
        json_data = None
        retry_counter = 0
        while(json_data is None):
            if retry_counter > 3:
                print(f"ERRROR! Couldn't get LLM to produce valid json for scan")
                return data 

            try:
                json_data = json.loads(result)

            except json.JSONDecodeError:
                retry_counter += 1

            


        return data

if __name__ == "__main__":
    from categorize.ocr import OCR
    o = OCR()
    data = o.forward(Data(images_file_path=[Path(argv[1])]))
    print(data)

    assert data.ocr_text is not None

    for part in client.chat(DEFAULT_MODEL, messages=messages, stream=True):
        print(part.message.content, end='', flush=True)
