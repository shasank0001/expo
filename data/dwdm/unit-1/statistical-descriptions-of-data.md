---
subject: dwdm
unit: 1
topic: statistical-descriptions-of-data
syllabus_ref: CSM3101 Unit-I
status: draft
---
# Statistical Descriptions of Data

## Overview

A statistical description compresses a collection of values so that its center, spread, shape, relationships, and unusual observations can be understood. No single statistic is sufficient: the mean alone can hide skewness, the standard deviation alone can hide a few extreme values, and correlation alone cannot establish causation.

This note follows the descriptive-statistics foundation used by Han, Kamber, and Pei and the data-quality, attribute-type, and outlier discussion in Tan, Steinbach, and Kumar. It covers measures of central tendency, dispersion, order statistics, distribution, correlation, and outliers, with calculations that can be reproduced by hand.

## Explanation

### 1. Why summarize data?

A raw list of observations is difficult to compare. A summary can answer questions such as:

- Where is the typical observation located?
- How much do values vary?
- Is the distribution symmetric or skewed?
- Are there clusters or gaps?
- Do two numeric attributes move together?
- Are any values unusually far from the main body?

A summary should be selected according to the data type and the analysis goal. It should be accompanied by the sample size, units, time period, and any important limitations. A compact number is not a substitute for understanding the underlying data.

### 2. Frequency distributions and proportions

For categorical data, count each category and calculate its proportion:

\[
p_i = \frac{n_i}{n}
\]

where \(n_i\) is the number of observations in category \(i\) and \(n\) is the total.

For numerical data, a frequency distribution groups values into intervals or bins. The bin width is a design choice. Narrow bins show local detail but may be noisy; wide bins are stable but may hide structure. The range covered by equal-width bins is approximately

\[
\text{bin width} = \frac{\text{maximum}-\text{minimum}}{\text{number of bins}}
\]

The actual algorithm may use a rounded or data-driven width. The bin boundaries and inclusion convention must be documented.

### 3. Measures of central tendency

#### Midrange

The midrange is

\[
\text{midrange} = \frac{x_{\min}+x_{\max}}{2}
\]

It is simple but sensitive to outliers because it uses the two extremes.

#### Mean

The arithmetic mean of \(n\) values is

\[
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
\]

The mean uses every value and is the basis for many statistical procedures, but extreme values can pull it away from the typical value.

#### Median

For ordered data \(x_{(1)} \le x_{(2)} \le \cdots \le x_{(n)}\),

\[
\text{median}=
\begin{cases}
x_{((n+1)/2)}, & n \text{ odd}\\[4pt]
\frac{x_{(n/2)}+x_{(n/2+1)}}{2}, & n \text{ even}
\end{cases}
\]

The median is robust to extreme values and is useful for skewed data or values with a meaningful order.

#### Mode

The mode is the most frequent value or values. A distribution can have no mode, one mode (unimodal), or several modes (multimodal). Mode is the main central-tendency measure for nominal categories.

#### Trimmed mean

A trimmed mean removes a chosen percentage of the smallest and largest observations before averaging. It can be more robust than the ordinary mean while using more data than the median.

No central measure is always best. For branch names, the mode is meaningful and the mean is not. For highly skewed income, the median or geometric mean may describe typical income better than the arithmetic mean.

### 4. Measures of dispersion

Dispersion describes how far values lie from one another and from the center.

#### Range

\[
\text{range}=x_{\max}-x_{\min}
\]

Range is easy to calculate but uses only two observations.

#### Variance

For a population of size \(N\),

\[
\sigma^2=\frac{1}{N}\sum_{i=1}^{N}(x_i-\mu)^2
\]

For a sample of size \(n\),

\[
s^2=\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2
\]

The sample denominator \(n-1\) estimates the population variance from a sample. Units are the square of the original measurement.

#### Standard deviation

The population standard deviation is

\[
\sigma=\sqrt{\sigma^2}
\]

and the sample standard deviation is

\[
s=\sqrt{s^2}
\]

Standard deviation returns to the original units and is easier to interpret. It is not a direct statement about every observation: a small fraction of values can be far from the mean.

#### Interquartile range and MAD

The interquartile range is

\[
IQR=Q_3-Q_1
\]

where \(Q_1\) and \(Q_3\) are the 25th and 75th percentiles. The median absolute deviation is

\[
MAD = \operatorname{median}(|x_i-\operatorname{median}(x)|)
\]

Both are useful when outliers make the standard deviation less robust.

#### Coefficient of variation

The coefficient of variation is

\[
CV=\frac{s}{\bar{x}}\times 100\%
\]

when the mean is positive. It compares relative variation across measurements with different units or scales, but it is not meaningful when the mean is near zero or the quantity is interval-scaled without a meaningful ratio interpretation.

### 5. Order statistics, quartiles, and box plots

The minimum, lower quartile, median, upper quartile, and maximum form the five-number summary:

\[
(x_{\min},\ Q_1,\ \text{median},\ Q_3,\ x_{\max})
\]

