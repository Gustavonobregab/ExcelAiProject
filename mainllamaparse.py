import os
from dotenv import load_dotenv
from llama_parse import LLamaParse


load_dotenv()
api_key = os.getenv("LLAMA_CLOUD_API_KEY")


documentos = LLamaParse(result_type= "markdown").load_data("Mocks/preenchido.xlsx")


print(len(documentos))