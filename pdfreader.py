import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                page_text = page_text.encode("utf-8", errors="replace").decode("utf-8")
                text += page_text
    return text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. If the answer is not in
    the context, respond with "answer is not available in the context" and avoid guessing.\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    
    return chain


def user_input(user_question, context=""):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    
    chain = get_conversational_chain()
    
    response = chain(
        {"input_documents": docs, "question": user_question, "context": context},
        return_only_outputs=True
    )
    context += f"\nQ: {user_question}\nA: {response['output_text']}\n"
    return response["output_text"], context
def translate_text(text, target_language="es"):  # e.g., "es" for Spanish
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)
    translate_prompt = f"Translate the following text to {target_language}:\n\n{text}\n\nTranslated Text:"
    response = model({"input": translate_prompt})
    return response["output_text"]


def main():
    st.set_page_config(page_title="Enhanced Chat with PDF", page_icon="💬")
    st.title("💬 Enhanced Chat with PDF using Gemini")
    
    st.write("Upload PDFs and ask questions")
    with st.sidebar:
        st.title("Options")
        pdf_docs = st.file_uploader("Upload PDF files:", accept_multiple_files=True, type=["pdf"])
        
        if st.button("Submit & Process"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("PDFs processed successfully! Ready for interaction.")
            else:
                st.warning("Please upload at least one PDF file.")
    user_question = st.text_input("Ask a Question from the PDF Files")
    
    if user_question:
        with st.spinner("Generating answer..."):
            answer, context = user_input(user_question, context=st.session_state.get("context", ""))
            st.session_state["context"] = context
            st.write("### Reply:")
            st.write(answer)
    if st.button("Submit"):
        st.session_state["context"] = ""


if __name__ == "__main__":
    main()
