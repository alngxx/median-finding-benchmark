# Median Finding: Randomized Quickselect vs Deterministic Median of Medians

UTS 41052 Advanced Algorithms, Programming Assignment 2, Theme 2 (deterministic vs randomized).
An Loc Nguyen and Thanh Trung Le.
Repository: https://github.com/alngxx/median-finding-benchmark
Video: [unlisted YouTube link]

<!--
HOW TO USE THIS FILE (delete this block before submitting)
- Text inside <!- - ... - -> blocks is a writing guide. It does not show when the file is rendered. Delete every guide block before submitting.
- [Square brackets] mark things to fill in.
- Section 1 (median of medians part) and section 3 were drafted with Claude and edited by Trung. Say so in section 8.
- Every number must come from a committed CSV in results/ (official run, commit 3cc528c). The numbers listed in the guide blocks were computed from those CSVs on 2 Nov.
- Target length: 4,000 to 6,000 words in total. Word targets per section are in each guide block.
- Use the /writing-clearly-and-concisely skill. No long dashes (CLAUDE.md).
-->

<!--
WHO WRITES WHAT (delete this block before submitting)

| Part | Writer | Status |
|---|---|---|
| 1. The problem | An Loc | to write |
| 1. Randomized quickselect | An Loc | to write |
| 1. Median of medians | Trung | drafted |
| 2. Comparison table and paragraphs | Both: An Loc the quickselect paragraph, Trung the median-of-medians paragraph | table drafted |
| 2. Predictions | (copied from the locked file, do not edit) | done |
| 3. Experimental methodology | Trung | drafted; add CPU model and the pilot sentence |
| 4.1 Scaling (E1) | Trung | to write |
| 4.2 Input families (E2) | Trung | to write |
| 4.3 Quickselect's tail (E3) | An Loc | to write |
| 4.4 Group size (E4) | Trung | to write |
| 4.5 Position of k (E5) | An Loc | to write |
| 4.6 Slow comparisons (E6) | Trung | to write |
| 4.7 Predictions against results | Trung fills the table; An Loc fills the rows P3, P8a, P8b | to write |
| 5.1 Surprise | Trung (a surprise about median of medians or E1, E2, E4, E6) | after the results call |
| 5.2 Surprise | An Loc (a surprise about quickselect, for example the asymmetry in k) | after the results call |
| 6. What we would do next | Trung | to write |
| 7. Contributions | Each writes their own paragraph | to write |
| 8.1 How each of us used AI | Each writes their own paragraph | to write |
| 8.2 Three AI mistakes | Both: agree on three, each writes up the ones from their own work | to write |
| 8.3 AI in group work | Both: An Loc drafts, Trung edits | to write |
| References | Each adds what they cite | started |
| Final edit, word count, remove guide blocks | Trung | last |

To avoid merge conflicts: each person edits only their own parts, pulls before starting and pushes after each session.
-->

## 1. The problem and the algorithms

<!--
GUIDE (about 700 words in total; An Loc: problem + quickselect, about 350; Trung: median of medians, drafted below)
The brief: "State the problem precisely. Describe each algorithm at a level that someone in the class who hasn't seen it could understand: the key idea, the complexity, and what makes it different from the others."
-->

### The problem (An Loc)

<!-- WRITER: An Loc -->

<!-- AI-DRAFT: An Loc to review and rewrite -->
Selection takes an unsorted list of n comparable values and an index k (0-indexed) and returns the k-th smallest value. The median is k = n // 2. Sorting the list and reading element k takes O(n log n) time, but it orders far more than the question needs, and both of our algorithms aim for O(n). They share one contract, `select(a, k, rng)`, which raises `ValueError` for an empty list or k out of range and compares elements only with `<` and `==`, so one wrapper counts the comparisons of both algorithms in the same way (README.md).

### Randomized quickselect (primary author: An Loc Nguyen)

<!-- WRITER: An Loc -->

