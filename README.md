# TUI 流体シミュレーション

## 概要
TUI (Text User Interface) で流体シミュレーションを実装したものです。

## インストール

textualをインストールしてください。
```bash
pip install textual
```

## 実行

```bash
python main.py
```

「ファイルをロード」を押すと、level.txtを読み込みます。
「リセット」を押すと、初期状態に戻ります。

## ファイル

- main.py: メインファイル
    - 本体です。
- simulation.py: シミュレーションファイル
    - シミュレーションの計算とか
- level.txt: レベルファイル
    - 初期配置を記述します。
    - `@`は壁
    - `#`は水
