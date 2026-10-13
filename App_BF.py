# Apresentação dos resultados com streamlit (usando modelo apresentado no curso da DSA e adaptando para esse fim)

# Importa bibliotecas de visualização e web app
import plotly.express as px  # Para criação de gráficos interativos
import streamlit as st       # A biblioteca principal para criar a Data App
import pandas as pd

# Configuração Inicial da Aplicação Streamlit
st.set_page_config(
    page_title="Análise Novo Bolsa Família",  # Título que aparece na aba do navegador
    page_icon=":bar_chart:",                  # Ícone (emoji) que aparece na aba do navegador
    layout="wide",                            # Define o layout da página para usar a largura total da tela
    initial_sidebar_state="expanded",         # Garante que a sidebar (menu lateral) comece aberta
)

# Função para mascarar valores em reais
def fmt_moeda(valor, casas=2):
    """
    Formata um número para o padrão monetário brasileiro.
    Ex.: 1234.56 → 'R$ 1.234,56'
    """
    formatado = f"{valor:,.{casas}f}"
    return formatado.replace(',', 'X').replace('.', ',').replace('X', '.')

# Função para mascarar as quantidades como numeros
def fmt_numero(valor, casas=0):
    """
    Formata um número inteiro no padrão brasileiro.
    Ex.: 18778305 → '18.778.305'
    """
    formatado = f"{valor:,.{casas}f}"
    return formatado.replace(',', '.').replace('.', ',') if casas > 0 else formatado.replace(',', '.')

