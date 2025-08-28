# pages/4_Analise_de_Dados.py
import streamlit as st
import pandas as pd
import numpy as np
import re
import math
import matplotlib.pyplot as plt

# tente usar scipy quando disponível para testes/t-quantis; se não, uso aproximações normais
try:
    from scipy import stats as _scipy_stats
    SCIPY_AVAILABLE = True
except Exception:
    _scipy_stats = None
    SCIPY_AVAILABLE = False

st.set_page_config(page_title="📊 Análise de Dados", layout="wide")
st.title("📊 Análise de Dados — Campeonato Brasileiro (Gols)")

# -------------------------
# Carregamento e limpeza
# -------------------------
CSV_PATH = "campeonato-brasileiro-gols.csv"

def load_and_clean(path):
    try:
        # ler como string para evitar conversões automáticas que quebram
        raw = pd.read_csv(path, dtype=str)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo CSV em `{path}`: {e}")
        st.stop()

    df = raw.copy()
    # normaliza nomes
    df.columns = df.columns.str.strip().str.lower()

    # renomear variações comuns para nomes padronizados
    rename_map = {}
    for c in df.columns:
        if c == "rodata":      
            rename_map[c] = "rodada"
        # possíveis variações
        if c.replace(" ", "").replace("-", "").replace("_", "") in ["partidaid", "idpartida"]:
            rename_map[c] = "partida_id"
        if "partida" == c:
            rename_map[c] = "partida_id"
        if "clube" in c:
            rename_map[c] = "clube"
        if "atleta" in c:
            rename_map[c] = "atleta"
        if "minuto" in c:
            rename_map[c] = "minuto"

    df = df.rename(columns=rename_map)

    # --- converter minuto robustamente ---
    # ex.: "45+1" -> 46, "90+3" -> 93, "45" -> 45. Se não for possível, vira NaN.
    def parse_minuto(x):
        if pd.isna(x):
            return np.nan
        s = str(x).strip()
        # remover parênteses e espaços extras
        s = s.replace("(", "").replace(")", "").strip()

        # padrão simples com + (ex: 45+1)
        m = re.match(r"^\s*(\d+)\s*\+\s*(\d+)\s*$", s)
        if m:
            try:
                return int(m.group(1)) + int(m.group(2))
            except:
                return np.nan
        # padrão simples número
        m2 = re.match(r"^\s*(\d+)\s*$", s)
        if m2:
            return int(m2.group(1))

        # pegar primeiro número encontrado (fallback)
        m3 = re.search(r"(\d+)", s)
        if m3:
            return int(m3.group(1))

        return np.nan

    if "minuto" in df.columns:
        df["minuto"] = df["minuto"].apply(parse_minuto)
        # manter como float (para permitir NaN); quando necessário, convert to int
        df["minuto"] = pd.to_numeric(df["minuto"], errors="coerce")
    else:
        st.warning("Coluna 'minuto' não encontrada no CSV. Verifique o arquivo.")
        df["minuto"] = np.nan

    # converter rodada para numérico quando possível
    if "rodada" in df.columns:
        df["rodada"] = pd.to_numeric(df["rodada"], errors="coerce")
    else:
        st.warning("Coluna 'rodada' não encontrada. Verifique se existe 'rodata' no CSV (foi mapeado automaticamente).")

    # padronizar strings em clube/atleta
    if "clube" in df.columns:
        df["clube"] = df["clube"].astype(str).str.strip()
    if "atleta" in df.columns:
        df["atleta"] = df["atleta"].astype(str).str.strip()

    return df

# carregar e salvar em session_state para outras páginas reaproveitarem
if "data" not in st.session_state:
    df = load_and_clean(CSV_PATH)
    st.session_state["data"] = df
else:
    df = st.session_state["data"]


# -------------------------
# Abas (1,2,3)
# -------------------------
aba1, aba2, aba3 = st.tabs([
    "Apresentação dos Dados",
    "Estatísticas e Distribuições",
    "Intervalos de Confiança & Testes"
])

# -------------------------
# ABA 1 - Apresentação (critério 1)
# -------------------------
with aba1:
    st.header("Apresentação dos Dados e Tipos de Variáveis")
    st.markdown("""
    - Cada linha do dataset representa **um gol** marcado no Campeonato Brasileiro.  
    - **Colunas principais (padronizadas):**
      - `partida_id` — identificador da partida (Qualitativa nominal)
      - `rodada` — número da rodada (Qualitativa ordinal)
      - `clube` — clube que marcou (Qualitativa nominal)
      - `atleta` — jogador que marcou (Qualitativa nominal)  
      - `minuto` — minuto do gol (Quantitativa discreta)
    """)
    st.subheader("Pré-visualização")
    st.dataframe(df.head(10))

    st.subheader("Perguntas principais de análise")
    st.markdown("""
    1. Como os gols estão distribuídos ao longo das **rodadas**?  
    2. Quais **atletas** e **clubes** mais marcaram (ranking)?  
    3. Em que **momentos do jogo** (minutos) os gols ocorrem com maior frequência?  
    4. Há evidência estatística de que **mais gols ocorrem no 2º tempo** (minuto > 45) do que no 1º tempo?
    """)