<!-- AI-DRAFT: An Loc to review and rewrite -->
Quickselect (Hoare, 1961; details of the citation not verified) repeats one round until it can answer. A round picks a pivot uniformly at random with `rng.randrange`, then splits the current list into three parts using only `<` and `==`: the elements less than the pivot, equal to it, and greater than it. If k is below the size of the less part, the loop continues with the less part. If k falls inside the equal part, the pivot is the answer. Otherwise the loop continues with the greater part, and k is reduced by the sizes of the less and equal parts. The loop is iterative, because Python's recursion limit is 1,000 (CLAUDE.md).

**Expected time.** A pivot lands in the middle half of the elements with probability 1/2, and then the next list has at most 3/4 of the elements. Counting a bad pivot as a round that does not shrink the list, the expected work satisfies T(n) <= n + T(n)/2 + T(3n/4)/2. This gives T(n) <= 2n + T(3n/4), so T(n) <= 8n element visits. The bound is loose; the measured counts are in sections 4.1 and 4.3. We have not checked the argument against CLRS (not verified). The worst case is O(n^2), but it needs a long run of bad pivots, so its probability is tiny.

**Duplicates and counting.** The 3-way split removes every element equal to the pivot in one round. A 2-way partition does not: on a list of all equal values with n = 2000, `select` used 4,000 comparisons and `select_two_way` used 1,500,499 (notes/anloc.md, from a unit test). Our 3-way split costs 1 comparison for an element less than the pivot and 2 otherwise (`<`, then `==`).

### Median of medians (primary author: Thanh Trung Le)

<!-- WRITER: Trung (drafted) -->

Median of medians (Blum, Floyd, Pratt, Rivest and Tarjan, 1973) uses the same loop as quickselect: pick a pivot, split the list into the elements less than, equal to and greater than the pivot, and keep only the part that holds the k-th smallest value. The difference is how the pivot is chosen. Quickselect picks it at random and relies on luck. Median of medians spends work on the choice, so that the pivot is never bad.

Each round works like this:

1. If the list has at most 25 elements (`BASE_CUTOFF`), sort it with insertion sort and return element k.
2. Split the list into groups of 5. Sort each group with insertion sort and take its middle element.
3. Call the algorithm recursively on the list of group medians to find their median. This value is the pivot.
4. Partition the list into less, equal and greater, and continue in the part that holds k.

**Why the pivot is always good.** Half of the group medians are at most the pivot. Each of those groups has 3 elements that are at most its median, and so at most the pivot. That gives at least about 3n/10 elements on the low side of the pivot, and by the same argument at least about 3n/10 on the high side (more precisely, at least 3n/10 - 6; Cormen et al., 2009, section 9.3). So whatever the input, the part we keep has at most about 7n/10 elements.

**Complexity.** Finding the pivot costs a recursive call on n/5 medians, the next round works on at most 7n/10 elements, and grouping and partitioning cost O(n):

T(n) <= T(n/5) + T(7n/10) + O(n)

Because 1/5 + 7/10 = 9/10 < 1, the work shrinks by a constant factor at each level and the total is O(n) in the worst case, for every input. With groups of 3 the same argument gives T(n/3) + T(2n/3) + O(n). The fractions sum to 1, so each level costs about the same and the total becomes O(n log n). Experiment E4 tests this. The extra memory is O(n) for the less, equal and greater lists.

**What makes it different.** Quickselect is O(n) only in expectation and can take O(n^2) on an unlucky run. Median of medians guarantees O(n) and gives the same result and the same cost on every run, but it pays for the guarantee with a larger constant: every round sorts all the groups and makes an extra recursive call just to choose the pivot.

**Our implementation.** Only the pivot step is recursive. Continuing into less or greater is a loop, so the recursion depth grows with the logarithm of n, base 5, and stays small. Elements are compared only with `<` and `==`, so the comparison counter treats both algorithms the same. The group size is a parameter (`group_size`, an odd integer of at least 3, default 5), and the cutoff of 25 is the same for every group size so that E4 compares group sizes alone.

## 2. Theoretical comparison and predictions (An Loc & Trung)

