const socket = io();
let serverAtual = "";

function login() {
    const nick = document.getElementById("nick").value;
    socket.emit("login", nick);
}

socket.on("logado", () => {
    document.getElementById("login").style.display = "none";
    document.getElementById("app").style.display = "flex";
});

socket.on("erro", (msg) => {
    alert(msg);
});

function criarServidor() {
    const nome = document.getElementById("serverNome").value;
    socket.emit("criarServidor", nome);
}

socket.on("listaServidores", (lista) => {
    const div = document.getElementById("listaServidores");
    div.innerHTML = "";

    lista.forEach(nome => {
        const btn = document.createElement("button");
        btn.innerText = nome;
        btn.onclick = () => entrarServidor(nome);
        div.appendChild(btn);
    });
});

function entrarServidor(nome) {
    serverAtual = nome;
    socket.emit("entrarServidor", nome);
}

function enviarMensagem() {
    const mensagem = document.getElementById("mensagem").value;
    socket.emit("mensagem", {
        serverNome: serverAtual,
        mensagem: mensagem
    });
}

socket.on("novaMensagem", (data) => {
    const chat = document.getElementById("chat");
    chat.innerHTML += `<p><b>${data.user}:</b> ${data.mensagem}</p>`;
});

function enviarPedido() {
    const amigo = document.getElementById("amigo").value;
    socket.emit("pedidoAmizade", amigo);
}
