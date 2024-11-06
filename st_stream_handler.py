from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
import streamlit as st

st.set_page_config(layout="wide")

# https://discuss.streamlit.io/t/detect-whether-code-is-being-run-from-mobile/26572/4


class StreamHandler(BaseCallbackHandler):
    # https://python.langchain.com/docs/how_to/streaming/#event-reference
    # https://python.langchain.com/docs/concepts/callbacks/
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")

st.info("You need your own keys to run commercial models", icon="ℹ️")
st.success("Green")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ChatMessage(role="assistant", content="How can I help you?")
    ]

for msg in st.session_state.messages:
    # TODO would probably need a way of displaying the pydantic data model
    with st.chat_message(msg.role):
        st.write(msg.content)
        with st.expander("References"):
            st.write("**REF1**")

if prompt := st.chat_input("Message"):
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    with st.chat_message("assistant"):
        container = st.empty()
        stream_handler = StreamHandler(container)
        llm = ChatOpenAI(api_key=openai_api_key, streaming=True)
        response = llm.invoke(
            st.session_state.messages,
            config={"callbacks": [stream_handler]},
        )
        st.session_state.messages.append(
            ChatMessage(role="assistant", content=response.content)
        )
        with st.expander("References"):
            st.write("**REF1**")