<!-- WRITER: Both (An Loc: quickselect paragraph; Trung: median-of-medians paragraph). Predictions block: copied, do not edit -->

<!--
GUIDE (about 800 words; both)
The brief: compare on paper (asymptotic complexity, constant factors and memory as far as you can reason, the input features each one is sensitive to), then commit to predictions written BEFORE the experiments. Do not revise them.
- Fill in or check the table below (theory only, no results).
- Add 2 or 3 short paragraphs on constant factors: work per round (quickselect: one partition pass; median of medians: sorting every group, building the medians list, a recursive call, then a partition pass), and what that means for comparisons per element.
- The predictions below are copied word for word from report/predictions.md at the tag predictions-locked (commit 3ae1dd7). Do not edit them.
-->

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

<!-- AI-DRAFT: An Loc to review and rewrite -->
Quickselect does one partition pass per round and no other work, so a round costs about the length of the current list, with 1 comparison for an element less than the pivot and 2 otherwise. The total varies from run to run because the pivots are random, and it does not depend on the order of the input, because the pivot is random. Duplicates make it cheaper, since the 3-way partition drops every element equal to the pivot. Its cost depends on k in expectation: with a random pivot, a k near an end lets each round discard more of the list.

[Paragraphs on constant factors and what each algorithm is sensitive to.]

### Predictions (locked before the experiments)

The predictions below were written before the official run and locked with the git tag `predictions-locked` (commit 3ae1dd7). They are copied unchanged. An Loc's draft was locked. Thanh Trung's draft, written after he saw rough numbers from a pilot run, is recorded in `report/predictions.md` but was not used.

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

<!-- WRITER: Trung (drafted) -->

<!--
GUIDE (about 900 words; Trung, drafted below)
The brief: "a skeptical reader could rerun your experiments from this section plus the repository and expect to see your plots reproduced."
Still to fill: the CPU model (Task Manager > Performance > CPU).
-->

All experiments run through one script, `bench/run_bench.py`, and every figure comes from `bench/plot.py` reading the committed CSV files in `results/`. The commands are:

```
python -m bench.run_bench all
python -m bench.plot
```

The official run (commit 3cc528c) took 1,553 s (about 26 minutes) on the machine described below.

### Input families

All generators are in `bench/generators.py`. Each takes a size n and a seed and uses its own `random.Random(seed)`, so every instance can be regenerated exactly.

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

E1, E2, E5 and E6 run quickselect, median of medians (group size 5) and the `sorted(a)[k]` baseline. The baseline is not one of the compared algorithms. It is Python's built-in Timsort, written in C, and it shows how pure-Python selection compares with the practical choice.

Two sizes differ from our first plan. The 2-way partition part of E2 runs at n = 10^4, not 10^5: on all-equal input the 2-way partition removes one element per round, which is about 0.375 n^2 comparisons (37,502,499 measured at n = 10^4). One such call took 1.24 s at n = 10^4, so at n = 10^5 each call would take about 2 minutes and that part alone about 2.5 hours. E6 stops at n = 10^5 with 5 instances to keep the full run under half an hour. A third experiment we planned, E7 (a McIlroy-style adversary), was dropped for lack of time (section 6).

### Measurement

- **Machine.** [CPU model], 16 logical CPUs, Windows 11, CPython 3.13.1 in a virtual environment, Power mode set to Best performance, plugged in, screen on, no other programs running.
- **Timing.** Each input is generated and copied before the timer starts, so we time the algorithm, not the generator. Each configuration gets one untimed warm-up run, then 5 timed runs with `time.perf_counter`, with Python's garbage collector switched off during each call. Every run is stored, and the figures show the median with the interquartile range, not only an average.
- **Comparison counts.** A separate, untimed run wraps every element in a `Counted` object (`bench/counting.py`) whose `<` and `==` add to a counter, and any other comparison raises an error. Counts do not depend on the machine, so they let us check explanations that timing alone cannot. We count every real `<` and `==`. Our 3-way partition costs 1 comparison for an element less than the pivot and 2 otherwise, so our counts can be up to twice a textbook count, which charges 1 per element. For this reason we do not test the textbook figures of about 1.5n comparisons for Floyd-Rivest and about 2n for any deterministic algorithm directly. Median of medians also counts the comparisons inside its insertion sorts.
- **Random seeds.** Instance i uses generator seed i. Quickselect's timed runs use seeds 1000i to 1000i + 4, and its counting run uses seed 1000i, so every run can be repeated exactly.

