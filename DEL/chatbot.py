import streamlit as st
from langchain_core.prompts import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    MessagesPlaceholder,
                                    SystemMessagePromptTemplate)
from langchain_openai import ChatOpenAI
from risk.assessment import build_assessment_chain

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    api_key=st.secrets["OPENAI_API_KEY"],
    streaming=True,
)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template("You are a helpful assistant."),
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{prompt}"),
    ]
)

chain = chat_prompt | llm

st.title("Scout Assistant")

with st.expander("Info"):
    st.markdown("# Heading \n Body.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me a question about Scouts"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Generating..."):
            risk_chain = build_assessment_chain()
            # response = st.write_stream(
            response = st.write(
                # risk_chain.stream(
                risk_chain.invoke(
                    {
                        "activity": "Pumpkin carving",
                        "location": "Scout hut",
                    }
                ).to_markdown()
            )
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write("https://www.scouts.org.uk/por/")

        # with st.spinner("Generating..."):
        #     response = st.write_stream(
        #         chain.stream(
        #             {
        #                 "messages": st.session_state.messages,
        #                 "prompt": prompt,
        #             }
        #         )
        #     )
        #     st.session_state.messages.append({"role": "assistant", "content": response})
