# Numbers seen before `predictions-locked` (open only after the tag)

An Loc: do not open this file until the tag `predictions-locked` is pushed. It contains results.

Compiled on 31 Oct 2026 by Claude, from Trung's session, for the disclosure in the methodology section. Values marked "approx." were read off figures, not from CSV files. None of these runs are part of the report's data.

## What Trung was told (in chat)

| Date | What Trung was told | Source |
|---|---|---|
| 21 Oct | Median of medians was about 2 to 2.5 times slower than quickselect on random input | throwaway implementations, 20 Oct |
| 25 Oct | Median of medians on n = 10^6 took about 1.2 s | final median_of_medians.py |
| 26 Oct | Test comment: comparisons per element for g = 5 measured "about 4n to 12n"; the mutation run took 51 s against about 4 s | final code |
| 27 Oct | Median of medians about 4 times slower than quickselect; `sorted()` about as fast as quickselect despite more comparisons; g = 3 comparisons / n rises with n while g = 5, 7, 9 stay flat; in E6 comparisons stay the same while time rises with prefix length | 2-instance pilot, final code |
| 29 Oct | The 2-way partition took about 4.4 s per call at n = 10^4 (from Trung's own progress log) | accidental full run, progress lines only |

## What Claude saw

### 20 Oct: harness check with throwaway implementations (not our final code)

The throwaway quickselect used up to 3 comparisons per element, so counts are not comparable with the final code. n up to 10^5, 2 to 3 instances.

- E1 time: median of medians about 2 to 2.5 times quickselect; `sorted()` fastest at every n up to 10^5.
- E3 (1000 seeds, n = 10^5): quickselect mean 11.81n, 99th percentile 21.25n, max 23.09n; median of medians 14.38n.
- E4: comparisons / n for g = 3 from about 15.5 to 20.1 (approx.); g = 5, 7, 9 about 12.6 to 14.5 (approx.).
- E2 duplicates: 2-way partition on all equal at n = 10^4 about 7.6 * 10^7 comparisons (approx.).

### 25 Oct: final median of medians, g = 5, n = 20,001, k = n - 1

Comparisons / n: random 9.66, sorted 7.17, reverse 11.36, all equal 3.50, few distinct 5.62, organ pipe 9.28. Random input with n = 10^6 took 1.21 s.

### 27 Oct: 2-instance pilot with the final code (E3 with 200 seeds), total 380 s

- E1 time per call (approx.): n = 10^3: quickselect 1.5e-4 s, median of medians 7.8e-4 s, `sorted()` 7.6e-5 s. n = 10^6: quickselect 0.31 s, median of medians 1.1 s, `sorted()` 0.28 s. Quickselect and `sorted()` about equal from n = 10^4 up.
- E1 comparisons / n (approx.): quickselect 3.2 to 6.2 (noisy), median of medians 9.2 to 10.0, `sorted()` 8.6 rising to 18.7.
- E2 time at n = 10^5, ms (approx.), quickselect / median of medians / sorted(): random 17 / 80 / 24, sorted 14 / 47 / 0.5, reverse 12 / 87 / 0.7, all equal 4 / 17 / 0.3, few distinct 11 / 27 / 7, organ pipe 13 / 70 / 1.
- E2 duplicates at n = 10^4: 2-way partition about 3.7 * 10^7 comparisons on all equal; about 6 * 10^4 and 5 * 10^5 on few distinct for its 2 instances (approx.).
- E3 (200 seeds): quickselect mean 4.85n, 99th percentile 8.90n, max 9.63n; median of medians 9.69n on the same instance.
- E4 comparisons / n (approx.): g = 3 from 10.4 to 13.3; g = 5 from 9.2 to 10.0; g = 7 from 9.1 to 10.1; g = 9 from 9.6 to 10.7. Time per element: g = 3 from 0.98 to 1.68 microseconds; g = 5, 7, 9 from about 0.72 to 1.13.
- E5 comparisons / n (approx.): quickselect 3.2 (k = 0), 4.5 (n/10), 3.7 (n/2), 4.2 (9n/10); median of medians about 9.9 at every k; `sorted()` 15.3.
- E6 at n = 10^5 (approx.): time per element for prefix 0 / 20 / 100: quickselect 0.18 / 0.25 / 0.22 microseconds, median of medians 0.84 / 0.87 / 0.94, `sorted()` 0.27 / 0.30 / 0.39. Comparisons / n the same for all prefix lengths: quickselect 7.8, median of medians 9.85, `sorted()` 15.3.
