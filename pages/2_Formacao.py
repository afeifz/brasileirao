import streamlit as st

st.set_page_config(page_title="Formação e Experiência", layout="wide")

# Título da página
st.title("🎓 Formação e Experiência")

# Espaço centralizado
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Formação Acadêmica
    st.subheader("📚 Formação Acadêmica")
    st.markdown(
        """
        - **Bacharelado em Engenharia de Software** — FIAP X (2024 – 2028)  
        - **Cursos online relevantes:** Python, SQL, React, Estatística Aplicada  
        """
    )

    st.write("")  # espaço

    # Certificações
    st.subheader("📑 Certificações")
    st.markdown(
        """
        - Front-End - Alura 
        - Nano Courses - FIAP
        """
    )
