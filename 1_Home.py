import streamlit as st

# Configuração simples da página
st.set_page_config(page_title="Dashboard - Home", layout="wide")

st.title("⚽ Campeonato Brasileiro - Dashboard de Gols")


col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.header("Olá, sou Mohamed")  
    st.write("")  # espaço

    #
    st.markdown(
        """
        **Resumo profissional:**  
        Estudante de T.I com experiência em Python, Front-End e Redes. 
        Gosto de construir aprendizado na área.
        """
    )

    st.write("")  

    # Objetivo profissional
    st.subheader("🎯 Objetivo profissional")
    st.markdown(
        """
        Atuar como **Profissional de T.I**, desenvolvendo soluções
        e evoluir na área.  
        """
    )

    st.write("") 

    # Contato/resumo rápido — simples e centralizado
    st.markdown("**Contato:** afeifz@gmail.com • [LinkedIn](https://linkedin.com/in/mohamedafif) • [GitHub](https://github.com/afeifz)")  

# Mensagem orientando o avaliador / usuário
st.info("Navegue pelas abas para ver Formação, Skills e a Análise de Dados")
