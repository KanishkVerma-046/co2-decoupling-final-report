## 6. Visualisation and communication

| In short |
| --- |
| Each chart was chosen for the question it answers, drawn so that the first thing a reader sees is the finding, and checked for colour-blind safety. Uncertainty is shown on the chart, not buried in a footnote. |

### 6.1 How the chart types were chosen

A chart type is a promise about what the eye can compare. People judge positions along a common scale most accurately, lengths almost as well, and areas and colour shades least well [@ClevelandMcGill1984]. So the charts here put the quantity that matters on a position or a length, and use colour only to say which group a mark belongs to. The Week 1 principle of choosing the chart from the question, not the other way round, was applied to every figure.

**Table 6.1: Chart choices, with the alternatives that were rejected and why.**

| Figure | Question it answers | Chart type | Why this form | Alternatives rejected | Design choices |
| --- | --- | --- | --- | --- | --- |
| 1.1 Key findings | What are the headline results and how far can they be trusted? | Tiles with one large number and a badge | Managers read numbers first; a badge puts the confidence next to each number | A table of results (too dense for a first look) | Badge says the level in words, so colour is never the only cue |
| 2.1 Journey | What was done in each step? | Four labelled boxes with arrows | The story is a sequence | A long vertical flowchart (too tall for a page) | Landscape, short sentences, no jargon |
| 5.1 Income and CO2 | How are income and CO2 per person related? | Scatter on logarithmic axes with a trend line | A scatter shows every country, the shape and the spread | A bar chart of averages (hides the spread); a map (shows place, not relationship) | Ticks show real dollars and tonnes; a handful of countries labelled directly |
| 5.2 Decoupling by group | How common is decoupling in each group? | Bars with intervals and counts | Bars are the clearest way to compare shares across four ordered groups | Pie charts (hard to compare); bars without intervals (hide uncertainty) | Direct labels give the percent and the counts; one dashed line for all countries |
| 5.3 Decoupling over time | Is decoupling becoming more common, and for whom? | Lines, one per group | Lines show change over time and let groups be compared | Stacked areas (hide individual groups); one panel per group (harder to compare) | Labels at the line ends instead of a legend; test years shaded |
| 5.7 Model skill | How good is the model, in plain terms? | Dot-and-interval plot plus bars | Intervals show that differences between models are small | A table of scores only; an ROC curve (harder for non-specialists) | No-skill line drawn; post hoc results marked in the figure itself |
| 5.10 Evidence matrix | How strong is the evidence for each finding? | Grid of symbols with a rating column | It shows at a glance which findings rest on one week only | A paragraph (slower); a heat map (implies a scale that does not exist) | Symbols differ in shape, not only in colour, and are explained in a key |
| 8.1 Roadmap | In what order should the recommendations be acted on? | Three columns of cards | Order and confidence are the two things a manager needs | A Gantt chart (implies dates and effort that are not known) | One badge per card |

**Design choices that apply everywhere.**

- **Colour-blind-safe palette.** A blue, vermilion, orange and grey set that stays distinct under common forms of colour blindness [@Wong2011], checked with a palette validator. Ordered groups (income) use one hue from light to dark, the usual rule for ordered categories [@HarrowerBrewer2003]. Nothing depends on colour alone: shapes, labels and words repeat the message.
- **Logarithmic scales explained.** Where income or CO2 spans several orders of magnitude, axes are logarithmic. The axis label says so in words ("each step is ten times more"), and the ticks show real values, not powers of ten.
- **Direct labels.** Names sit next to the lines, bars and dots they describe, so readers do not have to look back and forth to a legend.
- **Honest axes and plain labels.** Bars start at zero, no chart has two vertical scales, and axes read "Income per person (US$, log scale)" rather than a variable name.

### 6.2 Reading the key visuals

**The scatter (Figure 5.1).** Read it as a *tendency across countries*. The trend line is not a law: two countries with the same income can differ as much as a low-income and a high-income country. A reader should come away with "income tells you a lot, but not everything". The labelled countries make that concrete: Qatar sits far above the line, Switzerland well below it. Income groups are a good first sort and a poor last word.

**Decoupling by group (Figure 5.2).** The jump at the high-income bar is the story, and the intervals are the discipline: small groups give wide ranges. The dashed line makes a second point: across all countries, only about a third decoupled. Decoupling is not the norm but an outcome of particular conditions, which are more common in rich countries.

**Decoupling over time (Figure 5.3).** The eye is drawn to the high-income line, and rightly. But the zig-zag is also information: in one window the share can swing by tens of percentage points, which a single end-point comparison (Figure 5.2) hides. The shaded bands show which years the model never used and which it was tested on.

**Model skill (Figure 5.7).** The left panel puts all four models on one scale against the no-skill line. The overlapping intervals are the message: the models are better than chance and better than the simple rule, but not by much, and they are hard to tell apart. The right panel translates the score into something a manager can use ("of the top-scored fifth, about half decoupled") and is clearly labelled post hoc. The implication is that the model is at best a ranking aid.

**Evidence matrix (Figure 5.10).** The matrix shows how many findings depend on one lens only. The top rows are filled in two or more columns; the lower rows are mostly empty or half-filled. A reader should leave knowing which findings can be repeated to a sceptical audience and which need a caveat.

### 6.3 Communicating uncertainty to non-technical readers

- **Say what the number is and how sure we are, side by side.** One format throughout: number, interval, confidence badge.
- **Use words as well as numbers.** "About half" and "roughly one in three" help; the exact value follows in brackets.
- **Show intervals as lines on the chart.** A range drawn as a whisker is read faster than a range written in a sentence.
- **Say when a result was decided after the fact.** The words *post hoc* are explained once and then used consistently, and charts carry the label in the figure itself.
- **Separate "unlikely to be chance" from "large".** Effect sizes come first, in plain words.
- **Name what the data cannot say.** The caveat about production-based emissions travels with every mention of decoupling.

### 6.4 Common ways charts mislead, and how these figures avoid them

**Table 6.2: Misleading practices and the countermeasures used in this report.**

| Way a chart misleads | What was done instead |
| --- | --- |
| A truncated axis makes a small gap look large. | Bars start at zero. |
| Two vertical axes let any two lines appear to move together. | No dual axes; separate panels are used. |
| A log scale that is not explained makes a skewed cloud look tame. | Log scales are named in the axis label with plain-language ticks. |
| Averages hide spread, as in Anscombe's classic examples [@Anscombe1973]. | The scatter shows every country; bars carry intervals. |
| Small groups look as solid as large ones. | Counts are printed on the bars and intervals drawn. |
| Colour alone carries the meaning, which fails for colour-blind readers. | Labels, shapes and words repeat the meaning. |
| A cherry-picked end-point hides what happened in between. | The over-time figure shows every window. |
| A good-looking model score hides a poor decision rule. | Both ranking skill and the frozen-threshold result are shown. |
| Results found after the fact are shown as if planned. | They are marked post hoc in the chart and in the text. |
