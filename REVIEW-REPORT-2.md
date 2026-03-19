# Review Report: Yakudoshi and Mortality (2nd Review)

Date: 2026-03-19
System: Asura(Sonnet x3) + Monju(Opus x1)
Pre-processing: CrossRef API verification (12/12 MATCH, 0 MISMATCH, 2 URL_ONLY)
Previous review: REVIEW-REPORT.md (P1:5, P2:12, P3:3 -- all addressed in rewrite)

---

## Critical Findings (P1) -- None

No P1 findings. All 5 P1 issues from the 1st review have been resolved.

## Important Findings (P2) -- 2 items

| # | ID | Issue | Source | Action Required |
|---|-----|-------|--------|----------------|
| 1 | B-11/B-16 | Table 4: Poisson model rows show "--" for 95% CI. IRR reported without uncertainty estimate. Even if Poisson CIs are unreliable due to overdispersion, they should be reported (with a note) or the omission explained | Asura(3/3) | Either add Poisson CIs with a caveat note, or add a footnote explaining why CIs are omitted for the Poisson rows |
| 2 | B-24 | Sensitivity analysis results (all 7 analyses) report only IRR and p-value, no 95% CIs. Prevents quantitative comparison with primary estimates | Asura(2/3) | Add CIs to sensitivity analysis results, at minimum for Table 5 (spline df) and the in-text results (era, offset, age range) |

## Minor Findings (P3) -- 9 items

| # | ID | Issue | Source | Action Required |
|---|-----|-------|--------|----------------|
| 1 | A-12 | No minimum detectable effect size stated. Full-population justification is valid but an a priori statement of detectable IRR would strengthen the paper | Asura(3/3), Monju downgraded from P2 | Optional: add a sentence about minimum detectable effect size given the population |
| 2 | B-08 | Three parallel tests in local residual method (Wilcoxon, Mann-Whitney, permutation) are triangulation, not independent hypotheses, but this is not explicitly stated | Asura(3/3), Monju downgraded from P2 | Optional: add a brief note that these are confirmatory/triangulation tests |
| 3 | B-19 | AIC values reported only for selected model (df=9). AIC for alternative df (3,5,7) not shown. Table 5 sensitivity results partially compensate | Asura(3/3), Monju downgraded from P2 | Optional: add AIC values for df=3,5,7 in Table 5 or a supplementary table |
| 4 | C-10 | No ICMJE COI disclosure form referenced. Simple declaration present ("no competing interests") | Asura(3/3), Monju downgraded from P2 | Journal-dependent. Add ICMJE form reference if required by target journal |
| 5 | A-16 | Local residual window sensitivity results not labeled "exploratory" (unlike per-age analyses). Context makes it clear but labeling is inconsistent | Asura(2/3), Monju downgraded from P2 | Optional: add "exploratory" or "descriptive" label to residual window sensitivity |
| 6 | C-09 | Author contributions not in CRediT taxonomy format. Single-author paper reduces impact | Asura(3/3) | Journal-dependent. Convert to CRediT format if required |
| 7 | E-03 | "hon-yaku" used in Methods without prior definition in Introduction (mae-yaku and ato-yaku are defined) | Asura(2/3) | Add brief definition of hon-yaku in Introduction where mae-yaku/ato-yaku are defined |
| 8 | D-06 | Could cite Japanese anthropological sources on yakudoshi beliefs for additional cultural context, though current citations are adequate | Monju-independent | Optional: consider adding Murase or similar ethnographic references |
| 9 | E-05 | Figures 1-3 are captions only in manuscript (no embedded images). Cannot verify if figures are self-contained | Monju-independent | Ensure figures are included in submission package |

## Rejected by Monju

| # | Asura Finding | Rejection Reason |
|---|--------------|-----------------|
| 1 | C-03 (P1): No IRB approval/exemption number | For publicly available aggregate data in Japan, Article 3, Para 1, Item 1 of the cited guideline defines exemption directly by law. No IRB submission occurs, so no tracking number exists. Standard practice for aggregate public data analysis |
| 2 | C-02 (P1): IRB exemption self-declared | Same reasoning. The law defines the exemption criteria; no institutional body reviews cases that are exempt by legal definition |
| 3 | B-21 (P1): Software versions future/unreleased | Web search confirms all versions released by March 2026: Python 3.14 (Oct 2025), pandas 3.0 (Jan 2026), NumPy 2.4 (Dec 2025), SciPy 1.17 (Jan 2026), matplotlib 3.10 (Dec 2024). Asura's assessment was based on 2025 knowledge cutoff |
| 4 | A-24 (P2): Abstract omits d=-0.23 from sensitivity | Abstract correctly reports primary analysis values (d=0.02-0.11). The d=-0.23 is from a sensitivity analysis (window +/-5), not the primary. Including sensitivity values in abstract's primary results would be misleading. Body text fully discloses the sensitivity range |
| 5 | B-06 (P2): Alpha=0.05 not explicitly stated | "0.05/4" in the Bonferroni calculation makes the base alpha=0.05 explicit. Combined with "All statistical tests were two-sided," this is sufficiently clear |
| 6 | C-01 (P2): No Helsinki Declaration statement | Helsinki Declaration applies to human subjects research. This study uses publicly available aggregate statistics with no individual-level data. The Declaration is not applicable; citing Japanese ethical guidelines is appropriate |
| 7 | B-09 (P2): "n.s." in Table 5 Direction column | "n.s." is a categorical label in the Direction column (alongside "Higher"/"Lower"), not a substitute for a p-value. P-values are reported in their own column. Rounding (0.055 from 0.054717) is within standard 3-decimal-place precision |
| 8 | B-15 (P2/P3): Person-years not reported | Standard practice in rate models with offset. The offset implicitly contains exposure. Downgraded to not required, though reporting total person-years would be informative |
| 9 | B-10 (P3): "<0.001" formatting | Confirmed correct. p=0.0004 reported as "<0.001" is accurate |

## Comparison with 1st Review

| Metric | 1st Review | 2nd Review | Change |
|--------|-----------|-----------|--------|
| P1 (Critical) | 5 | 0 | -5 (all resolved) |
| P2 (Important) | 12 | 2 | -10 |
| P3 (Minor) | 3 | 9 | +6 (deeper review) |
| Total | 20 | 11 | -9 |
| Monju REJECT rate | 8/20 (40%) | 9/18 (50%) | +10pp |

Key improvement: All bibliographic hallucinations (4 fabricated references) and ethics citation issues from 1st review are fully resolved. CrossRef API pre-processing confirms 12/12 MATCH with 0 MISMATCH.

## Review Statistics

- Asura: 49 items x 3 agents
  - Agent 1: 18 findings (P1:3, P2:8, P3:7) -- checked 49/49
  - Agent 2: 24 findings (P1:1, P2:16, P3:7) -- checked 49/49
  - Agent 3: 14 findings (P1:0, P2:6, P3:8) -- checked 49/49
- Aggregation: 18 findings (2/3+), 11 reference-only (1/3)
- Monju verification: ACCEPT 9 / REJECT 9
- Monju independent: 2 findings (P3:2)
- Pre-processing: CrossRef API (12/12 MATCH, 2 URL_ONLY, 0 MISMATCH)

## Conclusion

The manuscript is in strong shape after the full rewrite. **P1 issues: 0.** The 2 remaining P2 items (missing CIs in Table 4 Poisson rows and sensitivity analyses) are straightforward to fix. The 9 P3 items are minor and largely journal-dependent. The paper is ready for medRxiv submission after addressing the P2 items.