# Função com os filtros na barra lateral
def dsa_filtros_sidebar(df_corrente_final):

    """
    Cria todos os widgets da sidebar (menu lateral).
    1. Exibe o banner da DSA.
    2. Cria os filtros de data, região, categoria e produto.
    3. Aplica os filtros ao DataFrame.
    4. Retorna o DataFrame filtrado.
    
    Parâmetros:
    df (pd.DataFrame): O DataFrame original completo (antes dos filtros).
    """
    
    # --- Banner da Sidebar ---
    # 'st.sidebar' ancora qualquer elemento streamlit na barra lateral
    # 'markdown' renderiza texto formatado.
    # 'unsafe_allow_html=True' é necessário para renderizar o bloco HTML/CSS customizado
    st.sidebar.markdown(
        """
        <div style="background-color:#00CC96; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px;">
            <h3 style="color:white; margin:0; font-weight:bold;">Análise do bolsa família por Município e UF</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


    # Adiciona um cabeçalho para a seção de filtros
    st.sidebar.header("🔍 Filtros")
    
    # --- Filtros de Seleção Única (Selectbox) ---
    
    # Filtro de UF
    # 1. Pega todos os valores únicos da coluna 'UF'
    # 2. 'sorted()' coloca em ordem alfabética para o menu
    all_uf = sorted(df_corrente_final["UF"].unique())
    
    # 3. Cria o widget com 'index=None' (sem seleção padrão)
    selected_uf = st.sidebar.selectbox(
        "UF",
        all_uf,
        index=None,
        placeholder="Selecione uma UF..."
    )
    
    # Filtro de Município (cascata: depende da UF escolhida)
    if selected_uf:
        municipios_da_uf = sorted(
            df_corrente_final[df_corrente_final["UF"] == selected_uf]["NMMUNICIPIO"].unique()
        )
        selected_municipio = st.sidebar.selectbox(
            "Município",
            municipios_da_uf,
            index=None,
            placeholder="Selecione um município..."
        )
    else:
        selected_municipio = None
        st.sidebar.info("Selecione uma UF para ver os municípios")

    # --- Lógica de Aplicação dos Filtros ---
    
    # Aplica a filtragem no DataFrame principal usando boolean indexing do Pandas
    df_dsa_filtrado = df_corrente_final.copy()

    # Aplica filtro de UF (se houver)
    if selected_uf:
        df_dsa_filtrado = df_dsa_filtrado[df_dsa_filtrado["UF"] == selected_uf]

    # Aplica filtro de Município (se houver)
    if selected_municipio:
        df_dsa_filtrado = df_dsa_filtrado[df_dsa_filtrado["NMMUNICIPIO"] == selected_municipio]

    # Feedback visual de quantos itens foram filtrados
    st.sidebar.markdown(f"**{len(df_dsa_filtrado):,}** municípios encontrados")
    
    # --- Rodapé da Sidebar ---
    
    # Adiciona uma linha horizontal para separar os filtros do rodapé
    st.sidebar.markdown("---")

    # Cria um "expander" para informações de suporte
    # 'expanded=False' garante que ele comece fechado
    with st.sidebar.expander("Dados obtidos do portal de transparência e Sidra", expanded = False):
        st.write("https://portaldatransparencia.gov.br/download-de-dados/novo-bolsa-familia e https://sidra.ibge.gov.br/tabela/6579")
    
    # Adiciona uma legenda de rodapé com 'st.sidebar.caption'
    st.sidebar.caption("Dashboard Desenvolvido com base no Curso Gratuito de Python da Data Science Academy - DSA")

    # Retorna o DataFrame recém-filtrado para ser usado no corpo principal da página
    return df_dsa_filtrado

# Função para os KPIs do Bolsa Família
def dsa_renderiza_cards_kpis(df):
    """
    Calcula e exibe os 4 principais KPIs do Bolsa Família em cards estilizados.
    
    Utiliza o DataFrame JÁ FILTRADO para fazer os cálculos.
    
    Parâmetros:
    df (pd.DataFrame): O DataFrame filtrado pela sidebar.
    
    Retorna:
    (tuple): Tupla com (total_pago, total_beneficiarios, valor_medio, cobertura)
    """
    
    # --- 1. Cálculos dos KPIs ---
    
    # Total pago no período filtrado
    total_pago = df["VALOR_TOTAL"].sum()
    
    # Total de beneficiários (soma dos únicos por município)
    total_beneficiarios = df["QTD_BENEFICIARIOS"].sum()
    
    # População total dos municípios (NaN são ignorados pelo sum)
    populacao_total = df["QTPOPULACAO"].sum()
    
    # Valor médio por beneficiário (ponderado)
    valor_medio = total_pago / total_beneficiarios if total_beneficiarios > 0 else 0
    
    # Cobertura: % da população atendida (ponderada)
    cobertura = total_beneficiarios / populacao_total * 100 if populacao_total > 0 else 0
    
    # --- 2. Criação do Layout ---
    
    c1, c2, c3, c4 = st.columns(4)
    
    # --- 3. Renderização dos Cards ---
    
    # Card 1: Valor Total Pago
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Valor Total Pago</h3>
            <h2>R$ {fmt_moeda(total_pago, casas=0)}</h2>
        </div>
        """, unsafe_allow_html=True)

    # Card 2: Beneficiários
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Beneficiários</h3>
            <h2>{fmt_numero(total_beneficiarios)}</h2>
        </div>
        """, unsafe_allow_html=True)

    # Card 3: Valor Médio por Beneficiário
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Média parcela Beneficiário</h3>
            <h2>R$ {fmt_moeda(valor_medio)}</h2>
        </div>
        """, unsafe_allow_html=True)

    # Card 4: Cobertura Populacional
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Cobertura Populacional</h3>
            <h2>{fmt_numero(cobertura, casas=2)}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Retorna os valores para uso externo (ex.: geração de PDF)
    return total_pago, total_beneficiarios, valor_medio, cobertura

