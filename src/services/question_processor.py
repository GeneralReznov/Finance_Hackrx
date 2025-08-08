from fastapi import  HTTPException
from ..config import constant
from ..services import qa_chain


async def answer(question: str) -> str:
    """
    """
    vector_store_current = constant.global_state.vector_store
    response, source_str = rag_response(question,vector_store_current)
    return response



def rag_response(question,vector_store):
    try:
        if vector_store.get()["documents"] == []:
            raise HTTPException(400, "No documents in vector store")
        # Always load from disk to ensure we have the latest data
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(question)
        sources = {f"{doc.metadata['source'][5:]}" for doc in docs}
        unique_sources = list(set(sources))
        source_str = "".join(unique_sources)
        chain = qa_chain.get_conversational_chain()
        response = chain.invoke({"input_documents": docs, "question": question})
        response_text = response["output_text"]
        return response_text, source_str
    except Exception as e:
        print(f"Error in rag_response: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")