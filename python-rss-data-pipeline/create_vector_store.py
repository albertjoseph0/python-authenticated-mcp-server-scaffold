from openai import OpenAI

client = OpenAI()

vector_store = client.vector_stores.create(
    name="Publisher Content Store",
)

print("Vector store ID:", vector_store.id)
