# Predictions

> Lock this file with the git tag `predictions-locked` before any experiment. Never edit it afterwards.

## Authorship

Drafted with Claude Code from the structure of the algorithms. An Loc states that he saw no experiment results. The drafting session reported opening these files: CLAUDE.md, README.md, .gitignore, pytest.ini, requirements.txt, .github/workflows/ci.yml, every .py file in selection/, bench/ and tests/ (tests/ partly: headers and test names for some files), notes/ai-error-log.md, notes/anloc.md, notes/trung.md and report/predictions.md. It listed results/ and figures/ (only .gitkeep files) and opened nothing outside the repo except its scratch folder. It also ran pytest, which runs the smoke tests, and ran each of e1 to e6 with --quick into a scratch folder, then read only row counts and algorithm names from those files, not timings. This is self-reported and not verified. Thanh Trung's separate draft was written after he saw numbers from a pilot run (details in the section below).

## Differences with Trung's draft

Changes An Loc made:

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

Prediction: Quickselect: all_equal is cheapest, and every other family is within 10% of random. Median of medians: reverse_sorted is the most expensive, because insertion sort on reversed groups does the most swaps.

Reason (one line): A random pivot ignores input order, and the 3-way partition finishes all_equal in one round.

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
