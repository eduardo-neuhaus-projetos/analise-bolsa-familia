# 📊 Análise do Bolsa Família por Município e UF

Dashboard interativo da distribuição do Bolsa Família por município e UF, 
utilizando dados oficiais do Governo Federal e do IBGE.

---

## 🎯 Sobre o Projeto

Este projeto analisa a **distribuição do Bolsa Família** em todos os 
municípios brasileiros, cruzando os dados de pagamentos do Portal da 
Transparência com as estimativas populacionais do IBGE.

O objetivo é permitir que **qualquer pessoa** possa explorar os dados de forma simples e 
visual, identificando padrões regionais, cobertura do programa e 
valores médios por beneficiário.

### 🔍 Principais Insights

- **18,7 milhões** de beneficiários atendidos em agosto/2026
- **R$ 12,7 bilhões** pagos no mês
- **8,79%** da população brasileira é atendida pelo programa
- Estados do Nordeste concentram a maior cobertura proporcional

---

## 🚀 Como Acessar

O dashboard está publicado e pode ser acessado publicamente em:

🔗 **[analise-bolsa-familia.streamlit.app](https://analise-bolsa-familia.streamlit.app)** _(substitua com sua URL)_

---

## ✨ Funcionalidades

- 🔎 **Filtros** por UF e Município
- 📈 **4 KPIs principais**: valor total pago, beneficiários, valor médio 
  e cobertura populacional
- 📋 **Tabela interativa** com dois modos de exibição:
  - **Formatado (BR)**: valores no padrão brasileiro (R$ 1.234,56)
  - **Ordenável**: Possibilita a ordenação correta clicando nos cabeçalhos da tabela
- 🎨 **Interface personalizada** com as cores do Brasil

---

## 🛠️ Stack Tecnológico

| Ferramenta | Uso |
|------------|-----|
| **Python 3.10+** | Linguagem principal |
| **Pandas** | Manipulação e limpeza dos dados |
| **Streamlit** | Construção do dashboard web |
| **Plotly** | (Futuras visualizações) |
| **PyArrow** | Leitura/escrita do formato Parquet |
| **DeepSeek** | Para extrair as sintaxes de python e streamlit e insights para apresentação |

---

## **DSA** Projeto base de apoio

Esse projeto foi concebido com base no curso gratuito realizado na DSA - [https://www.datascienceacademy.com.br/home](https://www.datascienceacademy.com.br/course/fundamentos-de-linguagem-python-do-basico-a-aplicacoes-de-ia) Capítulo 16.

---

## 📊 Fonte dos Dados

Os dados brutos **não estão incluídos no repositório** devido ao tamanho 
(~2 GB). Eles estão disponíveis gratuitamente nos portais oficiais:

### 1. Bolsa Família (Pagamentos)
- **Fonte:** [Portal da Transparência](https://portaldatransparencia.gov.br/download-de-dados/bolsa-familia-pagamentos)
- **Período:** Agosto/2026
- **Formato:** CSV

### 2. População por Município (IBGE)
- **Fonte:** [IBGE - SIDRA Tabela 6579](https://sidra.ibge.gov.br/tabela/6579)
- **Ano:** 2026
- **Formato:** CSV

---

## 🔄 Como Reproduzir Localmente

### Pré-requisitos
- Python 3.10 ou superior
- Git

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/eduardo-neuhaus-projetos/analise-bolsa-familia.git
cd analise-bolsa-familia

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# 3. Instale as dependências
requirements.txt

# 4. Execute o app
streamlit run App_BF.py
