from fastapi import HTTPException, APIRouter
from ..services import file_processor
from src.schemas.main_schema import HackRXRequest
from src.services import question_processor

router = APIRouter()
@router.post("/hackrx/run")
async def run_hackrx(payload:HackRXRequest):
    doc_link = payload.documents
    questions = payload.questions

    try:
        # Process the document and questions
        response = await file_processor.process_document(doc_link)
        print(f"Document processed: {response}")
        answers = []
        for question in questions:
            answer = await question_processor.answer(question)
            answers.append(answer)

        return {"answers": answers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}") 

