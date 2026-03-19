# PLAN: 前処理パイプライン + 論文フルスクラッチ

## Background
- 阿修羅・文殊レビューで14文献中5本（Ref[3],[5],[6],[8],[9]）の書誌情報にハルシネーション検出
- 29%の書誌捏造率 → パッチ修正ではなくフルスクラッチで合意済み
- 分析コード・統計結果自体は問題なし（文殊B-25,B-27で確認済み）

## Goals
- CrossRef APIで全文献の書誌情報を機械的に検証するスクリプトを作る
- manuscript.mdをフルスクラッチで書き直し、REVIEW-REPORTの全P1/P2指摘を解消する
- 再利用可能な前処理パイプラインとして、今後の論文作成でも使えるようにする

## Non-Goals
- 分析コード（analysis.py, plots.py等）の変更
- 新しい統計分析の追加
- statcheck（統計値の機械的検証）の実装（今回はCrossRefのみ）

## Test Strategy
- 前処理パイプライン: 既知のハルシネーション5本（Ref[3],[5],[6],[8],[9]）を検出できるか
- 論文: フルスクラッチ後に阿修羅・文殊レビュー2回目（別セッション）

---

## Phase 1: CrossRef API照合スクリプト ✅ COMPLETE
**変更対象:** `verify_references.py`（新規作成）
**ブリーフ:** manuscript.mdのReferencesセクションをパースし、CrossRef APIで各文献の書誌情報を照合。不一致・未発見を報告し、正しい書誌情報+DOIを提示する。

### タスク
- [x] References パーサー（番号付き参照リストを構造化データに変換）
- [x] CrossRef API クライアント（検索 + メタデータ取得 + 複数候補からベスト選択）
- [x] 照合ロジック（著者名・年・ジャーナル名・巻号の比較、略称対応）
- [x] レポート生成（ターミナル出力 + JSON保存）
- [x] テスト実行: 旧manuscript.mdで既知の5本を全検出確認

### 成功基準
- [x] Ref[3],[5],[6],[8],[9]の5本全てでMISMATCHを報告（5/5検出）
- [x] 正常な文献でfalse positive 0（Ref[1],[2],[4],[7],[10],[11],[14]全MATCH + [12],[13] URL_ONLY）
- [x] 全12学術文献のDOI取得済み

---

## Phase 2: 論文フルスクラッチ ✅ COMPLETE
**変更対象:** `manuscript.md`（全面書き直し）

### タスク
- [x] results_summary.txtの全数値を確認（27項目チェック全PASS）
- [x] 参考文献リストをPubMed/CrossRef検証済みの正確な情報で全面更新（DOI付き）
- [x] Abstract書き直し（318語、略語NB/df/AIC/IRR/CI全定義）
- [x] Introduction書き直し（正確な書誌情報での引用）
- [x] Methods書き直し（倫理条文番号、バイアス緩和策、欠損データ、両側検定追加）
- [x] Results書き直し（AIC値、感度分析IRR追加、死亡数正確値）
- [x] Discussion書き直し（正確な著者名での引用）
- [x] 全セクション間の整合性チェック
- [x] verify_references.py で最終照合（12/12 MATCH）
- [x] PDF再生成（70KB）

### 成功基準
- [x] verify_references.pyで全文献がMATCH（12/12 MATCH + 2 URL_ONLY）
- [x] REVIEW-REPORTのP1全5件が解消
- [x] REVIEW-REPORTのP2全12件が解消
- [x] Abstract 350語以下（318語）
- [x] results_summary.txtとの数値完全一致（27/27 PASS）

---

## 残: 阿修羅・文殊レビュー2回目（別セッション）
- フルスクラッチ後の論文に対して再実行
- システムのテスト2回目も兼ねる

## Risk / Trade-offs
| リスク | 影響 | 対策 |
|--------|------|------|
| CrossRef APIで見つからない文献 | 照合不能 | PubMed API をフォールバックとして使用 → 実際にRef[3],[6],[9]でPubMed使用 |
| フルスクラッチで新たなエラー導入 | 退行バグ | 書き直し後に阿修羅・文殊レビュー2回目（別セッション） |
| セッション内で完了しない | 中断リスク | Phase 1, 2とも完了。レビュー2回目のみ別セッション |
