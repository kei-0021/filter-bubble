# filter-bubble

## コマンドラインで解析だけ行いたい場合
- `/workspaces/filter-bubble/output/weights_plot.png`にフィルターバブルの生成過程がグラフとして出力される
```
python3 src/main.py
```

## streamlitの簡易UIでフィルターバブルを体験したい場合
```
python3 src/main.py
```

## Reactの本格UIでフィルターバブルを体験したい場合
- `Local:   http://localhost:5173/`を選ぶ
```
npm run dev -- --host
```