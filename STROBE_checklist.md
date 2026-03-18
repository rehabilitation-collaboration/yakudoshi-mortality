# STROBE Statement — Checklist of Items for Cohort Studies

**Manuscript:** Yakudoshi and Mortality: A Population-Based Analysis of Japan's Age-Specific Superstition Using 78 Years of National Data

| Item No | Item | Recommendation | Reported on page/section |
|---------|------|---------------|--------------------------|
| **Title and abstract** | | | |
| 1 | (a) Indicate the study's design with a commonly used term in the title or the abstract | "Population-based retrospective analysis" in title and abstract | Title, Abstract |
| | (b) Provide in the abstract an informative and balanced summary of what was done and what was found | Structured abstract with Background/Methods/Results/Conclusions | Abstract |
| **Introduction** | | | |
| 2 | Background/rationale: Explain the scientific background and rationale for the investigation being reported | Yakudoshi cultural context, prior superstition-health literature, gap in evidence | Introduction, para 1-3 |
| 3 | Objectives: State specific objectives, including any prespecified hypotheses | "We test whether all-cause mortality is elevated at yakudoshi ages" | Introduction, final para |
| **Methods** | | | |
| 4 | Study design: Present key elements of study design early in the paper | "Population-based retrospective analysis" | Methods, Study Design |
| 5 | Setting: Describe the setting, locations, and relevant dates | Japan, 1947-2024, JMD database | Methods, Study Design |
| 6 | Participants: (a) Give eligibility criteria, sources and methods of selection. Describe methods of follow-up. (b) For matched studies, give matching criteria and number of exposed and unexposed | Ages 15-80, complete national data, yakudoshi (exposed) vs non-yakudoshi (unexposed) ages defined | Methods, Study Design + Yakudoshi Age Definitions |
| 7 | Variables: Clearly define all outcomes, exposures, predictors, potential confounders, and effect modifiers | Outcome: death counts; Exposure: yakudoshi indicator; Confounders: age (spline), year (spline) | Methods, Statistical Analysis |
| 8 | Data sources/measurement: For each variable of interest, give sources of data and details of methods of assessment | JMD (Deaths_1x1.txt, Exposures_1x1.txt, Mx_1x1.txt); kazoedoshi conversion method | Methods, Study Design + Yakudoshi Age Definitions |
| 9 | Bias: Describe any efforts to address potential sources of bias | Ecological bias acknowledged; spline flexibility tested; two kazoedoshi offsets tested; Bonferroni correction applied | Methods, Sensitivity Analyses + Discussion, Limitations |
| 10 | Study size: Explain how the study size was arrived at | Complete national dataset 1947-2024; no sampling — full population used | Methods, Study Design |
| 11 | Quantitative variables: Explain how quantitative variables were handled in the analyses | Age modelled by cubic regression spline (df selected by AIC); year modelled by spline (df=3); exposure as offset | Methods, Statistical Analysis |
| 12 | Statistical methods | | |
| | (a) Describe all statistical methods, including those used to control for confounding | NB2 regression with age spline + year spline; local residual method | Methods, Statistical Analysis |
| | (b) Describe any methods used to examine subgroups and interactions | Male/female fitted separately; per-age analysis; era stratification | Methods, Statistical Analysis |
| | (c) Explain how missing data were addressed | JMD has no missing values in the analysis range (complete national registration) | Methods, Study Design |
| | (d) If applicable, explain how loss to follow-up was addressed | N/A — aggregate cross-sectional mortality data, no individual follow-up | — |
| | (e) Describe any sensitivity analyses | 7 pre-specified sensitivity analyses described | Methods, Sensitivity Analyses |
| **Results** | | | |
| 13 | Participants: (a) Report numbers at each stage. (b) Give reasons for non-participation. (c) Consider flow diagram | 5,148 age-year cells per sex; no exclusions within analysis range | Results, Study Population |
| 14 | Descriptive data: (a) Give characteristics of study participants. (b) Indicate missing data. (c) Summarise follow-up time | ~25.4M male and ~16.6M female deaths; 78 years of observation; no missing data | Results, Study Population |
| 15 | Outcome data: Report numbers of outcome events or summary measures over time | Death counts and IRRs reported; Figure 1 shows mortality curves over time | Results, Tables 1-5 + Figures |
| 16 | Main results: (a) Give unadjusted and adjusted estimates with precision. (b) Report category boundaries. (c) Consider absolute risk | IRR with 95% CI for all analyses; adjusted for age and year via splines | Results, Primary Analysis (Table 1) |
| 17 | Other analyses: Report subgroup, interaction, and sensitivity analyses | 7 sensitivity analyses reported; per-age analysis; era stratification | Results, Sensitivity Analyses |
| **Discussion** | | | |
| 18 | Key results: Summarise key results with reference to study objectives | No consistent yakudoshi effect; direction reversal with model specification | Discussion, Principal Findings |
| 19 | Limitations: Discuss limitations, including sources of potential bias | 6 limitations discussed (all-cause only, ecological design, kazoedoshi uncertainty, unmeasured belief, behavioural outcomes, model sensitivity) | Discussion, Strengths and Limitations |
| 20 | Interpretation: Give a cautious overall interpretation | Results are artifacts of age-curve modelling; consistent with prior null findings for superstitions | Discussion, Principal Findings + Comparison |
| 21 | Generalisability: Discuss the generalisability of the study results | Internal validity high (full population); external validity limited to yakudoshi-specific context; generalises to broader superstition-mortality question | Discussion, Generalisability |
| **Other information** | | | |
| 22 | Funding: Give the source of funding and the role of the funders | "This research received no specific funding" | Funding |

## Notes

- This checklist follows the STROBE Statement (von Elm et al., BMJ 2007; PLoS Med 2007)
- Reference: https://www.strobe-statement.org/checklists/
- Items marked N/A are not applicable to this study design (aggregate mortality data rather than individual-level cohort)
