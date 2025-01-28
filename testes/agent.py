
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.playwright.toolkit import PlayWrightBrowserToolkit
from playwright.sync_api import sync_playwright
from langchain_core.chat_history import InMemoryChatMessageHistory

# Carregar variáveis de ambiente
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('TOKEN_OPENAI')
session_id = "test-session"
memory = InMemoryChatMessageHistory(session_id=session_id)
model = ChatOpenAI(model='gpt-4o-mini', temperature=0)
prompt =ChatPromptTemplate.from_messages([
                ("system", '''
                  Você é um assistente de investimentos. 
                    Mostre no formato de tabela os dividendos pagos a partir do link passado pelo usuário
                 '''), # Configura o comportamento do agente como um "assistente útil".
                ("placeholder", "{chat_history}"), #Adiciona um espaço reservado para o histórico da conversa anterior
                ("human", "{input}"), # Contém a entrada dinâmica do usuário, representada pelo placeholder {input}.
                ("placeholder", "{agent_scratchpad}"), # agente pode armazenar seus pensamentos ou processos intermediários.
            ])
     



with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)  # Use headless=True para evitar a interface gráfica
    toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=browser)
    tools = toolkit.get_tools()
    agent = initialize_agent(
        llm=model,
        tools=tools, 
        prompt=prompt,
        agent = AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        ) #criando o agente
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools, 
        verbose=True,

        ) #executando o agente
#config para manter interações individuais e manter o histórico da conversa,
    config = {"configurable": {"session_id": "test-session"}}
    
    try:
        print("Digite suas perguntas. Pressione Ctrl+C para sair.")
        agent_with_memory = RunnableWithMessageHistory(
        agent_executor,
            lambda session_id: memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        
        while True:
            input_text = input("Você>> ")  # Entrada do usuário
            response = agent_with_memory.invoke({"input": input_text})
            print(response.get('output'))
    
    except KeyboardInterrupt:
        print("\nEncerrando o programa. Até mais!")

    
    
    
    # try:
    #     agent_with_memory = RunnableWithMessageHistory(
    #     agent_executor,
    #     lambda session_id:memory,
    #     input_messages_key="input",
    #     history_messages_key="chat_history",
    #     )
    #     response = agent_with_memory.invoke({"input": input_text},config=config)
    #     return response.get('output')

    # except Exception as e:
    #     print(f"Error do agent: {e}")
    #     return "Desculpe, não consegui processar sua solicitação. Erro {e}"

