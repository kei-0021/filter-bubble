# filter-bubble

## コマンドラインで解析だけ行いたい場合
- `/workspaces/filter-bubble/output/weights_plot.png`にフィルターバブルの生成過程がグラフとして出力される
```
PYTHONPATH=. python3 server/main.py
```

## streamlitの簡易UIでフィルターバブルを体験したい場合
- `Local URL: http://localhost:8501`を選ぶ
- HTMLやCSSでの装飾が無いので、シンプルなUIとなっている
```
PYTHONPATH=. streamlit run server/app.py
```

## Reactの本格UIでフィルターバブルを体験したい場合
- `Local:   http://localhost:5173/`を選ぶ
- こちらはHTML/CSS/JavaScriptにReactを組み合わせたリッチなUIとなっている
```
npm run dev -- --host
```