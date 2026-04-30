from pathlib import Path
from typing import List
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents(data_dir: Path) -> List:
    documents = []

    for path in data_dir.glob("*"):
        if path.suffix.lower() == ".txt":
            loader = TextLoader(str(path), encoding="utf-8")
            documents.extend(loader.load())

        elif path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(path))
            documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    return splitter.split_documents(documents)
