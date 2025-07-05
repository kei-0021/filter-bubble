import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom/client";
import MenuScreen from "./components/TitleScene.jsx";
import FilterBubbleZoo from "./components/Zoo.jsx";

const App = () => {
  const [started, setStarted] = useState(false);
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return started ? (
    <FilterBubbleZoo
      initialWeights={{ bird: 0.5, panda: 0.5 }}
      width={windowSize.width * 1.0}
      height={windowSize.height * 1.0}
    />
  ) : (
    <MenuScreen onStart={() => setStarted(true)} />
  );
};

ReactDOM.createRoot(document.getElementById("app")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

