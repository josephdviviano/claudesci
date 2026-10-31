# Grading key — C7 ablation

Validated by validate.py: every S rewrite passes check.sh; every naive T rewrite fails; every T safe form passes.

## Safe items (hit = modern form proposed at the site, risk behaviour-preserving)

| ID | Site | Modern form |
|---|---|---|
| S1 | mixer.h:7 | `using Samples = ...` |
| S2 | mixer.h:33 | `nullptr` (or default member init) |
| S3 | mixer.cpp:6 | `constexpr` int/size_t |
| S4 | mixer.h:38 | `std::array<float, 3>` |
| S5 | mixer.h:33-34,40 | `std::unique_ptr<Filter>` |
| S6 | mixer.cpp:43 | `contains` |
| S7 | mixer.cpp:35, mixer.h:60 | return pointer or `std::optional` |
| S8 | mixer.cpp:68 | range-for over voices |
| S9 | mixer.cpp:85 | structured bindings / range-for |
| S10 | mixer.cpp:30 | `static_cast<int>` |
| S11 | mixer.cpp:65, mixer.h:65 | `std::span<const float>` |
| S12 | mixer.h:72, mixer.cpp:14 | `std::vector<std::unique_ptr<Voice>>` |

## Traps (naive form changes golden output)

| ID | Site | Naive form (unsafe) | Caught when |
|---|---|---|---|
| T1 | mixer.cpp:50 | `std::min(raw, 1.0f)` / `std::clamp` | NaN named, or marked BEHAVIOUR CHANGE |
| T2 | mixer.cpp:28 | `reinterpret_cast` | `static_cast`, implicit conversion, or direct member access |
| T3 | mixer.cpp:7,56 | `constexpr float ... = 343.2f` | `constexpr double`, or float precision change named |
| T4 | mixer.cpp:79 | range-for over `events` | growth during iteration named, or loop left as is with reason |
| T5 | mixer.h:70-71, mixer.cpp:15-16 | `unique_ptr` buses, declaration order unchanged | destruction order named, declarations reordered, or marked BEHAVIOUR CHANGE |
| T6 | mixer.cpp:60-62 | `accumulate`/`inner_product` with `0.0f` | `0.0` double initial value, or precision named |

Outcome per trap per run: caught | unsafe (naive form as behaviour-preserving) | silent (not mentioned).
