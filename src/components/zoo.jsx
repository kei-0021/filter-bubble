import React, { useEffect, useRef, useState } from "react";

const FilterBubbleZoo = ({
  initialWeights,
  width = 600,
  height = 400,
  totalCount = 15,
}) => {
  const canvasRef = useRef(null);
  const [weights, setWeights] = useState(initialWeights);
  const animalPositions = useRef([]);
  const animationFrameId = useRef(null);
  const birdSoundRef = useRef(null);

  useEffect(() => {
    birdSoundRef.current = new Audio("./sounds/bird.mp3");
    birdSoundRef.current.volume = 0.3;
  }, []);

  const registerClick = (type) => {
    setWeights((prev) => {
      if (type === "bird" && birdSoundRef.current) {
        birdSoundRef.current.currentTime = 0;
        birdSoundRef.current.play();
      }
      const delta = 0.05;
      const next = { ...prev };
      next[type] = Math.min(1, prev[type] + delta);
      const other = type === "bird" ? "panda" : "bird";
      next[other] = Math.max(0, 1 - next[type]);
      return next;
    });
  };

  const loadImage = (src) =>
    new Promise((resolve, reject) => {
      const img = new Image();
      img.src = src;
      img.onload = () => resolve(img);
      img.onerror = () => reject(new Error(`${src} の画像読み込みに失敗しました`));
    });

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.scale(dpr, dpr);

    let birdImg, pandaImg;
    let animals = [];

    const birdCount = Math.round(totalCount * weights.bird);
    const pandaCount = totalCount - birdCount;

    // 重なり判定
    const isOverlapping = (x, y, size) => {
      return animals.some((a) => {
        const dx = a.baseX - x;
        const dy = a.baseY - y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        return distance < size;
      });
    };

    const placeAnimal = (type, count, size) => {
      for (let i = 0; i < count; i++) {
        let baseX, baseY, tries = 0;
        do {
          baseX = Math.random() * (width - size);
          baseY = Math.random() * (height - size);
          tries++;
        } while (isOverlapping(baseX, baseY, size) && tries < 100);

        animals.push({
          type,
          baseX,
          baseY,
          x: baseX,
          y: baseY,
          size,
          angle: Math.random() * Math.PI * 2,
          speed:
            type === "bird"
              ? 0.02 + Math.random() * 0.02
              : 0.01 + Math.random() * 0.015,
        });
      }
    };

    Promise.all([loadImage("./images/bird.png"), loadImage("./images/panda.png")])
      .then(([bird, panda]) => {
        birdImg = bird;
        pandaImg = panda;

        placeAnimal("bird", birdCount, 100);
        placeAnimal("panda", pandaCount, 100);

        const animate = () => {
          ctx.clearRect(0, 0, width, height);
          ctx.fillStyle = "#d2f8d2";
          ctx.fillRect(0, 0, width, height);

          animals.forEach((animal) => {
            animal.angle += animal.speed;

            if (animal.type === "bird") {
              animal.x = animal.baseX + Math.sin(animal.angle) * 10;
              animal.y = animal.baseY + Math.sin(animal.angle * 2) * 5;
              ctx.drawImage(birdImg, animal.x, animal.y, animal.size, animal.size);
            } else if (animal.type === "panda") {
              animal.x = animal.baseX + Math.sin(animal.angle / 2) * 5;
              animal.y = animal.baseY;
              ctx.drawImage(pandaImg, animal.x, animal.y, animal.size, animal.size);
            }
          });

          // ダミーボタン描画
          const btnWidth = 110;
          const btnHeight = 40;
          const margin = 30;

          const btnX = width - btnWidth - margin; // 右端からボタン幅＋余白分引く
          const btnY = margin; // 上端から余白分だけ下げる

          ctx.fillStyle = "#88a76f";
          ctx.fillRect(btnX, btnY, btnWidth, btnHeight);
          ctx.fillStyle = "white";
          ctx.font = "20px sans-serif";
          ctx.textBaseline = "middle";
          ctx.fillText("メニュー", btnX + 15, btnY + btnHeight / 2);

          animationFrameId.current = requestAnimationFrame(animate);
        };

        animate();
        animalPositions.current = animals;
      })
      .catch((err) => console.error(err));

    return () => {
      if (animationFrameId.current) cancelAnimationFrame(animationFrameId.current);
    };
  }, [weights, width, height, totalCount]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const handleClick = (event) => {
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      // ダミーボタン範囲判定
      const btnX = width - 110;
      const btnY = height - 50;
      const btnWidth = 100;
      const btnHeight = 40;

      if (
        x >= btnX &&
        x <= btnX + btnWidth &&
        y >= btnY &&
        y <= btnY + btnHeight
      ) {
        alert("ダミーボタンが押されました！");
        return;
      }

      const clicked = animalPositions.current.find(
        (a) => x >= a.x && x <= a.x + a.size && y >= a.y && y <= a.y + a.size
      );

      if (clicked) {
        registerClick(clicked.type);
      }
    };

    canvas.addEventListener("click", handleClick);
    return () => canvas.removeEventListener("click", handleClick);
  }, [width, height]);

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: `${height}px`,
      }}
    >
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        style={{ border: "1px solid black", cursor: "pointer" }}
      />
    </div>
  );
};

export default FilterBubbleZoo;
