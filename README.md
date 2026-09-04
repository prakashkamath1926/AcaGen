<div align="center">

# 🎓 AcaGen

### Automated Course Content Generator

**AcaGen** is an AI-powered course content generation system that transforms uploaded PDF course material into interactive, context-aware learning resources using **Retrieval-Augmented Generation (RAG)**.

Instead of manually searching through lengthy course documents, users can upload their course material once and use natural-language queries to generate **answers, MCQs, flashcards, revision notes, and week-wise study plans** based on the relevant content retrieved from their documents.

AcaGen combines **PyMuPDF** for PDF text extraction, **LangChain** for recursive text chunking, **ChromaDB** for persistent vector storage and retrieval, and **Qwen3:8B** running locally through **Ollama** for content generation.




\

**Upload → Retrieve → Generate → Learn**

</div>

---

## 📌 Overview

**AcaGen** is an AI-powered academic content generation system designed to reduce the effort required to convert course material into useful study resources.

Users can upload one or more PDF documents containing lecture notes, syllabi, or other academic material. AcaGen extracts the text, divides it into meaningful chunks, stores those chunks in a persistent ChromaDB vector store, and retrieves the most relevant content for a user's topic or question.

The retrieved context is then provided to **Qwen3:8B**, running locally through **Ollama**, to generate content grounded in the uploaded material.

AcaGen currently supports:

* ❓ Question & Answer / Doubt Solving
* 📝 MCQ Generation
* 🃏 Flashcard Generation
* 📒 Notes Generation
* 📅 Week-Wise Study Planning
* 📥 Downloadable generated content
* 📚 Multiple PDF processing
* 💬 Session-based Q&A chat history

> **AcaGen is currently designed as a local RAG application, with document processing and LLM inference performed locally.**

---

## ✨ Features

### 📄 Multiple PDF Upload

Upload multiple PDF documents through the Streamlit interface and process them together as course material.

### ❓ RAG-Based Q&A

Ask questions about the uploaded material. AcaGen retrieves the most relevant document chunks and uses them as context for Qwen3:8B to generate an answer.

### 📝 MCQ Generation

Enter a topic and generate multiple-choice questions based on the retrieved course material.

### 🃏 Flashcard Generation

Generate concise question-and-answer flashcards for a selected topic. Flashcards are displayed interactively using expandable cards.

### 📒 Notes Generation

Generate structured revision notes based on the relevant portions of the uploaded material.

### 📅 Week-Wise Study Planner

Generate a topic-focused study plan organized into weekly learning objectives.

### 📥 Download Generated Content

Generated MCQs, notes, and study plans can be downloaded as `.txt` files directly from the application.

### 📊 Processing Feedback

The interface provides processing status and a progress bar while PDF documents are being processed.

### 💬 Chat History

Questions and generated answers are maintained in the current Streamlit session and displayed through the sidebar.

---

## 🧠 How AcaGen Works

AcaGen follows a straightforward **Retrieval-Augmented Generation (RAG)** pipeline.

```text
                    ┌─────────────────────┐
                    │   Academic PDFs     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      PyMuPDF        │
                    │   Text Extraction   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ RecursiveCharacter  │
                    │    Text Splitter    │
                    │ 1000 / 200 overlap  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      ChromaDB       │
                    │ Persistent Storage   │
                    └──────────┬──────────┘
                               │
                        User Query/Topic
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Top-4 Retrieval  │
                    │ Relevant Chunks     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Context + Prompt    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Qwen3:8B via      │
                    │       Ollama        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Generated Content   │
                    │ Q&A / MCQs / Cards  │
                    │ Notes / Study Plan  │
                    └─────────────────────┘
```

---

## 🔍 RAG Pipeline

### 1. PDF Text Extraction

AcaGen uses **PyMuPDF** to open uploaded PDF files and extract text page by page.

```python
doc = pymupdf.open(pdf_path)

for page in doc:
    text = page.get_text()
```

The extracted page text is combined into a single text representation for further processing.

---

### 2. Text Chunking

Large documents are divided into smaller chunks using LangChain's `RecursiveCharacterTextSplitter`.

Current configuration:

```text
Chunk Size    : 1000
Chunk Overlap : 200
```

The recursive splitter attempts to preserve natural text boundaries while creating chunks.

The overlap helps retain contextual information between neighboring chunks.

---

