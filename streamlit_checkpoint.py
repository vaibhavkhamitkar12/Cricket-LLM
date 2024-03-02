import streamlit as st
import os
import pyodbc
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.agents import AgentType, create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# Set up environment variables
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"
os.environ["OPENAI_API_BASE"] = "https://cricai.openai.azure.com//openai/deployments/cricaidep/chat/completions?api-version=2023-07-01"
os.environ["OPENAI_API_KEY"] = "905cac03e827471192d7d24351bf6374"
os.environ["OPENAI_CHAT_MODEL"] = "gpt-35-turbo-16k"

# Your ODBC connection string
odbc_str = 'Driver={ODBC Driver 18 for SQL Server};Server='+ st.secrets["server"] +','+ st.secrets["id"] +';Database='+ st.secrets["database"] +';Uid='+ st.secrets["username"] +';Pwd='+ st.secrets["pass"] +';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Create ODBC connection
conn = pyodbc.connect(odbc_str)

llm = AzureChatOpenAI(
    model=os.getenv("OPENAI_CHAT_MODEL"),
    deployment_name=os.getenv("OPENAI_CHAT_MODEL"),
    temperature=0
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "Your system message here."),
    ("user", "{question}\n ai: "),
])

db = SQLDatabase(conn)

sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_toolkit.get_tools()

sqldb_agent = create_sql_agent(
    llm=llm,
    toolkit=sql_toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Streamlit app
def run_chatbot():
    st.title("Streamlit Chatbot for Cricket Data")

    input_text = st.text_input("You:", "Type your question here...")
    if st.button("Send"):
        response = sqldb_agent.run(input_text)
        st.text_area("Chatbot:", response, height=100)

if __name__ == "__main__":
    run_chatbot()
