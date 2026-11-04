# Median Finding: Randomized Quickselect vs Deterministic Median of Medians

UTS 41052 Advanced Algorithms, Programming Assignment 2, Theme 2 (deterministic vs randomized).
An Loc Nguyen and Thanh Trung Le.
Repository: https://github.com/alngxx/median-finding-benchmark
Video: https://youtu.be/vJGVU6C06bs

## 1. The problem and the algorithms

### The problem (An Loc)

Selection returns the k-th smallest value (k is 0-indexed) of an unsorted list of n comparable values; the median is k = n // 2. Both algorithms aim for O(n), against O(n log n) for sorting. They share the contract `select(a, k, rng)`, raise `ValueError` for an empty list or k out of range, and compare only with `<` and `==` (README.md).

### Randomized quickselect (primary author: An Loc Nguyen)

Quickselect (Cormen et al., 2009, section 9.2) splits the list around a random pivot (`rng.randrange`) into the parts less than, equal to and greater than it. It returns the pivot if k falls in the equal part and otherwise keeps the part that holds k, adjusting k for the greater part. This 3-way split costs 1 comparison for an element less than the pivot and 2 otherwise (`<`, then `==`), and unlike a 2-way partition it removes every copy of the pivot at once (Section 4.2). The loop is iterative because Python's recursion limit is 1,000 (CLAUDE.md).

**Expected time.** A pivot lands in the middle half with probability 1/2 and then leaves at most 3/4 of the list. If I count a bad pivot as a round that does not shrink the list, T(n) <= n + T(n)/2 + T(3n/4)/2, so T(n) <= 2n + T(3n/4) <= 8n element visits. The bound is loose: the `<` count (element visits) averages 3.38n at k = n/2 over 300 seeds (analysis/anloc_asymmetry.md).

### Median of medians (primary author: Thanh Trung Le)

Median of medians uses the same loop but chooses the pivot so that it is never bad. It insertion-sorts a list of at most 25 elements (`BASE_CUTOFF`) and returns element k. Otherwise it splits the list into groups of 5, insertion-sorts each group, and recursively finds the median of the group medians to use as the pivot.

**Why the pivot is always good.** Half of the group medians are at most the pivot, and so are 3 elements in each of their groups, so at least about 3n/10 elements lie on each side (at least 3n/10 - 6; Cormen et al., 2009, section 9.3). A round therefore keeps at most about 7n/10 elements, whatever the input.

**Complexity.** The pivot costs a recursive call on n/5 medians, the next round works on at most 7n/10 elements, and grouping and partitioning cost O(n):

T(n) <= T(n/5) + T(7n/10) + O(n)

Since 1/5 + 7/10 = 9/10 < 1, the work shrinks by a constant factor per level, so the total is O(n) in the worst case. With groups of 3 the fractions in T(n/3) + T(2n/3) + O(n) sum to 1, so every level costs about the same and the total is O(n log n), which E4 tests. Only the pivot step recurses, and every `group_size` uses the cutoff of 25, so E4 compares group sizes alone.

## 2. Theoretical comparison and predictions (An Loc & Trung)

| | Randomized quickselect | Median of medians (g = 5) |
|---|---|---|
| Time, expected | O(n) | O(n) |
| Time, worst case | O(n^2), with tiny probability | O(n) |
| Same cost on every run? | No, depends on the random pivots | Yes |
| Work per round | one partition pass | sort every group of 5, find the median of medians recursively, then one partition pass |
| Extra memory | O(n) for the less, equal and greater lists | O(n) for those lists plus the medians list |
| Sensitive to input order? | No, the pivot is random | Yes, through the insertion sorts inside groups |
| Sensitive to duplicates? | 3-way partition removes every element equal to the pivot | the same |
| Sensitive to the position of k? | Yes, in expectation | Little, the pivot is near the median for any k |

### Predictions (locked before the experiments)

These predictions are copied unchanged from the tag `predictions-locked` (commit 3ae1dd7), set before the official run. Claude Code drafted them and An Loc edited them, having seen only the two numbers listed in report/predictions.md; we did not use Thanh Trung's draft, which followed a pilot run. The locked line "Changes An Loc made: none" is inaccurate; branch backup-predictions (commits 7d5380b and affc099) has the corrected text.

#### P1: Which algorithm is faster on random inputs, and by what factor?

- Prediction: Quickselect is faster by 2x to 5x.

