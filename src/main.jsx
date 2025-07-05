import React from "react";
import ReactDOM from "react-dom/client";
import BirdZoo from "./components/zoo.jsx";

const canvasWidth = 1200;  // 好きなサイズに調整OK
const canvasHeight = 700;

ReactDOM.createRoot(document.getElementById("app")).render(
  <React.StrictMode>
    <BirdZoo birdCount={2} width={canvasWidth} height={canvasHeight} />
  </React.StrictMode>
);