# -------------------------
# ABA 2 - Estatísticas e distribuições (critério 2)
# -------------------------
with aba2:
    st.header("Medidas Centrais, Dispersão e Distribuições")

    df_min = df.dropna(subset=["minuto"]).copy()
    if len(df_min) == 0:
        st.warning("Não há dados válidos em 'minuto' para fazer análise. Verifique a limpeza.")
    else:
        # medidas
        media = df_min["minuto"].mean()
        mediana = df_min["minuto"].median()
        try:
            moda = int(df_min["minuto"].mode().iloc[0])
        except:
            moda = "N/A"
        desvio = df_min["minuto"].std()
        variancia = df_min["minuto"].var()

        c1, c2, c3 = st.columns(3)
        c1.metric("Média (minuto)", f"{media:.2f}")
        c2.metric("Mediana (minuto)", f"{mediana:.2f}")
        c3.metric("Moda (minuto)", f"{moda}")

        st.write(f"**Desvio padrão:** {desvio:.2f} — **Variância:** {variancia:.2f}")

        st.write("")
        st.info("Interpretação breve: média e mediana próximas indicam distribuição relativamente simétrica; a moda mostra minutos com maior concentração (ex: pênaltis, finais de tempo).")

        # Histograma
        st.subheader("Histograma dos minutos dos gols")
        fig, ax = plt.subplots(figsize=(10,4))
        ax.hist(df_min["minuto"], bins=20)
        ax.set_xlabel("Minuto do jogo")
        ax.set_ylabel("Quantidade de gols")
        ax.set_title("Distribuição dos gols ao longo dos minutos")
        st.pyplot(fig)

        # Boxplot
        st.subheader("Boxplot dos minutos dos gols")
        fig2, ax2 = plt.subplots(figsize=(8,2))
        ax2.boxplot(df_min["minuto"], vert=False)
        ax2.set_xlabel("Minuto do jogo")
        st.pyplot(fig2)

        # Estatísticas por rodada (gols por rodada)
        st.subheader("Gols por Rodada")
        if "rodada" in df.columns:
            gols_por_rodada = df_min.groupby("rodada").size().reset_index(name="total_gols").sort_values("rodada")
            st.line_chart(gols_por_rodada.set_index("rodada")["total_gols"])
            st.write(f"Média de gols por rodada: {gols_por_rodada['total_gols'].mean():.2f}")
            st.write(f"Desvio padrão por rodada: {gols_por_rodada['total_gols'].std():.2f}")
        else:
            st.warning("Coluna 'rodada' não disponível para calcular gols por rodada.")

        # Correlação (minuto vs rodada) - só faz sentido numérico
        st.subheader("Correlação entre 'minuto' e 'rodada' (Pearson)")
        if "rodada" in df.columns:
            corr = pd.DataFrame({"minuto": df_min["minuto"], "rodada": df_min["rodada"]}).dropna().corr().iloc[0,1]
            st.write(f"Coeficiente de correlação (Pearson) minuto x rodada: **{corr:.3f}**")
            st.caption("Correlação fraca é esperada — minuto do gol depende mais de dinâmica da partida que da rodada.")
        else:
            st.write("Rodada ausente → não é possível calcular correlação.")

        # Top artilheiros e clubes (rápido)
        st.subheader("Top Artilheiros (ranking)")
        artilheiros = df_min["atleta"].value_counts().reset_index()
        artilheiros.columns = ["atleta", "gols"]
        st.dataframe(artilheiros.head(10))

        st.subheader("Top Clubes (ranking)")
        clubes = df_min["clube"].value_counts().reset_index()
        clubes.columns = ["clube", "gols"]
        st.dataframe(clubes.head(10))

