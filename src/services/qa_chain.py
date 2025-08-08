from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from ..config import constant

genai.configure(api_key=constant.global_state.google_api_key)
def get_conversational_chain():
    
    prompt_template = """
    You are an expert in finance specilizing in credit and insurance policy services. You have to analyse the given context and give a concise answer to the question asked within two lines.
    
    If the answer is not present in the context gracefully say the answer is not present in the provided context. 

    Only give the answer, dont give anything else, no extra comments.
    Context: {context}
    Question: {question}
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)


