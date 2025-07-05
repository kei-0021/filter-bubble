import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom/client";
import FilterBubbleZoo from "./components/zoo.jsx";

const App = () => {
  const [size, setSize] = useState({
    width: window.innerWidth * 1.0,
    height: window.innerHeight * 0.9,
  });

  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth * 0.9,
        height: window.innerHeight * 0.6,
      });
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <>
      <h1 style={{ textAlign: "center" }}>Filter Bubble Zoo</h1>
      <FilterBubbleZoo
        width={size.width}
        height={size.height}
        initialWeights={{ bird: 0.5, panda: 0.5 }}
      />
    </>
  );
};

ReactDOM.createRoot(document.getElementById("app")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
