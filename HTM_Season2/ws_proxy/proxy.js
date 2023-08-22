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

/*
Incoming message format:
{
  "secret_key": <SECRET_KEY>,
  "cmd": <COMMAND>,
  "params": [
    "key1": "value1",
    "key2": "value2",
    ...
  ]
}
*/

wss.on("connection", function connection(ws) {
  ws.on("message", function incoming(message) {
    try {
      const msg = JSON.parse(message);
      if (msg.secret_key != SECRET_KEY) throw new Error("Invalid secret key");
      delete msg.secret_key;
      wss.broadcast(JSON.stringify(msg));
    } catch (e) {
      console.log(`Error: ${e}`);
    }
  });
});