### Correctness and fairness

- Every answer, timed or counted, is checked against `sorted(a)[k]` before it is stored, and on every instance quickselect and median of medians must return the same value. Any mismatch stops the run.
- Both algorithms are pure Python, share one interface (`select(a, k, rng)`), receive the same instances, and compare only with `<` and `==`.
- The test suite has 207 tests, including edge cases (one element, all equal, two values, sorted, reverse, negative numbers, floats, strings) and error cases. We also used mutation testing: we deliberately inserted bugs to check that the tests catch them. Two bugs in median of medians gave correct answers and passed the first version of the tests: choosing the first group median as the pivot, which loses the O(n) guarantee, and ignoring the group size in the recursive call, which would have made E4 wrong. We added a test that comparisons stay below 30n on every input family and a test of the group size passed to the recursive call, and both bugs are now caught.

### Checking that the timings are trustworthy

Our first official run (commit 4f701e8) had to be discarded. The same configuration (random input, n = 10^5, k = n/2) is timed in several experiments, so its time should agree across them. In that run median of medians took 64 ms in E1 but 154 ms in E4 and 161 ms in E5: the processor slowed down during the run, most likely because Windows reduced performance after the screen turned off. We re-ran everything with the settings above. In the official run the same configuration agrees within 4% for median of medians (63 to 65 ms across E1, E2, E4 and E5) and for `sorted()` (10.9 to 11.6 ms). Quickselect varies more: the identical computation took 14.2 ms in E1 and 11.8 ms in E5. Comparison counts were identical in both runs, as expected with fixed seeds.

### Predictions and the pilot run

The predictions in section 2 were committed and tagged `predictions-locked` in git before the official run, and the git history shows the order. Before that, while testing the harness, we saw rough numbers from small pilot runs, and one full run was started by mistake before the tag; that output was moved out of the repository without being analysed. [One or two sentences from pilot-numbers-seen.md: which numbers Trung was told, which Claude saw.] Every number in this report comes from the official run.

## 4. Results and analysis

<!--
GUIDE (about 1,300 words; Trung leads E1, E2, E4, E6; An Loc writes E3 and E5)
The brief: "The prose is the important part: what do the results show, and why? Connect what you observe back to the structure of the algorithms." Explain WHY in terms of what the algorithms do, and check explanations by measuring (count operations, or vary the one input feature the explanation depends on).
For each subsection: one figure, two to four numbers, then why. End each subsection with which predictions held.
-->

### 4.1 Scaling (E1) (Trung)

<!-- WRITER: Trung -->

![E1 time](../figures/e1_time_loglog.png)
![E1 comparisons](../figures/e1_comparisons_per_n.png)

<!--
NUMBERS (median time per call, ms; quickselect / median of medians / sorted()):
 n = 10^3: 0.135 / 0.597 / 0.038
 n = 10^4: 1.126 / 6.260 / 0.805
 n = 10^5: 14.217 / 65.072 / 11.567
 n = 2.15 * 10^5: 29.509 / 143.276 / 27.464
 n = 4.64 * 10^5: 119.547 / 361.708 / 83.374
 n = 10^6: 419.880 / 881.256 / 241.086
