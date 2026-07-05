# LDMV Works Homepage

LDMV Works の一般公開用ホームページです。
PC向けインディーゲームを企画・開発する個人スタジオの公式ページとして、GitHub Pagesで公開することを想定しています。

## サイト構成

- `index.html`: 1ページ構成のトップページ
- `styles.css`: レスポンシブ対応のCSS
- `assets/logo.svg`: favicon用の簡易ロゴ
- `assets/logo.png`: 黒背景用のLDMV Worksロゴ画像
- `assets/title-menu-ja.png`: 開発中タイトルの画面スクリーンショット
- `.nojekyll`: GitHub PagesでJekyll処理を無効化するためのファイル

## 表示言語

標準表示は日本語です。
ヘッダー右側の `JP / EN` スイッチで英語表示に切り替えられます。
切り替えはCSSだけで実装しており、JavaScriptは使用していません。

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
