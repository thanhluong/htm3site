import * as dotenv from "dotenv";
dotenv.config();

import { WebSocketServer } from "ws";

const WS_PORT = process.env.WS_PORT || 4443;
const SECRET_KEY = process.env.SECRET_KEY || "secret";

const wss = new WebSocketServer({ port: WS_PORT });

console.log(`WS Server is listening on port ${WS_PORT}`);

wss.broadcast = function broadcast(msg) {
  wss.clients.forEach(function each(client) {
    client.send(msg);
  });
};
