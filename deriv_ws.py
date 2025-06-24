import websocket
import threading
import json

def iniciar_conexao(token, estrategia, stake, martingale, fator_marti, stop_gain, stop_loss, delay):
    def on_message(ws, message):
        print("📩 Mensagem recebida:", message)

    def on_open(ws):
        print("🔌 Conectado!")
        auth_msg = json.dumps({ "authorize": token })
        ws.send(auth_msg)

    def on_error(ws, error):
        print("❌ Erro:", error)

    def on_close(ws, close_status_code, close_msg):
        print("🔌 Conexão encerrada.")

    ws = websocket.WebSocketApp(
        "wss://ws.derivws.com/websockets/v3",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()