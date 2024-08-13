import os
import streamlit as st

from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

# Configurations
load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

# pipeline
pinecone_index = pc.Index("dps-bmz-test")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index, text_key="content")
query_engine = VectorStoreIndex.from_vector_store(vector_store).as_query_engine()


# streamlit app settings
st.set_page_config(
    page_title="Prompt Bot",
    page_icon=":hourglass_flowing_sand:",
    layout="centered"
)
st.markdown("<h1 style='text-align: center;'>⏳ Prompt Bot </h1>", unsafe_allow_html=True)
st.markdown(" ")
st.markdown(
    "<p style='text-align: center;'>"
    "Ask any questions about the following documents ️↠",
    unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h4 style='text-align: center;'> ⏳ Instructions to Prompt:  </h4>", unsafe_allow_html=True)
    st.markdown("1. The prompt may be as long as you like, but not longer than a page.")
    st.markdown("2. All documents are stored in the database. You can ask questions about these files: ")
    st.markdown(" - All Modul_AA_IDN_Energy_REEP")
    st.markdown(" - All Modul_BE_DZA_Nachhaltige Stadtentwicklung_Abfall")
    st.markdown(" - All Modul_BE_IDN_Energy_REEP")
    st.markdown(" - All Modul_Final Report_DZA_Nachhaltige Stadtentwicklung_Abfall")
    st.markdown(" - All Modul_VS_IDN_Energy_ETAP")
    st.markdown(" - All Modul_VS_IDN_Energy_SOCOOL")
    st.markdown(" - All Programm_BE_IDN_Climate and Forest_NA")
    st.markdown(" - Programm_Bericht_South Africa_TVET and Employment_Final")
    st.markdown(" - Programm+Module_BE_IDN_Energy_NA_2021")
    st.markdown(" - Programmentwurf_South_Africa_TVET and Employment_2023")

# display files
file_names = ["Modul_AA_IDN_Energy_REEP_2022.pdf",
              "Modul_ÄA_IDN_Energy_REEP_2023.pdf",
              "Modul_BE_DZA_Nachhal...icklung_Abfall_2018.pdf",
              "Modul_BE_DZA_Nachhal...icklung_Abfall_2021.pdf",
              "Modul_BE_DZA_Nachhal...icklung_Abfall_2022.pdf",
              "Modul_BE_IDN_Energy_REEP_2021.pdf",
              "Modul_BE_IDN_Energy_REEP_2022.pdf",
              "Modul_BE_IDN_Energy_REEP_2023.pdf",
              "Modul_Final Report_D...cklung_Abfall_2023.pdf",
              "Modul_VS_IDN_Energy_ETAP_2023.pdf",
              "Modul_VS_IDN_Energy_SOCOOL_2022.pdf",
              "Programm_BE_IDN_Cli...d Forest_NA_2020.pdf",
              "Programm_BE_IDN_Cli...d Forest_NA_2021.pdf",
              "Programm_BE_IDN_Cli...d Forest_NA_2022.pdf",
              "Programm_BE_IDN_Energy_NA_2020.pdf",
              "Programm_BE_IDN_Energy_NA_2021.pdf",
              "Programm_BE_IDN_Energy_NA_2022.pdf",
              "Programm_BE_IDN_Energy_NA_2023.pdf",
              "Programm_Bericht_So...Employment_Final.pdf",
              "Programm+Module_BE..._Energy_NA_2021.pdf",
              "Programmentwurf_South_Africa_TVET and Employment_2023.pdf"]

qa_data = []

# query functionality
processing_container = st.empty()
processing_container.markdown(" ")
question = st.text_input("Please enter your question:")

if st.button('Generate :sparkles:'):
    prompt = question + (" Return the answer in markdown. Answer in English. Be detailed and include proofs from the"
                         " documents.")
    processing_container.markdown("""<p style="color: #3ae2a5;">Processing question...</p>""", unsafe_allow_html=True)

    st.markdown("Prompt: ")
    st.markdown(prompt, unsafe_allow_html=True)
    st.markdown("Response: ")
    answer = query_engine.query(prompt)
    processing_container.markdown("""<p style="color: #3ae2a5;">Response Generated!</p>""", unsafe_allow_html=True)

    st.markdown(answer, unsafe_allow_html=True)
    qa_data.append({'Question': prompt, 'Answer': answer})
