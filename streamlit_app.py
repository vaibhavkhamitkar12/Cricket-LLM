# app.py
import streamlit as st

def main():
    st.title("Simple Streamlit App")
    
    # Add a text input widget
    user_input = st.text_input("Enter your name:", "Your Name")
    
    # Display a message using the user input
    st.write(f"Hello, {user_input}!")

    # Add a slider widget
    age = st.slider("Select your age:", 0, 100, 25)
    st.write(f"You selected age: {age}")

    # Add a button widget
    if st.button("Click me!"):
        st.success("Button clicked!")

if __name__ == "__main__":
    main()
