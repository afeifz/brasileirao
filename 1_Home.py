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
        Analista de Dados com experiência em Python, ETL e visualização. 
        Gosto de transformar dados em insights acionáveis para negócio.
        """
    )

    st.write("")  # espaço

    # Objetivo profissional
    st.subheader("🎯 Objetivo profissional")
    st.markdown(
        """
        Atuar como **Analista/Cientista de Dados**, desenvolvendo análises estatísticas
        e dashboards interativos que apoiem decisões estratégicas.  
        """
    )

    st.write("")  # espaço

    # Contato/resumo rápido — simples e centralizado
    st.markdown("**Contato:** seu-email@exemplo.com • [LinkedIn](https://linkedin.com) • [GitHub](https://github.com)")  # TODO: editar

# Mensagem orientando o avaliador / usuário
st.info("Navegue pelas abas para ver Formação, Skills e a Análise de Dados")