# Função para customização da interface com CSS usando as cores do Brasil
def dsa_set_custom_theme():

    """
    Define e injeta CSS customizado no app Streamlit.
    Usa a paleta de cores do Brasil (verde, amarelo, azul) para
    contextualizar o tema do dashboard do Bolsa Família.
    """

    # --- 1. Definição das Cores do Tema (Paleta Brasil) ---

    brasil_green = "#009739"    # Verde bandeira (cor principal)
    brasil_yellow = "#FFDF00"   # Amarelo bandeira (destaque)
    brasil_blue = "#012169"     # Azul bandeira (fundo escuro)
    brasil_white = "#FFFFFF"    # Branco (texto)
    brasil_green_light = "#00B84C"  # Verde mais claro (hover)
    dark_text = "#0A2540"       # Texto escuro para usar sobre o amarelo

    # --- 2. Criação do Bloco de Estilo CSS ---

    css = f"""
    <style>

        /* --- Estilização dos Cards de KPI --- */
        .metric-card {{
            background: linear-gradient(135deg, {brasil_blue} 0%, #0A3D62 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid {brasil_green};
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.4);
            text-align: center;
            margin-bottom: 10px;
            transition: transform 0.2s ease;

            min-height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            
        }}

        /* Efeito ao passar o mouse no card */
        .metric-card:hover {{
            transform: translateY(-3px);
            border-left: 5px solid {brasil_yellow};
        }}

        /* Estilo do subtítulo do card (ex: "Valor Total Pago") */
        .metric-card h3 {{
            margin: 0;
            font-size: 1.1rem;
            color: {brasil_yellow};
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        /* Estilo do valor principal do card */
        .metric-card h2 {{
            margin: 10px 0 0 0;
            font-size: 1.5rem;
            color: {brasil_white};
            font-weight: bold;
        }}

        /* Estilo do texto 'delta' (ex: "Mês corrente") */
        .metric-card .delta {{
            font-size: 0.85rem;
            color: #B0C4DE;
            margin-top: 8px;
        }}

        /* --- Estilização dos Filtros da Sidebar --- */
        /* Aplica destaque verde na borda dos selectbox */
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
            border: 1px solid {brasil_green} !important;
            border-radius: 6px !important;
        }}

        /* Ao passar o mouse / focar, a borda vira amarela */
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {{
            border: 2px solid {brasil_yellow} !important;
        }}

        /* --- Estilização do Cabeçalho da Sidebar --- */
        [data-testid="stSidebar"] h2 {{
            color: {brasil_green} !important;
            font-weight: bold !important;
        }}

        /* --- Estilização do Cabeçalho Principal --- */
        h1 {{
            color: {brasil_green} !important;
            border-bottom: 3px solid {brasil_yellow};
            padding-bottom: 10px;
        }}

        /* --- Destaque para o subheader --- */
        h2 {{
            color: {brasil_white} !important;
        }}

        /* --- Estilização das Métricas Nativas (st.metric) --- */
        [data-testid="stMetricValue"] {{
            color: {brasil_green} !important;
            font-weight: bold !important;
        }}

        /* --- Estilização dos Botões --- */
        .stButton > button {{
            background-color: {brasil_green} !important;
            color: {brasil_white} !important;
            border: none !important;
            border-radius: 6px !important;
            font-weight: bold !important;
            transition: background-color 0.2s ease;
        }}

        .stButton > button:hover {{
            background-color: {brasil_green_light} !important;
            color: {brasil_yellow} !important;
        }}

        /* --- Estilização dos DataFrames --- */
        [data-testid="stDataFrame"] {{
            border: 1px solid {brasil_green} !important;
            border-radius: 6px !important;
        }}

        /* --- Estilização dos Inputs de Texto --- */
        input[type="text"] {{
            border: 1px solid {brasil_green} !important;
            border-radius: 6px !important;
        }}

        /* --- Faixa decorativa no topo do app (opcional) --- */
        .brasil-bar {{
            height: 5px;
            background: linear-gradient(90deg, 
                {brasil_green} 0%, 
                {brasil_green} 33%, 
                {brasil_yellow} 33%, 
                {brasil_yellow} 66%, 
                {brasil_blue} 66%, 
                {brasil_blue} 100%
            );
            border-radius: 3px;
            margin-bottom: 15px;
        }}

        /* --- Alinhamento das colunas do Streamlit (mesma altura) --- */
        [data-testid="stHorizontalBlock"] {{
            align-items: stretch !important;
        }}

        [data-testid="column"] {{
            display: flex;
            flex-direction: column;
        }}

    </style>
    """

    # --- 3. Injeção do CSS na Página ---

    st.markdown(css, unsafe_allow_html=True)

