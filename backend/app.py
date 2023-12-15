# Filename - server.py

from flask import Flask, jsonify, request
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
import os
from flask_cors import CORS, cross_origin


# Initializing flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


conversation_chain = None
# Store state data in a dictionary if necessary
state_data = {
    'vectorstore_created': True,
    # Add other relevant data
}

@app.route('/reset', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def reset():
    global conversation_chain
    conversation_chain = None
    process()

    return jsonify({'status': 'success', 'message': 'State reset successfully'})

def process():
    global conversation_chain

    # List of specific PDFs to process
    pdf_docs= [
        'b1.pdf',
        'b2.pdf',
        'b3.pdf',
        'b4.pdf',
        'b5.pdf'
        # Add more PDFs as needed
    ]
    raw_text = get_pdf_text(pdf_docs)
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)
    conversation_chain = get_conversation_chain(vectorstore)


@app.route('/ask', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def ask():
    # data = request.get_json()
    user_question = request.args.get('user_question')
    # user_question = data.get('user_question')
 
    # print(user_question)
    # print(conversation_chain)
    if not conversation_chain:
        return jsonify({'status': 'error', 'message': 'Conversation chain not initialized'})

    response = conversation_chain({'question': user_question})

    chat_history = response['chat_history']

    # Format response for frontend
    formatted_response = []
    for i, message in reversed(list(enumerate(chat_history))):
        if i % 2 == 0:
            formatted_response.append({'type': 'user', 'content': message.content})
        else:
            formatted_response.append({'type': 'bot', 'content': message.content})

    return jsonify({'status': 'success', 'chat_history': formatted_response})


def get_pdf_text(pdf_files):
    # Extract PDF text and process
    text = ""
    for pdf_file in pdf_files:
        pdf_path = pdf_file
        pdf_text = extract_text_from_pdf(pdf_path)
        text += pdf_text

    # print(text)
    return text

def extract_text_from_pdf(pdf):
    text = ""
 
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
    
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(temperature=0)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    print('conv chain created')

    return conversation_chain

@app.route('/')
def get():
    return "<h1>hi</h1>"

# Running app
if __name__ == '__main__':
    load_dotenv()
    app.run(host="0.0.0.0")
