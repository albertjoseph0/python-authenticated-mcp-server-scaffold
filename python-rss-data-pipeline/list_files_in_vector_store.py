# list all the files in the openai vector store

import openai
import os

client = openai.OpenAI()

VECTOR_STORE_ID = "<your vector store id>"

response = client.vector_stores.files.list(vector_store_id=VECTOR_STORE_ID)

# Get file metadata
def get_file_info(file_id):
    file_info = client.vector_stores.files.retrieve(
        vector_store_id=VECTOR_STORE_ID, file_id=file_id)
    return file_info

# print name and id of each file
for file in response.data:
    file_metadata = client.files.retrieve(file.id)
    print(file_metadata.filename)
