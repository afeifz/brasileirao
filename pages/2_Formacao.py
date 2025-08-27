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
        - **Bacharelado em [Seu Curso]** — Universidade X (Ano início – Ano fim)  
        - **Curso Técnico em [Área]** — Instituição Y (Ano início – Ano fim)  
        - **Cursos online relevantes:** Python, SQL, Análise de Dados, Estatística Aplicada  
        """
    )

    st.write("")  # espaço

    # Certificações
    st.subheader("📑 Certificações")
    st.markdown(
        """
        - Certificação X — Instituição A (Ano)  
        - Certificação Y — Instituição B (Ano)  
        """
    )

    st.write("")  # espaço

    # Experiência Profissional
    st.subheader("💼 Experiência Profissional")
    st.markdown(
        """
        - **Cargo 1** — Empresa A (Ano início – Ano fim)  
          Principais atividades: análise de dados, criação de dashboards e relatórios.  

        - **Cargo 2** — Empresa B (Ano início – Ano fim)  
          Principais atividades: extração e tratamento de dados, automação em Python.  

        - **Estágios/Projetos:** desenvolvimento de scripts para ETL e dashboards em Streamlit.  
        """
    )
