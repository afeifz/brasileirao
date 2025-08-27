import streamlit as st

st.set_page_config(page_title="Skills", layout="wide")

# Título da página
st.title("🛠️ Skills")

# Espaço centralizado
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Hard Skills
    st.subheader("💻 Hard Skills")
    st.markdown(
        """
        - **Linguagens de Programação:** Python, SQL, R  
        - **Bibliotecas/Data Science:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn  
        - **Dashboards/BI:** Streamlit, Power BI, Tableau  
        - **Banco de Dados:** MySQL, PostgreSQL  
        - **Outros:** Git, Excel Avançado, APIs REST  
        """
    )

    st.write("")  # espaço

    # Soft Skills
    st.subheader("🤝 Soft Skills")
    st.markdown(
        """
        - Comunicação clara e objetiva  
        - Trabalho em equipe e colaboração  
        - Resolução de problemas  
        - Pensamento analítico e crítico  
        - Aprendizado contínuo e adaptabilidade  
        """
    )

    st.write("")  # espaço

    # Idiomas
    st.subheader("🌍 Idiomas")
    st.markdown(
        """
        - Português — Nativo  
        - Inglês — Intermediário/Avançado  
        - Espanhol — Básico  
        """
    )
