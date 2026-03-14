# Medical RAG Assistant

A medical question-answering assistant based on Retrieval-Augmented Generation (RAG), specifically designed to answer healthcare-related questions.

## Features

- 📚 **Multi-document Support**: Supports PDF format medical documents
- 🔍 **Hybrid Retrieval**: Combines BM25 and vector retrieval systems
- 🎯 **Intelligent Re-ranking**: Uses BGE re-ranking model to optimize retrieval results
- 💬 **Conversation Memory**: Supports multi-turn dialogue context memory
- 🌐 **Web Interface**: User-friendly interface based on Streamlit
- 🚀 **Efficient Retrieval**: Accelerates similarity search using FAISS vector database

## Tech Stack

- **Frontend Interface**: Streamlit
- **RAG Framework**: LangChain
- **Vector Database**: FAISS
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Re-ranking Model**: BAAI/bge-reranker-base
- **LLM**: DeepSeek Chat
- **Document Processing**: PyPDF

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd rag_system
```

### 2. Create virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file and add your DeepSeek API key:
```
DEEPSEEK_API_KEY=your_api_key_here
```

### 5. Prepare data
Place PDF documents in the `data/` directory.

## Usage

### Launch the application
```bash
streamlit run streamlit_app.py
```

### Access the application
Open your browser and navigate to: `http://localhost:8501`

### Usage workflow
1. Enter medical-related questions in the input box
2. The system retrieves relevant information from documents
3. Generates context-based answers
4. Displays answers and citation sources

## Project Structure

```
rag_system/
├── app/                    # Core modules
│   ├── ingestion.py       # Document loading
│   ├── vectorstore.py     # Vector store construction
│   ├── retriever.py       # Hybrid retriever
│   ├── reranker.py        # Re-ranking module
│   ├── memory.py          # Conversation memory
│   └── rag_pipeline.py    # RAG pipeline
├── data/                  # PDF document data
├── vectorstore/           # Vector storage
│   └── faiss_index/       # FAISS index files
├── streamlit_app.py       # Streamlit application entry
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── .env                   # Environment variables (need to create manually)
```

## Configuration

### Environment Variables
- `DEEPSEEK_API_KEY`: DeepSeek API key (required)

### Model Configuration
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- Re-ranking model: `BAAI/bge-reranker-base`
- LLM model: `deepseek-chat`

### Retrieval Parameters
- Chunk size: 800 characters
- Chunk overlap: 100 characters
- Retrieval count: 4 documents
- Re-ranking count: 3 documents
- Hybrid weights: BM25(0.4) + Vector retrieval(0.6)

## Important Notes

1. **API Key Security**: Do not commit API keys to version control systems
2. **Document Format**: Currently supports PDF format documents only
3. **Hardware Requirements**:
   - Minimum 8GB RAM
   - GPU recommended for better embedding and re-ranking performance
4. **First-time Run**: First run requires building FAISS index, time depends on document count
5. **Privacy Protection**: Medical data is sensitive, ensure data security

## Troubleshooting

### Common Issues
1. **ModuleNotFoundError**: Ensure all dependencies are installed
2. **API Key Error**: Check API key in `.env` file
3. **Insufficient Memory**: Reduce chunk size or use smaller embedding model
4. **PDF Reading Error**: Ensure PDF files are not corrupted and readable

### Getting Help
If you encounter issues, check:
- Dependency versions are correct
- Environment variables are configured
- Data files exist

## License
No license specified yet.

## Contributing
Issues and improvement suggestions are welcome.