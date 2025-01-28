import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter



'''carregador de documentos assíncrono baseado no navegador Chromium. Permite extrair conteúdo de páginas da web utilizando 
um navegador headless (sem interface gráfica).'''
from langchain_community.document_loaders import AsyncChromiumLoader

'''um transformador de documentos que usa o BeautifulSoup.
Ele é utilizado para processar e limpar HTML extraído, removendo elementos desnecessários e estruturando o conteúdo.'''
from langchain_community.document_transformers import BeautifulSoupTransformer


load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('TOKEN_OPENAI')

llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)
schema={
    'properties':{
        'Tipo':{'type':'string'},
        'Data com':{'type':'string'},
        'Pagamento':{'type':'string'},
        'valor':{'type':'string'},
    }
}

url =  "https://investidor10.com.br/fiis/mxrf11/"

def screap_with_playwrigth(url):
    loader = AsyncChromiumLoader(url)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    
    #extrai o conteúdo da tabela no Html
    docs_transformer = bs_transformer.transform_documents( 
        documents= docs, #leitur do documento
        tags_to_extract=['table'], #extrai o conteúd da tag table
    )
        
    #tranformando os dados em chuncks,
    chunks = RecursiveCharacterTextSplitter.from_tiktoken_encoder( #utilizando tokenizador da Openai apra transformar o documento em chunks
        chunk_size=2000, 
        chunk_overlap=0
    )
    #quebrando os chunks
    splits = chunks.split_documents(documents=docs_transformer)
   
    
    # extracted_content = []
    # for split in splits:
    #     print(split.page_content)
        
        
        # extracted_content.extend(
        #     extract(
        #         schema=schema,
        #         content = split.page_content
        #     )
        # )
    
 

screap_with_playwrigth(url)

