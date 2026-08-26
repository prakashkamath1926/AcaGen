import streamlit as st
import pymupdf
from pathlib import Path
from utils.chunker import create_chunks
from utils.vector_store import store_chunks
from utils.retriever import retriever_chunks
from utils.generator import generate_answer
from utils.mcq_generator import generate_mcqs
from utils.flashcard_generator import generate_flashcards
from utils.notes import generate_notes
from utils.week import week_wise
st.set_page_config(
    page_title="AcaGen",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)
if "processed" not in st.session_state:
    st.session_state["processed"]=False
if "chat_history" not in st.session_state:
    st.session_state["chat_history"]=[]
st.title("AcaGen")
st.subheader("Automated Course Content Generator")
uploaded_files=st.file_uploader(
    "Upload Course Material",
    type=["pdf"],
    accept_multiple_files=True
)
st.sidebar.title("🎓 AcaGen")
st.sidebar.subheader("📊 Status")
if st.session_state["processed"]:
    st.sidebar.success("All PDFs processed")
else:
    st.sidebar.warning("No PDFs Processed")
st.sidebar.subheader("📚 Uploded Files")
if uploaded_files:
    st.write("Uploaded Files:")
    for file in uploaded_files:
        st.write(file.name)
        st.sidebar.write("📄",file.name)
if st.button("Process PDF"):
    st.success("Processing Started...")
    progress_bar=st.progress(0)
    status=st.empty()
    total_files=len(uploaded_files)
    data_folder=Path("Data")
    data_folder.mkdir(exist_ok=True)
    for index,file in enumerate(uploaded_files):
        status.write(f"Processing:{file.name}({index+1}/{total_files})")
        pdf_path=data_folder/file.name
        with open(pdf_path,"wb") as f:
             f.write(file.getvalue())
        doc=pymupdf.open(pdf_path)
        all_txt=""
        for page in doc:
            text=page.get_text()
            all_txt=all_txt+text
        doc.close()
        chunks=create_chunks(all_txt)
        store_chunks(chunks)
        progress=(index+1)/total_files
        progress_bar.progress(progress,text=f"Processing...{progress*100:.0f}%")
    st.success("All PDFs are processed successfully")
    st.session_state["processed"]=True
tab1,tab2,tab3,tab4,tab5=st.tabs([
    "❓Q&A","📝MCQs","🃏Flashcards","📒Notes","📅Week-Wise Planner"
])
with tab1:
    question=st.text_input("Ask a Question:")
    if st.button("Get Answer"):
        if st.session_state["processed"]:
            retrieved_chunks=retriever_chunks(question)
            answer=generate_answer(question,retrieved_chunks)
            st.subheader("Answer")
            st.write(answer)
            st.session_state["chat_history"].append(
                {
                    "question":question,
                    "answer":answer
                }
            )
        else:
            st.warning("Please process the PDFs first")
st.sidebar.subheader("📜 Chat History")
if st.session_state["chat_history"]:
    for chat in st.session_state["chat_history"]:
        if isinstance(chat,dict):
            with st.sidebar.expander( f"❓{chat['question'][:30]}..."):
                st.write(f"**🙋 Question:**{chat['question']}")
                st.write(f"**🤖 Answer:**{chat['answer']}")
        else: st.sidebar.write(chat)
with tab2:
    mcq_topic=st.text_input("Enter Topic For MCQs: ")
    if st.button("Generate MCQs"):
        retrieved_chunks=retriever_chunks(mcq_topic)
        mcqs=generate_mcqs(mcq_topic,retrieved_chunks)
        st.subheader("MCQs")
        st.write(mcqs)
        st.download_button(
            label="Download MCQs",
            data=mcqs,
            file_name="mcqs.txt",
            mime="text/plain"
        )
with tab3:
    flashcard_topic=st.text_input("Enter Topic For Flashcards: ")
    if st.button("Generate Flashcards"):
        retrieved_chunks=retriever_chunks(flashcard_topic)
        flashcards=generate_flashcards(flashcard_topic,retrieved_chunks)
        st.subheader("FLASHCARDS")
        flashcards=flashcards.replace("**","")
        flashcards=flashcards.split("---")[0]
        cards=flashcards.split("Front:")
        for card in cards[1:]:
            front,back=card.split("Back:")
            with st.expander(front.strip()):
                st.write(back.strip())
with tab4:
    notes_topic=st.text_input("Enter Topic For Notes: ")
    if st.button("Generate Notes"):
        retrieved_chunks=retriever_chunks(notes_topic)
        notes=generate_notes(notes_topic,retrieved_chunks)
        st.subheader("NOTES")
        st.write(notes)
        st.download_button(
            label="Download Notes",
            data=notes,
            file_name="notes.txt",
            mime="text/plain"
        )
    
with tab5:
    plan_topic=st.text_input("Enter Topic For Week Planner: ")
    if st.button("Generate Planner Week-Wise"):
        retrieved_chunks=retriever_chunks(plan_topic)
        plan=week_wise(plan_topic,retrieved_chunks)
        st.subheader("WEEK-WISE PLANNER")
        st.write(plan)
        st.download_button(
            label="Download Week-Wise Study Plan",
            data=plan,
            file_name="study_plan.txt",
            mime="text/plain"
        )