### 3. Vector Storage

The generated chunks are stored in a persistent **ChromaDB** collection.

```python
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="course_material"
)
```

ChromaDB provides the persistent local vector-store layer used for retrieval.

---

### 4. Retrieval

When a user enters a question or topic, AcaGen queries ChromaDB and retrieves the **top 4 relevant chunks**.

```python
results = collection.query(
    query_texts=[query],
    n_results=4
)
```

The value `4` is a practical retrieval choice for this implementation, balancing contextual coverage against unnecessary or noisy information.

---

### 5. Prompt Construction

The retrieved chunks are combined into a context and inserted into a feature-specific prompt.

Conceptually:

```text
Retrieved Chunks
       │
       ▼
   Context
       │
       ▼
Context + User Query/Topic
       │
       ▼
 Feature-Specific Prompt
```

Different generation tasks use different prompts—for example, Q&A, MCQs, flashcards, notes, and study planning.

---

### 6. Local LLM Generation

The final prompt is sent to **Qwen3:8B** through Ollama.

```python
response = chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
```

The generated response is then returned to the Streamlit interface.

---

## 🛠️ Tech Stack

| Component                | Technology              | Purpose                                |
| ------------------------ | ----------------------- | -------------------------------------- |
| **Programming Language** | Python 3.13+            | Core application logic                 |
| **Frontend / UI**        | Streamlit               | Interactive web interface              |
| **PDF Processing**       | PyMuPDF                 | PDF text extraction                    |
| **Text Chunking**        | LangChain Text Splitter | Recursive document chunking            |
| **Vector Store**         | ChromaDB                | Persistent local storage and retrieval |
| **LLM Runtime**          | Ollama                  | Local model execution                  |
| **Language Model**       | Qwen3:8B                | Content generation                     |
| **Unique IDs**           | UUID                    | Unique chunk identifiers               |

---

## 📂 Project Structure

```text
AcaGen/
│
├── streamlit_app.py
│
├── utils/
│   ├── chunker.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── generator.py
│   ├── mcq_generator.py
│   ├── flashcard_generator.py
│   ├── notes.py
│   ├── week.py
│   └── prompts.py
│
├── Data/
│
├── chroma_db/
│
├── requirements.txt
│
├── .gitignore
│
└── README.md
```

### Module Responsibilities

| File                     | Responsibility                                 |
| ------------------------ | ---------------------------------------------- |
| `streamlit_app.py`       | Main application interface and feature routing |
| `chunker.py`             | Splits extracted text into chunks              |
| `vector_store.py`        | Stores chunks in ChromaDB                      |
| `retriever.py`           | Retrieves relevant document chunks             |
| `generator.py`           | Generates RAG-based answers                    |
| `mcq_generator.py`       | Generates MCQs                                 |
| `flashcard_generator.py` | Generates flashcards                           |
| `notes.py`               | Generates revision notes                       |
| `week.py`                | Generates week-wise study plans                |
| `prompts.py`             | Stores generation prompts                      |

---

## ⚙️ Requirements

Before running AcaGen, make sure you have:

* **Python 3.13+**
* **Ollama**
* Sufficient local resources to run the **Qwen3:8B** model
* The Python dependencies listed in `requirements.txt`

> The exact performance of local Qwen3:8B inference depends on your CPU, RAM, GPU, and Ollama configuration.

---

## 🚀 Installation

### 1. Clone the Repository

Replace the repository URL below with the actual GitHub repository URL after publishing the project.

```bash
git clone https://github.com/<your-username>/AcaGen.git
cd AcaGen
```

---

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install and Run Ollama

Install Ollama on your system and make sure the Ollama service is running.

Pull the required model:

```bash
ollama pull qwen3:8b
```

Verify that the model is available:

```bash
ollama list
```

You should see:

```text
qwen3:8b
```

---

### 5. Run AcaGen

```bash
streamlit run streamlit_app.py
```

Streamlit will start the application locally.

---

## ▶️ Usage

### Step 1 — Upload Course Material

Upload one or more PDF documents using the file uploader.

### Step 2 — Process PDFs

Click:

```text
Process PDF
```

