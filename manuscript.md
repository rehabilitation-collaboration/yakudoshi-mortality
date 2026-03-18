# Yakudoshi and Mortality: A Population-Based Analysis of Japan's Age-Specific Superstition Using 78 Years of National Data

Mizuki Shirai (ORCID: 0009-0005-3615-0670)

Rehabilitation Collaboration (NPO), Japan

**Corresponding author:** Mizuki Shirai, Rehabilitation Collaboration (NPO), Japan. Email: rehabilitation.collaboration@gmail.com

---

## Abstract

**Background:** Yakudoshi (unlucky years) is one of the most widely observed superstitions in Japan, in which certain ages are believed to bring calamity, illness, or death. Despite its cultural significance, no epidemiological study has examined whether mortality rates are actually elevated at yakudoshi ages. We investigated whether all-cause mortality is associated with yakudoshi ages in the Japanese population.

**Methods:** We conducted a population-based retrospective analysis using the Japanese Mortality Database (JMD), which provides age-specific mortality data for Japan from 1947 to 2024 (78 years). Yakudoshi ages were defined as 25, 42, and 61 for males and 19, 33, 37, and 61 for females (in kazoedoshi, the traditional Japanese counting system), converted to Western age equivalents. The primary analysis used negative binomial regression with cubic regression splines modelling the age-mortality relationship (degrees of freedom selected by AIC) and a binary indicator for yakudoshi ages. The dispersion parameter alpha was estimated by AIC-based grid search. The secondary analysis used a local residual method comparing mortality at each yakudoshi age to the mean of neighbouring ages. Seven pre-specified sensitivity analyses examined robustness.

