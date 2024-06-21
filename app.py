import streamlit as st
import google.generativeai as genai
import spacy
from spacy_streamlit import visualize_parser
from google.generativeai.types import HarmCategory, HarmBlockThreshold


def main():

    st.title("English Learning App")
    st.image("images/english.jpg")

    nlp = spacy.load("en_core_web_sm")
    models = ["en_core_web_sm"]

    user_input = st.sidebar.text_area("Enter english sentences")
    pos = st.sidebar.selectbox("Part of speech", ("Yes", "No"))
    recommendation = st.sidebar.selectbox("Recommendation",[1, 2, 3, 4, 5])
    button = st.sidebar.button("Submit")

    user_input_2 = nlp(user_input)

    genai.configure(api_key="AIzaSyCRsJNf1U6iAyboUrpooTCcCMxOKyqbLQA")
    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 500
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

    model = genai.GenerativeModel(model_name = "models/gemini-1.5-pro",
                                   generation_config = generation_config,
                                   safety_settings = safety_settings)

    if button:
        if pos == "Yes":
            visualize_parser(user_input_2)

            response_recommendation = model.generate_content(f"Recommend {recommendation} another ways to write this text: {user_input}. Don't format anything.")
            response_translate = model.generate_content(f"Translate {user_input} to vietnamese please. Don't format anything.")

            st.markdown("## Translate to vietnamese:")
            st.write(response_translate.text)

            st.markdown(f"## {recommendation} ways to write this text:")
            st.write(response_recommendation.text)
        else:
            response_recommendation = model.generate_content(f"Recommend {recommendation} another ways to write this text: {user_input}. Don't format anything.")
            response_translate = model.generate_content(f"Translate {user_input} to vietnamese please. Don't format anything.")

            st.markdown("## Translation:")
            st.write(response_translate.text)

            st.markdown(f"## {recommendation} ways of this text:")
            st.write(response_recommendation.text)

if __name__ == "__main__":
    main()