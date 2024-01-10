from openai import OpenAI
import streamlit as st
from src.constants import openai_api_key
from src.streamlit_utils import streamlit_init
from src.llm_utils import get_llm_response


streamlit_init()
client = OpenAI(api_key=openai_api_key)


if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        print(messages)
        full_response = get_llm_response(messages=messages)
        print(full_response)

        # for response in client.chat.completions.create(
        #     model=st.session_state["openai_model"],
        #     messages=messages,
        #     stream=True,
        # ):
        #     full_response += response.choices[0].delta.content or ""
        #     message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
