import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_extraction_chain
from pprint import pprint


'''carregador de documentos assíncrono baseado no navegador Chromium. Permite extrair conteúdo de páginas da web utilizando 
um navegador headless (sem interface gráfica).'''
from langchain_community.document_loaders import AsyncChromiumLoader

'''um transformador de documentos que usa o BeautifulSoup.
Ele é utilizado para processar e limpar HTML extraído, removendo elementos desnecessários e estruturando o conteúdo.'''
from langchain_community.document_transformers import BeautifulSoupTransformer


load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('TOKEN_OPENAI')

llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)
schema = {
 'properties': {
 'posicao': {'type': 'integer'},
 'time': {'type': 'string'},
 'jogos': {'type': 'integer'},
 'vitorias': {'type': 'integer'},
 'empates': {'type': 'integer'},
 'derrotas': {'type': 'integer'},
 'gols_pro': {'type': 'integer'},
 'gols_contra': {'type': 'integer'},
 'saldo_gols': {'type': 'integer'},
 'pontos': {'type': 'integer'},
 },
}

def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema,llm=llm,).invoke(content).get('text')


def scrape_with_playwright(urls, schema=None):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        documents=docs,
        tags_to_extract=['table'],
    )
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=0,
    )
    splits = splitter.split_documents(documents=docs_transformed,)
    extracted_content = []
    for split in splits:
        extracted_content.extend(extract(
            schema=schema,
            content=split.page_content,
            ))
        
    return extracted_content

 
if __name__ == '__main__':
    urls = ['https://ge.globo.com/futebol/brasileirao-serie-a/']
    extracted_content = scrape_with_playwright(
    urls=urls,
    schema=schema,
    )
    pprint(
    object=extracted_content,
    indent=4,
    sort_dicts=False,
    )
    with open('data.json', 'w') as fp:
        json.dump(
            obj=extracted_content,
            fp=fp,
            ensure_ascii=False,
            indent=4,
        )
