import streamlit as st
from sqlalchemy import create_engine
import os
#from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.agents import AgentType, create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

os.environ["OPENAI_API_TYPE"]="azure"
os.environ["OPENAI_API_VERSION"]="2023-07-01-preview"
os.environ["OPENAI_API_BASE"]="https://cricai.openai.azure.com//openai/deployments/cricaidep/chat/completions?api-version=2023-07-01" # Your Azure OpenAI resource endpoint
os.environ["OPENAI_API_KEY"]="905cac03e827471192d7d24351bf6374" # Your Azure OpenAI resource key
os.environ["OPENAI_CHAT_MODEL"]="gpt-35-turbo-16k" # Use name of deploymenta

# Your ODBC connection string
odbc_str = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=DESKTOP-HM7LQLF\\VAIBHAVSERVER;DATABASE=cricllm;Trusted_Connection=yes;TrustServerCertificate=yes;'

# Create SQLAlchemy engine
db_engine = create_engine(f'mssql+pyodbc:///?odbc_connect={odbc_str}')

llm = AzureChatOpenAI(model=os.getenv("OPENAI_CHAT_MODEL"),
                      deployment_name=os.getenv("OPENAI_CHAT_MODEL"),
                      temperature=0)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         """
          You are a helpful AI assistant expert in querying SQL Database.
          You are an assistant that provides statistical and analytical answers to user's question about Matches and ball_to_ball table.       

         """
         ),
        ("user", "{question}\n ai: "),
    ]
)

db = SQLDatabase(db_engine)

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
    st.title("🏏 Cricket Data Chatbot")
    st.sidebar.header("User Options")

    # Create a sidebar for user options
    user_question = st.sidebar.text_input("Ask a question:", "How many matches did Mumbai Indians win?")
    submit_button = st.sidebar.button("Ask Chatbot")

    # Main content area
    st.markdown("---")

    # Display a cricket-themed image
    st.image("cricket_image.jpg", caption="Cricket Image", use_column_width=True)

    # Add a colorful and styled title
    st.markdown(
        "<h1 style='text-align: center; color: #ff9900;'>Interactive Cricket Chatbot</h1>",
        unsafe_allow_html=True
    )

    # Display user input and chatbot response
    st.subheader("User Input:")
    st.write(f"You: {user_question}")

    if submit_button:
        # Fetch chatbot response
        response = sqldb_agent.run(user_question)

        # Display chatbot response
        st.subheader("Chatbot Response:")
        st.info(response)

    # Add a fun cricket GIF
    st.markdown("---")
    #st.image("cricket_gif.gif", caption="Cricket GIF", use_column_width=True)

if __name__ == "__main__":
    run_chatbot()
