# Predictions

> Lock this file with the git tag `predictions-locked` before any experiment. Never edit it afterwards.

## Authorship

Drafted with Claude Code from the structure of the algorithms. An Loc states that he saw no experiment results. The drafting session reported opening these files: CLAUDE.md, README.md, .gitignore, pytest.ini, requirements.txt, .github/workflows/ci.yml, every .py file in selection/, bench/ and tests/ (tests/ partly: headers and test names for some files), notes/ai-error-log.md, notes/anloc.md, notes/trung.md and report/predictions.md. It listed results/ and figures/ (only .gitkeep files) and opened nothing outside the repo except its scratch folder. It also ran pytest, which runs the smoke tests, and ran each of e1 to e6 with --quick into a scratch folder, then read only row counts and algorithm names from those files, not timings. This is self-reported and not verified. An Loc also saw two numbers before these predictions were locked: the comparison counts for quickselect and its two-way variant on all_equal with n = 2000 (4,000 and 1,500,499, from a unit test), and Thanh Trung's report that the two-way variant took about 4.4 s per call at n = 10^4. Neither is the subject of P1 to P9. Thanh Trung's separate draft was written after he, and Claude in his session, saw experiment numbers. As he reported it (not verified by An Loc): (a) a harness check with throwaway implementations covering E1 to E5 at n up to 10^5, after which he was told one time ratio (median of medians vs quickselect on random input); (b) after median of medians was written, comparison counts per element on the six integer families at n = 20,001 and one running time at n = 10^6, of which he was told the running time; (c) a comment in tests/test_median_of_medians.py that gives a measured range of comparisons per element for g = 5, committed in the repo; (d) a 2-instance pilot of E1 to E6 with the final code, seen by Claude in full, after which he was told four qualitative findings (time ratio of median of medians to quickselect, how sorted() compares with quickselect in time, the trend of g = 3 against g = 5, 7 and 9, and how prefix length affects comparisons and time); (e) an accidental full run that printed only per-stage progress times, with its CSV files moved out of the repo unopened. His views on P1, P4, P6 and P9 are therefore not independent of the data. The session that drafted An Loc's predictions opened tests/test_median_of_medians.py (at least its header and test names), so it may have seen the comment in (c). None of P1 to P9c is stated in comparisons per element for median of medians.

## Differences with Trung's draft

| Prediction | An Loc | Trung | Result of comparison |
|---|---|---|---|
| P1 | 2x to 5x, quickselect faster | 2x to 4x | Compatible (inside An Loc's range) |
| P2 | slope 0.9 to 1.2 for both | slope close to 1, comparisons / n stays flat, quickselect noisier between instances | Compatible |
| P3 | max is 1.5 to 3 times the mean | mean about 4n to 6n, p99 about 2x mean, max under 3x mean | Compatible |
| P4 | slightly, hard to see | visibly, about 1.5x per element from 10^3 to 10^6 | DISAGREEMENT |
| P5 | within 10% in time | within 10% in comparisons, g = 7 not faster in time | Compatible |
| P6 | sorted() wins at small n, quickselect may win at 10^6 | sorted() wins at every size, the gap narrows | DISAGREEMENT |
| P7 | all_equal and few_distinct cheapest for quickselect, reverse_sorted worst for median of medians | same as An Loc, plus sorted cheapest for median of medians, and about 0.375 n^2 comparisons for the 2-way partition on all_equal | Compatible |
| P8a | quickselect cheaper at the ends | k = n/2 most expensive, k = 0 cheapest, k = n/10 and 9n/10 in between and close | Compatible |
| P8b | median of medians within 10% across k | about the same for every k | Compatible |
| P9a | identical comparison counts | comparison counts do not change with prefix length | Same |
| P9b | time ratio changes by less than 20% | no ratio threshold; only says the order of the algorithms does not change | Different |
| P9c | within 30% at prefix length 100 | grows by less than 50% | Different |

Decision: An Loc's predictions are locked unchanged, because they are the only ones written without access to experiment numbers. Trung's versions of P4, P6 and P9c are recorded here as noted and not adopted. Details from Trung's draft that cite a formula (Knuth's expected cost) are not verified in our counting and are not adopted.

Changes An Loc made: the first draft was written by Claude Code. An Loc reviewed it and changed these: added numbers to P2 and P5; rewrote P6 and P7 (P7 corrected for duplicates); split P8 and P9 into separate claims; wrote the Authorship note. He did not write the first draft himself.

## P1: Which algorithm is faster on random inputs, and by what factor?

Prediction: Quickselect is faster by 2x to 5x.

Reason (one line): Median of medians sorts every group and builds extra lists, and in pure Python that overhead costs more than quickselect's single pass per round.

## P2: Are both algorithms linear on a log-log plot?

Prediction: The slope of a log-log plot of time vs n is between 0.9 and 1.2 for both algorithms.

Reason (one line): Quickselect is linear in expectation and median of medians is linear in the worst case, so only constant factors differ.

## P3: How wide is the spread of quickselect comparison counts?

Prediction: The maximum over 1000 seeds is 1.5 to 3 times the mean.

Reason (one line): One bad early pivot keeps most of the list, so the count has a long right tail, but a pivot that bad is rare at n = 10^5.

## P4: Does median of medians with g = 3 grow faster than with g = 5?

Prediction: Slightly, but the difference is hard to see on the plot.

Reason (one line): The worst case with g = 3 is n log n, but random input gives pivots far better than the worst case, so the curve stays close to linear.

## P5: How does g = 7 compare with g = 5?

Prediction: g = 7 and g = 5 are within 10% of each other in time.

Reason (one line): A larger group costs more to sort per element, but it leaves fewer medians to recurse on, and the two effects roughly cancel.

## P6: Does `sorted()` beat both algorithms?

Prediction: sorted() beats both algorithms at small n. At n = 10^6, quickselect is within 2x of sorted() and might beat it.

Reason (one line): sorted() is n log n but runs in C, while quickselect does a few linear passes in Python.

Most uncertain prediction.

## P7: What is the worst input family for each algorithm?

Prediction: Quickselect: all_equal and few_distinct are the cheapest families. random, sorted and reverse_sorted are within 10% of each other in time and comparisons. Median of medians: reverse_sorted is the most expensive, because insertion sort on reversed groups does the most swaps.

Reason (one line): The 3-way partition removes every element equal to the pivot, so duplicates shrink the list quickly, and a random pivot ignores input order.

## P8a: Does the position of k change quickselect's cost (E5)?

Prediction: Quickselect is cheaper at k = 0 and k = 9n/10 than at k = n/2, in time and in comparisons.

Reason (one line): With a random pivot, a k near an end lets each round throw away more of the list in expectation.

## P8b: Does the position of k change median of medians' cost (E5)?

Prediction: Median of medians is within 10% across k = 0, n/10, n/2 and 9n/10.

Reason (one line): The pivot is near the median whatever k is, so each round keeps about half of the list for any k.

## P9a: Do shared prefixes change the comparison counts (E6)?

Prediction: For the same seed, comparison counts are identical across prefix lengths.

Reason (one line): The prefix is the same for every string, so it does not change which string is smaller, and the seeds do not depend on the prefix length.

## P9b: Do shared prefixes change the time ratio between the algorithms (E6)?

Prediction: The ratio of running times between the two algorithms changes by less than 20% across prefix lengths.

Reason (one line): The prefix changes the cost of each comparison and not their number.

## P9c: Do shared prefixes change the running time (E6)?

Prediction: Running time at prefix length 100 is within 30% of prefix length 0 for both algorithms.

Reason (one line): Python compares strings in C, so interpreter overhead dominates.