# -------------------------
# ABA 3 - Intervalos de Confiança e Testes (critério 3)
# -------------------------
with aba3:
    st.header("Intervalos de Confiança e Testes de Hipótese")

    df_min = df.dropna(subset=["minuto"]).copy()
    n = len(df_min)
    st.write(f"Amostra válida (minutos): n = {n}")

    if n == 0:
        st.warning("Sem dados de 'minuto' para calcular IC / testes.")
    else:
        # --- IC para a média do minuto (95%) ---
        mean_all = df_min["minuto"].mean()
        sd_all = df_min["minuto"].std(ddof=1)
        se_all = sd_all / math.sqrt(n)

        if SCIPY_AVAILABLE:
            t_crit = _scipy_stats.t.ppf(0.975, df=n-1)
        else:
            # aproximação normal quando scipy não disponível
            t_crit = 1.96

        ci_low = mean_all - t_crit * se_all
        ci_high = mean_all + t_crit * se_all

        st.subheader("Intervalo de Confiança (95%) para a média do minuto do gol")
        st.write(f"Média = {mean_all:.2f}")
        st.write(f"IC 95% ≈ [{ci_low:.2f}, {ci_high:.2f}] (usando t_crit = {t_crit:.3f})")

        st.write("---")

        # --- Teste: Existe evidência de que mais gols ocorrem no 2º tempo? (proporção) ---
        st.subheader("Teste de hipótese (proporção): mais gols no 2º tempo?")
        # Definir 2º tempo como minuto > 45
        n_second = (df_min["minuto"] > 45).sum()
        p_hat = n_second / n

        st.write(f"Quantidade de gols no 2º tempo: {n_second} / {n} → p̂ = {p_hat:.3f}")

        # Teste H0: p = 0.5  vs H1: p > 0.5 (mais gols no 2º tempo)
        # z = (p_hat - 0.5)/sqrt(0.5*0.5/n)
        denom = math.sqrt(0.5 * 0.5 / n)
        if denom == 0:
            st.warning("Amostra insuficiente para teste de proporção.")
        else:
            z_stat = (p_hat - 0.5) / denom
            # calculo p-valor usando normal cdf (one-sided)
            def normal_cdf(x):
                return 0.5 * (1 + math.erf(x / math.sqrt(2)))
            p_value_one_sided = 1 - normal_cdf(z_stat)

            st.write(f"Estatística z = {z_stat:.3f}")
            st.write(f"P-valor (one-sided, H1: p > 0.5) = {p_value_one_sided:.4f}")

            alpha = 0.05
            if p_value_one_sided < alpha:
                st.success("Resultado: Rejeitamos H0 a 5% → evidência de que há mais gols no 2º tempo.")
            else:
                st.info("Resultado: Não rejeitamos H0 a 5% → sem evidência suficiente de mais gols no 2º tempo.")

            # IC normal para proporção (aprox)
            z95 = 1.96 if not SCIPY_AVAILABLE else _scipy_stats.norm.ppf(0.975)
            se_p = math.sqrt(p_hat * (1 - p_hat) / n)
            ci_p_low = max(0, p_hat - z95 * se_p)
            ci_p_high = min(1, p_hat + z95 * se_p)
            st.write(f"IC 95% para p (aprox normal): [{ci_p_low:.3f}, {ci_p_high:.3f}]")

        st.write("---")

        # --- Teste t (Welch) comparando média dos minutos 1º tempo vs 2º tempo ---
        st.subheader("Teste de diferença de médias (1º tempo x 2º tempo) — Welch t-test")
        g1 = df_min[df_min["minuto"] <= 45]["minuto"]
        g2 = df_min[df_min["minuto"] > 45]["minuto"]
        n1 = len(g1)
        n2 = len(g2)

        st.write(f"n1 (1º tempo) = {n1} — n2 (2º tempo) = {n2}")

        if n1 < 2 or n2 < 2:
            st.warning("Amostras demasiado pequenas para realizar teste t com confiança.")
        else:
            mean1 = g1.mean()
            mean2 = g2.mean()
            sd1 = g1.std(ddof=1)
            sd2 = g2.std(ddof=1)
            se_diff = math.sqrt(sd1**2 / n1 + sd2**2 / n2)
            t_stat = (mean2 - mean1) / se_diff

            # graus de liberdade de Welch
            df_welch_num = (sd1**2 / n1 + sd2**2 / n2) ** 2
            df_welch_den = ( (sd1**4) / (n1**2 * (n1 - 1)) ) + ( (sd2**4) / (n2**2 * (n2 - 1)) )
            df_welch = df_welch_num / df_welch_den if df_welch_den != 0 else min(n1, n2) - 1

            # p-valor (one-sided: mean2 > mean1)
            if SCIPY_AVAILABLE:
                pval_one_sided = _scipy_stats.t.sf(t_stat, df=df_welch)  # survival function
                tcrit = _scipy_stats.t.ppf(0.975, df=df_welch)
            else:
                # aproximação normal para p-valor e tcrit
                pval_one_sided = 1 - (0.5 * (1 + math.erf(t_stat / math.sqrt(2))))
                tcrit = 1.96

            st.write(f"mean1 = {mean1:.2f} (1º tempo) — mean2 = {mean2:.2f} (2º tempo)")
            st.write(f"t (Welch) = {t_stat:.3f} — df ≈ {df_welch:.1f}")
            st.write(f"P-valor (one-sided, H1: mean2 > mean1) = {pval_one_sided:.4f}")

            if pval_one_sided < alpha:
                st.success("Resultado: Rejeitamos H0 a 5% → média de minuto no 2º tempo é maior que no 1º tempo.")
            else:
                st.info("Resultado: Não rejeitamos H0 a 5% → sem evidência suficiente de diferença significativa nas médias.")

            # IC para diferença de médias (mean2 - mean1) com tcrit (aprox)
            diff = mean2 - mean1
            ci_diff_low = diff - tcrit * se_diff
            ci_diff_high = diff + tcrit * se_diff
            st.write(f"IC 95% para (mean2 - mean1): [{ci_diff_low:.2f}, {ci_diff_high:.2f}] (tcrit ≈ {tcrit:.3f})")

    st.write("")

# fim do arquivo
