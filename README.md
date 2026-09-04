<div align="center">

# 🎓 AcaGen
### Automated Course Content Generator

A local Retrieval-Augmented Generation (RAG) application that transforms academic PDF material into interactive, topic-focused learning content.

**Upload** &rarr; **Retrieve** &rarr; **Generate** &rarr; **Learn**

</div>

---

## 📌 Overview
AcaGen is an AI-powered academic content generation system designed to reduce the effort required to convert course material into useful study resources.

Users can upload one or more PDF documents containing lecture notes, syllabi, or other academic material. AcaGen extracts the text, divides it into meaningful chunks, stores those chunks in a persistent ChromaDB vector store, and retrieves the most relevant content for a user's topic or question.

The retrieved context is then provided to Qwen3:8B, running locally through Ollama, to generate content grounded in the uploaded material.

AcaGen currently supports:
* ❓ Question & Answer / Doubt Solving
* 📝 MCQ Generation
* 🃏 Flashcard Generation
* 📒 Notes Generation
* 📅 Week-Wise Study Planning
* 📥 Downloadable generated content
* 📚 Multiple PDF processing
* 💬 Session-based Q&A chat history

AcaGen is designed as a local RAG application, with document processing and LLM inference performed entirely on your device.

---

## ✨ Features

* **📄 Multiple PDF Upload:** Upload multiple PDF documents through the Streamlit interface and process them together as course material.
* **❓ RAG-Based Q&A:** Ask questions about the uploaded material. AcaGen retrieves the most relevant document chunks and uses them as context for Qwen3:8B to generate an answer.
* **📝 MCQ Generation:** Enter a topic and generate multiple-choice questions based on the retrieved course material.
* **🃏 Flashcard Generation:** Generate concise question-and-answer flashcards for a selected topic. Flashcards are displayed interactively using expandable cards.
* **📒 Notes Generation:** Generate structured revision notes based on the relevant portions of the uploaded material.
* **📅 Week-Wise Study Planner:** Generate a topic-focused study plan organized into weekly learning objectives.
* **📥 Download Generated Content:** Generated MCQs, notes, and study plans can be downloaded as `.txt` files directly from the application.
* **📊 Processing Feedback:** The interface provides real-time processing status and a progress indicator while PDF documents are being indexed.
* **💬 Chat History:** Questions and generated answers are maintained in the current Streamlit session and displayed through the sidebar.

---

## 🧠 How AcaGen Works

AcaGen follows an end-to-end local Retrieval-Augmented Generation (RAG) pipeline:

```mermaid
flowchart TD
    subgraph Ingestion ["1. Document Ingestion Pipeline"]
        A["📄 Academic PDFs"] --> B["⚙️ PyMuPDF (fitz)<br><i>Text Extraction</i>"]
        B --> C["✂️ RecursiveCharacterTextSplitter<br><i>Chunk: 1000 | Overlap: 200</i>"]
        C --> D[("🗄️ ChromaDB<br><i>Persistent Vector Store</i>")]
    end

    subgraph Retrieval ["2. Context Retrieval"]
        E["👤 User Query / Topic"] --> F["🔍 Top-4 Vector Retrieval"]
        D -. Semantic Query .-> F
        F --> G["📋 Relevant Context Chunks"]
    end

    subgraph Generation ["3. Local Inference & UI"]
        G --> H["📝 Context + Feature Prompt"]
        H --> I["🤖 Qwen3:8B<br><i>via Ollama Runtime</i>"]
        I --> J["💻 Streamlit UI<br><i>Q&A | MCQs | Flashcards | Notes | Study Plan</i>"]
    end

    classDef primary fill:#f8f9fa,stroke:#4a5568,stroke-width:1.5px,color:#1a202c;
    classDef storage fill:#edf2f7,stroke:#2b6cb0,stroke-width:2px,color:#2b6cb0;
    classDef model fill:#fefcbf,stroke:#b7791f,stroke-width:2px,color:#744210;
    
    class A,B,C,E,F,G,H,J primary;
    class D storage;
    class I model;