A box plot shows a box from \(Q_1\) to \(Q_3\), a line at the median, whiskers near the non-outlier extremes, and separate points for possible outliers. Quartile definitions differ between software packages, especially for small samples, so the convention should be stated.

A common outlier rule is the \(1.5IQR\) rule:

\[
\text{lower fence}=Q_1-1.5IQR,\qquad
\text{upper fence}=Q_3+1.5IQR
\]

Values outside the fences are candidates for investigation, not automatically erroneous.

### 6. Shape of a distribution

A distribution can be:

- **symmetric:** left and right sides are approximately balanced;
- **right-skewed or positively skewed:** a long tail extends to the right;
- **left-skewed or negatively skewed:** a long tail extends to the left;
- **bimodal:** two prominent peaks;
- **uniform:** approximately even across the range.

The mean is often pulled toward a long tail. The median may be a better description of the typical value in a skewed distribution. A histogram or density plot should be inspected alongside numerical summaries.

### 7. Outliers

An outlier is an observation unusually far from the rest. Common reasons include:

- measurement or entry error;
- a different unit;
- a valid extreme population value;
- a mixture of populations;
- a rare event;
- a genuinely novel phenomenon.

A \(z\)-score is

\[
z_i=\frac{x_i-\bar{x}}{s}
\]

for a sample standard deviation. A value near or beyond \(\pm 3\) is often flagged by a simple rule, but the threshold is not universal. The distribution, domain, and analysis purpose matter.

### 8. Covariance and correlation

Covariance measures whether two numeric attributes tend to increase or decrease together. For a sample,

\[
s_{XY}=\frac{\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})}{n-1}
\]

The Pearson correlation coefficient is

\[
r=\frac{s_{XY}}{s_Xs_Y}
\]

It lies between -1 and 1:

- \(r\approx 1\): strong positive linear association;
- \(r\approx -1\): strong negative linear association;
- \(r\approx 0\): little linear association, not necessarily no relationship.

Correlation is affected by outliers and nonlinear relationships. It does not establish causation. A common cause, a selection effect, or a coincident time trend can create a strong correlation.

## Worked examples

### Example A: Mean, median, and mode

Data:

```text
40, 45, 45, 50, 60, 90
```

Mean:

\[
\bar{x}=\frac{40+45+45+50+60+90}{6}
=\frac{330}{6}=55
\]

Sorted data are already ordered. The median is the average of the third and fourth values:

\[
\text{median}=\frac{45+50}{2}=47.5
\]

The mode is 45. The mean is higher than the median because 90 pulls it upward. The values illustrate why a mean-only summary can mislead.

### Example B: Variance and standard deviation

Use data:

```text
40, 50, 60, 70, 100
```

Mean:

\[
\bar{x}=64
\]

Squared deviations:

```text
x     x - mean   squared deviation
40       -24           576
50       -14           196
60        -4            16
70         6            36
100       36          1296
Sum                    2120
```

Population variance:

\[
\sigma^2=\frac{2120}{5}=424,\qquad
\sigma=\sqrt{424}\approx20.59
\]

Sample variance:

\[
s^2=\frac{2120}{4}=530,\qquad
s=\sqrt{530}\approx23.02
\]

The correct denominator depends on whether the five values are treated as the entire population or as a sample.

### Example C: Quartiles and the IQR rule

Sorted data:

```text
12, 15, 18, 21, 24, 27, 30, 36, 40, 45
```

Using the median-of-halves convention:

- \(Q_1=18\)
- median \(=(24+27)/2=25.5\)
- \(Q_3=36\)
- \(IQR=36-18=18\)

Fences:

\[
\text{lower}=18-1.5(18)=18-27=-9
\]

\[
\text{upper}=36+1.5(18)=36+27=63
\]

No value in this sample is outside the fences. If a value of 2 were added, it would fall below the lower fence \(-9\) and become a candidate outlier; a value of 50 would remain within the upper fence. In either case, the value should be investigated rather than automatically deleted.

### Example D: Correlation

Data:

```text
x: 1, 2, 3, 4, 5
y: 2, 4, 5, 4, 6
```

Means:

\[
\bar{x}=3,\qquad \bar{y}=4.2
\]

The sample covariance is

\[
s_{XY}=\frac{4.4+0.2+0-0.2+3.6}{4}
=\frac{8}{4}=2
\]

Sample standard deviations are \(s_X=\sqrt{2.5}\) and \(s_Y=\sqrt{2.2}\). Therefore,

\[
r=\frac{2}{\sqrt{2.5}\sqrt{2.2}}
=\frac{2}{\sqrt{5.5}}
\approx0.853
\]

This is strong positive linear association in this small sample. It does not show that changing \(x\) causes \(y\), and more observations or an experiment would be needed for a causal claim.

### Example E: Outlier investigation

Marks are:

```text
40, 50, 60, 65, 70
```

The mean is 57 and the sample standard deviation is approximately 12.04. A mark of 100 has

