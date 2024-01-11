from openai import OpenAI
import streamlit as st
from src.constants import openai_api_key
from src.streamlit_utils import streamlit_init, move_focus
from src.llm_utils import get_llm_response
from src.agent_utils import get_agent_response
from langchain_core.messages import AIMessage, HumanMessage

chat_history = []


streamlit_init()
client = OpenAI(api_key=openai_api_key)


if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        chat_history = []
        for m in st.session_state.messages:
            print(m)
            if m["role"] == "user":
                chat_history.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                chat_history.append(AIMessage(content=m["content"]))

        ai_resp = get_agent_response(prompt=prompt, chat_history=chat_history)
        message_placeholder.markdown("▌")
        message_placeholder.markdown(ai_resp)
    st.session_state.messages.append({"role": "assistant", "content": ai_resp})
