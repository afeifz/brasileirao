import streamlit as st

# Configuração simples da página
st.set_page_config(page_title="Dashboard - Home", layout="wide")

# TÍTULO DO DASHBOARD (mantive o seu tema)
st.title("⚽ Campeonato Brasileiro - Dashboard de Gols")

# Espaço centralizado com 3 colunas; o conteúdo fica na coluna do meio
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.header("Olá — Mohamed")  # TODO: substitua pelo seu nome se quiser
    st.write("")  # espaço

    # Resumo profissional curto (2-3 linhas)
    st.markdown(
        """
        **Resumo profissional:**  
        Estudante de T.I com experiência em Python, Front-End e Redes. 
        Gosto de construir aprendizado na área.
        """
    )

    st.write("")  # espaço

    # Objetivo profissional
    st.subheader("🎯 Objetivo profissional")
    st.markdown(
        """
        Atuar como **Profissional de T.I**, desenvolvendo soluções
        e evoluir na área.  
        """
    )

    st.write("")  # espaço

    # Contato/resumo rápido — simples e centralizado
    st.markdown("**Contato:** afeifz@gmail.com • [LinkedIn](https://linkedin.com/in/mohamedafif) • [GitHub](https://github.com/afeifz)")  # TODO: editar

# Mensagem orientando o avaliador / usuário
st.info("Navegue pelas abas para ver Formação, Skills e a Análise de Dados")
