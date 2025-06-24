
import websocket, json, threading

def iniciar_conexao(token, stake, stop_gain, stop_loss, martingale, fator_martingale, estrategia, log_area):
    def on_open(ws):
        ws.send(json.dumps({"authorize": token}))

    def on_message(ws, message):
        data = json.loads(message)
        if "msg_type" in data and data["msg_type"] == "authorize":
            log_area.markdown("✅ Conectado à Deriv!")
            estrategia(ws, stake, stop_gain, stop_loss, martingale, fator_martingale, log_area)
        elif "error" in data:
            log_area.markdown(f"❌ Erro: {data['error']['message']}")

    def on_error(ws, error):
        log_area.markdown(f"❌ Erro na conexão: {error}")

    def on_close(ws, a, b):
        log_area.markdown("🔌 Conexão encerrada.")

    ws = websocket.WebSocketApp("wss://ws.binaryws.com/websockets/v3?app_id=1089",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    threading.Thread(target=ws.run_forever).start()