AcaGen will:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
ChromaDB Storage
```

### Step 3 — Select a Feature

Choose one of the available tabs:

```text
Q&A
MCQs
Flashcards
Notes
Week-Wise Planner
```

### Step 4 — Enter a Question or Topic

Depending on the selected feature, enter a question or topic.

### Step 5 — Generate

AcaGen retrieves relevant chunks from ChromaDB and passes them to the appropriate generation module.

### Step 6 — Review / Download

Review the generated content in the Streamlit interface.

MCQs, notes, and week-wise plans can also be downloaded as text files.

---

## 🔐 Privacy & Local Processing

AcaGen is designed around local document processing and local LLM inference.

The current implementation uses:

* Local PDF processing with PyMuPDF
* Local persistent ChromaDB storage
* Local Qwen3:8B inference through Ollama

No cloud LLM API is required for the current implementation.

This makes the project suitable for experimenting with academic material without requiring the uploaded content to be sent to a hosted LLM API.

> **Note:** Local processing does not automatically mean every component of a user's operating environment is private or secure. Deployment, machine configuration, file permissions, and network configuration still matter.

---

## ⚠️ Current Limitations

AcaGen is currently a working prototype and has several limitations.

### Document Limitations

* Supports PDF input.
* Text extraction depends on text being available in the PDF.
* Scanned, handwritten, and image-only content is not currently processed through OCR.

### AI Limitations

* Generation quality depends on the retrieved context and Qwen3:8B's capabilities.
* The current retrieval pipeline uses a fixed top-4 retrieval setting.
* There is no dedicated reranking or query-rewriting stage.
* The system does not guarantee that every generated statement is factually correct.

### Application Limitations

The current version does **not** include:

* User authentication
* Login system
* User-provided model API key management
* Cloud LLM deployment
* LangGraph-based agent workflows
* Multimodal document understanding
* Email integrations
* Google Docs integration
* Human-in-the-loop approval workflows

These are potential future improvements rather than current features.

---

## 🔮 Future Scope

### 🔐 User Authentication & API Key Management

Introduce a dedicated login system and an interface for configuring model/API credentials where required.

A supporting rulebook or setup guide could explain how users obtain and configure model API keys.

### 🖼️ OCR & Image-Based Content

Extend document processing to identify text contained in:

* Scanned documents
* Handwritten notes
* Whiteboards
* Images embedded inside course material

OCR could work alongside the existing PDF extraction pipeline.

### 👁️ Multimodal AI

Extend AcaGen beyond plain extracted text so that visual information such as diagrams, figures, handwritten content, and other document elements can also contribute to generation.

### 🔗 External Tools & Integrations

Potential integrations include:

* Email
* Google Docs
* Other educational productivity tools

### 🤖 More Advanced RAG

Future versions could explore:

* Query rewriting
* Reranking
* Hybrid retrieval
* More advanced chunking strategies
* Agentic RAG workflows
* LangGraph-based orchestration

---

## 🎯 Project Objective

The objective of AcaGen is to demonstrate how **Retrieval-Augmented Generation can be applied to educational workflows** to transform unstructured course material into useful, topic-focused learning resources.

Rather than relying solely on an LLM's internal knowledge, AcaGen first retrieves relevant information from the user's uploaded academic material and then uses that context during generation.

```text
Academic Material
       ↓
Information Retrieval
       ↓
Context-Grounded Generation
       ↓
Learning Resources
```

---

## 📊 Project Status

**Current Status: Functional Prototype**

Implemented:

* [x] Multiple PDF upload
* [x] PDF text extraction
* [x] Recursive text chunking
* [x] Persistent ChromaDB storage
* [x] Top-4 retrieval
* [x] RAG-based Q&A
* [x] MCQ generation
* [x] Flashcard generation
* [x] Notes generation
* [x] Week-wise study planner
* [x] Streamlit interface
* [x] Session chat history
* [x] Downloadable generated content
* [x] Local Qwen3:8B inference through Ollama

Planned:

* [ ] Authentication
* [ ] API key configuration
* [ ] OCR support
* [ ] Multimodal AI
* [ ] External tool integrations
* [ ] Advanced RAG capabilities

---

## 👨‍💻 Author

**Prakash Kamath**

B.Tech — Computer Science & Engineering
JK Lakshmipat University, Jaipur

---

## 📄 License

This project is intended to be released under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

---

<div align="center">

### 🎓 AcaGen

**From course material to personalized learning content.**

Built with Python, RAG, ChromaDB, Ollama, Qwen3:8B, and Streamlit.

</div>
