import streamlit as st
from deriv_ws import iniciar_conexao
from estrategias.predador_de_tendencia import executar_predador_tendencia

st.title("Robô Predador de Tendência - Deriv")
token = st.text_input("Token da API", type="password")
stake = st.number_input("Stake inicial", min_value=0.35, value=1.00)
stop_loss = st.number_input("Limite de perda (stop loss)", value=10.0)
stop_gain = st.number_input("Meta de lucro (stop gain)", value=20.0)
fator_martingale = st.number_input("Fator Martingale", value=2.0)

status_box = st.empty()

if st.button("Iniciar robô"):
    if token:
        status_box.info("🔄 Iniciando conexão com a Deriv...")
        iniciar_conexao(token, stake, stop_loss, stop_gain, fator_martingale, executar_predador_tendencia, status_box)
    else:
        st.warning("⚠️ Por favor, insira seu token da API para continuar.")