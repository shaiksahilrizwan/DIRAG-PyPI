# DIRAG

DIRAG is a command-line assistant for local Ollama models with optional PDF retrieval-augmented generation.

## Install

```powershell
python -m pip install dirag
```

For development:

```powershell
python -m pip install -e .
dirag --help
```

## Configure

Users must manually create `dirag.json` in the directory where they run the command:

```json
{
  "ollama_url": "http://localhost:11434",
  "model": "llama3.2",
  "embed_model": "nomic-embed-text",
  "collection_name": "dirag-documents"
}
```

DIRAG does not create or modify this file.

## Use

Start a chat:

```powershell
dirag chat
```

Resume a saved chat:

```powershell
dirag chat --session <session-id>
```

When PDF files and RAG settings are present in the current directory, DIRAG creates a local Chroma vector store and indexes the PDFs.
