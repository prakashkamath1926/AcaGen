import chromadb
client=chromadb.PersistentClient(path="chroma_db")
collection=client.get_or_create_collection(
    name="course_material"
)
def retriever_chunks(query):
    results=collection.query(
        query_texts=[query],
        n_results=4
    )
    return results["documents"][0]
