import React, { useEffect, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import { useGamepads } from "react-gamepads";
import "./App.css";
import { Button } from "antd";

function App() {
  const [controlWsInput, setControlWsInput] = useState("ws://localhost:8001");
  const [controlWsURL, setControlWsURL] = useState("ws://localhost:8001");
  const { sendMessage, readyState } = useWebSocket(controlWsURL);
  const [gamepads, setGamepads] = useState({});
  useGamepads((gamepads) => setGamepads(gamepads));

  const keyDownHandler = (event: React.KeyboardEvent<HTMLInputElement>) => {
    switch (event.key) {
      case "ArrowUp":
        sendMessage("y1");
        break;
      case "ArrowDown":
        sendMessage("y2");
        break;
      case "ArrowLeft":
        sendMessage("x1");
        break;
      case "ArrowRight":
        sendMessage("x2");
        break;
      case "Enter":
        sendMessage("x0");
        sendMessage("y0");
        break;
    }
  };

  const keyUpHandler = (event: React.KeyboardEvent<HTMLInputElement>) => {
    switch (event.key) {
      case "ArrowUp":
        sendMessage("y0");
        break;
      case "ArrowDown":
        sendMessage("y0");
        break;
      case "ArrowLeft":
        sendMessage("x0");
        break;
      case "ArrowRight":
        sendMessage("x0");
        break;
    }
  };

  useEffect(() => {
    console.log(gamepads);
    if (readyState === ReadyState.OPEN) {
    }
  }, [gamepads, sendMessage, readyState]);

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  return (
    <div className="App">
      <div>
        <label>Control WebSocket URL:</label>
        <input
          type="text"
          value={controlWsInput}
          onChange={(e) => setControlWsInput(e.target.value)}
        />
        <Button onClick={() => setControlWsURL(controlWsInput)}>
          {" "}
          Connect{" "}
        </Button>
      </div>
      <div>
        <label>Connection Status:</label>
        <span>{connectionStatus}</span>
      </div>
      <div>
        <label>Click Here To Control:</label>
        <input type="text" onKeyDown={keyDownHandler} onKeyUp={keyUpHandler} />
      </div>
      <div>
        <label>Touch Controls</label>
        <Button
          id="up"
          onTouchStart={() => sendMessage("y1")}
          onTouchEnd={() => sendMessage("y0")}
        >
          {" "}
          Up{" "}
        </Button>
        <Button
          id="down"
          onTouchStart={() => sendMessage("y2")}
          onTouchEnd={() => sendMessage("y0")}
        >
          {" "}
          Down{" "}
        </Button>
        <Button
          id="left"
          onTouchStart={() => sendMessage("x1")}
          onTouchEnd={() => sendMessage("x0")}
        >
          {" "}
          Left{" "}
        </Button>
        <Button
          id="right"
          onTouchStart={() => sendMessage("x2")}
          onTouchEnd={() => sendMessage("x0")}
        >
          {" "}
          Right{" "}
        </Button>
        <Button
          id="shoot"
          onTouchStart={() => sendMessage("s1")}
          onTouchEnd={() => sendMessage("s0")}
        >
          {" "}
          Shoot{" "}
        </Button>
      </div>
    </div>
  );
}

export default App;
