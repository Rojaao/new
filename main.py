import streamlit as st
from deriv_ws import iniciar_conexao
from estrategias import predador_de_tendencia, seis_em_sete_digit, zero_matador

def main():
    st.set_page_config(page_title="Robô Deriv Predador", layout="centered")
    st.title("🤖 Robô Deriv Predador")

    token = st.text_input("🎯 Token da API", type="password")
    estrategia = st.selectbox("🎯 Estratégia", ["Predador de Tendência", "6em7Digit", "0Matador"])
    stake = st.number_input("💰 Stake inicial", min_value=0.35, value=1.00, step=0.10)
    martingale = st.checkbox("🎲 Ativar Martingale", value=True)
    fator_marti = st.number_input("🎯 Fator de Martingale", min_value=1.0, value=2.0, step=0.1)
    stop_gain = st.number_input("🟢 Stop Gain", min_value=1.0, value=10.0, step=1.0)
    stop_loss = st.number_input("🔴 Stop Loss", min_value=1.0, value=10.0, step=1.0)
    delay = st.slider("⏱ Delay entre entradas (segundos)", 1, 60, 5)

    if st.button("🚀 Iniciar Robô"):
        st.success("Iniciando conexão com a Deriv...")
        iniciar_conexao(token, estrategia, stake, martingale, fator_marti, stop_gain, stop_loss, delay)