import streamlit as st
from deriv_bot import DerivBot

st.set_page_config(page_title="Deriv Tick Bot", layout="centered")
st.title("🤖 Deriv Tick Bot - Digit Over/Under 4 com Martingale")

if 'bot' not in st.session_state:
    st.session_state.bot = None

token = st.text_input("🔑 Token da API Deriv", type="password")
symbol = st.selectbox("📈 Índice de Volatilidade", ["R_100", "R_75", "R_50", "R_25"])
stake = st.number_input("💰 Valor Inicial da Entrada", min_value=0.35, value=1.00, step=0.01)
take_profit = st.number_input("📈 Ganho Máximo Permitido", min_value=1.0, value=10.0, step=0.5)
stop_loss = st.number_input("📉 Perda Máxima Permitida", min_value=1.0, value=10.0, step=0.5)
martingale = st.checkbox("🔁 Ativar Martingale", value=True)
multiplier = st.number_input("🔢 Multiplicador de Martingale", min_value=1.0, value=2.0, step=0.1)
max_consec_losses = st.number_input("❌ Limite de Perdas Consecutivas", min_value=1, value=3, step=1)

if st.button("🚀 Iniciar Robô"):
    if token:
        st.session_state.bot = DerivBot(token, symbol, stake, take_profit, stop_loss, martingale, multiplier, max_consec_losses)
        st.session_state.bot.run()
    else:
        st.error("Token da API é obrigatório.")

if st.session_state.bot:
    st.session_state.bot.display_status()