from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import eventlet
import os

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'neonsecret'
socketio = SocketIO(app, cors_allowed_origins="*")

users = {}
servers = {}
friend_requests = {}

def validar_nick(nick):
    if not nick:
        return False

    if nick.endswith("jr"):
        return 1 <= len(nick) <= 50
    return 1 <= len(nick) <= 15

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("login")
def login(nick):
    if not validar_nick(nick):
        emit("erro", "Nick inválido!")
        return

    users[request.sid] = nick
    friend_requests[nick] = []

    emit("logado", nick)
    emit("listaServidores", list(servers.keys()))

@socketio.on("criarServidor")
def criar_servidor(nome):
    if nome not in servers:
        servers[nome] = []

    emit("listaServidores", list(servers.keys()), broadcast=True)

@socketio.on("entrarServidor")
def entrar_servidor(nome):
    if nome in servers:
        join_room(nome)
        emit("entrouServidor", nome)

@socketio.on("mensagem")
def mensagem(data):
    server_nome = data.get("serverNome")
    msg = data.get("mensagem")

    if server_nome and msg:
        emit("novaMensagem", {
            "user": users.get(request.sid),
            "mensagem": msg
        }, room=server_nome)

@socketio.on("pedidoAmizade")
def pedido_amizade(destino):
    remetente = users.get(request.sid)
    if destino in friend_requests:
        friend_requests[destino].append(remetente)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
