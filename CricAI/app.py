import streamlit as st
from sqlalchemy import create_engine
import os
#from dotenv import load_dotenv
from langchain_community.chat_models import AzureChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.agents import AgentType, create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

os.environ["OPENAI_API_TYPE"]="azure"
os.environ["OPENAI_API_VERSION"]="2023-07-01-preview"
os.environ["OPENAI_API_BASE"]="https://cricai.openai.azure.com//openai/deployments/cricaidep/chat/completions?api-version=2023-07-01" # Your Azure OpenAI resource endpoint
os.environ["OPENAI_API_KEY"]="905cac03e827471192d7d24351bf6374" 
os.environ["OPENAI_CHAT_MODEL"]="gpt-35-turbo-16k"

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
          DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
          If the question does not seem related to the database, just return "I don't know" as the answer.
          You are an assistant that provides statistical and analytical answers to user's question about Matches and ball_to_ball table.

          Matches table:
          
          ID: A unique identifier for each cricket match, column type - int
          City: The city where the match took place, providing geographical context for the event. column type - varchar
          Date: The date of the match.
          Season: The season year of that match.
          MatchNumber: The match number within the season and also describes type of matches like Final,
          Qualifier 2,
          Eliminator,
          Qualifier 1,if match is of playoffs type.
          Team1: The name of the first team playing in the match. column type - varchar
          Team2: The name of the second team playing in the match. column type - varchar
          Venue: The name of the stadium where the match was held. column type - varchar
          TossWinner: The name of team winning the toss. column type - varchar
          TossDecision: The decision made by the toss-winning team which can be bat or field. column type - varchar
          SuperOver: Whether a Super Over was played to break a tie, Y if played , N if super over is not player. 
          WinningTeam: The name of team that won the that match. column type - varchar
          WonBy: Describes how the match was won by Runs,Wickets, SuperOver or NoResult. column type - varchar
          Margin: The margin of victory, if corresponding WonBy cell is "Runs" then no. of runs would mentioned, if corresponding Wonby cell is "Wickets" then no. of wickets by which winning team won would be monetioned. column type - int
          Method: The method of winning either D/L or NA , if there is rain then D/L method is used , otherwise NA which describes normal match. column type - varchar
          Player_of_Match: The name of Man of the Match player. column type - varchar 
          Team1Players: A list of players in Team 1, providing information about the team composition.
          Team2Players: A list of players in Team 2
          Umpire1: The name of first umpire officiating the match. column type - varchar
          Umpire2: The name of second umpire officiating the match. column type - varchar

          ball_to_ball table: 
          
          ID: Unique identifier for each cricket match.
          innings: Indicates the inning number of the match (1 or 2).
          overs: The current over of the match.In range of 0 to 20
          ballnumber: The sequential number of the ball within the over. 6 balls in an over
          batter: The name of batsman currently facing the ball. 
          bowler: The name bowler delivering the ball.
          non-striker: The name of non-striker batsman at the crease.
          extra_type: Type of extra run scored in the ball (e.g., legbyes, wides, byes,No ball, penalty,N/A - if no extra run is scored in that ball).
          batsman_run: Number of runs scored by the batsman in that particular ball of that particular over.
          extras_run: Additional runs scored through extras if any in that particular ball of that particular over.
          total_run: Total runs scored in the ball, including extras.
          non_boundary: Indicates if the run was a boundary (if non boundary then 1, if boundary or 6 then value is 1).
          isWicketDelivery: Indicates if the ball resulted in a wicket.(If wicket delivery then value is 1 , if not a wicket delivery than value is 0)
          player_out: Name of the Batsman dismissed (if applicable, otherwise N/A).
          kind: Type of dismissal (e.g., caught, bowled, caught and bowled, hit wicket, stumped,lbw, run out,obstructing the field, retired hurt, ).
          fielders_involved: Name of the Fielders involved in the dismissal.(only if caught, caught and bowled, stumped, run out in corresponding kind of dismissal field)
          BattingTeam: The Name of the team batting during this phase of the match.
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
def run_continuous_chatbot():
    st.title("🏏 Continuous Messaging Cricket Chatbot")
    st.sidebar.header("User Options")

    # Create a sidebar for user options
    user_question = st.sidebar.text_input("Ask a question:", "How many matches did Mumbai Indians win?")
    submit_button = st.sidebar.button("Ask Chatbot")

    # Main content area
    st.markdown("---")

    # Display the cricket-themed image
    st.image("cricket_image.jpg", caption="Cricket Image", use_column_width=True)

    # Add a colorful and styled title
    st.markdown(
        "<h1 style='text-align: center; color: #ff9900;'>Continuous Messaging Cricket Chatbot</h1>",
        unsafe_allow_html=True
    )

    # Display user input and chatbot responses in a continuous chat style
    chat_history = []

    if submit_button:
        # Fetch chatbot response
        response = sqldb_agent.run(user_question)

        # Update chat history
        chat_history.append(("User", user_question))
        chat_history.append(("Chatbot", response))

    # Display chat history
    st.subheader("Chat History:")
    for sender, message in chat_history:
        st.write(f"{sender}: {message}")

    # Add a fun cricket GIF
    st.markdown("---")
    #st.image("images/cricket_gif.gif", caption="Cricket GIF", use_column_width=True)

if __name__ == "__main__":
    run_continuous_chatbot()
