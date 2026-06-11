import chromadb

client = chromadb.PersistentClient(
    path="./vector_store"
)

collection = client.get_or_create_collection(
    name="captures"
)

def store_capture(
    capture_id: int,
    text: str,
    intent: str,
    tags
):


    collection.add(
        ids=[str(capture_id)],
        documents=[text],
        metadatas=[
            {
                "capture_id": capture_id,
                "intent": intent,
                "tags": ",".join(tags)
            }
        ]
    )

def search_memory(
    query: str,
    n_results: int = 3
):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results