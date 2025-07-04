import streamlit as st
import websocket, json, threading, time

class DerivBot:
    def __init__(self, token, symbol, stake, tp, sl, martingale, multiplier, max_losses):
        self.token = token
        self.symbol = symbol
        self.stake = stake
        self.initial_stake = stake
        self.tp = tp
        self.sl = sl
        self.martingale = martingale
        self.multiplier = multiplier
        self.max_losses = max_losses

        self.profit = 0
        self.balance = 0
        self.wins = 0
        self.losses = 0
        self.consec_losses = 0
        self.digits = []
        self.running = True
        self.waiting_result = False
        self.connected = False
        self.last_error = ""
        self.account_id = ""

        self.ws = websocket.WebSocketApp("wss://ws.derivws.com/websockets/v3",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def on_open(self, ws):
        ws.send(json.dumps({"authorize": self.token}))

    def on_message(self, ws, message):
        data = json.loads(message)

        if 'error' in data:
            self.running = False
            self.last_error = data['error']['message']
            return

        msg_type = data.get("msg_type")

        if msg_type == "authorize":
            self.account_id = data["authorize"]["loginid"]
            self.balance = float(data["authorize"]["balance"])
            self.connected = True
            ws.send(json.dumps({"ticks": self.symbol}))

        elif msg_type == "tick":
            digit = int(data["tick"]["quote"][-1])
            self.digits.append(digit)
            if len(self.digits) > 15:
                self.digits.pop(0)
            if len(self.digits) == 15 and not self.waiting_result and self.running:
                self.analyze_and_trade()

        elif msg_type == "buy":
            self.contract_id = data["buy"]["contract_id"]
            self.waiting_result = True

        elif msg_type == "proposal_open_contract":
            if data["proposal_open_contract"]["is_sold"]:
                profit = float(data["proposal_open_contract"]["profit"])
                self.balance += profit
                self.profit += profit

                if profit > 0:
                    self.wins += 1
                    self.consec_losses = 0
                    self.stake = self.initial_stake
                else:
                    self.losses += 1
                    self.consec_losses += 1
                    if self.martingale:
                        self.stake *= self.multiplier

                self.waiting_result = False
                self.check_profit_and_continue()

    def analyze_and_trade(self):
        over = sum(1 for d in self.digits if d > 4)
        contract_type = "DIGITUNDER" if over > 7 else "DIGITOVER"
        contract = {
            "buy": 1,
            "price": round(self.stake, 2),
            "parameters": {
                "amount": round(self.stake, 2),
                "basis": "stake",
                "contract_type": contract_type,
                "currency": "USD",
                "duration": 1,
                "duration_unit": "t",
                "symbol": self.symbol
            },
            "passthrough": {"ref": "tickbot"}
        }
        self.ws.send(json.dumps(contract))

    def check_profit_and_continue(self):
        if self.profit >= self.tp or self.profit <= -self.sl or self.consec_losses >= self.max_losses:
            self.running = False

    def on_error(self, ws, error):
        self.last_error = str(error)

    def on_close(self, ws, close_status_code, close_msg):
        self.connected = False

    def run(self):
        thread = threading.Thread(target=self.ws.run_forever)
        thread.start()

    def display_status(self):
        if self.last_error:
            st.error(f"Erro: {self.last_error}")
        elif not self.connected:
            st.warning("Conectando...")
        else:
            st.success(f"Conectado: {self.account_id}")
            st.info(f"Saldo: ${self.balance:.2f}")
            st.info(f"Lucro: ${self.profit:.2f}")
            st.info(f"Wins: {self.wins} | Losses: {self.losses} | Consecutivas: {self.consec_losses}")
            st.info(f"Próximo valor de entrada: ${self.stake:.2f}")
            st.info("Últimos dígitos: " + str(self.digits))