import streamlit as st
from langchain.agents import AgentType, create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from sqlalchemy import create_engine

# Your ODBC connection string
odbc_str = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-HM7LQLF\\VAIBHAVSERVER;DATABASE=cricllm;Trusted_Connection=yes;TrustServerCertificate=yes;'

# Create SQLAlchemy engine
db_engine = create_engine(f'mssql+pyodbc:///?odbc_connect={odbc_str}')

# Azure OpenAI setup
os.environ["OPENAI_API_TYPE"]="azure"
os.environ["OPENAI_API_VERSION"]="2023-07-01-preview"
os.environ["OPENAI_API_BASE"]="https://cricai.openai.azure.com//openai/deployments/cricaidep/chat/completions?api-version=2023-07-01"  # Your Azure OpenAI resource endpoint
os.environ["OPENAI_API_KEY"]="905cac03e827471192d7d24351bf6374"  # Your Azure OpenAI resource key
os.environ["OPENAI_CHAT_MODEL"]="gpt-35-turbo-16k"  # Use name of deployment

llm = AzureChatOpenAI(model=os.getenv("OPENAI_CHAT_MODEL"), deployment_name=os.getenv("OPENAI_CHAT_MODEL"), temperature=0)

# SQLDatabase and SQLDatabaseToolkit instances
db = SQLDatabase(db_engine)
sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Prepare few-shot examples
few_shot_examples = [
    {"role": "system", "content": "You are a helpful assistant that can answer questions about SQL queries."},
    {"role": "user", "content": "How many matches did Mumbai Indians won by more than 5 wicket margin?"},
    {"role": "assistant", "content": "Let me find that information for you..."},
]

# Create SQL agent for few-shot learning
sqldb_agent = create_sql_agent(llm=llm, toolkit=sql_toolkit, agent_type=AgentType.FEW_SHOT, few_shot_examples=few_shot_examples, verbose=True)

# Streamlit app
def run_chatbot():
    st.title("Streamlit Chatbot for Cricket Data")

    input_text = st.text_input("You:", "Type your question here...")
    if st.button("Send"):
        response = sqldb_agent.run(input_text)
        st.text_area("Chatbot:", response, height=100)

if __name__ == "__main__":
    run_chatbot()
