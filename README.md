# LDMV Works Homepage

> **公開先は GitHub Pages (`https://ldmvworks.github.io/`) のみです。OpenAI Sites / `chatgpt.site` は使用しません。**

LDMV Works の一般公開用ホームページです。
PC向けインディーゲームを企画・開発する個人スタジオの公式ページとして、GitHub Pagesで公開することを想定しています。

同じ内容をCodexのSitesでも公開できる構成です。GitHub Pages用の`index.html`を正本として利用するため、本文を二重に管理する必要はありません。

## サイト構成

- `index.html`: 1ページ構成のトップページ
- `styles.css`: レスポンシブ対応のCSS
- `assets/logo.svg`: favicon用の簡易ロゴ
- `assets/logo.png`: 黒背景用のLDMV Worksロゴ画像
- `assets/title-menu-ja.png`: 開発中タイトルの画面スクリーンショット
- `.nojekyll`: GitHub PagesでJekyll処理を無効化するためのファイル
- `app/`, `worker/`, `vite.config.ts`: Sites公開用の実行構成
- `.openai/hosting.json`: Sitesの公開先を識別する設定
- `public/og.png`: Sitesで共有した際のプレビュー画像

## 表示言語

標準表示は日本語です。
ヘッダー右側の `JP / EN` スイッチで英語表示に切り替えられます。
切り替えはCSSだけで実装しており、JavaScriptは使用していません。

Sites側には公開基盤としてReact/Vinextの構成がありますが、ページ内の言語切り替えやスライド表示は従来どおりHTML/CSSのみです。

## Sitesでの確認

1. 依存関係をインストールする。

   ```powershell
   npm install
   ```

2. ローカル表示を起動する。

   ```powershell
   npm run dev
   ```

3. 公開前のビルドを確認する。

   ```powershell
   npm run build
   ```

Sitesへの公開はCodex上のSites機能から行います。`.openai/hosting.json`の`project_id`は公開先との紐付けに使うため、追加後は削除・書き換えをしないでください。

## 公開手順

1. GitHub CLIのログイン状態を確認する。

   ```powershell
   gh auth status
   ```

2. 対象リポジトリが見えることを確認する。

   ```powershell
   gh repo view ldmvworks/ldmvworks.github.io
   ```

3. 作業場所にリポジトリをcloneする。

   ```powershell
   git clone https://github.com/ldmvworks/ldmvworks.github.io.git
   cd ldmvworks.github.io
   ```

4. このディレクトリ内のファイルをリポジトリ直下へ配置する。

5. 変更内容を確認してcommitする。

   ```powershell
   git status
   git add index.html styles.css README.md .nojekyll .gitignore assets/
   git commit -m "Add LDMV Works homepage"
   ```

6. `main` ブランチへpushする。

   ```powershell
   git branch -M main
   git push -u origin main
   ```

7. GitHubのリポジトリ画面で、Pages設定を確認する。

   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/root`

8. 公開URLを開いて表示を確認する。

   <https://ldmvworks.github.io/>

## 更新手順

1. `index.html` または `styles.css` を編集する。
2. ブラウザで `index.html` を直接開き、PC幅とスマホ幅で表示を確認する。
3. 掲載内容が現在の事実と合っているか確認する。
4. 変更をcommitしてpushする。

   ```powershell
   git status
   git add index.html styles.css README.md assets/
   git commit -m "Update homepage"
   git push
   ```

## 公開前チェック

- 公開する連絡先は事業用メールを基本とし、非公開情報は掲載しない。
- 現在の状態と異なる表現を書かない。
- ゲーム本体のソースコードをこのリポジトリに入れない。
- 開発中の内容は、確定した実績ではなく「開発中」「目標」として表現する。
