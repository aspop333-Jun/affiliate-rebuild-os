# agents.md
以下のレポジトリ構成に従ってください
affiliate-rebuild-os/
├─ README.md
├─ docs/
│  ├─ 00_overview.md
│  ├─ 01_rules/
│  │  ├─ publishing_policy.md          # 1日4本・投稿分散・非公開方針など
│  │  ├─ ai_usage_policy.md            # AIの役割と禁止（AI臭対策）
│  │  ├─ review_checklist.md           # 公開前レビュー観点（地雷除去）
│  │  └─ style_guide_candy_kotaro.md    # 文体規約（口調・構造・NG表現）
│  ├─ 02_workflows/
│  │  ├─ workflow_scrap_build.md        # 非公開→再設計→公開→SC確認
│  │  ├─ workflow_gsc.md               # GSCの見方・記録・再クロール手順
│  │  └─ workflow_release_calendar.md  # 投稿カレンダー運用
│  └─ 03_templates/
│     ├─ article_outline.md            # 見出し骨格テンプレ
│     ├─ article_draft.md              # 原稿テンプレ（導入/本題/まとめ）
│     ├─ internal_link_map.md          # 内部リンク設計テンプレ
│     └─ notion_pages.md               # Notionに貼る用テンプレ集
├─ prompts/
│  ├─ system/                          # 変更頻度低・基盤プロンプト
│  │  ├─ outline_generator.md
│  │  ├─ improvement_detector.md
│  │  └─ rewrite_to_candy_style.md
│  ├─ tasks/                           # 実行タスク別
│  │  ├─ faq_builder.md
│  │  ├─ meta_title_desc.md
│  │  └─ eeat_signals.md
│  └─ eval/
│     ├─ ai_smell_checker.md           # AI臭検知用プロンプト
│     └─ human_signal_checker.md       # 人間運営シグナル検知
├─ sites/
│  ├─ _shared/
│  │  ├─ taxonomy.md                   # 共通カテゴリ/タグ方針
│  │  └─ url_rules.md                  # URL構造ルール
│  ├─ site01/
│  │  ├─ site_profile.md               # サイトの狙い・読者・禁止事項
│  │  ├─ gsc_notes.md                  # 除外理由の記録
│  │  ├─ backlog.csv                   # 対象URL/テーマ/優先度
│  │  ├─ release_plan.csv              # 投稿日・時間・状態
│  │  └─ articles/
│  │     ├─ 0001/
│  │     │  ├─ source.md               # 旧記事の要点（コピペではなく要約）
│  │     │  ├─ outline.md
│  │     │  ├─ draft.md
│  │     │  ├─ review.md               # 指摘と修正履歴
│  │     │  └─ publish_log.md          # 公開日/URL/SC状況
│  │     └─ ...
│  └─ site02/ ...
├─ data/
│  ├─ gsc_exports/                     # GSCエクスポート置き場（生データ）
│  ├─ url_lists/                       # 未インデックスURL一覧
│  └─ results/                         # インデックス/順位の集計
├─ scripts/
│  ├─ gsc/
│  │  ├─ parse_exports.py              # エクスポート整形（任意）
│  │  └─ build_index_report.py         # 状況レポート生成（任意）
│  ├─ ops/
│  │  ├─ generate_release_calendar.py  # 1日4本制限のカレンダー生成
│  │  └─ create_article_folder.py      # 記事フォルダ雛形作成
│  └─ README.md
├─ ops/
│  ├─ decisions/                       # 方針決定ログ（いつ何を変えたか）
│  ├─ changelog.md
│  └─ risk_register.md                 # リスクと回避策
└─ .github/
   ├─ ISSUE_TEMPLATE/
   │  ├─ article_task.md               # 記事タスク化
   │  └─ review_request.md             # レビュー依頼テンプレ
   └─ PULL_REQUEST_TEMPLATE.md





## Affiliate Rebuild OS｜Agent Operating Specification

---

## 0. このドキュメントの位置づけ

このリポジトリは  
**「未インデックス資産を、Googleに通る形で再起動するための運用OS」**である。

本ドキュメント（agents.md）は、
- 人間（運用者）
- AI（生成・補助）
- ルール（Google・運用制約）

の**役割分担と責任範囲**を定義する。

---

## 1. Agent 定義

### 1.1 Human Agent（Owner）

**責任**
- 最終判断
- 文体・温度感の決定
- 公開可否の判断
- ルール変更の承認

**やること**
- AI生成物の取捨選択
- 人間文体（キャンディ・コタロー調）への最終編集
- Google Search Consoleでの確認
- 投稿ペースの遵守

**やらないこと**
- 構造を考えずに文章を書くこと
- 勘だけで量産すること
- AI生成物を無検証で公開すること

---

### 1.2 AI Agent（Editor / Assistant）

**役割**
- 情報整理
- 構造設計
- 抜け漏れ検知
- 改善提案

**許可されている作業**
- 見出し構成案の生成
- 既存記事要約（コピー不可）
- 改善点の指摘
- FAQ候補の洗い出し
- E-E-A-T要素の整理

**禁止事項**
- 最終文体の決定
- 導入文・まとめ文の完成稿生成
- 量産前提の自動出力
- SEOワードの過剰挿入

> 原則：**AIは編集者。語り手ではない。**

---

### 1.3 Reviewer Agent（Third Eye）

※ 初期フェーズでは **ChatGPTが兼任**  
※ 型が固まったら人間省略可

**目的**
- AI臭・機械臭の除去
- Google的に危険な構造の検知
- 型崩れの早期発見

**チェック観点**
- 見出しが説明調になっていないか
- 文体が均一すぎないか
- 「一般的に」「重要です」等のAI臭語が多くないか
- 人間の迷い・余白があるか

## 2. 作業フローと Agent 関与ポイント
---旧ページ非公開（Human）
↓
構造設計（AI）
↓
AI下書き生成（AI）
↓
人間文体へ再編集（Human）
↓
事前レビュー（Reviewer）
↓
修正（Human）
↓
新規投稿として公開（Human）
↓
GSC確認・記録（Human）


## 3. 投稿ペース制約（絶対ルール）

- 1サイトあたり **1日最大4記事**
- 投稿時間は分散（例：9 / 13 / 17 / 21）
- 急激な増加は禁止
- 連日投稿は可

この制約は **自動化しても解除してはならない**。

---

## 4. 文体・表現ポリシー

### 基本方針
- 深夜ラジオ調
- 一人語り
- フレンドリーだが軽すぎない
- 読者に説明しすぎない

### NG表現
- 教科書的定義から始まる導入
- 箇条書き主体の本文
- SEOを意識しすぎた単語反復
- 結論を断言しすぎる語調

---

## 5. ディレクトリと責務

### /docs
- ルール・思想・手順の唯一の正
- 変更時は `ops/decisions/` に理由を残す

### /prompts
- AIに与える指示の正式資産
- プロンプト変更＝挙動変更とみなす

### /sites
- サイト別の差分管理
- 記事単位で履歴を残す

### /data
- GSC・結果の証跡
- 感覚ではなく事実で判断するための置き場

---

## 6. 成功判定（Agent終了条件）

以下が成立した時、
このリポジトリは **「完成フェーズ」**に入る。

- モデルサイトで3〜5記事が安定インデックス
- 同一文体・構造で再現可能
- 手順書を見れば第三者が回せる

---

## 7. 最重要原則

> **記事を作るな。  
> 型を作れ。  
> AIを使うな。  
> AIを管理せよ。**

---

## 8. 変更ポリシー

- ルール変更は必ず記録する
- 成果が出ない場合は  
  記事ではなく **Agent設計を疑う**

