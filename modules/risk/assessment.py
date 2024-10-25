import itertools
import json

import streamlit as st
from langchain_openai import ChatOpenAI

from .models import ExampleRiskAssessment, RiskAssessment
from .prompts import assessment_prompt, user_prompt


def get_examples():

    with open("modules/risk/assessment_examples.json") as f:
        examples = json.load(f)

    examples = [
        ExampleRiskAssessment(**example).to_messages(user_prompt)
        for example in examples
    ]

    return list(itertools.chain(*examples))


def build_assessment_chain():

    examples = get_examples()

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.5,
        api_key=st.secrets["OPENAI_API_KEY"],
    )

    llm = model.with_structured_output(RiskAssessment)
    app = assessment_prompt.partial(examples=examples, n_min=7) | llm

    return app