- Reason (one line): Median of medians sorts every group and builds extra lists, and in pure Python that overhead costs more than quickselect's single pass per round.

#### P2: Are both algorithms linear on a log-log plot?

- Prediction: The slope of a log-log plot of time vs n is between 0.9 and 1.2 for both algorithms.

- Reason (one line): Quickselect is linear in expectation and median of medians is linear in the worst case, so only constant factors differ.

#### P3: How wide is the spread of quickselect comparison counts?

- Prediction: The maximum over 1000 seeds is 1.5 to 3 times the mean.

- Reason (one line): One bad early pivot keeps most of the list, so the count has a long right tail, but a pivot that bad is rare at n = 10^5.

#### P4: Does median of medians with g = 3 grow faster than with g = 5?

- Prediction: Slightly, but the difference is hard to see on the plot.

- Reason (one line): The worst case with g = 3 is n log n, but random input gives pivots far better than the worst case, so the curve stays close to linear.

#### P5: How does g = 7 compare with g = 5?

- Prediction: g = 7 and g = 5 are within 10% of each other in time.

- Reason (one line): A larger group costs more to sort per element, but it leaves fewer medians to recurse on, and the two effects roughly cancel.

#### P6: Does `sorted()` beat both algorithms?

- Prediction: sorted() beats both algorithms at small n. At n = 10^6, quickselect is within 2x of sorted() and might beat it.

- Reason (one line): sorted() is n log n but runs in C, while quickselect does a few linear passes in Python.

Most uncertain prediction.

#### P7: What is the worst input family for each algorithm?

- Prediction: Quickselect: all_equal and few_distinct are the cheapest families. random, sorted and reverse_sorted are within 10% of each other in time and comparisons. Median of medians: reverse_sorted is the most expensive, because insertion sort on reversed groups does the most swaps.

- Reason (one line): The 3-way partition removes every element equal to the pivot, so duplicates shrink the list quickly, and a random pivot ignores input order.

#### P8a: Does the position of k change quickselect's cost (E5)?

- Prediction: Quickselect is cheaper at k = 0 and k = 9n/10 than at k = n/2, in time and in comparisons.

- Reason (one line): With a random pivot, a k near an end lets each round throw away more of the list in expectation.

#### P8b: Does the position of k change median of medians' cost (E5)?

- Prediction: Median of medians is within 10% across k = 0, n/10, n/2 and 9n/10.

- Reason (one line): The pivot is near the median whatever k is, so each round keeps about half of the list for any k.

#### P9a: Do shared prefixes change the comparison counts (E6)?

- Prediction: For the same seed, comparison counts are identical across prefix lengths.

- Reason (one line): The prefix is the same for every string, so it does not change which string is smaller, and the seeds do not depend on the prefix length.

#### P9b: Do shared prefixes change the time ratio between the algorithms (E6)?

- Prediction: The ratio of running times between the two algorithms changes by less than 20% across prefix lengths.

- Reason (one line): The prefix changes the cost of each comparison and not their number.

#### P9c: Do shared prefixes change the running time (E6)?

- Prediction: Running time at prefix length 100 is within 30% of prefix length 0 for both algorithms.

- Reason (one line): Python compares strings in C, so interpreter overhead dominates.

## 3. Experimental methodology (Trung)

`bench/run_bench.py` runs every experiment, and `bench/plot.py` draws every figure from the committed CSV files in `results/`:

```
python -m bench.run_bench all
python -m bench.plot
```

The official run (commit 3cc528c) took 1,553 s (about 26 minutes; notes/trung.md), and every number here comes from it. Before the predictions tag we saw rough pilot numbers (`notes/pilot-numbers-seen.md` lists what Thanh Trung and Claude saw, with dates), and the output of one full run started by mistake was moved out of the repository unanalysed.

### Input families

| Family | Content | Why we include it |
|---|---|---|
| random | random permutation of 0 to n - 1 | the typical case |
| sorted, reverse | 0 to n - 1 ascending, or descending | tests whether the order of the input matters |
| all equal | n copies of 0 | the extreme case of duplicates; separates the 3-way and 2-way partitions |
| few distinct | n values drawn from 0 to 9 | many duplicates, but not all equal |
| organ pipe | rises to a peak in the middle, then falls | a structured order that is neither sorted nor random. For even n the peak value appears twice (n = 6 gives 0 1 2 2 1 0) |
| strings | a fixed prefix of 0, 20 or 100 letters, then 10 random letters | makes each comparison more expensive without changing the order |

