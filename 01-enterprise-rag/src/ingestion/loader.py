import logging
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader, CSVLoader
from langchain_core.documents import Document

logger = logging.getLogger(__name__)
LOADER_MAP = {".pdf": PyPDFLoader, ".txt": TextLoader, ".md": UnstructuredMarkdownLoader, ".csv": CSVLoader}

class DocumentLoader:
    def __init__(self, data_dir="data/raw"):
        self.data_dir = Path(data_dir)

    def load_file(self, file_path):
        suffix = file_path.suffix.lower()
        loader_class = LOADER_MAP.get(suffix)
        if not loader_class:
            return []
        try:
            docs = loader_class(str(file_path)).load()
            for doc in docs:
                doc.metadata.update({"source_file": file_path.name, "file_type": suffix, "category": file_path.parent.name})
            return docs
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return []

    def load_all(self):
        all_docs = []
        for fp in self.data_dir.rglob("*"):
            if fp.is_file() and fp.suffix.lower() in LOADER_MAP:
                all_docs.extend(self.load_file(fp))
        logger.info(f"Loaded {len(all_docs)} documents")
        return all_docs
