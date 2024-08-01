import streamlit as st

st.set_page_config(layout="centered", page_title="Credit Bot", initial_sidebar_state="collapsed")
st.markdown("#### CreditWatch.")

def get_bot_response(user_input):
    if "hello" in user_input.lower():
        return "Hello! How can I help you today?"
    elif "how are you" in user_input.lower():
        return "I'm doing well, thank you for asking!"
    else:
        return "I'm not sure how to respond to that. Can you try rephrasing?"

def clear_messages():
    st.session_state.messages = []

def main():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is your question?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = get_bot_response(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()

# Create a two-column layout for buttons
col1, col2 = st.columns(2)

# Add "Clear Chat History" button in the first column
if col1.button("Clear Chat History", use_container_width=True):
    clear_messages()

# Add "Back" button in the second column
if col2.button("Back", type="primary", use_container_width=True):
    st.switch_page("pages/credit_watch.py")