# ProTox3-Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![ProTox-3](https://img.shields.io/badge/ProTox-3.0-green.svg)](https://tox.charite.de/protox3/)

**言語**: [English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md)

**ProTox3-Automation** は、化合物の毒性予測をバッチ処理するための包括的な自動化ツールキットで、特に**細胞毒性（Cytotoxicity）**予測結果の抽出に焦点を当てています。

## ✨ 主な機能

- 🔄 **SMILES変換** - SMILESを自動的にCanonical形式に変換
- 🤖 **バッチ予測** - ProTox-3ウェブサイトへの自動アクセスによる毒性予測
- 📊 **データ抽出** - 予測結果からCytotoxicityデータを抽出
- 📈 **結果集約** - すべての結果を単一のCSVファイルに統合
- 🚀 **効率的な処理** - バッチ処理とバックグラウンド実行をサポート

## 🎯 使用例

- 創薬における毒性評価
- 化学物質の安全性スクリーニング
- 学術研究における毒性予測
- 大規模化合物ライブラリの毒性分析

## 📋 システム要件

- Python 3.7以上
- Chrome/Chromiumブラウザ
- 安定したインターネット接続
- 少なくとも1GBの利用可能なディスク容量

## 🚀 クイックスタート

### ワンクリックインストール（推奨）

```bash
# リポジトリをクローン
git clone https://github.com/biao-ma/ProTox3-Automation.git
cd ProTox3-Automation

# インストールスクリプトを実行
bash setup.sh

# 使用開始
bash run_protox.sh
```

### 手動インストール

```bash
# 1. リポジトリをクローン
git clone https://github.com/biao-ma/ProTox3-Automation.git
cd ProTox3-Automation

# 2. 仮想環境を作成
python3 -m venv venv
source venv/bin/activate

# 3. 依存関係をインストール
pip install -r requirements.txt

# 4. データを準備
# PubChem_IDとSMILES列を含むCSVファイルをdata/ディレクトリに配置

# 5. スクリプトを実行
python3 src/protox_full_automation.py
```

## 📊 使用例

### すべての化合物を処理

```bash
python3 src/protox_full_automation.py
```

### 特定範囲の化合物を処理

```bash
# 化合物0-10を処理
python3 src/protox_full_automation.py 0 10

# 化合物10-20を処理
python3 src/protox_full_automation.py 10 20
```

### バックグラウンドで実行

```bash
nohup python3 src/protox_full_automation.py > protox.log 2>&1 &
```

## 📁 プロジェクト構造

```
ProTox3-Automation/
├── README.md                      # プロジェクトドキュメント（英語）
├── README.zh-CN.md               # 中国語ドキュメント
├── README.ja.md                  # 日本語ドキュメント
├── LICENSE                        # ライセンス
├── requirements.txt               # Python依存関係
├── setup.sh                       # ワンクリックインストールスクリプト
├── run_protox.sh                  # クイックスタートスクリプト
├── data/                          # データディレクトリ
│   └── example_input.csv         # サンプル入力ファイル
├── src/                           # ソースコードディレクトリ
│   ├── protox_full_automation.py # メイン自動化スクリプト
│   ├── extract_cytotoxicity.py   # 結果集約スクリプト
│   └── convert_smiles.py         # SMILES変換スクリプト
├── results/                       # 出力ディレクトリ
│   ├── CID_*.csv                 # 個別化合物レポート
│   └── cytotoxicity_summary.csv  # 最終集約ファイル
└── docs/                          # ドキュメントディレクトリ
    ├── QUICK_START.md            # クイックスタートガイド
    ├── INSTALLATION.md           # 詳細インストールガイド
    ├── USER_GUIDE.md             # ユーザーガイド
    └── TROUBLESHOOTING.md        # トラブルシューティングガイド
```

## ⏱️ 処理時間の目安

| タスク | 時間 |
|------|------|
| 単一化合物 | 5-10分 |
| 10化合物 | 1-2時間 |
| 100化合物 | 8-16時間 |

## 📊 出力形式

### 個別化合物レポート (CID_*.csv)

```csv
Classification,Target,Shorthand,Prediction,Probability
Organ toxicity,Hepatotoxicity,dili,Active,0.62
Organ toxicity,Neurotoxicity,neuro,Active,0.61
...
Toxicity end points,Cytotoxicity,cyto,Inactive,0.62
...
```

### 集約ファイル (cytotoxicity_summary.csv)

```csv
PubChem_ID,Classification,Target,Shorthand,Prediction,Probability
311434,Toxicity end points,Cytotoxicity,cyto,Inactive,0.62
54576693,Toxicity end points,Cytotoxicity,cyto,Active,0.71
...
```

## 🔧 設定オプション

`config.py`で以下のオプションをカスタマイズできます：

```python
# ProTox-3ウェブサイトURL
PROTOX_URL = 'https://tox.charite.de/protox3/index.php?site=compound_input'

# 入力ファイルパス
INPUT_FILE = 'data/input.csv'

# 出力ディレクトリ
OUTPUT_DIR = 'results/'

# タイムアウト設定（秒）
MAX_WAIT_TIME = 900  # 15分
```

## 📚 ドキュメント

- [クイックスタートガイド](docs/QUICK_START.md)
- [詳細インストールガイド](docs/INSTALLATION.md)
- [ユーザーガイド](docs/USER_GUIDE.md)
- [トラブルシューティング](docs/TROUBLESHOOTING.md)
- [APIドキュメント](docs/API.md)

## 🤝 コントリビューション

コントリビューションを歓迎します！参加方法の詳細については[CONTRIBUTING.md](CONTRIBUTING.md)をご覧ください。

### コントリビューション方法

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを開く

## 📝 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルをご覧ください

## ⚠️ 免責事項

- このツールは研究および教育目的のみです
- ProTox-3ウェブサイトの利用規約を遵守してください
- データを商業目的で使用しないでください
- 予測結果は参考用であり、意思決定の唯一の根拠として使用すべきではありません

## 🙏 謝辞

- [ProTox-3](https://tox.charite.de/protox3/) - 毒性予測サービスの提供
- [RDKit](https://www.rdkit.org/) - ケモインフォマティクスツールキット
- [Selenium](https://www.selenium.dev/) - ブラウザ自動化ツール

## 📞 お問い合わせ

- 問題報告: [GitHub Issues](https://github.com/biao-ma/ProTox3-Automation/issues)
- 機能リクエスト: [GitHub Discussions](https://github.com/biao-ma/ProTox3-Automation/discussions)

## 🌟 スター履歴

このプロジェクトが役に立った場合は、⭐️をください！

---

**最終更新**: 2026-01-08  
**バージョン**: 1.0.0
