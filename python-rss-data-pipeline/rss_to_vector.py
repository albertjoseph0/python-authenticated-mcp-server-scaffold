import modal
from io import BytesIO
from datetime import datetime

image = modal.Image.debian_slim().pip_install("feedparser", "openai")

app = modal.App("rss-to-vector-pipeline", image=image)

def upload_article_to_vector_store(client, title, content):

    import os
    # Save content to a BytesIO buffer
    file_content = BytesIO(content.encode("utf-8"))
    file_name = f"{title[:50].replace(' ', '_')}.txt"
    file_tuple = (file_name, file_content)
    # Upload file to OpenAI (purpose="assistants")
    result = client.files.create(
        file=file_tuple,
        purpose="assistants"
    )
    file_id = result.id
    print(f"Uploaded file: {file_name} (ID: {file_id})")
    # Attach file to vector store
    client.vector_stores.files.create(vector_store_id=os.getenv("VECTOR_STORE_ID"), file_id=file_id)
    print(f"Attached file {file_id} to vector store {os.getenv('VECTOR_STORE_ID')}")
    return file_id

@app.function(schedule=modal.Period(hours=6), secrets=[modal.Secret.from_name("openai-secret")])
def rss_to_vector_job():
    from openai import OpenAI
    import feedparser
    import os
    print(f"[Modal] Job started at {datetime.utcnow().isoformat()}Z")
    client = OpenAI()
    # Parse the RSS feed
    feed = feedparser.parse(os.environ["RSS_FEED_URL"])
    print(f"Fetched {len(feed.entries)} entries from RSS feed.")
    for entry in feed.entries:
        url = entry.get("link")
        title = entry.get("title", "untitled")
        content = entry.get("summary", "") or entry.get("content", [{}])[0].get("value", "")
        if not content:
            print(f"Skipping entry with no content: {url}")
            continue
        # Upload article to vector store
        upload_article_to_vector_store(client, title, content)
    print(f"[Modal] Job finished at {datetime.utcnow().isoformat()}Z") 