st.set_page_config(page_title="Bolsa Família", page_icon="🇧🇷", layout="wide")

@st.cache_data
def carregar_dados():
    """Lê o arquivo salvo em parquet!"""
    return pd.read_parquet("df_corrente_final.parquet")

def main():
    dsa_set_custom_theme()
    st.title("Bolsa Família — Agosto de 2026")
    
    df = carregar_dados()
    df_filtrado = dsa_filtros_sidebar(df)
    dsa_renderiza_cards_kpis(df_filtrado)
    #st.dataframe(df_filtrado)

# ============================================================
# TABELA DE MUNICÍPIOS (com toggle de visualização)
# ============================================================

    st.subheader("📋 Dados por município")
    
    # --- Seletor de modo de exibição ---
    modo_visualizacao = st.radio(
        "Modo de exibição",
        ["📊 Formatado (BR)", "🔢 Ordenável (numérico)"],
        horizontal=True,
        label_visibility="collapsed",
        help="Formatado: valores no padrão brasileiro (R$ 1.234,56). "
             "Ordenável: permite clicar nos cabeçalhos para ordenar, mas usa o padrão americano."
    )
    
    # --- Visão 1: Formatada (padrão brasileiro) ---
    if modo_visualizacao == "📊 Formatado (BR)":
    
        # Cria cópia só com as colunas desejadas
        df_exibicao = df_filtrado[[
            'UF',
            'NMMUNICIPIO',
            'QTD_BENEFICIARIOS',
            'QTPOPULACAO',
            'VALOR_TOTAL'
        ]].copy()
    
        # Formata as colunas com as funções BR
        df_exibicao['QTD_BENEFICIARIOS'] = df_exibicao['QTD_BENEFICIARIOS'].apply(fmt_numero)
        df_exibicao['QTPOPULACAO'] = df_exibicao['QTPOPULACAO'].apply(fmt_numero)
        df_exibicao['VALOR_TOTAL'] = df_exibicao['VALOR_TOTAL'].apply(fmt_moeda)
    
        # Renomeia as colunas para exibição
        df_exibicao = df_exibicao.rename(columns={
            'UF': 'Estado',
            'NMMUNICIPIO': 'Município',
            'QTD_BENEFICIARIOS': 'Beneficiários',
            'QTPOPULACAO': 'População',
            'VALOR_TOTAL': 'Valor Total',
        })
    
        # Exibe
        st.dataframe(
            df_exibicao,
            use_container_width=True,
            hide_index=True,
            height=500
        )
    
# --- Visão 2: Ordenável (numérica) ---
    else:
    
        # Seleciona só as colunas desejadas
        df_ordenavel = df_filtrado[[
            'UF',
            'NMMUNICIPIO',
            'QTD_BENEFICIARIOS',
            'QTPOPULACAO',
            'VALOR_TOTAL'
        ]].copy()
    
        st.dataframe(
            df_ordenavel,
            column_config={
                "UF": "Estado",
                "NMMUNICIPIO": "Município",
                "QTD_BENEFICIARIOS": st.column_config.NumberColumn(
                    "Beneficiários", format="%d"
                ),
                "QTPOPULACAO": st.column_config.NumberColumn(
                    "População", format="%d"
                ),
                "VALOR_TOTAL": st.column_config.NumberColumn(
                    "Valor Total", format="R$ %.2f"
                ),
            },
            use_container_width=True,
            hide_index=True,
            height=500
        )
if __name__ == "__main__":
    main()
    