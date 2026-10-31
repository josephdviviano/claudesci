# Stale C++ — C7 reference

Read the project's language standard first (`CMAKE_CXX_STANDARD`). Rows marked
(20) need C++20.

Report a row only where the modern form removes a line, a decision point, or a
defect class. The third column is the condition under which the rewrite keeps
behaviour. If you cannot show that the condition holds, mark the finding
BEHAVIOUR CHANGE.

| Stale | Modern | Keeps behaviour when |
|---|---|---|
| Owning raw pointer, `new`/`delete` | `std::unique_ptr`, `std::make_unique` | One owner, and destruction order is the same. Members are destroyed after the destructor body, in reverse declaration order |
| Paired acquire/release calls | RAII type, `std::scoped_lock` | Every exit path already released, in the same order |
| C array member | `std::array` | The struct layout is the same. Add `static_assert(sizeof(T) == N)` if the struct is serialized |
| Pointer and length parameters | `std::span` (20) | No caller uses pointer arithmetic past the length |
| `#define` constant | `constexpr` | The macro is not used in `#if` or token pasting, and the type is the same as the literal's (`0.5` is `double`, `0.5f` is `float`) |
| Function-like macro | `constexpr` function or template | No argument has a side effect that the macro evaluated twice, and mixed-type arguments get the same conversions |
| `NULL` or `0` as a pointer | `nullptr` | No overload takes an integer in the same position |
| Unscoped `enum` | `enum class` | No implicit integer conversion is used, and the underlying type and serialized width are the same |
| `typedef` | `using` | Always |
| C-style cast | `static_cast`, `const_cast` | Always, if it compiles. Do not substitute `reinterpret_cast` for a cast that did a `static_cast`: it compiles and drops the base-class pointer adjustment |
| Out-parameter and `bool` return | Return a struct or `std::optional` | Every caller checked the `bool` before it read the out-parameter |
| Sentinel value (`-1`, `nullptr`) | `std::optional` | The sentinel never goes into serialized data or across an ABI |
| Index loop over a container | Range-for, `<algorithm>`, ranges (20) | The body does not change the container size, and the iteration order is the same |
| Hand-written sum | `std::accumulate` | The initial value has the type of the old accumulator. `std::reduce` and parallel policies change the order of float addition |
| Hand-written min, max, clamp | `std::min`, `std::max`, `std::clamp` | NaN inputs give the same result. For `std::clamp`, `lo <= hi` on every call |
| `find` compared to `end()` | `contains` (20) | Always |
| `memcpy` between unrelated types | `std::bit_cast` (20) | Both types are trivially copyable and the same size |
| `sprintf` into a buffer | `std::format` (20), `std::to_chars` | The output text is identical, including float precision |
| `.first`, `.second`, `std::get` | Structured bindings | The binding is `auto&` or `const auto&` where the old code did not copy |