Ratio median of medians / quickselect: 4.4 to 5.6 for n up to 2.15 * 10^5, then 3.0 and 2.1.
Ratio quickselect / sorted(): 3.59 at 10^3, 1.07 at 2.15 * 10^5 (closest), 1.74 at 10^6. sorted() is faster at every n.
Log-log slope of time vs n: quickselect 1.13, median of medians 1.05, sorted() 1.23.
Time per element (ns): quickselect 135, 113, 142, 137 (n up to 2.15 * 10^5), then 258 and 420; median of medians 597 to 665, then 779 and 881; sorted() 38 rising to 241.
Comparisons per element (median over 10 instances): quickselect 3.9 to 5.9 (min to max over instances at 10^5: 3.05 to 8.74); median of medians 9.07 rising to 10.03; sorted() 8.65 rising to 18.63 (n log2 n).
Points to explain: why median of medians is about 5 times slower (work per round; about 2 times the comparisons plus list building); why quickselect's time per element triples above 2 * 10^5 while its comparisons barely change (candidate: memory layout and cache; see 4.2); why sorted() wins despite 2 to 3 times more comparisons (C vs Python).
Predictions: P1, P2, P6.
-->

[Text.]

### 4.2 Input families (E2) (Trung)

<!-- WRITER: Trung -->

![E2 families](../figures/e2_families_time.png)
![E2 duplicates](../figures/e2_duplicates_comparisons.png)

<!--
NUMBERS at n = 10^5 (median time ms; comparisons / n), quickselect | median of medians | sorted():
 random:       12.25 ms, 4.52n | 62.77 ms, 9.91n | 10.95 ms, 15.32n
 sorted:       10.30 ms, 4.41n | 41.46 ms, 7.37n |  0.37 ms, 1.00n
 reverse:       9.79 ms, 4.06n | 73.99 ms, 11.41n |  0.42 ms, 1.00n
 all equal:     3.65 ms, 2.00n | 16.43 ms, 3.50n |  0.34 ms, 1.00n
 few distinct:  7.44 ms, 4.20n | 22.83 ms, 3.87n |  4.54 ms, 7.14n
 organ pipe:    9.82 ms, 5.32n | 57.78 ms, 9.41n |  0.60 ms, 2.00n
Duplicates part at n = 10^4 (comparisons; 3-way | 2-way): all equal 20,000 | 37,502,499 (= 0.375 n^2); few distinct 35,600 | 508,873; random 44,655 | 28,650. Time on all equal: 0.4 ms | 1.24 s.
Points to explain:
- Quickselect on random is slower than on sorted (19%) and reverse (25%) at nearly the same comparison count, and organ pipe has MORE comparisons (5.32n) but is faster than random. Comparisons do not explain this. Candidate: memory layout (random_perm shuffles the Python int objects, so a pass jumps around memory; sorted and reverse keep them in memory order). Check before claiming it.
- Median of medians: reverse costs the most comparisons (insertion sort on reversed groups), sorted the fewest of the distinct families; its time follows its comparisons closely.
- sorted() is almost free on sorted, reverse and organ pipe (Timsort finds runs: 1n or 2n comparisons).
- The 2-way partition is quadratic on all equal and also bad on few distinct; it is slightly cheaper than the 3-way on distinct values (1 comparison per element instead of up to 2).
Predictions: P7.
-->

[Text.]

### 4.3 Quickselect's tail (E3) (An Loc)

<!-- WRITER: An Loc -->

![E3 tail](../figures/e3_quickselect_tail.png)

<!--
NUMBERS (An Loc), 1000 seeds, one instance, n = 10^5, k = n/2:
 mean 5.05n, median 4.87n, min 2.08n, 99th percentile 8.99n, max 9.86n, standard deviation 1.49n. max / mean = 1.95, p99 / mean = 1.78.
 Median of medians on the same instance: 9.69n. Quickselect used more comparisons than median of medians in 2 of 1000 seeds.
 sorted(): 15.32n.
Predictions: P3.
-->

<!-- AI-DRAFT: An Loc to review and rewrite -->
The figure `figures/e3_quickselect_tail.png` shows the comparison counts of 1000 runs of quickselect on one instance (n = 10^5, k = n/2), one run per rng seed. All numbers in this subsection come from analysis/anloc_numbers.md, which reads results/e3.csv.