\[
z=\frac{100-57}{12.04}\approx3.57
\]

It is an unusual value. The analyst checks whether 100 is a valid exceptional result, a typo for 10, or a student from a different assessment scheme. The appropriate decision depends on evidence.

## Key terms & formulas

- **Central tendency:** the typical location of a distribution.
- **Mean:** \(\bar{x}=\frac{1}{n}\sum x_i\).
- **Median:** the middle ordered value or the average of the two middle values.
- **Mode:** the most frequent value or values.
- **Midrange:** \((x_{\min}+x_{\max})/2\).
- **Trimmed mean:** an average after removing selected extreme values.
- **Dispersion:** the spread of observations.
- **Range:** \(x_{\max}-x_{\min}\).
- **Population variance:** \(\sigma^2=\frac{1}{N}\sum(x_i-\mu)^2\).
- **Sample variance:** \(s^2=\frac{1}{n-1}\sum(x_i-\bar{x})^2\).
- **Standard deviation:** the square root of variance.
- **IQR:** \(Q_3-Q_1\).
- **MAD:** median of absolute deviations from the median.
- **Coefficient of variation:** \(CV=(s/\bar{x})100\%\), when appropriate.
- **Five-number summary:** minimum, \(Q_1\), median, \(Q_3\), maximum.
- **IQR fence:** \(Q_1-1.5IQR\) and \(Q_3+1.5IQR\).
- **Covariance:** \(\frac{\sum (x_i-\bar{x})(y_i-\bar{y})}{n-1}\) for a sample.
- **Pearson correlation:** \(r=s_{XY}/(s_Xs_Y)\).
- **z-score:** \(z_i=(x_i-\bar{x})/s\).
- **Right skew:** a longer tail toward larger values.
- **Left skew:** a longer tail toward smaller values.
- **Outlier:** an observation unusually distant from the data distribution.

## Common mistakes

1. **Using the mean for nominal categories.** A branch name has no meaningful average.
2. **Forgetting the sample-variance denominator.** Use \(n-1\) for a sample estimate and \(N\) for a population.
3. **Using the median calculation for odd and even samples incorrectly.** Odd data have one middle value; even data have two.
4. **Treating range as a complete measure of spread.** It ignores every observation except the extremes.
5. **Calling any high value an error.** A valid rare observation may be an important outlier.
6. **Applying the same quartile convention without saying so.** Software and textbooks can differ for small samples.
7. **Reading correlation as causation.** A common cause or time trend can produce a high \(r\).
8. **Interpreting \(r=0\) as no relationship.** It means no strong *linear* relationship; a curved pattern may remain.
9. **Using one statistic for every data shape.** A skewed distribution may need median, quantiles, and a log or robust scale.
10. **Ignoring sample size and units.** A precise-looking decimal does not make an estimate reliable.

## Exam prep

### Likely 2-mark questions

1. **Define mean, median, and mode.**  
   *Hint:* Mean is the arithmetic average, median is the ordered middle, and mode is the most frequent value.

2. **Give the population and sample variance formulas.**  
   *Hint:* Population uses \(1/N\); sample uses \(1/(n-1)\).

3. **What is the IQR?**  
   *Hint:* \(Q_3-Q_1\), the spread of the middle 50% of ordered values.

4. **What does Pearson correlation measure?**  
   *Hint:* The direction and strength of linear association between two numeric variables.

5. **Why is the median useful for skewed data?**  
   *Hint:* Extreme values have limited influence on its position.

6. **Define an outlier.**  
   *Hint:* A value unusually far from the main distribution; it may be erroneous or valid.

7. **What is a histogram?**  
   *Hint:* A graph of frequencies across intervals of a numerical attribute.

8. **Why is correlation not causation?**  
   *Hint:* It describes association only; confounding, coincidence, or a common cause may explain it.

### Likely long-answer questions

1. **Explain measures of central tendency and dispersion with formulas and examples.**  
   *Answer hint:* Define mean, median, mode, range, variance, standard deviation, and IQR. Calculate both center and spread and explain how outliers or skewness affect the choice.

2. **Calculate the five-number summary and identify possible outliers.**  
   *Answer hint:* Sort the data, state the quartile convention, compute median and IQR, calculate the 1.5IQR fences, and investigate rather than automatically delete values outside them.

3. **Explain covariance and Pearson correlation with a numerical example.**  
   *Answer hint:* Show deviations, sample covariance, standard deviations, and \(r\). Interpret direction and strength while stressing that correlation does not establish a causal relationship.

4. **Compare the mean and median for a skewed distribution.**  
   *Answer hint:* Use a right-skewed numeric example, compute both measures, show how the tail shifts the mean, and recommend reporting a robust summary and the distribution shape.

5. **Describe how a statistical summary supports data-mining preparation.**  
   *Answer hint:* Discuss detecting missing or implausible values, skewness, outliers, units, class proportions, and feature distributions before choosing preprocessing or a model.
