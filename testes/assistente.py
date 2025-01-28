import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.playwright.toolkit import PlayWrightBrowserToolkit
from playwright.sync_api import sync_playwright
from langchain_core.chat_history import InMemoryChatMessageHistory

# Carregar variáveis de ambiente
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('TOKEN_OPENAI')

# Configuração do modelo
model = ChatOpenAI(model='gpt-4o-mini', temperature=0)
schema={
    'properties':{
        'Tipo':{'type':'string'},
        'Data com':{'type':'string'},
        'Pagamento':{'type':'string'},
        'valor':{'type':'string'},
    }
}


# Prompt
prompt = ChatPromptTemplate.from_messages([
    ('system', '''
     Você é um assistente de investimentos. 
     Mostre no formato de tabela os dividendos pagos a partir do link passado pelo usuário
     
     '''),
    ('human', '{input}'),
    ('placeholder', '{agent_scratchpad}'),
])

# Criar o navegador síncrono do Playwright
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)  # Use headless=True para evitar a interface gráfica
    toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=browser)
    tools = toolkit.get_tools()

    # Inicializar o agente
    config = {"configurable": {"session_id": "test-session"}}
    agent = initialize_agent(
        tools=tools,
        llm=model,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # Loop de interação
    try:
        print("Digite suas perguntas. Pressione Ctrl+C para sair.")
        while True:
            urls=[
                "https://statusinvest.com.br/fundos-imobiliarios/mxrf11",
               
            ]
            input_text = input("Você>> ")  # Entrada do usuário
        
            response = agent.invoke({"input": f'{input_text} {urls}'}, config=config)
            print(response.get('output'))
    except KeyboardInterrupt:
        print("\nEncerrando o programa. Até mais!")