### Experiments

| ID | Question | Setup |
|---|---|---|
| E1 | How do both algorithms scale? | random, k = n/2, 10 sizes from 10^3 to 10^6 spaced evenly on a log scale, 10 instances per size |
| E2 | Which inputs hurt which algorithm? | all six integer families at n = 10^5, k = n/2, 10 instances. A second part compares quickselect's 3-way partition with a 2-way partition on the same six families at n = 10^4 |
| E3 | How long is quickselect's tail? | one fixed random instance, n = 10^5, k = n/2, run with random seeds 0 to 999, comparison counts only |
| E4 | Why groups of 5? | median of medians with group size 3, 5, 7 and 9, same sizes and instances as E1 |
| E5 | Does the position of k matter? | random, n = 10^5, k = 0, n/10, n/2 and 9n/10, 10 instances |
| E6 | What changes when comparisons are slow? | strings with prefix length 0, 20 and 100, the E1 sizes up to 10^5, k = n/2, 5 instances |

E1, E2, E5 and E6 also run the `sorted(a)[k]` baseline (Python's Timsort, in C) as the practical choice, not a compared algorithm. E2's 2-way part stops at n = 10^4 because it is quadratic on all-equal input (Section 4.2), E6 stops at n = 10^5 with 5 instances to keep the full run under half an hour, and we dropped E7, an adversary experiment (Section 6).

### Measurement

- **Machine.** AMD Ryzen 9 6900HS Creator Edition (8 cores, 16 logical processors; L1 cache 512 KB, L2 4 MB, L3 16 MB), Windows 11 Home, CPython 3.13.1 in a virtual environment; Best performance power mode, plugged in, screen on, no other programs.
- **Timing.** Inputs are generated and copied before the timer starts. Each configuration gets one untimed warm-up and 5 timed runs (`time.perf_counter`, garbage collector off), and the figures show the median and interquartile range.
- **Comparison counts.** A separate, untimed run wraps each element in a `Counted` object (`bench/counting.py`) that counts `<` and `==` and raises on any other comparison. Counts are machine-independent, include median of medians' insertion sorts, and can reach twice a textbook count because of our 3-way partition (Section 1).
- **Random seeds.** Each generator (`bench/generators.py`) uses its own `random.Random(seed)`, and instance i uses seed i; quickselect uses rng seeds 1000i to 1000i + 4 for timing and 1000i for counting, so every run can be repeated.
- **Correctness and fairness.** Every answer is checked against `sorted(a)[k]`, and both pure-Python algorithms must agree on the same instances, or the run stops. The 207 tests cover edge and error cases, and mutation testing found two gaps, now closed (Section 8.2, example 5).

### Timing check

We discarded our first official run (commit 4f701e8) after median of medians took 64 ms in E1 but 154 ms in E4 and 161 ms in E5 on the same configuration (random, n = 10^5, k = n/2). The processor had slowed down, most likely because Windows reduced performance after the screen turned off; we did not test this. In the re-run, median of medians agrees within 4% (63 to 65 ms across E1, E2, E4 and E5) and `sorted()` within 6% (10.9 to 11.6 ms), quickselect varies more (14.2 ms in E1, 11.8 ms in E5), and comparison counts match the first run.

## 4. Results and analysis

### 4.1 Scaling (E1) (Trung)

![E1 time](../figures/e1_time_loglog.png)
![E1 comparisons](../figures/e1_comparisons_per_n.png)

Both algorithms are linear (P2), but median of medians is 4.4 to 5.6 times slower up to n = 2.15 * 10^5 (65.1 against 14.2 ms at n = 10^5), after which quickselect slows down per element (Section 5.1). Sorting every group of 5 gives median of medians 9.1n to 10.0n comparisons, about twice quickselect's 3.9n to 5.9n. The rest is likely Python overhead that counts miss (slicing groups, building the medians list, recursion); we did not test this.

`sorted()` beats quickselect at every n (P6) despite 1.6 to 3.4 times more comparisons (8.7n rising to 18.6n), likely because Timsort compares in C rather than in the Python interpreter; we did not test this.

### 4.2 Input families (E2) (Trung)

![E2 families](../figures/e2_families_time.png)
![E2 duplicates](../figures/e2_duplicates_comparisons.png)

Input order hardly changes quickselect's comparisons (P7, Section 4.7), and we treat its time differences as noise: the interquartile ranges overlap (10.2 to 14.7 ms against 8.2 to 11.8 ms for random and sorted), identical runs varied by about 20% between experiments, and the layout check found no effect (ratio 0.98 at n = 10^5, `analysis/trung_memory_layout.md`).

Median of medians depends on order through its insertion sorts: reverse input costs most (P7 row) because every group arrives reversed, and sorted input least among the distinct families (7.37n, 41.5 ms).

On all equal input at n = 10^4 the 2-way partition makes 37,502,499 comparisons (0.375 n^2) and takes 1.24 s, against 20,000 comparisons and 0.4 ms for the 3-way partition. On distinct values it makes about a third fewer comparisons (2.87n against 4.47n) but is slower (1.85 against 1.11 ms).

### 4.3 Quickselect's tail (E3) (An Loc)

![E3 tail](../figures/e3_quickselect_tail.png)

Over 1000 rng seeds on one instance (n = 10^5, k = n/2), quickselect's mean is 505,000 comparisons (5.05 per element) and its median 487,000 (4.87), a right skew (analysis/anloc_numbers.md; results/e3.csv). The standard deviation is 1.49 per element, the 99th percentile 8.99, the minimum 2.08 and the maximum 986,000 (9.86 per element, 1.95 times the mean). With the instance fixed, the random pivots cause all of this spread, likely because a bad early pivot keeps most of the list for another pass while a good one removes about half; we did not test this.

Median of medians, which makes no random choices, used 969,000 comparisons (9.69 per element); quickselect's unlucky tail reaches that cost but stays below it in 998 of the 1000 seeds.

### 4.4 Group size (E4) (Trung)

![E4 group size](../figures/e4_group_size.png)

Groups of 3 lose linearity (P4), as the g = 3 recurrence in Section 1 predicts, and their time per element rises from 773 to 1,368 ns; g = 5 comparisons rise only 11% (9.07 to 10.03). Groups of 7 and 9 make slightly more comparisons (10.11n and 10.73n at 10^6), yet g = 7 is 4 to 8% faster than g = 5 at every n, perhaps through fewer list slices and Python calls per element; we did not measure this.

### 4.5 Position of k (E5) (An Loc)

![E5 k position](../figures/e5_k_position.png)

Source: analysis/anloc_numbers.md (results/e5.csv).

| k | comparisons per element (median over 10 instances) | min to max over instances | time (ms, pooled median of all 50 timed runs) | time min to max (ms, over the 50 runs) |
|---|---|---|---|---|
| 0 | 2.59 | 2.17 to 3.86 | 6.58 | 4.00 to 33.5 |
| n/10 | 3.14 | 2.43 to 6.46 | 8.49 | 5.00 to 16.7 |
| n/2 | 4.52 | 3.05 to 8.74 | 11.8 | 7.21 to 20.8 |
| 9n/10 | 4.35 | 2.06 to 5.81 | 9.77 | 4.49 to 29.8 |

Median of medians stays at 9.90 to 9.92 comparisons per element for every k (P8b).

### 4.6 Slow comparisons (E6) (Trung)

![E6 shared prefix](../figures/e6_shared_prefix.png)

Shared prefixes slow every comparison without changing the order, so comparison counts stay identical across prefix lengths (quickselect 6.70n, median of medians 9.88n, `sorted()` 15.32n at n = 10^5). From prefix length 0 to 100, time rises by 24%, 9% and 76%, yet the extra time per comparison is similar (4.9, 6.4 and 7.1 ns), likely the cost of scanning the 100 shared characters in C (we did not test this). That cost is small next to median of medians' time, which is likely dominated by Python overhead (we did not test this), and large next to `sorted()`'s.

### 4.7 Predictions against results (Trung; rows P3, P8a and P8b by An Loc)

| Prediction | Result | Held? |
|---|---|---|
| P1 | Median of medians / quickselect time: 4.4 to 5.6 for n up to 2.15 * 10^5, 3.0 at 4.64 * 10^5, 2.1 at 10^6 | Mostly held (above 5 at four sizes) |
| P2 | Log-log slope 1.13 for quickselect, 1.05 for median of medians | Held |
| P3 | Maximum / mean = 1.95 over 1000 seeds, predicted 1.5 to 3 (analysis/anloc_numbers.md) | Held |
| P4 | g = 3 comparisons per element +33% (10.05 to 13.32) from 10^3 to 10^6, against +11% for g = 5; clearly visible | Failed |
| P5 | g = 7 / g = 5 time 0.92 to 0.96 at every n | Held |
| P6 | sorted() faster than quickselect at every n: 3.59 times at 10^3, 1.07 at 2.15 * 10^5, 1.74 at 10^6; quickselect never wins | Held (the "might beat it" part did not happen) |
| P7 | Quickselect: all equal 2.00n, few distinct 4.20n; random / sorted / reverse 4.52n / 4.41n / 4.06n, time 12.3 / 10.3 / 9.8 ms with overlapping ranges. Median of medians: reverse most expensive (11.41n, 74.0 ms) | Partly held: duplicates are cheapest in time (all equal 3.6 ms, few distinct 7.4 ms) but not in comparisons (reverse 4.06n is below few distinct 4.20n); random, sorted and reverse differ by 11% in comparisons; the median-of-medians part held |
| P8a | E5 medians (analysis/anloc_numbers.md): 2.59 comparisons per element at k = 0 and 4.52 at n/2, so k = 0 is clearly cheaper. At k = 9n/10 it is 4.35, only 4% below n/2, and the ranges overlap (2.06 to 5.81 against 3.05 to 8.74). Time: 6.58, 11.8 and 9.77 ms. The 300-seed supplementary means (analysis/anloc_asymmetry.md, comparisons only, k = 0 not rerun) are 4.17 (standard error 0.094) at 9n/10 against 5.07 (0.096) at n/2, so that end is clearly cheaper too | Held |
| P8b | Largest relative difference across k = 0, n/10, n/2, 9n/10: 0.146% in comparisons, 0.950% in time, predicted within 10% (analysis/anloc_numbers.md) | Held |
| P9a | Counts identical across prefix lengths for every instance | Held |
| P9b | Median of medians / quickselect time 4.94, 5.04, 4.36 (at most 14% change) | Held |
| P9c | Prefix 100 against 0: quickselect +24%, median of medians +9% | Held |

Quickselect wins on time at every size and on comparisons in 998 of 1000 seeds (Section 4.3). Median of medians wins only on its worst-case guarantee and identical cost every run, which we did not test against an adversary because E7 was dropped.

## 5. What surprised us

### 5.1 Quickselect slows down once the data outgrows the cache (Trung)

**Predicted and measured.** P2 holds over the whole range and P1 mostly holds, but both hide a jump at large n: quickselect's time per element is flat up to n = 2.15 * 10^5 (113 to 144 ns), then reaches 258 ns at 4.64 * 10^5 and 420 ns at 10^6, while its comparisons per element barely change (5.2n to 5.9n).

**Explanation and check.** `random_perm` creates the int objects in value order and then shuffles the list, so a pass over it jumps around memory. At about 40 bytes per element (an int object plus a pointer), the data grows from about 8.6 MB at 2.15 * 10^5 to 18.6 MB at 4.64 * 10^5, crossing our processor's 16 MB L3 cache (the 40 bytes and the 16 MB L3 cache are not recorded in results/environment.txt; our estimate). `analysis/trung_memory_layout.py` repeats each run, with the same values and seeds, on a list whose int objects were created in list order: layout makes no difference at n = 10^5 (ratio 0.98), but at 4.64 * 10^5 and 10^6 the shuffled layout makes quickselect 1.92 and 2.09 times slower, against 1.17 and 1.22 for median of medians and 1.30 and 1.25 for `sorted()`. Yet in list order, quickselect's time per element still doubles (132 to 267 ns from 10^5 to 10^6), so layout explains about half the jump. The rest may come from the pointer list outgrowing the cache or from building new lists; we did not measure this or count cache misses.

### 5.2 An asymmetry in k that did not survive a larger sample (An Loc)

**Predicted and measured.** P8a said k = 0 and k = 9n/10 cost less than k = n/2 because a k near an end lets each round discard more, a reason that treats both ends alike, so k = n/10 and k = 9n/10 should cost the same. Yet in E5 the median cost was 3.14 comparisons per element at k = n/10 and 4.35 at k = 9n/10 (a gap of 1.21), and the means were 3.65 and 4.25 (a gap of 0.60; analysis/anloc_numbers.md).

**Explanation.** Our first guess, the counting rule (Section 1), cannot cause this gap in expectation. A round on m distinct elements whose pivot has rank r costs 2m - r comparisons at k and, with the pivot of rank m - 1 - r, m + 1 + r at the mirror position m - 1 - k, leaving lists of the same size. A uniform pivot rank gives both an expected (3m + 1)/2, so by induction on m the expected totals are equal. An independent Claude Code review session derived this, and we checked it (8.2, example 4); `analysis/anloc_symmetry.py` checks it exactly for list sizes up to 60, and the cost model against the real `select` (analysis/anloc_symmetry.md).

**Test and conclusion.** We ran 300 other seeds (1000 to 1299) with the same instance and rng seed for every k (analysis/anloc_asymmetry.md; supplementary, not part of the committed E5 data). Mean comparisons per element were 3.98 (standard error 0.0611) at k = n/10, 5.07 (0.0957) at k = n/2 and 4.17 (0.0942) at k = 9n/10, and the paired difference between k = 9n/10 and k = n/10, 0.190 (standard error 0.123), is about 1.5 standard errors from 0. Separate `<` and `==` counts matched the committed E5 totals in 40 of 40 runs. So the E5 gap was sampling noise from too few instances for so variable a cost (2.06 to 5.81 per element at one k), and an independent derivation caught it, not the data.

## 6. What we would do next (Trung)

Four questions remain: what an adaptive adversary (E7), which can defeat deterministic pivot rules (not verified), does to a random pivot and to median of medians; how the lecturer's suggested faster selection algorithms, which we did not try, compare; whether list building explains the rest of quickselect's large-n slowdown (Section 5.1), as an in-place partition would test; and how textbook counting (1 comparison per element) compares with published figures.

## 7. Individual contributions

**An Loc Nguyen.** I specified and reviewed quickselect, its 2-way variant, and their tests, the generators (`bench/generators.py`) and the counting wrapper (`bench/counting.py`), while Claude Code wrote most of the code. I set up the repository, `CLAUDE.md` with specific rules, and the README. I specified the E3, E5, 300-seed, and symmetry analysis scripts, which Claude Code wrote. I wrote or edited Sections 1 (the problem and quickselect), 2 (the note on the predictions), 4.3, 4.5, 5.2, my rows in 4.7, and my individual reflection. I reviewed and edited the locked predictions and kept the AI error log and a shared task list (not committed). For the video, I recorded the overview and the quickselect deep dive, with subtitles show up as I speak. I spent about 17 hours in total.

**Thanh Trung Le.** I am the primary author of median of medians and its tests, and I own the runner (`bench/run_bench.py`), the plots (`bench/plot.py`) and their smoke tests. Claude generated the first version of each; I reviewed and ran median of medians and its tests and, with mutation testing, closed two gaps in them. I ran every experiment, re-ran them after noticing that a CPU slowdown spoiled the first official run, and wrote the memory-layout check (`analysis/trung_memory_layout.py`). With Claude drafting and me editing, I wrote Sections 1 (median of medians), 3, 4.1, 4.2, 4.4, 4.6, 5.1 and 6 and my rows of 4.7, and did the main final edit. For the video I recorded my deep dive and the results and stitched the segments; An Loc recorded the overview and the quickselect deep dive. I read An Loc's `quickselect.py` and found no problems but did not test it independently. I spent about 20 hours.

## 8. AI use

### 8.1 How each of us used AI

**An Loc Nguyen.**

- I used Claude (claude.ai chat) to plan the work, write prompts for Claude Code, draft emails to the lecturer, check report numbers against the analysis files, and draft Sections 5.2, 7, 8 and my reflection from our committed files, which I read and edited.
- I used Claude Code (Sonnet 5.5, medium effort) to write the generators, the counter, quickselect, the tests, the README, `CLAUDE.md`, the analysis scripts and the first draft of my parts of Sections 1, 2 and 4.
- I also used Claude Code (Opus 5.5) to review quickselect, build the slides and rewrite my sections in plainer language, which I read and edited, and Claude drafted my video scripts, which I edited. The review ran in a separate session from the coding session.
- Thanh Trung removed the AI-DRAFT marks in the final edit, and I read and checked my paragraphs on 4 November.
- What I checked: I compared every number in my report parts with `analysis/anloc_numbers.md` and `analysis/anloc_asymmetry.md`, and I read quickselect and Cormen et al. (2009, section 9.2).
- What I took on trust: Thanh Trung's code, results and sections, and the 207 passing tests.

**Thanh Trung Le.**

- I used Claude (claude.ai, one long session with a cloud workspace) for most of my part. It generated median of medians and its tests, the runner, the plots, the smoke tests, and the memory-layout script; computed the numbers in my sections from the CSVs; and drafted my report sections, my status reports to An Loc, and my unused predictions draft.
- I also used it to explain median of medians and the recurrence until I could explain them myself.
- What I checked: I ran pytest (207 passing) and every experiment on my machine, re-ran everything after the CPU slowdown, ran the memory-layout check, and checked my numbers against the CSVs.
- What I took on trust: that the tests cover the important cases beyond the two gaps mutation testing found, and the statistics Claude computed that I did not recompute.

### 8.2 Where AI was wrong, unhelpful or misleading

**1. A wrong expected-time argument in a comment (An Loc).** Claude Code wrote that quickselect's expected work is n + 3n/4 + ... = 4n, assuming every pivot is good, though a bad pivot can remove almost nothing. The independent review pointed this out, and I redid the recurrence by hand to get the 8n bound in Section 1. We rewrote the comment.

**2. An experiment size that was infeasible (An Loc).** The brief I wrote with Claude asked E2 to run the 2-way partition at n = 10^5 on every family, about 3.75 * 10^9 comparisons per call on all-equal input. Thanh Trung's session caught this against my measured 1,500,499 comparisons at n = 2000, and we cut that part of E2 to n = 10^4.

**3. A wrong explanation of the counter (An Loc).** Claude said `Counted` needed its `TypeError` methods because reflected comparisons such as `a > b` would go uncounted, but Python counts them through `__lt__` and `__eq__`; the overrides only enforce the `<` and `==` rule. Claude noticed on rechecking Python's comparison rules, and we corrected the docstring in `bench/counting.py`, which was wrong from e0edf6c (24 October) to 07f63d4 (3 November).

**4. A wrong explanation of an asymmetry (Both).** When E5 showed a gap between k = n/10 and k = 9n/10, a draft guide note suggested, and Claude supported, that our counting rule makes a search near the top pay more. An independent review session derived that this cannot happen in expectation, and we checked it (Section 5.2). We removed the explanation from Sections 4.5 and 5.2.

**5. Tests that missed two complexity bugs (Thanh Trung).** The first median-of-medians tests, generated by Claude, checked answers but not cost, and mutation testing showed two bugs passing them: a pivot taken from the first group median (losing the O(n) guarantee) and a group size dropped from the recursive call (which would have made E4 wrong). With the first bug the test run took 51 s instead of about 4 s, yet every test passed. We added tests that comparisons stay below 30n on every input family and that the group size reaches the recursive call.

**6. A memory-layout claim that was noise (Thanh Trung).** Claude's first draft of Section 4.2 blamed memory layout for quickselect being 19% slower on random than on sorted input at almost the same comparison count. Trung's layout check found no effect at n = 10^5 (ratio 0.98) and the interquartile ranges overlap, so we rewrote 4.2 to treat the difference as noise.

**7. A citation nobody had read (An Loc).** Claude suggested citing a 1961 paper that neither of us had read and kept it with a "not verified" note. We removed it and now cite only Cormen et al., 2009.

### 8.3 AI in group work

**Where it helped.** Written briefs (`CLAUDE.md`) kept two people and two Claude Code sessions on the same rules: one author per file, only `<` and `==`, and no git command that changes the repository (An Loc allowed a few fetch and fast-forward pull commands in some prompts). Status files kept each of us informed, a plan check caught an infeasible experiment (example 2), and the error log kept mistakes visible.

**Where it hurt or threatened to.** An AI drafted the locked predictions, so they do not purely reflect what either of us believed (Section 2). AI-written text also carried errors between us, caught only by rereading: a role split swap and an overstated proposal-email rule in the plan files, and the inaccurate "Changes An Loc made: none" that Claude wrote into the locked predictions in Trung's session. AI drafts looked finished before anyone checked the numbers (a first E5 table used a different time statistic than the figures: 6.80 ms vs. 6.58 ms at k = 0), and passing tests made it easy to skip reading each other's work.

## References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to algorithms* (3rd ed.). MIT Press.