**Results:** The dataset comprised approximately 25.4 million male and 16.6 million female deaths (ages 15-80) over 78 years. Poisson regression showed substantial overdispersion (deviance/df = 71-89). Negative binomial regression with data-estimated alpha (males 0.028, females 0.040) found that males had nominally significant *lower* mortality at yakudoshi ages (IRR 0.97, 95% CI 0.94-0.99, p = 0.004) — the opposite of what the superstition would predict — while females showed no significant association (IRR 1.02, 95% CI 1.00-1.05, p = 0.055). Critically, the direction of association reversed for both sexes depending on spline flexibility (male IRR ranged from 0.97 to 1.04; female IRR ranged from 0.96 to 1.02 across df = 3-9), demonstrating model dependence. The local residual method showed negligible effect sizes (Cohen's d = 0.02-0.11). No sensitivity analysis produced results consistent with a genuine yakudoshi effect.

**Conclusions:** We found no evidence of a consistent yakudoshi effect on mortality. Apparent associations were contradictory in direction between sexes and reversed sign depending on model specification, indicating they are artifacts of age-curve modelling rather than genuine biological signals. This study provides the first epidemiological examination of yakudoshi, adding to the literature demonstrating that culturally significant "unlucky" periods do not influence mortality at the population level.

**Keywords:** yakudoshi, superstition, mortality, Japan, epidemiology, cultural belief, negative binomial regression

---

## Introduction

Superstitions about unlucky numbers, dates, and periods exist in cultures worldwide, and several have been subjected to epidemiological scrutiny. Studies have examined whether Friday the 13th increases traffic accidents [1,2] or surgical complications [3], whether the number four elevates cardiac mortality among Chinese and Japanese Americans [4], whether the Chinese Ghost Month affects drowning rates [5], whether the Chinese New Year period influences in-hospital mortality [6], and whether discharge from hospital is delayed to avoid unlucky days of the Japanese lunar calendar [7]. The findings have been mixed: initial studies sometimes report significant associations [1,4], but subsequent replications with larger samples and improved methodology typically fail to confirm them [2,3,8,9]. Austin et al. demonstrated that apparent associations between astrological signs and health outcomes are artefacts of multiple comparisons, disappearing entirely in validation cohorts [10].

Japan has a rich tradition of calendar-based superstitions influencing health-related behaviour. Kaku documented that the folk belief in Hinoe-Uma (丙午, the "Fire Horse" year of the sexagenary cycle) caused a dramatic decline in the Japanese birth rate in 1966 through increased induced abortions — a striking demonstration of superstition's power to alter population-level vital statistics [11]. Hira et al. showed that belief in the six-day lunar calendar (Taian-Butsumetsu) influences the timing of hospital discharge, with patients preferring to leave on "lucky" days [7].

Yakudoshi (厄年, literally "calamity year") is one of the most widely observed superstitions in Japan. The belief holds that certain ages bring heightened vulnerability to misfortune, illness, and death. For males, the yakudoshi ages are 25, 42, and 61; for females, 19, 33, 37, and 61 — all expressed in kazoedoshi (数え年), the traditional Japanese age-counting system in which a person is one year old at birth and gains a year every New Year's Day rather than on their birthday. The year before yakudoshi (mae-yaku, 前厄) and after (ato-yaku, 後厄) are also considered inauspicious.

Among these, the "great calamity years" (taiyaku, 大厄) hold particular cultural significance: age 42 for men and 33 for women. The male taiyaku of 42 carries additional weight because 42 can be read as "shi-ni" (死に), meaning "unto death" in Japanese — a linguistic association that reinforces the superstition through numerological wordplay. Similarly, the female taiyaku of 33 can be read as "sanzan" (散々), meaning "terrible" or "disastrous."

The cultural impact of yakudoshi is substantial. Millions of Japanese visit Shinto shrines and Buddhist temples annually for yakuyoke (厄除け) or yakubarai (厄払い) — ritual purification ceremonies intended to ward off the calamities of yakudoshi. The practice reflects a genuine, widespread belief that these specific ages carry elevated risk, yet no study has empirically examined whether mortality at yakudoshi ages actually differs from what would be expected given the overall age-mortality relationship.

This study aims to provide the first epidemiological investigation of yakudoshi. Using 78 years of national mortality data from the Japanese Mortality Database, we test whether all-cause mortality is elevated at yakudoshi ages after accounting for the smooth, age-dependent increase in mortality risk.

---

## Methods

### Study Design and Data Source

We conducted a population-based retrospective analysis of age-specific mortality in Japan using the Japanese Mortality Database (JMD), maintained by the National Institute of Population and Social Security Research (IPSS) [12]. The JMD provides annual death counts, population exposure (person-years), and central death rates (Mx) by single year of age and sex for Japan from 1947 to 2024. The JMD methodology is compatible with the Human Mortality Database (HMD) protocol, ensuring international comparability [13].

We used three JMD data files: death counts (Deaths_1x1.txt), population exposure (Exposures_1x1.txt), and death rates (Mx_1x1.txt), all in the 1x1 format (single year of age x single calendar year). The analysis was restricted to ages 15-80 to exclude infant and child mortality patterns, which follow a distinct J-shaped curve, and extreme old-age mortality, which is subject to greater measurement uncertainty. The study used the complete national dataset for the entire period available (1947-2024); no sample size calculation was performed because the analysis encompassed the full population rather than a sample.

### Ethical Considerations

This study used publicly available, de-identified aggregate statistics from a national database maintained by a government-affiliated research institute. No individual-level data were accessed. The study was therefore exempt from institutional review board approval under the ethical guidelines for medical and biological research involving human subjects (Ministry of Education, Culture, Sports, Science and Technology / Ministry of Health, Labour and Welfare, Japan), which exempt research using publicly available data that cannot identify individuals.

### Yakudoshi Age Definitions

Yakudoshi ages are traditionally defined in kazoedoshi. Because the JMD records age in Western years (mannenrei, 満年齢), conversion was necessary. A person of kazoedoshi age N is approximately mannenrei N-1 (after their birthday in a given year) or N-2 (before their birthday). For the primary analysis, we used an offset of 1 (kazoedoshi minus 1), yielding the following mannenrei equivalents:

- **Males:** 24, 41, 60 (from kazoedoshi 25, 42, 61)
- **Females:** 18, 32, 36, 60 (from kazoedoshi 19, 33, 37, 61)

Adjacent years (mae-yaku and ato-yaku, +/-1 year from each hon-yaku) were examined separately. This dual-calendar approach follows Panesar and Panesar, who tested the "deadly number four" hypothesis using both Gregorian and lunar calendar dates [8].

### Statistical Analysis

#### Primary Analysis: Negative Binomial Regression

We modelled death counts using negative binomial regression with a log link and log-transformed population exposure as an offset:

log(E[Deaths]) = log(Exposure) + f(Age) + beta_1 x Yakudoshi + g(Year)

where f(Age) is a cubic regression spline with degrees of freedom selected by Akaike Information Criterion (AIC), Yakudoshi is a binary indicator (1 for yakudoshi ages, 0 otherwise), and g(Year) is a cubic regression spline with 3 degrees of freedom to account for the nonlinear secular decline in mortality over 78 years. The coefficient beta_1 was exponentiated to obtain the incidence rate ratio (IRR) with 95% confidence intervals. Models were fitted separately for males and females.

Negative binomial regression was chosen over Poisson regression because mortality data aggregated across 78 years of substantial demographic change exhibited severe overdispersion (deviance/df >> 1 under the Poisson model), which would have inflated type I error rates. We used the NB2 parametrization, where Var(Y) = mu + alpha * mu^2. The dispersion parameter alpha was estimated independently for each sex using a two-stage AIC-based grid search (coarse search over log10(alpha) in [-4, 2], then fine search around the optimum with step 0.05). Alpha was estimated from a null model without the yakudoshi indicator to avoid circularity. We report Poisson results as a sensitivity analysis for comparison. For the spline flexibility sensitivity analysis, alpha was held constant at the primary estimate to isolate the effect of spline degrees of freedom.

We also fitted individual models for each yakudoshi age to examine age-specific effects. Per-age analyses were considered exploratory and are reported without multiple comparison adjustment.

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
5. **Historical era:** Stratifying by postwar (1947-1960), high-growth (1961-1990), and modern (1991-2024) periods.
6. **Age range:** Narrowing to 20-70 and widening to 15-90 to assess sensitivity to the analysis window.
7. **Local residual window:** Varying the neighbour window from +/-2 to +/-5 ages.

#### Multiple Comparisons

Four primary comparisons were pre-specified (male/female x hon-yaku only/with mae-ato-yaku). A Bonferroni-corrected significance threshold of alpha = 0.0125 (0.05/4) was applied to the primary analysis. Sensitivity and per-age analyses were interpreted descriptively.

### Software

All analyses were conducted in Python 3.14 using pandas 3.0, NumPy 2.4, SciPy 1.17, statsmodels 0.14, patsy 1.0, and matplotlib 3.9. Analysis code was developed with the assistance of Claude (Anthropic, claude-opus-4-20250514), an AI language model, which was used for code generation and debugging; the author reviewed, tested, and takes full responsibility for all code and results. Analysis code is available at https://github.com/rehabilitation-collaboration/yakudoshi-mortality.

---

## Results

### Study Population

The JMD dataset comprised 78 years of observation (1947-2024) across ages 15-80, yielding 5,148 age-year cells per sex. Within the analysis age range (15-80), the data encompassed approximately 25.4 million male deaths and 16.6 million female deaths (Figure 1).

### Model Selection and Overdispersion

AIC-based model selection favoured 9 degrees of freedom for the age spline in both sexes. Poisson regression showed substantial overdispersion, with deviance-to-residual-degrees-of-freedom ratios of 71.1 (males) and 89.0 (females), confirming that the Poisson variance assumption was violated and that standard Poisson p-values would be unreliable. The negative binomial dispersion parameter was estimated independently for each sex by two-stage AIC grid search, yielding alpha = 0.028 (males) and alpha = 0.040 (females). The resulting deviance/df ratios were 0.99 (males) and 0.95 (females), indicating adequate model fit. All subsequent primary results are from negative binomial regression.

### Primary Analysis: Negative Binomial Regression

Table 1 shows the primary negative binomial regression results. For males, the overall IRR for yakudoshi ages was 0.966 (95% CI 0.944-0.989, p = 0.004), indicating nominally significant but *lower* mortality at yakudoshi ages — the opposite of what the yakudoshi superstition would predict. For females, the IRR was 1.024 (1.000-1.050, p = 0.055), which did not reach nominal significance.

Including mae-yaku and ato-yaku showed a similar pattern: the male IRR was 0.957 (0.942-0.973, p < 0.001) and the female IRR was 1.032 (1.014-1.050, p < 0.001). While the female result with mae/ato-yaku reached significance, the contradictory directions between sexes — males showing lower and females showing higher mortality — is inconsistent with a genuine yakudoshi effect.

**Table 1. Primary Negative Binomial Regression Results**

| Sex | Analysis | IRR | 95% CI | p-value | Direction |
|-----|----------|-----|--------|---------|-----------|
| Male | Hon-yaku only | 0.966 | 0.944-0.989 | 0.004 | Lower |
| Male | With mae/ato-yaku | 0.957 | 0.942-0.973 | <0.001 | Lower |
| Female | Hon-yaku only | 1.024 | 1.000-1.050 | 0.055 | n.s. |
| Female | With mae/ato-yaku | 1.032 | 1.014-1.050 | <0.001 | Higher |

### Per-Age Analysis

Individual yakudoshi ages showed inconsistent effects (Table 2). For males, only age 24 (kazoedoshi 25) reached nominal significance (IRR 0.933, p = 0.001), but in the direction of *lower* mortality. Ages 41 (taiyaku, the most feared "death year") and 60 were non-significant. For females, only age 18 (kazoedoshi 19) was nominally significant (IRR 1.057, p = 0.029); the taiyaku age of 32 (kazoedoshi 33) was non-significant (IRR 1.033, p = 0.196).

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

The local residual analysis, which is independent of the regression model specification, showed negligible effect sizes. For males, Cohen's d was +0.024 (p = 0.377), indicating virtually no difference between yakudoshi and non-yakudoshi ages. For females, d was +0.107 (p = 0.032), a small effect that did not survive Bonferroni correction (Figure 2).

**Table 3. Local Residual Method Results**

| Sex | Mean residual (yakudoshi) | Mean residual (non-yakudoshi) | Cohen's d | p (permutation) |
|-----|--------------------------|-------------------------------|-----------|-----------------|
| Male | -0.001 | -0.003 | +0.024 | 0.377 |
| Female | +0.007 | -0.001 | +0.107 | 0.032 |

### Sensitivity Analyses

Sensitivity analyses demonstrated that the apparent associations were artifacts of model specification (Figure 3).

**Poisson versus negative binomial:** Poisson regression produced nominally significant p-values for both sexes, but these were unreliable due to severe overdispersion (deviance/df = 71-89). Negative binomial regression, with deviance/df near 1.0, provided appropriate variance estimation (Table 4).

**Table 4. Poisson vs Negative Binomial Comparison**

| Sex | Model | IRR | p-value | Deviance/df |
|-----|-------|-----|---------|-------------|
| Male | Poisson | 0.987 | <0.001 | 71.1 |
| Male | Negative Binomial | 0.966 | 0.004 | 0.99 |
| Female | Poisson | 1.005 | 0.002 | 89.0 |
| Female | Negative Binomial | 1.024 | 0.055 | 0.95 |

**Spline flexibility:** To isolate the effect of spline flexibility, the dispersion parameter alpha was held constant at the primary estimate while varying the spline degrees of freedom. For males, the IRR was 1.042 (p < 0.001) at df = 3 but reversed to 0.966 (p = 0.004) at df = 9 (the AIC-selected value). For females, the IRR was 0.962 (p = 0.001) at df = 3 but reversed to 1.024 (p = 0.055) at df = 9. The complete reversal of effect direction for both sexes as the spline becomes more flexible strongly suggests that the apparent associations are artifacts of how the age-mortality curve is modelled, not genuine biological signals (Table 5).

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

**Historical era:** No era showed a consistent yakudoshi effect. For males, the growth (1961-1990) and modern (1991-2024) eras showed significant *lower* mortality (both p < 0.001), while the postwar era was non-significant (p = 0.419). For females, only the modern era reached nominal significance (IRR 1.022, p = 0.005). The opposite directions between sexes and inconsistency across eras argue against a genuine effect.

**Kazoedoshi conversion:** Using offset 2 instead of offset 1 rendered both sexes non-significant (male p = 0.059, female p = 0.356), indicating that the primary results are sensitive to the age conversion assumption.

**Age range:** Narrowing to ages 20-70 eliminated significance for both sexes (male p = 0.748, female p = 0.804). Widening to 15-90 also rendered both non-significant (male p = 0.230, female p = 0.109). The primary results were thus specific to the 15-80 age range and did not generalize.

**Local residual window:** Varying the neighbour window from +/-2 to +/-5 ages produced consistent results. Cohen's d remained below 0.2 for all window sizes in both sexes, confirming that the null finding from the local residual method is robust to the choice of window size.

---

## Discussion

### Principal Findings

This study provides the first epidemiological examination of yakudoshi, the Japanese belief that certain ages bring heightened risk of misfortune and death. Using 78 years of national mortality data encompassing the entire Japanese population, we found no evidence of a consistent yakudoshi effect on all-cause mortality.

Negative binomial regression found a nominally significant association for males only, but in the direction of *lower* mortality — the opposite of what the yakudoshi superstition predicts. The female association did not reach significance (p = 0.055). Most critically, the direction of association reversed for both sexes when the spline flexibility was varied, demonstrating that the apparent associations are artifacts of age-curve modelling rather than genuine biological signals. The model-free local residual analysis confirmed negligible effect sizes (Cohen's d = 0.02-0.11).

A critical methodological finding was that Poisson regression produced spuriously significant results due to severe overdispersion in the 78-year dataset. Furthermore, the choice of negative binomial dispersion parameter matters substantially: fixing alpha at an arbitrary value can either over- or under-correct for overdispersion. We addressed this by estimating alpha from the data using AIC-based grid search, yielding deviance/df ratios near 1.0 — indicating appropriate model fit.

### Comparison with Prior Literature

Our findings are consistent with the broader pattern in the superstition-and-health literature. Phillips et al. reported elevated cardiac mortality on the 4th of the month among Chinese and Japanese Americans [4], but Panesar and Panesar failed to replicate this finding in Hong Kong using both Gregorian and lunar calendar analyses [8], and Smith challenged the original analysis on methodological grounds [9]. Scanlon et al. found increased hospital admissions on Friday the 13th [1], but Radun and Summala demonstrated that this result was likely an artefact of methodological limitations [2]. Doshi et al., using over 400,000 surgical cases, found no association between Friday the 13th and adverse surgical outcomes [3]. Lin et al., examining over 190,000 admissions, found elevated mortality during the Chinese New Year holiday but attributed this to reduced staffing and delayed care-seeking rather than superstition [6].

The recurring pattern — initial positive findings followed by null replications — has been attributed to small sample sizes, multiple testing, publication bias, and inadequate statistical modelling in the initial studies [2,3]. Our study illustrates an additional pitfall: the sensitivity of results to model specification. The direction reversal with spline flexibility that we observed serves as a cautionary example of how modelling choices can produce spuriously significant results even in large datasets.

Hira et al. demonstrated that a related Japanese superstition (the six-day lunar calendar) does influence hospital discharge behaviour [7], and Kaku documented dramatic effects of the Hinoe-Uma superstition on the 1966 birth rate [11]. The distinction is important: these studies documented the effect of superstition on *behaviour*, not on *mortality*. People may indeed alter their behaviour based on yakudoshi beliefs — visiting shrines, taking extra precautions — but our data suggest that these culturally mediated responses do not manifest as detectable changes in population-level mortality.

### Alternative Explanations

Following the approach of Phillips et al. [4], we consider and reject several alternative explanations:

- **Psychosomatic effect:** While acute psychological stress can trigger cardiac events [4,14], yakudoshi designates an entire year rather than a specific stressful moment. Moreover, the contradictory direction between sexes (lower mortality for males, higher for females) is inconsistent with a psychosomatic mechanism, which would predict elevated mortality in both sexes.

- **Protective behaviour masking a true effect:** If yakudoshi believers take extra precautions during their unlucky years (visiting doctors more frequently, avoiding risk), this could suppress mortality. However, a protective effect would predict lower mortality at yakudoshi ages for both sexes, not the contradictory pattern we observed. Moreover, the direction reversal with spline flexibility indicates that the apparent associations are model artifacts rather than genuine signals to be explained.

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

Using 78 years of Japanese national mortality data, we found no evidence of a consistent yakudoshi effect on all-cause mortality. The only nominally significant regression result pointed in the opposite direction (lower male mortality at yakudoshi ages), was sensitive to model specification (with effect direction reversing across spline degrees of freedom), and did not generalize across age ranges or kazoedoshi conversion assumptions. The model-free local residual analysis confirmed negligible effect sizes. These results add to the growing body of evidence that culturally significant "unlucky" periods do not influence mortality at the population level, despite their profound influence on behaviour.

---

## Data Availability

The Japanese Mortality Database is publicly available from the National Institute of Population and Social Security Research (IPSS) at https://www.ipss.go.jp/p-toukei/JMD/index.asp. Analysis code is available at https://github.com/rehabilitation-collaboration/yakudoshi-mortality.

## Acknowledgments

The author used Claude (Anthropic, claude-opus-4-20250514), an AI language model, to assist with manuscript drafting and editing. The author reviewed, revised, and takes full responsibility for the content of this publication.

## Funding

This research received no specific funding.

## Competing Interests

The author declares no competing interests.

## Author Contributions

MS conceived the study, conducted the analysis, and wrote the manuscript.

---

## References

1. Scanlon TJ, Luben RN, Scanlon FL, Singleton N. Is Friday the 13th bad for your health? BMJ. 1993;307:1584-1586.
2. Radun I, Summala H. Females do not have more injury road accidents on Friday the 13th. BMC Public Health. 2004;4:54.
3. Doshi A, Bouck Z, Englesbe M, et al. Friday the 13th and surgical outcomes: a population-based cohort study. Ann Surg Open. 2024;5(2):e427.
4. Phillips DP, Liu GC, Kwok K, Jarvinen JR, Zhang W, Abramson IS. The Hound of the Baskervilles effect: natural experiment on the influence of psychological stress on timing of death. BMJ. 2001;323:1443-1446.
5. Yang CH, Huang YT, Jeng SF. Ghost month and mortality in Taiwan: a natural experiment on the effects of cultural beliefs on health. Soc Sci Med. 2008;67:104-112.
6. Lin CM, Li CY, Mao IF. Chinese New Year and in-hospital mortality: a population-based cohort study. BMJ Open. 2019;9:e024133.
7. Hira K, Fukui T, Endoh A, Rahman M, Maekawa M. Influence of superstition on the date of hospital discharge and medical cost in Japan: retrospective and descriptive study. BMJ. 1998;317:1680-1683.
8. Panesar SS, Panesar NS. Is four a deadly number for the Chinese? MJA. 2003;179:656-658.
9. Smith GD. The Hound of the Baskervilles effect [letter]. BMJ. 2002;324:1098.
10. Austin N, Gallus S, Li K. Astrological signs and health: is there a link? A large-scale study. BMJ. 2006;332:1513-1514.
11. Kaku K. Increased induced abortion rate in 1966, an aspect of a Japanese folk superstition. Ann Hum Biol. 1975;2:111-115.
12. National Institute of Population and Social Security Research. Japanese Mortality Database. Available at: https://www.ipss.go.jp/p-toukei/JMD/index.asp. Accessed 2026.
13. Wilmoth JR, Andreev K, Jdanov D, Glei DA. Methods protocol for the Human Mortality Database. Available at: https://www.mortality.org/File/GetDocument/Public/Docs/MethodsProtocol.pdf.
14. Leor J, Poole WK, Kloner RA. Sudden cardiac death triggered by an earthquake. N Engl J Med. 1996;334:413-419.

---

## Figures

**Figure 1.** Age-specific mortality rates in Japan, 1947-2024. Each thin line represents one calendar year; the thick line shows the median across all years. Vertical bands indicate yakudoshi ages (in kazoedoshi). Left panel: males; right panel: females. Note the "accident hump" in young males around age 20-25, which coincides with the male yakudoshi age of 25 (kazoedoshi).

**Figure 2.** Distribution of local residuals at yakudoshi versus non-yakudoshi ages across 78 years. Box plots show the interquartile range; individual observations at yakudoshi ages are overlaid as jittered points. Statistics show the mean difference, permutation test p-value, and Cohen's d. Neither sex shows a meaningful difference in residual distributions.

**Figure 3.** Forest plot of incidence rate ratios (IRR) from negative binomial regression. Top section: per-age analysis. Middle and bottom sections: sensitivity analyses for spline flexibility, historical era, and kazoedoshi conversion offset. The dashed vertical line indicates the null (IRR = 1.0). Note the reversal of effect direction with spline flexibility for both sexes.
