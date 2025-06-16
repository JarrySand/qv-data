# QV Data Analysis

このプロジェクトは、Quadratic Voting (QV) の投票データを分析するためのツールセットです。

## 機能

- 投票データの取得と保存
- 重複投票の検出
- 投票統計の分析
- レポート生成

## ディレクトリ構造

```
qv-data/
├── data/           # 生データとCSVファイルを保存
├── src/            # Pythonスクリプト
│   ├── fetch_votes.py
│   ├── check_duplicates.py
│   ├── generate_duplicate_report.py
│   ├── calculate_unique_votes.py
│   └── requirements.txt
└── report/         # 生成されたレポートを保存
```

## セットアップ

1. リポジトリのクローン:
```bash
git clone https://github.com/yourusername/qv-data.git
cd qv-data
```

2. 依存関係のインストール:
```bash
cd src
pip install -r requirements.txt
```

## 使用方法

1. 投票データの取得:
```bash
python src/fetch_votes.py
```

2. 重複投票のチェック:
```bash
python src/check_duplicates.py
```

3. 重複投票レポートの生成:
```bash
python src/generate_duplicate_report.py
```

4. 投票統計の計算:
```bash
python src/calculate_unique_votes.py
```

## 出力

- `data/`: 生のJSONデータとCSVファイル
- `report/`: 分析レポート（Markdown形式）

## ライセンス

MIT License 