import streamlit as st

def main():
    st.title("Interactive Chatbot")

    # User input
    user_input = st.text_area("You:", "Type something...", height=100)

    if st.button("Send"):
        # Display user input
        st.text_area("You:", user_input, height=100)

        # Get chatbot response
        chatbot_response = get_chatbot_response(user_input)

        # Display chatbot response
        st.text_area("Chatbot:", chatbot_response, height=100)

def get_chatbot_response(user_input):
    # Add your chatbot logic here
    # For simplicity, let's just echo the user's input
    return f"Chatbot says: '{user_input}'"

if __name__ == "__main__":
    main()
