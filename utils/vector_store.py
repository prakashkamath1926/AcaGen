import chromadb
import uuid
client=chromadb.PersistentClient(path="chroma_db")
collection=client.get_or_create_collection(
    name="course_material"
)
def store_chunks(chunks):
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[str(uuid.uuid4())]
        )
    print("Chunks Stored successfully")
