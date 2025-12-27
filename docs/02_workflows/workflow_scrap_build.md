# Workflow: Scrap & Build

未インデックスの旧記事を、新規記事として蘇らせる標準フロー。

## Phase 1: Preparation (Scrap)
1.  **選定**: `sites/siteXX/backlog.csv` からリライト対象のURLを選ぶ。
2.  **原文確保**: 旧記事の内容をコピーし、`sites/siteXX/articles/YYYY/source.md` に保存する。
3.  **非公開化**:
    *   WordPress管理画面で該当記事を「下書き」に戻す、または「ゴミ箱」へ移動する。
    *   **重要**: 完全に削除せず、バックアップとして残すが、Web上からは消す（404状態にする）。

## Phase 2: Reconstruction (Design & Draft)
1.  **構成案作成**:
    *   AIプロンプト `prompts/system/outline_generator.md` を使用。
    *   キーワードと検索意図を入力し、構成案を出力。
    *   人間が確認・修正し、`outline.md` に保存。
2.  **下書き生成**:
    *   構成案を元に、AIにセクションごとに執筆させる。
    *   内容は `draft.md` に保存。

## Phase 3: Humanization (Rewrite)
1.  **文体変換**:
    *   `style_guide_candy_kotaro.md` に従い、人間がリライトする。
    *   この段階で「体験談」「独自見解」「語り」を大幅に追加する。
2.  **レビュー**:
    *   `review_checklist.md` を用いてセルフチェック。
    *   OKなら `review.md` に「承認」と記録。

## Phase 4: Publication (Build)
1.  **WordPress投稿**:
    *   **新規投稿** として作成（旧記事の編集ではない）。
    *   新しいパーマリンク（URLスラッグ）を設定。
2.  **装飾・画像**:
    *   見出しタグ(h2, h3)を適切に設定。
    *   アイキャッチ画像を設定。
3.  **公開設定**:
    *   `sites/siteXX/release_plan.csv` で指定された日時に予約投稿、または即時公開。

## Phase 5: Observation
1.  **URL検査**:
    *   公開直後に Search Console で「URL検査」→「インデックス登録をリクエスト」。
2.  **記録**:
    *   `publish_log.md` に公開日時とURLを記録。
3.  **追跡**:
    *   3日後、7日後にインデックス状況を確認。
