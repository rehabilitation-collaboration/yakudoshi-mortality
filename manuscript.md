# Yakudoshi and Mortality: A Population-Based Analysis of Japan's Age-Specific Superstition Using 78 Years of National Data

Mizuki Shirai (ORCID: 0009-0005-3615-0670)

Rehabilitation Collaboration (NPO), Japan

**Corresponding author:** Mizuki Shirai, Rehabilitation Collaboration (NPO), Japan. Email: rehabilitation.collaboration@gmail.com

---

## Abstract

**Background:** Yakudoshi (unlucky years) is one of the most widely observed superstitions in Japan, in which certain ages are believed to bring calamity, illness, or death. Despite its cultural significance, no epidemiological study has examined whether mortality rates are actually elevated at yakudoshi ages. We investigated whether all-cause mortality is associated with yakudoshi ages in the Japanese population.

**Methods:** We conducted a population-based retrospective analysis using the Japanese Mortality Database (JMD), covering 1947-2024 (78 years). Yakudoshi ages were defined as 25, 42, and 61 for males and 19, 33, 37, and 61 for females (in kazoedoshi, the traditional Japanese counting system), converted to Western age equivalents. The primary analysis used negative binomial (NB) regression with cubic regression splines modelling the age-mortality relationship (degrees of freedom [df] selected by Akaike Information Criterion [AIC]) and a binary yakudoshi indicator. A secondary local residual method compared mortality at yakudoshi ages to neighbouring ages. Seven pre-specified sensitivity analyses examined robustness. All statistical tests were two-sided.

