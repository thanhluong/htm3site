import { WebSocketServer } from "ws";

WS_PORT = process.env.WS_PORT || 4443;

const wss = new WebSocketServer({ port: WS_PORT });

wss.broadcast = function broadcast(msg) {
  wss.clients.forEach(function each(client) {
    console.log("client info:", client);
    client.send(msg);
  });
};
