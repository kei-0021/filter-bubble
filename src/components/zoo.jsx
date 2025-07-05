import React, { useEffect, useRef } from "react";

const BirdZoo = ({ birdCount, width = 600, height = 400 }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    // キャンバスサイズを設定（DPR対応）
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.scale(dpr, dpr);

    const birdImg = new Image();
    birdImg.src = "/images/bird.png";

    const birdDrawWidth = 100;
    const birdDrawHeight = 100;

    birdImg.onload = () => {
      ctx.clearRect(0, 0, width, height);
      for (let i = 0; i < birdCount; i++) {
        const x = Math.random() * (width - birdDrawWidth);
        const y = Math.random() * (height - birdDrawHeight);
        ctx.drawImage(birdImg, x, y, birdDrawWidth, birdDrawHeight);
      }
    };

    birdImg.onerror = () => {
      console.error("鳥の画像読み込みに失敗しました");
    };
  }, [birdCount, width, height]);

  return (
    <canvas
      ref={canvasRef}
      style={{ border: "1px solid black", display: "block" }}
    />
  );
};

export default BirdZoo;
