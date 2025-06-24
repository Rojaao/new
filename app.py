
import streamlit as st
from deriv_ws import iniciar_conexao
from estrategias.predador_tendencia import executar_estrategia

st.title("🤖 Robô Deriv - Predador de Tendência")

token = st.text_input("🔐 Token da API da Deriv", type="password")
stake = st.number_input("💵 Stake Inicial", value=1.0)
stop_gain = st.number_input("📈 Stop Gain", value=10.0)
stop_loss = st.number_input("📉 Stop Loss", value=10.0)
martingale = st.checkbox("🎯 Usar Martingale", value=True)
fator_martingale = st.number_input("🔁 Fator Martingale", value=2.0)
btn_iniciar = st.button("🚀 Iniciar Robô")

log_area = st.empty()

if btn_iniciar and token:
    log_area.markdown("⏳ Conectando à Deriv...")
    iniciar_conexao(token, stake, stop_gain, stop_loss, martingale, fator_martingale, executar_estrategia, log_area)