The mean is 505,000 comparisons (5.05 per element) and the median is 487,000 (4.87 per element), so the distribution is skewed to the right. The standard deviation is 1.49 per element. The 99th percentile is 8.99 per element, and the maximum is 986,000 comparisons (9.86 per element), which is 1.95 times the mean. The minimum is 2.08 per element. Every run uses the same instance, so all of this spread comes from the random pivots. A likely reason for the long right tail is that a bad early pivot keeps most of the list for another full pass, while a good one removes about half; we did not test this explanation.

Median of medians, which makes no random choices, used 969,000 comparisons (9.69 per element) on the same instance. Quickselect used fewer comparisons than median of medians in 998 of the 1000 seeds, and more in the other 2. The unlucky tail of quickselect therefore reaches the cost of median of medians but almost never passes it.

Prediction P3 (maximum between 1.5 and 3 times the mean) held: the measured ratio is 1.95.

### 4.4 Group size (E4) (Trung)

<!-- WRITER: Trung -->

![E4 group size](../figures/e4_group_size.png)

<!--
NUMBERS: comparisons / n at n = 10^3, 10^4, 10^5, 10^6:
 g = 3: 10.05, 11.83, 12.74, 13.32 (+33%)
 g = 5:  9.07,  9.63,  9.91, 10.03 (+11%)
 g = 7:  9.31,  9.86, 10.04, 10.11
 g = 9:  9.95, 10.49, 10.66, 10.73
Time per element (ns) at the same n: g = 3: 773, 886, 958, 1368; g = 5: 597, 607, 629, 885; g = 7: 574, 575, 584, 814; g = 9: 585, 595, 597, 810.
g = 7 / g = 5 time: 0.92 to 0.96 at every n (g = 7 is 4 to 8% faster).
Points to explain: g = 3 grows (fractions 1/3 + 2/3 = 1, so O(n log n)); g = 5, 7, 9 nearly flat; why g = 7 is slightly faster than g = 5 even though its comparisons are slightly higher (fewer, larger groups: fewer list slices and Python calls per element). All four rise in time per element at 10^6 (same memory effect as E1).
Predictions: P4, P5.
-->

[Text.]

### 4.5 Position of k (E5) (An Loc)

<!-- WRITER: An Loc -->

![E5 k position](../figures/e5_k_position.png)

<!--
NUMBERS (An Loc), n = 10^5 (median time ms; comparisons / n):
 quickselect: k = 0: 6.58 ms, 2.59n; n/10: 8.49 ms, 3.14n; n/2: 11.82 ms, 4.52n; 9n/10: 9.77 ms, 4.35n
 median of medians: 63.0 to 63.6 ms, 9.90n to 9.92n for every k
 sorted(): about 11.1 ms, 15.32n for every k
Point to explain: quickselect is not symmetric (n/10 is much cheaper than 9n/10). Candidate: our 3-way partition costs 1 comparison for an element below the pivot and 2 for one not below, so a search near the top pays more. Check by counting < and == separately.
Predictions: P8a, P8b.
-->

<!-- AI-DRAFT: An Loc to review and rewrite -->
The table gives the median over 10 instances at n = 10^5, with the minimum and maximum over instances (analysis/anloc_numbers.md, from results/e5.csv).

| k | comparisons per element | min to max | time (ms) |
|---|---|---|---|
| 0 | 2.59 | 2.17 to 3.86 | 6.80 |
| n/10 | 3.14 | 2.43 to 6.46 | 8.87 |
| n/2 | 4.52 | 3.05 to 8.74 | 11.6 |
| 9n/10 | 4.35 | 2.06 to 5.81 | 9.71 |

Median of medians does not depend on k: its median comparisons per element are 9.90, 9.90, 9.91 and 9.92 for the four k, and the largest relative difference across the four k is 0.146% in comparisons and 1.22% in time (same file). With a random pivot, a k near an end lets each round discard more of the list, which fits k = 0 being cheapest and k = n/2 most expensive.

