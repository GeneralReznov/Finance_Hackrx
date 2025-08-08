from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..services import vector_store
import requests
import pymupdf

def process_file(pdf_data) -> str:
    docs = []
    try:
        doc = pymupdf.open(stream=pdf_data, filetype="pdf")
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            docs.append({
                "page_content": page.get_text("text", sort=True),
                "meta_data": {
                    "source": f"page_{page_num + 1}",
                    "page_number": page_num + 1
                }
            })
        return docs        

    except Exception :
        raise ValueError("Unsupported file type:")    
    
def get_langchain_document(extracted_content):
    documents = [Document(
            page_content=item["page_content"],
            metadata=item["meta_data"]  
            ) for item in extracted_content]
    return documents


def get_docs_chunks(documents):
    """Split text into manageable chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return text_splitter.split_documents(documents)


async def process_document(url: str):
    try:
        print(f"Processing document from URL: {url}")
        response = requests.get(url)
        pdf_data = response.content
        response.raise_for_status()
        doc = process_file(pdf_data)
        lang_docs = get_langchain_document(doc)    
        chunked_docs = get_docs_chunks(lang_docs)
        vector_store.create_vector_store(chunked_docs)
        
    except Exception as e:
        print(f"Processing error: {str(e)}")



