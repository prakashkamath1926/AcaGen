import pymupdf
from pathlib import Path
from utils.chunker import create_chunks
from utils.vector_store import store_chunks
from utils.retriever import retriever_chunks
from utils.generator import generate_answer
doc_path=Path("Data")
pdf_files=list(doc_path.glob("*.pdf"))
for doc_path in pdf_files:
    print(" Processing File:",doc_path.name)
    doc=pymupdf.open(doc_path)
    all_txt=""
    for page in doc:
       text=page.get_text()
       all_txt=all_txt+text
    output_folder=Path("output")
    output_file=output_folder / f"{doc_path.stem}.txt"
    with open(output_file,"w",encoding="utf-8") as file:
        file.write(all_txt)
    chunks=create_chunks(all_txt)
    store_chunks(chunks)
print("Text File created")
print("Text Extraction Completed")
print("Creating Dataset")
total_pages=doc.page_count
total_char=len(all_txt)
total_words=len(all_txt.split())
print("Dataset Completed")
print("Filename:",doc_path.name)
print("Pages:",total_pages)
print("characters:",total_char)
print("words:",total_words)
print("Staus: Stage 2")
print("Total Chunks:",len(chunks))
question=input("Ask a Question:")
retrieved_chunks=retriever_chunks(question)
answer=generate_answer(question,retrieved_chunks)
print(answer)