The table also shows a gap between k = n/10 (3.14) and k = 9n/10 (4.35). A candidate cause is our counting rule: an element less than the pivot costs 1 comparison and any other element costs 2, so a search near the top might pay more. But the ranges overlap heavily (2.43 to 6.46 against 2.06 to 5.81), so we ran a supplementary test.

**Supplementary, not part of the committed E5 data.** This run uses 300 different seeds (1000 to 1299), the same n, and the same instance and rng seed for every k. It reports means, not medians (analysis/anloc_asymmetry.md). The total comparisons per element are 3.98 (standard error 0.0611) at k = n/10, 5.07 (0.0957) at k = n/2 and 4.17 (0.0942) at k = 9n/10. The paired difference between k = 9n/10 and k = n/10 is 0.190 per element with standard error 0.123, which is less than two standard errors from zero and not significant. The E5 gap was therefore mostly sampling noise. (These are different statistics, a median over 10 instances and a mean over 300 seeds; over the same 10 instances the means were 3.65 and 4.25, analysis/anloc_numbers.md.) The direction of the remaining difference is consistent with the counting rule, but the data cannot show that the rule causes it. What the supplementary run does show clearly is that both ends are cheaper than the middle: 3.98 and 4.17 against 5.07, differences much larger than the standard errors.

Predictions P8a and P8b are assessed in section 4.7.

### 4.6 Slow comparisons (E6) (Trung)

<!-- WRITER: Trung -->

![E6 shared prefix](../figures/e6_shared_prefix.png)

<!--
NUMBERS at n = 10^5 (median time ms for prefix 0 / 20 / 100):
 quickselect: 13.92 / 13.99 / 17.22 (+24%)
 median of medians: 68.71 / 70.50 / 75.06 (+9%)
 sorted(): 14.31 / 17.00 / 25.18 (+76%)
Comparisons / n are identical for every prefix length: quickselect 6.70, median of medians 9.88, sorted() 15.32 (P9a held exactly, for every instance).
Ratio median of medians / quickselect: 4.94, 5.04, 4.36 (changes by 12%).
Extra time per comparison from prefix 0 to 100: quickselect 4.9 ns, median of medians 6.4 ns, sorted() 7.1 ns. This checks the explanation: the prefix adds about the same few nanoseconds to every comparison (a C scan of 100 shared characters); sorted() slows the most in relative terms because its own cost per comparison is the smallest and it does the most comparisons.
Predictions: P9a, P9b, P9c.
-->

[Text.]

### 4.7 Predictions against results (Trung) (An Loc fills rows P3, P8a, P8b)

<!-- WRITER: Trung (An Loc fills rows P3, P8a, P8b) -->

<!-- Fill in from the numbers above: held, partly held, or failed, with the number. -->

<!-- AI-DRAFT: An Loc to review and rewrite (rows P3, P8a, P8b) -->

| Prediction | Result | Held? |
|---|---|---|
| P1 | | |
| P2 | | |
| P3 | Maximum / mean = 1.95 over 1000 seeds, predicted 1.5 to 3 (analysis/anloc_numbers.md) | Held |
| P4 | | |
| P5 | | |
| P6 | | |
| P7 | | |
| P8a | E5 medians (analysis/anloc_numbers.md): 2.59 comparisons per element at k = 0, 4.52 at n/2, 4.35 at 9n/10; time 6.80, 11.6 and 9.71 ms. At 9n/10 the comparisons are only 4% below n/2 and the ranges overlap (2.06 to 5.81 against 3.05 to 8.74), so E5 alone is not clear. Supplementary 300-seed means (analysis/anloc_asymmetry.md, comparisons only, not part of the committed E5 data): 3.98 at n/10, 5.07 at n/2, 4.17 at 9n/10, so both ends are cheaper than the middle | Partly held |
| P8b | Largest relative difference across k = 0, n/10, n/2, 9n/10: 0.146% in comparisons, 1.22% in time, predicted within 10% (analysis/anloc_numbers.md) | Held |
| P9a | | |
| P9b | | |
| P9c | | |

## 5. What surprised us

