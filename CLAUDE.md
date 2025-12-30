# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

Piston は、90以上のプログラミング言語をサポートする高性能・高セキュリティなコード実行エンジン。API サーバー経由でコードを安全に実行でき、Linux の Isolate (namespaces + chroot + cgroup) を使用したサンドボックス環境で動作する。

## 開発コマンド

### 環境の起動・停止

```bash
./piston select dev          # 開発環境を選択 (初回のみ)
./piston start               # 起動
./piston stop                # 停止
./piston restart             # 再起動
./piston logs                # ログ表示
./piston bash                # コンテナシェルを開く
./piston rebuild             # ビルドして再起動
```

### コード整形 (Lint)

```bash
./piston lint                # Prettier で全ファイルをフォーマット
npx prettier --write <path>  # 特定ファイルのみフォーマット
```

### パッケージ管理

```bash
./piston list-pkgs                    # 利用可能なパッケージ一覧
./piston build-pkg <pkg> <ver>        # パッケージをビルド
./piston clean-pkgs                   # ビルド成果物をクリーン
```

### CLI のセットアップ

```bash
cd cli && npm i && cd -
```

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────────┐
│                       Docker Container                       │
├─────────────────────────────────────────────────────────────┤
│  api/                          cli/                          │
│  ├─ Express Server             ├─ yargs CLI                  │
│  ├─ Routes (api/v2.js)         └─ commands/                  │
│  ├─ Job Manager (job.js)           ├─ execute.js             │
│  ├─ Runtime Manager                └─ ppman.js               │
│  └─ Package Manager                                          │
├─────────────────────────────────────────────────────────────┤
│                    Isolate Sandbox                           │
│  (Linux namespaces + chroot + cgroup)                        │
├─────────────────────────────────────────────────────────────┤
│  packages/                                                   │
│  └─ <lang>/<version>/                                        │
│      ├─ metadata.json  (言語情報、エイリアス)                │
│      ├─ build.sh       (ビルドスクリプト)                    │
│      ├─ run            (実行スクリプト)                      │
│      └─ environment    (環境変数)                            │
└─────────────────────────────────────────────────────────────┘
```

### 主要コンポーネント

| ファイル | 役割 |
|---------|------|
| `api/src/index.js` | Express サーバー初期化 |
| `api/src/api/v2.js` | API エンドポイント定義 |
| `api/src/job.js` | ジョブ実行管理 (READY → PRIMED → EXECUTED) |
| `api/src/runtime.js` | 言語ランタイム管理 |
| `api/src/package.js` | パッケージのインストール・管理 |
| `api/src/config.js` | 環境変数による設定管理 |

### API エンドポイント

| メソッド | パス | 目的 |
|---------|------|------|
| GET | `/api/v2/runtimes` | インストール済み言語一覧 |
| POST | `/api/v2/execute` | コード実行 |
| WebSocket | `/api/v2/connect` | インタラクティブ実行 |

## 設定 (環境変数)

主要な環境変数 (`PISTON_` プレフィックス):

| 変数 | デフォルト | 説明 |
|-----|---------|------|
| `PISTON_LOG_LEVEL` | INFO | ログレベル |
| `PISTON_BIND_ADDRESS` | 0.0.0.0:2000 | API バインドアドレス |
| `PISTON_DISABLE_NETWORKING` | true | ネットワーク無効化 |
| `PISTON_COMPILE_TIMEOUT` | 10000 | コンパイルタイムアウト (ms) |
| `PISTON_RUN_TIMEOUT` | 3000 | 実行タイムアウト (ms) |
| `PISTON_MAX_PROCESS_COUNT` | 64 | 最大プロセス数 |
| `PISTON_OUTPUT_MAX_SIZE` | 1024 | 出力最大サイズ |

詳細は `docs/configuration.md` を参照。

## テスト

セキュリティテストは `/tests/` にある:

```bash
python3 tests/fork.py              # フォーク爆弾テスト
python3 tests/fallocate.py         # ディスク満杯攻撃テスト
python3 tests/network.py           # ネットワークアクセステスト
```

パッケージのテストは GitHub Actions (`package-pr.yaml`) で自動実行される。

## 言語パッケージの追加

1. `packages/<lang>/<version>/` ディレクトリを作成
2. 必須ファイルを作成:
   - `metadata.json` - 言語名、バージョン、エイリアス
   - `build.sh` - ビルドスクリプト
   - `run` - 実行スクリプト
3. `./piston build-pkg <lang> <version>` でビルド
4. README.md にバッジを追加

## コードスタイル

Prettier 設定 (`.prettierrc.yaml`):
- シングルクォート使用
- タブ幅: 4
- Arrow関数の括弧: 省略

### コミットメッセージ

- **Conventional Commits は使用しない** (`fix:`, `feat:` などのプレフィックスは不要)
- 変更内容を簡潔に説明する通常の形式で記述

## GitHub Actions

### permissions 設定

ghcr.io や GitHub Releases を使用するワークフローでは、明示的な permissions 設定が必要:

```yaml
jobs:
    job_name:
        runs-on: ubuntu-latest
        permissions:
            contents: write    # リリースへのアップロード時
            packages: write    # ghcr.io へのプッシュ時
            packages: read     # ghcr.io からのプル時
```

### Docker イメージワークフロー

| ワークフロー | 用途 | トリガーパス |
|-------------|------|-------------|
| `api-push.yaml` | API イメージ | `api/**` |
| `repo-push.yaml` | Repo Builder イメージ | `repo/**` |
| `package-push.yaml` | パッケージビルド | `packages/**` |

## 前提条件

- Docker & Docker Compose
- cgroup v2 有効化 (cgroup v1 は無効化)
- Node.js >= 15 (CLI 開発時)