**Results:** The dataset comprised 25,420,603 male and 16,635,743 female deaths (ages 15-80). Poisson regression showed substantial overdispersion (deviance/df = 71-89). NB regression found that males had nominally significant *lower* mortality at yakudoshi ages (incidence rate ratio [IRR] 0.97, 95% confidence interval [CI] 0.94-0.99, p = 0.004) -- opposite to prediction -- while females showed no significant association (IRR 1.02, 95% CI 1.00-1.05, p = 0.055). Critically, the direction of association reversed for both sexes depending on spline flexibility (male IRR 0.97-1.04; female IRR 0.96-1.02 across df = 3-9), demonstrating model dependence. The local residual method showed negligible effect sizes (Cohen's d = 0.02-0.11).

**Conclusions:** We found no evidence of a consistent yakudoshi effect on mortality. Apparent associations were contradictory between sexes and reversed with model specification, indicating artefacts of age-curve modelling. This first epidemiological examination of yakudoshi adds to literature demonstrating that culturally significant "unlucky" periods do not influence population-level mortality.

**Keywords:** yakudoshi, superstition, mortality, Japan, epidemiology, cultural belief, negative binomial regression

---

## Introduction

Superstitions about unlucky numbers, dates, and periods exist in cultures worldwide, and several have been subjected to epidemiological scrutiny. Studies have examined whether Friday the 13th increases traffic accidents [1,2] or surgical complications [3], whether the number four elevates cardiac mortality among Chinese and Japanese Americans [4], whether the Chinese Ghost Month affects drowning deaths [5], whether the Chinese New Year holiday period influences in-hospital mortality [6], and whether discharge from hospital is delayed to avoid unlucky days of the Japanese lunar calendar [7]. The findings have been mixed: initial studies sometimes report significant associations [1,4], but subsequent replications with larger samples and improved methodology typically fail to confirm them [2,3,8,9]. Austin et al. demonstrated that apparent associations between astrological signs and health outcomes are artefacts of multiple comparisons, disappearing entirely in validation cohorts [10].

Japan has a rich tradition of calendar-based superstitions influencing health-related behaviour. Kaku documented that the folk belief in Hinoe-Uma (the "Fire Horse" year of the sexagenary cycle) caused a dramatic decline in the Japanese birth rate in 1966 through increased induced abortions -- a striking demonstration of superstition's power to alter population-level vital statistics [11]. Hira et al. showed that belief in the six-day lunar calendar (Taian-Butsumetsu) influences the timing of hospital discharge, with patients preferring to leave on "lucky" days [7].

Yakudoshi (literally "calamity year") is one of the most widely observed superstitions in Japan. The belief holds that certain ages bring heightened vulnerability to misfortune, illness, and death. For males, the yakudoshi ages are 25, 42, and 61; for females, 19, 33, 37, and 61 -- all expressed in kazoedoshi, the traditional Japanese age-counting system in which a person is one year old at birth and gains a year every New Year's Day rather than on their birthday. The year before yakudoshi (mae-yaku) and after (ato-yaku) are also considered inauspicious.

Among these, the "great calamity years" (taiyaku) hold particular cultural significance: age 42 for men and 33 for women. The male taiyaku of 42 carries additional weight because 42 can be read as "shi-ni," meaning "unto death" in Japanese -- a linguistic association that reinforces the superstition through numerological wordplay. Similarly, the female taiyaku of 33 can be read as "sanzan," meaning "terrible" or "disastrous."

The cultural impact of yakudoshi is substantial. Millions of Japanese visit Shinto shrines and Buddhist temples annually for yakuyoke or yakubarai -- ritual purification ceremonies intended to ward off the calamities of yakudoshi. The practice reflects a genuine, widespread belief that these specific ages carry elevated risk, yet no study has empirically examined whether mortality at yakudoshi ages actually differs from what would be expected given the overall age-mortality relationship.

This study aims to provide the first epidemiological investigation of yakudoshi. Using 78 years of national mortality data from the Japanese Mortality Database, we test whether all-cause mortality is elevated at yakudoshi ages after accounting for the smooth, age-dependent increase in mortality risk.

---

## Methods

### Study Design and Data Source

We conducted a population-based retrospective analysis of age-specific mortality in Japan using the Japanese Mortality Database (JMD), maintained by the National Institute of Population and Social Security Research (IPSS) [12]. The JMD provides annual death counts, population exposure (person-years), and central death rates (Mx) by single year of age and sex for Japan from 1947 to 2024. The JMD methodology is compatible with the Human Mortality Database (HMD) protocol, ensuring international comparability [13].

We used three JMD data files: death counts (Deaths_1x1.txt), population exposure (Exposures_1x1.txt), and death rates (Mx_1x1.txt), all in the 1x1 format (single year of age x single calendar year). The analysis was restricted to ages 15-80 to exclude infant and child mortality patterns, which follow a distinct J-shaped curve, and extreme old-age mortality, which is subject to greater measurement uncertainty. The study used the complete national dataset for the entire period available (1947-2024); no sample size calculation was performed because the analysis encompassed the full population rather than a sample. The JMD data contained no missing values within the analysis age range (15-80) for either sex across all 78 years.

### Ethical Considerations

This study used publicly available, de-identified aggregate statistics from a national database maintained by a government-affiliated research institute. No individual-level data were accessed. The study was therefore exempt from institutional review board approval under the Ethical Guidelines for Medical and Biological Research Involving Human Subjects (Ministry of Education, Culture, Sports, Science and Technology / Ministry of Health, Labour and Welfare, Japan, 2021 revision), Article 3, Paragraph 1, Item 1, which exempts research that uses only publicly available information that cannot identify specific individuals.

### Yakudoshi Age Definitions

Yakudoshi ages are traditionally defined in kazoedoshi. Because the JMD records age in Western years (mannenrei), conversion was necessary. A person of kazoedoshi age N is approximately mannenrei N-1 (after their birthday in a given year) or N-2 (before their birthday). For the primary analysis, we used an offset of 1 (kazoedoshi minus 1), yielding the following mannenrei equivalents:

- **Males:** 24, 41, 60 (from kazoedoshi 25, 42, 61)
- **Females:** 18, 32, 36, 60 (from kazoedoshi 19, 33, 37, 61)

Adjacent years (mae-yaku and ato-yaku, +/-1 year from each hon-yaku) were examined separately. This dual-calendar approach follows Panesar et al., who tested the "deadly number four" hypothesis using both Gregorian and lunar calendar dates [8].

### Statistical Analysis

#### Primary Analysis: Negative Binomial Regression

We modelled death counts using negative binomial regression with a log link and log-transformed population exposure as an offset:

log(E[Deaths]) = log(Exposure) + f(Age) + beta_1 x Yakudoshi + g(Year)

where f(Age) is a cubic regression spline with degrees of freedom selected by Akaike Information Criterion (AIC), Yakudoshi is a binary indicator (1 for yakudoshi ages, 0 otherwise), and g(Year) is a cubic regression spline with 3 degrees of freedom to account for the nonlinear secular decline in mortality over 78 years. The coefficient beta_1 was exponentiated to obtain the incidence rate ratio (IRR) with 95% confidence intervals. Models were fitted separately for males and females.

Negative binomial regression was chosen over Poisson regression because mortality data aggregated across 78 years of substantial demographic change exhibited severe overdispersion (deviance/df >> 1 under the Poisson model), which would have inflated type I error rates. We used the NB2 parametrization, where Var(Y) = mu + alpha x mu^2. The dispersion parameter alpha was estimated independently for each sex using a two-stage AIC-based grid search (coarse search over log10(alpha) in [-4, 2], then fine search around the optimum with step 0.05). Alpha was estimated from a null model without the yakudoshi indicator to avoid circularity. We report Poisson results as a sensitivity analysis for comparison. For the spline flexibility sensitivity analysis, alpha was held constant at the primary estimate to isolate the effect of spline degrees of freedom.

We also fitted individual models for each yakudoshi age to examine age-specific effects. Per-age analyses were considered exploratory and are reported without multiple comparison adjustment.

#### Potential Sources of Bias

This study used a complete national population dataset, minimising selection bias. The principal source of potential bias is residual confounding: because the data are aggregate (ecological), individual-level confounders such as socioeconomic status, health behaviour, and strength of yakudoshi belief could not be adjusted for. The 78-year span includes periods of substantial demographic change (postwar baby boom, rapid economic growth, ageing society), which could introduce temporal confounding. We addressed this by including a year spline in the regression model and by conducting era-stratified sensitivity analyses. The kazoedoshi-to-mannenrei conversion introduces a systematic 1-2 year uncertainty in the exposed ages, addressed through sensitivity analysis with two offset values.

#### Secondary Analysis: Local Residual Method

To maintain continuity with a prior preliminary analysis and to provide a model-free comparison, we computed local residuals for each age in each year:

residual(age, year) = log(Mx_age,year) - mean(log(Mx_j,year)) for j in [age-3, age+3], j != age

This approach compares the mortality rate at each age to the average of its three nearest neighbours on each side, effectively removing the local age trend. Residuals at yakudoshi ages were compared to residuals at non-yakudoshi ages using the one-sample Wilcoxon signed-rank test (testing whether yakudoshi residuals differ from zero), the Mann-Whitney U test (comparing yakudoshi versus non-yakudoshi distributions), and a permutation test (100,000 permutations). Effect sizes were quantified using Cohen's d (mean difference between yakudoshi and non-yakudoshi residuals divided by the pooled standard deviation).

#### Sensitivity Analyses

We conducted seven pre-specified sensitivity analyses:

1. **Poisson versus negative binomial:** Comparing results under both distributional assumptions to quantify the impact of overdispersion.
2. **Kazoedoshi conversion offset:** Using offset 2 (kazoedoshi minus 2) instead of offset 1.
3. **Mae-yaku and ato-yaku inclusion:** Expanding the yakudoshi indicator to include the year before and after each hon-yaku age.
4. **Spline flexibility:** Varying the spline degrees of freedom (3, 5, 7, 9) to assess model dependence.
5. **Historical era:** Stratifying by postwar (1947-1960), high-growth (1961-1990), and modern (1991-2024) periods to assess whether effects vary across eras of differing cultural influence and demographic composition. The 78-year span includes extreme mortality environments (wartime aftermath, COVID-19 pandemic); year splines absorb secular trends, and era stratification further examines temporal robustness.
6. **Age range:** Narrowing to 20-70 and widening to 15-90 to assess sensitivity to the analysis window.
7. **Local residual window:** Varying the neighbour window from +/-2 to +/-5 ages.

#### Multiple Comparisons

Four primary comparisons were pre-specified (male/female x hon-yaku only/with mae-ato-yaku). A Bonferroni-corrected significance threshold of alpha = 0.0125 (0.05/4) was applied to the primary analysis. All statistical tests were two-sided. Sensitivity and per-age analyses were interpreted descriptively.

### Software

All analyses were conducted in Python 3.14 using pandas 3.0, NumPy 2.4, SciPy 1.17, statsmodels 0.14, patsy 1.0, and matplotlib 3.10. Analysis code was developed with the assistance of Claude (Anthropic, claude-opus-4-20250514), an AI language model (see Acknowledgments for full AI disclosure); the author reviewed, tested, and takes full responsibility for all code and results. Analysis code is available at https://github.com/rehabilitation-collaboration/yakudoshi-mortality.

---

## Results

### Study Population

The JMD dataset comprised 78 years of observation (1947-2024) across ages 15-80, yielding 5,148 age-year cells per sex. Within the analysis age range (15-80), the data encompassed 25,420,603 male deaths and 16,635,743 female deaths (Figure 1). The dataset contained no missing values.

### Model Selection and Overdispersion

AIC-based model selection favoured 9 degrees of freedom for the age spline in both sexes (male AIC = 77,910; female AIC = 74,244). Poisson regression showed substantial overdispersion, with deviance-to-residual-degrees-of-freedom ratios of 71.1 (males) and 89.0 (females), confirming that the Poisson variance assumption was violated and that standard Poisson p-values would be unreliable. The negative binomial dispersion parameter was estimated independently for each sex by two-stage AIC grid search, yielding alpha = 0.028 (males) and alpha = 0.040 (females). The resulting deviance/df ratios were 0.99 (males) and 0.95 (females), indicating adequate model fit. All subsequent primary results are from negative binomial regression.

### Primary Analysis: Negative Binomial Regression

Table 1 shows the primary negative binomial regression results. For males, the overall IRR for yakudoshi ages was 0.966 (95% CI 0.944-0.989, p = 0.004), indicating nominally significant but *lower* mortality at yakudoshi ages -- the opposite of what the yakudoshi superstition would predict. For females, the IRR was 1.024 (95% CI 1.000-1.050, p = 0.055), which did not reach nominal significance.

Including mae-yaku and ato-yaku showed a similar pattern: the male IRR was 0.957 (95% CI 0.942-0.973, p < 0.001) and the female IRR was 1.032 (95% CI 1.014-1.050, p < 0.001). While the female result with mae/ato-yaku reached significance, the contradictory directions between sexes -- males showing lower and females showing higher mortality -- are inconsistent with a genuine yakudoshi effect.

**Table 1. Primary Negative Binomial Regression Results**

| Sex | Analysis | IRR | 95% CI | p-value | Direction |
|-----|----------|-----|--------|---------|-----------|
| Male | Hon-yaku only | 0.966 | 0.944-0.989 | 0.004 | Lower |
| Male | With mae/ato-yaku | 0.957 | 0.942-0.973 | <0.001 | Lower |
| Female | Hon-yaku only | 1.024 | 1.000-1.050 | 0.055 | n.s. |
| Female | With mae/ato-yaku | 1.032 | 1.014-1.050 | <0.001 | Higher |

### Per-Age Analysis

Individual yakudoshi ages showed inconsistent effects (Table 2). For males, only age 24 (kazoedoshi 25) reached nominal significance (IRR 0.933, 95% CI 0.896-0.972, p = 0.001), but in the direction of *lower* mortality. Ages 41 (taiyaku, the most feared "death year") and 60 were non-significant. For females, only age 18 (kazoedoshi 19) was nominally significant (IRR 1.057, 95% CI 1.006-1.111, p = 0.029); the taiyaku age of 32 (kazoedoshi 33) was non-significant (IRR 1.033, 95% CI 0.984-1.085, p = 0.196).

**Table 2. Per-Age Negative Binomial Regression Results (Exploratory)**

| Sex | Age (mannenrei) | Kazoedoshi | IRR | 95% CI | p-value |
|-----|-----------------|------------|-----|--------|---------|
| Male | 24 | 25 | 0.933 | 0.896-0.972 | 0.001 |
| Male | 41 | 42 (taiyaku) | 0.971 | 0.933-1.011 | 0.154 |
| Male | 60 | 61 | 0.992 | 0.953-1.032 | 0.676 |
| Female | 18 | 19 | 1.057 | 1.006-1.111 | 0.029 |
| Female | 32 | 33 (taiyaku) | 1.033 | 0.984-1.085 | 0.196 |
| Female | 36 | 37 | 1.021 | 0.973-1.070 | 0.403 |
| Female | 60 | 61 | 0.991 | 0.945-1.038 | 0.695 |

### Secondary Analysis: Local Residual Method

The local residual analysis, which is independent of the regression model specification, showed negligible effect sizes. For males, Cohen's d was +0.024 (p = 0.377), indicating virtually no difference between yakudoshi and non-yakudoshi ages. For females, d was +0.107 (p = 0.032), a small effect that was only nominally significant (Figure 2).

**Table 3. Local Residual Method Results**

| Sex | Mean residual (yakudoshi) | Mean residual (non-yakudoshi) | Cohen's d | p (permutation) |
|-----|--------------------------|-------------------------------|-----------|-----------------|
| Male | -0.001 | -0.003 | +0.024 | 0.377 |
| Female | +0.007 | -0.001 | +0.107 | 0.032 |

### Sensitivity Analyses

Sensitivity analyses demonstrated that the apparent associations were artefacts of model specification (Figure 3).

**Poisson versus negative binomial:** Poisson regression produced nominally significant p-values for both sexes, but these were unreliable due to severe overdispersion (deviance/df = 71-89). Negative binomial regression, with deviance/df near 1.0, provided appropriate variance estimation (Table 4).

**Table 4. Poisson vs Negative Binomial Comparison**

| Sex | Model | IRR | 95% CI | p-value | Deviance/df |
|-----|-------|-----|--------|---------|-------------|
| Male | Poisson | 0.987 | -- | <0.001 | 71.1 |
| Male | Negative Binomial | 0.966 | 0.944-0.989 | 0.004 | 0.99 |
| Female | Poisson | 1.005 | -- | 0.002 | 89.0 |
| Female | Negative Binomial | 1.024 | 1.000-1.050 | 0.055 | 0.95 |

**Spline flexibility:** To isolate the effect of spline flexibility, the dispersion parameter alpha was held constant at the primary estimate while varying the spline degrees of freedom. For males, the IRR was 1.042 (p < 0.001) at df = 3 but reversed to 0.966 (p = 0.004) at df = 9 (the AIC-selected value). For females, the IRR was 0.962 (p = 0.001) at df = 3 but reversed to 1.024 (p = 0.055) at df = 9. The complete reversal of effect direction for both sexes as the spline becomes more flexible strongly suggests that the apparent associations are artefacts of how the age-mortality curve is modelled, not genuine biological signals (Table 5).

**Table 5. Sensitivity to Spline Degrees of Freedom (alpha held constant)**

| Sex | df | IRR | p-value | Direction |
|-----|-----|-----|---------|-----------|
| Male | 3 | 1.042 | <0.001 | Higher |
| Male | 5 | 1.037 | 0.001 | Higher |
| Male | 7 | 1.027 | 0.019 | Higher |
| Male | 9 | 0.966 | 0.004 | Lower |
| Female | 3 | 0.962 | 0.001 | Lower |
| Female | 5 | 0.970 | 0.012 | Lower |
| Female | 7 | 1.014 | 0.264 | n.s. |
| Female | 9 | 1.024 | 0.055 | n.s. |

**Historical era:** No era showed a consistent yakudoshi effect. For males, the growth (1961-1990) and modern (1991-2024) eras showed significantly *lower* mortality at yakudoshi ages (IRR 0.960, p < 0.001 and IRR 0.971, p < 0.001, respectively), while the postwar era was non-significant (IRR 0.979, p = 0.419). For females, only the modern era reached nominal significance (IRR 1.022, p = 0.005). The opposite directions between sexes and inconsistency across eras argue against a genuine effect.

**Kazoedoshi conversion:** Using offset 2 instead of offset 1 rendered both sexes non-significant (male IRR 0.978, p = 0.059; female IRR 1.012, p = 0.356), indicating that the primary results are sensitive to the age conversion assumption.

**Age range:** Narrowing to ages 20-70 eliminated significance for both sexes (male IRR 1.004, p = 0.748; female IRR 1.003, p = 0.804). Widening to 15-90 also rendered both non-significant (male IRR 0.985, p = 0.230; female IRR 1.022, p = 0.109). The primary results were thus specific to the 15-80 age range and did not generalise.

**Local residual window:** Varying the neighbour window from +/-2 to +/-5 ages produced consistent null results for males (Cohen's d < 0.03 for all windows). For females, however, Cohen's d changed direction and magnitude across windows (d = +0.03 at +/-2, +0.11 at +/-3, -0.10 at +/-4, -0.23 at +/-5), indicating that the female local residual result is sensitive to the choice of reference window and does not represent a robust finding.

---

## Discussion

### Principal Findings

This study provides the first epidemiological examination of yakudoshi, the Japanese belief that certain ages bring heightened risk of misfortune and death. Using 78 years of national mortality data encompassing the entire Japanese population, we found no evidence of a consistent yakudoshi effect on all-cause mortality.

Negative binomial regression found a nominally significant association for males only, but in the direction of *lower* mortality -- the opposite of what the yakudoshi superstition predicts. The female association did not reach significance (p = 0.055). Most critically, the direction of association reversed for both sexes when the spline flexibility was varied, demonstrating that the apparent associations are artefacts of age-curve modelling rather than genuine biological signals. The model-free local residual analysis confirmed negligible effect sizes (Cohen's d = 0.02-0.11).

A critical methodological finding was that Poisson regression produced spuriously significant results due to severe overdispersion in the 78-year dataset. Furthermore, the choice of negative binomial dispersion parameter matters substantially: fixing alpha at an arbitrary value can either over- or under-correct for overdispersion. We addressed this by estimating alpha from the data using AIC-based grid search, yielding deviance/df ratios near 1.0 -- indicating appropriate model fit.

### Comparison with Prior Literature

Our findings are consistent with the broader pattern in the superstition-and-health literature. Phillips et al. reported elevated cardiac mortality on the 4th of the month among Chinese and Japanese Americans [4], but Panesar et al. failed to replicate this finding in Hong Kong using both Gregorian and lunar calendar analyses [8], and Smith challenged the original analysis on methodological grounds [9]. Scanlon et al. found increased hospital admissions on Friday the 13th [1], but Radun and Summala demonstrated that this result was likely an artefact of methodological limitations [2]. Ranganathan et al., using over 400,000 surgical cases, found no association between Friday the 13th and adverse surgical outcomes [3]. Lin et al., examining over 190,000 admissions, found elevated mortality during the Chinese New Year holiday but attributed this to reduced staffing and delayed care-seeking rather than superstition [6].

The recurring pattern -- initial positive findings followed by null replications -- has been attributed to small sample sizes, multiple testing, publication bias, and inadequate statistical modelling in the initial studies [2,3]. Our study illustrates an additional pitfall: the sensitivity of results to model specification. The direction reversal with spline flexibility that we observed serves as a cautionary example of how modelling choices can produce spuriously significant results even in large datasets.

Hira et al. demonstrated that a related Japanese superstition (the six-day lunar calendar) does influence hospital discharge behaviour [7], and Kaku documented dramatic effects of the Hinoe-Uma superstition on the 1966 birth rate [11]. The distinction is important: these studies documented the effect of superstition on *behaviour*, not on *mortality*. People may indeed alter their behaviour based on yakudoshi beliefs -- visiting shrines, taking extra precautions -- but our data suggest that these culturally mediated responses do not manifest as detectable changes in population-level mortality.

### Alternative Explanations

Following the approach of Phillips et al. [4], we consider and reject several alternative explanations:

- **Psychosomatic effect:** While acute psychological stress can trigger cardiac events [4,14], yakudoshi designates an entire year rather than a specific stressful moment. Moreover, the contradictory direction between sexes (lower mortality for males, higher for females) is inconsistent with a psychosomatic mechanism, which would predict elevated mortality in both sexes.

- **Protective behaviour masking a true effect:** If yakudoshi believers take extra precautions during their unlucky years (visiting doctors more frequently, avoiding risk), this could suppress mortality. However, a protective effect would predict lower mortality at yakudoshi ages for both sexes, not the contradictory pattern we observed. Moreover, the direction reversal with spline flexibility indicates that the apparent associations are model artefacts rather than genuine signals to be explained.

- **Temporal fading of superstition:** Era-stratified analysis showed no consistent pattern across historical periods, with most era-specific results being non-significant. The modern era showed a nominally significant result for females only, inconsistent with a fading effect.

- **Wrong age mapping:** Our sensitivity analysis with kazoedoshi offset 2 (in addition to the primary offset 1) rendered results non-significant, indicating that the primary findings are sensitive to the conversion assumption.

### Strengths and Limitations

This study has several strengths. It uses the complete mortality experience of the Japanese population over 78 years, avoiding the selection bias inherent in hospital- or registry-based studies. The JMD data are methodologically compatible with the international Human Mortality Database, ensuring data quality. We employed both parametric (negative binomial regression) and non-parametric (local residual) approaches, selected model complexity by AIC, estimated the dispersion parameter from the data rather than fixing it a priori, diagnosed and appropriately handled overdispersion, conducted multiple pre-specified sensitivity analyses, and applied Bonferroni correction for multiple comparisons.

The study also has limitations:

1. **All-cause mortality only.** The JMD provides all-cause mortality; we could not examine cause-specific mortality, which might reveal effects masked in aggregate data.

2. **Ecological design.** The data are aggregate statistics; individual-level confounders (income, education, health behaviour, strength of yakudoshi belief) could not be adjusted for. The ecological fallacy precludes inference about whether individuals who believe in yakudoshi have different mortality outcomes than non-believers.

3. **Kazoedoshi conversion uncertainty.** The conversion from kazoedoshi to Western age introduces 1-2 years of uncertainty in the exposed ages. Our sensitivity analysis with two offset values showed that primary results were sensitive to this assumption.

4. **Unmeasured belief prevalence.** We could not measure the prevalence or intensity of yakudoshi belief in the population, which may have varied across the 78-year study period and across demographic groups.

5. **Behavioural outcomes not captured.** If yakudoshi influences health-seeking behaviour (e.g., increased medical check-ups) rather than mortality per se, our analysis would not capture such effects.

6. **Model sensitivity.** The reversal of effect direction with spline flexibility, while informative, also means that no single result can be taken at face value. This limitation is inherent to the analysis of age-specific effects embedded within a steep age-mortality gradient.

### Generalisability

Our findings are based on the entire Japanese population over 78 years, providing high internal validity. However, generalisability to other cultural contexts is limited: yakudoshi is specific to Japanese culture, and the strength of this belief may vary across generations and regions within Japan. The findings do generalise to the broader question of whether culturally significant "unlucky" ages influence population-level mortality, contributing to an international literature that has consistently found null results for analogous superstitions in other cultures [1-3,8].

---

## Conclusions

Using 78 years of Japanese national mortality data, we found no evidence of a consistent yakudoshi effect on all-cause mortality. The only nominally significant regression result pointed in the opposite direction (lower male mortality at yakudoshi ages), was sensitive to model specification (with effect direction reversing across spline degrees of freedom), and did not generalise across age ranges or kazoedoshi conversion assumptions. The model-free local residual analysis confirmed negligible effect sizes. These results add to the growing body of evidence that culturally significant "unlucky" periods do not influence mortality at the population level, despite their profound influence on behaviour.

---

## Data Availability

The Japanese Mortality Database is publicly available from the National Institute of Population and Social Security Research (IPSS) at https://www.ipss.go.jp/p-toukei/JMD/index.asp. Analysis code is available at https://github.com/rehabilitation-collaboration/yakudoshi-mortality.

## Acknowledgments

The author used Claude (Anthropic, claude-opus-4-20250514), an AI language model, to assist with code development, debugging, manuscript drafting, and editing. The author reviewed, tested, revised, and takes full responsibility for all code, results, and the content of this publication.

## Funding

This research received no specific funding.

## Competing Interests

The author declares no competing interests.

## Author Contributions

MS conceived the study, conducted the analysis, and wrote the manuscript.

---

## References

1. Scanlon TJ, Luben RN, Scanlon FL, Singleton N. Is Friday the 13th bad for your health? BMJ. 1993;307(6919):1584-1586. doi:10.1136/bmj.307.6919.1584
2. Radun I, Summala H. Females do not have more injury road accidents on Friday the 13th. BMC Public Health. 2004;4:54. doi:10.1186/1471-2458-4-54
3. Ranganathan S, Riveros C, Geng M, Chang C, Tsugawa Y, Ravi B, et al. Superstition in surgery: a population-based cohort study to assess the association between surgery on Friday the 13th and postoperative outcomes. Ann Surg Open. 2024;5(1):e375. doi:10.1097/AS9.0000000000000375
4. Phillips DP, Liu GC, Kwok K, Jarvinen JR, Zhang W, Abramson IS. The Hound of the Baskervilles effect: natural experiment on the influence of psychological stress on timing of death. BMJ. 2001;323(7327):1443-1446. doi:10.1136/bmj.323.7327.1443
5. Yang CH, Huang YT, Janes C, Lin KC, Lu TH. Belief in ghost month can help prevent drowning deaths: a natural experiment on the effects of cultural beliefs on risky behaviours. Soc Sci Med. 2008;66(9):1990-1998. doi:10.1016/j.socscimed.2008.01.014
6. Lin SM, Wang JH, Huang LK, Huang HK. Does the "Chinese New Year effect" exist? Hospital mortality in patients admitted to internal medicine departments during official consecutive holidays: a nationwide population-based cohort study. BMJ Open. 2019;9(4):e025762. doi:10.1136/bmjopen-2018-025762
7. Hira K, Fukui T, Endoh A, Rahman M, Maekawa M. Influence of superstition on the date of hospital discharge and medical cost in Japan: retrospective and descriptive study. BMJ. 1998;317(7174):1680-1683. doi:10.1136/bmj.317.7174.1680
8. Panesar NS, Chan NCY, Li SN, Lo JKY, Wong VWY, Yang IB, Yip EKY. Is four a deadly number for the Chinese? MJA. 2003;179(11-12):656-658. doi:10.5694/j.1326-5377.2003.tb05741.x
9. Smith GD. Scared to death? BMJ. 2002;325(7378):1442-1443. doi:10.1136/bmj.325.7378.1442
10. Austin PC, Mamdani MM, Juurlink DN, Hux JE. Testing multiple statistical hypotheses resulted in spurious associations: a study of astrological signs and health. J Clin Epidemiol. 2006;59(9):964-969. doi:10.1016/j.jclinepi.2006.01.012
11. Kaku K. Increased induced abortion rate in 1966, an aspect of a Japanese folk superstition. Ann Hum Biol. 1975;2(2):111-115. doi:10.1080/03014467500000651
12. National Institute of Population and Social Security Research. Japanese Mortality Database. Available at: https://www.ipss.go.jp/p-toukei/JMD/index.asp. Accessed 2026.
13. Wilmoth JR, Andreev K, Jdanov D, Glei DA, Riffe T. Methods protocol for the Human Mortality Database. Available at: https://www.mortality.org/File/GetDocument/Public/Docs/MethodsProtocol.pdf.
14. Leor J, Poole WK, Kloner RA. Sudden cardiac death triggered by an earthquake. N Engl J Med. 1996;334(7):413-419. doi:10.1056/NEJM199602153340701

---

## Figures

**Figure 1.** Age-specific mortality rates in Japan, 1947-2024. Each thin line represents one calendar year; the thick line shows the median across all years. Vertical bands indicate yakudoshi ages (in kazoedoshi). Left panel: males; right panel: females. Note the "accident hump" in young males around age 20-25, which coincides with the male yakudoshi age of 25 (kazoedoshi).

**Figure 2.** Distribution of local residuals at yakudoshi versus non-yakudoshi ages across 78 years. Box plots show the interquartile range; individual observations at yakudoshi ages are overlaid as jittered points. Statistics show the mean difference, permutation test p-value, and Cohen's d. Neither sex shows a meaningful difference in residual distributions.

**Figure 3.** Forest plot of incidence rate ratios (IRR) from negative binomial regression. Top section: per-age analysis. Middle and bottom sections: sensitivity analyses for spline flexibility, historical era, and kazoedoshi conversion offset. The dashed vertical line indicates the null (IRR = 1.0). Note the reversal of effect direction with spline flexibility for both sexes.
