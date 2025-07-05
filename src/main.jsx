import React from "react";
import ReactDOM from "react-dom/client";
import FilterBubbleZoo from "./components/zoo.jsx";

const canvasWidth = 1200;  // 好きなサイズに調整OK
const canvasHeight = 700;

ReactDOM.createRoot(document.getElementById("app")).render(
  <React.StrictMode>
    <FilterBubbleZoo initialWeights={{ bird: 0.5, panda: 0.5 }} />
  </React.StrictMode>
);
