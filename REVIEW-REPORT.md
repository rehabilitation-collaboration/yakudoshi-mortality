# Review Report: Yakudoshi and Mortality

Date: 2026-03-19
System: Asura(Sonnet x3) + Monju(Opus x1)
Pre-processing: Not run (pipeline not yet implemented)

---

## Critical Findings (P1) — 修正必須

| # | ID | Issue | Source | Action Required |
|---|-----|-------|--------|----------------|
| 1 | D-01/D-02 | Ref [3]: 著者名・article numberが架空。実際はRanganathan S et al., Ann Surg Open 2024;5(2):e375 | Monju-independent | PubMed (PMID 38883950) で正しい書誌情報を確認し修正 |
| 2 | D-02 | Ref [5]: 著者名・タイトル・巻・頁が全て誤り。実際はYang CH, Huang YT, Janes C, Lin KC, Lu TH. Soc Sci Med 2008;66(9):1990-1998 | Monju-independent | PubMed (PMID 18313821) で修正 |
| 3 | D-02 | Ref [6]: 著者名・article numberが誤り。実際はLin SM, Wang JH, Huang LK, Huang HK. BMJ Open 2019;9(4):e025762 | Monju-independent | PubMed (PMID 31005924) で修正 |
| 4 | D-02 | Ref [9]: 巻・頁・タイトルが誤り。実際はSmith G. "Scared to death?" BMJ 2002;325(7378):1442-1443 | Monju-independent | PubMed (PMID 12493656) で修正 |
| 5 | C-03 | 倫理審査の承認/免除番号なし。自己判断での免除主張のみ | Asura(3/3) | 免除の根拠条項（ガイドライン条文番号）を明記 |

## Important Findings (P2) — 修正推奨

| # | ID | Issue | Source | Action Required |
|---|-----|-------|--------|----------------|
| 1 | D-02 | Ref [8]: 著者帰属が不正確。実際の筆頭著者はPanesar NS、共著者6名あり。"Panesar SS"は存在しない | Monju-independent | PubMed (PMID 14636150) で修正 |
| 2 | D-06 | 一部の関連文献が欠落している可能性（Nahya 2002等） | Monju-independent | 網羅性を再確認 |
| 3 | D-07 | Ref [5]の本文中記述と書誌エントリの不一致（内容は正しいがメタデータが架空） | Monju-independent | D-02修正で解消 |
| 4 | C-02 | IRB免除の正式な条項・カテゴリ番号が未記載 | Asura(2/3) | 該当条文を特定して引用 |
| 5 | A-10 | Methods内にバイアス緩和策の記述なし（Discussionのみ） | Asura(2/3) | STROBE推奨に従いMethodsで言及 |
| 6 | A-13 | 欠損データの取扱い記述なし | Asura(2/3) | 「欠損なし」等の明示的記載を追加 |
| 7 | B-07 | 片側/両側検定の指定なし（全検定で未記載） | Asura(3/3) | 「全て両側検定」等を明記 |
| 8 | B-19 | AIC値が未報告（選択基準として使用しているのに数値なし） | Asura(3/3) | 主要モデルのAIC値をテーブルまたは補足で報告 |
| 9 | B-20 | 外れ値の取扱い記述なし（78年間に戦時・COVID含む） | Asura(3/3) | 外れ年の影響について言及（年スプラインで吸収、または年代別感度分析で対応済みと記載） |
| 10 | B-24 | 一部感度分析でIRR/CIが未報告（p値のみ） | Asura(3/3) | 年代別・年齢範囲の感度分析にIRR/CI追加 |
| 11 | B-15 | 死亡数が「approximately」表記で正確値なし | Asura(2/3) | 正確な合計値を報告 |
| 12 | E-03 | AbstractでIRR, AIC, CI, dfが初出時に未定義 | Asura(3/3) | Abstractで初出時に展開（少なくともIRRとAIC） |

## Minor Findings (P3) — 任意

| # | ID | Issue | Source | Action Required |
|---|-----|-------|--------|----------------|
| 1 | D-02 | Ref [13]: 日付・バージョン番号なし、共著者Riffe T欠落 | Monju-independent | 最新版の情報で更新 |
| 2 | D-03 | 全14文献でDOI未記載 | Monju-independent | 可能な限りDOI追加 |
| 3 | C-09 | 著者貢献がCRediT形式でない（単著なので影響小） | Asura(3/3) | ターゲットジャーナルの要件に応じて対応 |

## Rejected by Monju（文殊が棄却）

| # | Asura Finding | Rejection Reason |
|---|--------------|-----------------|
| 1 | A-15: 一部感度分析の目的が不明確 | 各分析の目的は文脈から自明。#7「局所残差窓の変更」はロバスト性検証の一環として明確 |
| 2 | A-16: Per-age分析の「探索的」ラベルがResults本文で不十分 | Methodsで明記 + Table題に(Exploratory) + Results本文で"nominally"使用。十分なラベリング |
| 3 | B-06: 名目有意水準alpha=0.05が明示されていない | Bonferroni補正の式「0.05/4」にalpha=0.05が明示的に含まれている |
| 4 | B-08: 二次・Per-age分析の多重比較文脈が不十分 | 「Sensitivity and per-age analyses were interpreted descriptively」と明記されており、これが当該分析の多重比較方針 |
| 5 | B-09: p値報告の軽微な不整合 | 全p値をAbstract・本文・テーブル間で照合したが不整合は確認できず |
| 6 | B-17: 率の期間・母集団単位（per 100,000等）未記載 | offset付き回帰モデルではIRR（無次元比）が出力であり、「per N人」の乗数は不要 |
| 7 | C-01: ヘルシンキ宣言への言及なし | ヘルシンキ宣言はヒト対象研究に適用。本研究は匿名化済み公開集計データの二次分析であり、引用は不要 |
| 8 | A-12: サンプルサイズの正当化が薄い | 全数調査（population census）では標本サイズ計算は不適切。論文の説明は正確かつ完全 |

## Review Statistics

- Asura: 49 items x 3 agents
  - Agent 1: 15 findings (P1:2, P2:11, P3:2)
  - Agent 2: 22 findings (P1:1, P2:15, P3:6)
  - Agent 3: 18 findings (P1:1, P2:13, P3:4)
- Aggregation: 20 findings (2/3+), 7 reference-only (1/3)
- Monju verification: ACCEPT 12 / REJECT 8
- Monju independent: 8 findings (P1:3, P2:3, P3:2)
- Pre-processing: Not run

## Key Observation

14文献中4本（29%）の書誌情報にAIハルシネーションの痕跡あり。本文中の引用文脈は正確（著者は各論文の内容を理解している）だが、Reference listのメタデータ（著者名、巻号、頁数、article number）が捏造されている。Claudeによる執筆支援を使用した論文に特有のパターン。投稿前にPubMed/CrossRefで全文献の書誌情報を検証することを強く推奨する。
