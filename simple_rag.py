import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Load dos modelos
embeddings_model = OpenAIEmbeddings()
llm = ChatOpenAI(model='gpt-4o-mini', max_tokens=200)

# Diretório de persistência dos embeddings
VECTORSTORE_DIR = './vectorstore'


def load_data():
    # Verificar se a base vetorial já foi persistida
    if os.path.exists(VECTORSTORE_DIR):
        # Carregar a base vetorial persistida
        vector_db = Chroma(persist_directory=VECTORSTORE_DIR,
                           embedding_function=embeddings_model)
    else:
        print("Não Carrega")
        # Carregar PDF e gerar novos embeddings
        pdf_link = "./DOC-SF238339076816-20230503.pdf"
        loader = PyPDFLoader(pdf_link, extract_images=False)
        pages = loader.load_and_split()

        # Separar pedaços de documentos
        text_spliter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=20,
            length_function=len,
            add_start_index=True
        )

        chunks = text_spliter.split_documents(pages)

        # Criar a base vetorial e persistir no disco
        vector_db = Chroma.from_documents(
            chunks, embedding=embeddings_model, persist_directory=VECTORSTORE_DIR
        )

    # Retornar o retriever para buscar documentos
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    return retriever


def get_relevant_documents(question: str):
    retriever = load_data()
    context = retriever.invoke(question)
    return context


def ask(question: str, llm: ChatOpenAI):
    TEMPLATE = '''
      Você é um especialista em legislação e tecnologia, responda a pergunta abaixo utilizando o contexto informado.
      
      Contexto: {context}
      
      Pergunta: {question}
    '''
    prompt = PromptTemplate(
        input_variables=['context', 'question'],
        template=TEMPLATE
    )

    sequence = RunnableSequence(prompt | llm)

    context = get_relevant_documents(question)

    response = sequence.invoke({"context": context, "question": question})

    return response.content


print(ask('Quais os riscos da lei para minha empresa?', llm))