<!--
GUIDE (about 500 words; both, each on results about their own algorithm). Heavily weighted (10%).
The lecturer's PA1 feedback: for each surprise give (1) what we predicted in section 2, (2) what we measured (the plot or the number), (3) an explanation we have CHECKED. Specific beats general.
Candidates (pick on the results call):
- Memory layout: quickselect's time does not follow its comparisons (random vs sorted in E2; time per element triples above 2 * 10^5 in E1). Check: same comparisons, different memory layout.
- Quickselect asymmetric in k (E5): n/10 3.14n vs 9n/10 4.35n. Check: count < and == separately.
- g = 3 grows clearly (+33% in comparisons, +77% in time per element), against our locked P4 ("slightly, hard to see").
- sorted() in C beats quickselect at every n despite 2 to 3 times more comparisons.
-->

### 5.1 [Surprise title] (Trung)

<!-- WRITER: Trung -->

[Predicted: ... Measured: ... Explanation and how we checked it: ...]

### 5.2 [Surprise title] (Loc)

<!-- WRITER: An Loc -->

[Predicted: ... Measured: ... Explanation and how we checked it: ...]

## 6. What we would do next (Trung)

<!-- WRITER: Trung -->

<!--
GUIDE (about 150 words; Trung). The natural extension, and questions the work opened that we could not answer.
Candidates: E7, the McIlroy-style adversary (dropped); Floyd-Rivest and QuickselectAdaptive (Alexandrescu, 2016), which the lecturer suggested; an in-place partition to test the memory-layout explanation; the same runs on another machine and Python version; counting comparisons the textbook way to compare with the 1.5n and 2n figures.
-->

[Text.]

## 7. Individual contributions

<!-- WRITER: each person writes their own paragraph -->

<!--
GUIDE (about 200 words; each writes their own paragraph). Beyond your primary algorithm. Be honest; an uneven split is fine but must be visible. Mention that the git name "Taki" is Thanh Trung Le.
-->

**An Loc Nguyen.** [Paragraph.]

**Thanh Trung Le.** [Paragraph.]

## 8. AI use

<!--
GUIDE (about 500 words). The brief requires all three:
1. Each member's own paragraph on how they personally used AI tools.
2. At least 3 specific examples across the group of AI being wrong, unhelpful or misleading, each with how it was noticed and what we did. Keep them in notes/ai-error-log.md too.
   Candidates: (a) the first median-of-medians tests missed two complexity bugs, caught by mutation testing (the test run went from about 4 s to 51 s on the pivot bug); (b) the planned E2 size was infeasible, 0.375 n^2 comparisons, caught by estimating from our own counts; (c) Claude said the Dijkstra priority-queue topic was not on the topic list, caught by reading the list.
3. A reflection on AI in group work: where it helped the group function (for example status reports between us, explaining each other's code), and where it hurt or threatened to (for example predictions drafted by an AI that had seen pilot numbers).
Also say what you took on trust without checking.
-->

### 8.1 How each of us used AI

<!-- WRITER: each person writes their own paragraph -->

**An Loc Nguyen.** [Paragraph.]

**Thanh Trung Le.** [Paragraph.]

### 8.2 Where AI was wrong, unhelpful or misleading

<!-- WRITER: Both -->

1. [Example: what the AI did, why it was wrong, how we noticed, what we did.]
2. [Example.]
3. [Example.]

### 8.3 AI in group work

<!-- WRITER: Both (An Loc drafts, Trung edits) -->

[Paragraph.]

## References

<!-- WRITER: each adds what they cite -->

<!-- Check every entry. Remove the ones you do not cite. -->

Alexandrescu, A. (2016). *Fast deterministic selection*. arXiv:1606.00484.

Blum, M., Floyd, R. W., Pratt, V., Rivest, R. L., & Tarjan, R. E. (1973). Time bounds for selection. *Journal of Computer and System Sciences, 7*(4), 448-461.

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to algorithms* (3rd ed.). MIT Press.

Hoare, C. A. R. (1961). Algorithm 65: Find. *Communications of the ACM, 4*(7), 321-322.