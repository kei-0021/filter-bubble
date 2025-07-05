import React, { useEffect, useRef, useState } from "react";

const FilterBubbleZoo = ({ initialWeights, width = 1200, height = 700, totalCount = 10 }) => {
  const canvasRef = useRef(null);
  const [weights, setWeights] = useState(initialWeights);
  const animalPositions = useRef([]); // 動物の位置と種類を保持

  const registerClick = (type) => {
    setWeights((prev) => {
      const delta = 0.05;
      const next = { ...prev };
      next[type] = Math.min(1, prev[type] + delta);
      const other = type === "bird" ? "panda" : "bird";
      next[other] = Math.max(0, 1 - next[type]);
      return next;
    });
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.scale(dpr, dpr);

    ctx.clearRect(0, 0, width, height);
    animalPositions.current = [];

    const drawAnimals = (img, count, size, type) => {
      for (let i = 0; i < count; i++) {
        const x = Math.random() * (width - size);
        const y = Math.random() * (height - size);
        ctx.drawImage(img, x, y, size, size);
        animalPositions.current.push({ x, y, size, type });
      }
    };

    const loadAndDraw = (src, count, type) => {
      const img = new Image();
      img.src = src;
      img.onload = () => drawAnimals(img, count, 100, type);
      img.onerror = () => console.error(`${src} の画像読み込みに失敗しました`);
    };

    const birdCount = Math.round(totalCount * weights.bird);
    const pandaCount = totalCount - birdCount;

    loadAndDraw("./images/bird.png", birdCount, "bird");
    loadAndDraw("./images/panda.png", pandaCount, "panda");
  }, [weights, width, height, totalCount]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const handleClick = (event) => {
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      const clicked = animalPositions.current.find((a) =>
        x >= a.x && x <= a.x + a.size &&
        y >= a.y && y <= a.y + a.size
      );

      if (clicked) {
        registerClick(clicked.type);
      }
    };

    canvas.addEventListener("click", handleClick);
    return () => canvas.removeEventListener("click", handleClick);
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{ border: "1px solid black", display: "block", cursor: "pointer" }}
    />
  );
};

export default FilterBubbleZoo;
