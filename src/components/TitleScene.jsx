import React from "react";

const MenuScreen = ({ onStart }) => (
  <div
    style={{
      textAlign: "center",
      padding: "2rem",
      fontFamily: "sans-serif",
      backgroundColor: "#f0f8ff",
      height: "100vh",
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
    }}
  >
    <h1>Filter Bubble Zoo</h1>
    <p>好きな動物をクリックして可愛がろう。<br />お気に入りばかり可愛がると……？</p>
    <button
      onClick={onStart}
      style={{
        fontSize: "1.5rem",
        padding: "1rem 2rem",
        marginTop: "2rem",
        cursor: "pointer",
      }}
    >
      入園する
    </button>
  </div>
);

export default MenuScreen;
