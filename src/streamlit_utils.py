import streamlit as st


def print_chat_list():
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def streamlit_init():
    st.title("AJent - AJ's custom agent")
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": "You are a smart assistant.You help the user. if something is not clear or you need more details, ask the user for it. Answer the user in concise helpful manner. Don't put too much data to the user. You can use markdown to respond if necessary",
            },
            {
                "role": "assistant",
                "content": "Hi, I am your friendly neighbourhood asssistant. Ask me to do any actions!",
            },
        ]

    print_chat_list()


def move_focus():
    # inspect the html to determine which control to specify to receive focus (e.g. text or textarea).
    pass
    # st.components.v1.html(
    #     f"""
    #         <script>
    #             window.scrollTo(0, document.body.scrollHeight);
    #         </script>
    #     """,
    # )
