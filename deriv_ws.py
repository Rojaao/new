import websocket
import threading
import json

def iniciar_conexao(token, stake, stop_loss, stop_gain, fator_martingale, estrategia_func, status_box):
    ws_url = "wss://ws.derivws.com/websockets/v3?app_id=1089"

    def on_open(ws):
        auth_msg = json.dumps({ "authorize": token })
        ws.send(auth_msg)

    def on_message(ws, message):
        data = json.loads(message)
        if 'msg_type' in data:
            if data['msg_type'] == 'authorize':
                status_box.success("✅ Conectado com sucesso!")
                estrategia_func(ws, stake, stop_loss, stop_gain, fator_martingale)
            elif data['msg_type'] == 'error':
                status_box.error("❌ Erro: " + data['error'].get('message', 'Erro desconhecido'))

    def on_error(ws, error):
        status_box.error(f"❌ Erro na conexão: {error}")

    def on_close(ws, *args):
        status_box.info("🔌 Conexão encerrada.")

    ws_app = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    t = threading.Thread(target=ws_app.run_forever)
    t.start()