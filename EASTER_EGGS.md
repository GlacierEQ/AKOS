# Easter Egg Vocabulary

Easter eggs are signals to experts. They are not explained.
They are not footnoted. They do not wink at the reader.
They simply exist, accurately, where only the right person will see them.

## The Rule

> The textbook crowd sees a constant.
> The expert sees the reference.
> The Easter egg works because it never explains itself.

## Active Vocabulary

### Numbers

| Value | Name | Origin | How to use |
|---|---|---|---|
| `42` | ANSWER | Hitchhiker's Guide / Elon's personal number | Default AoA, version suffix, timeout, horizon |
| `1.21` | FLUX_THRESHOLD | Back to the Future — 1.21 gigawatts | Version numbers, threshold constants |
| `math.e` | EULER | Euler's number — exactly, not 2.718 | Sigma thresholds, decay constants |
| `0.31415` | PI_FLOOR | π — one digit short, intentionally | Confidence floors, probability bounds |
| `18_000` | MAX_TILES | Starship tile count (not Shuttle's 24,000) | Capacity limits in SpaceX repos |
| `64` | FFT_WINDOW | Power of two — FFT window size | Comment: *engineers who ask why already know why* |
| `84` | DOUBLE_ANSWER | `42 * 2` — defined as such, not as 84 | Time horizons, buffer windows |
| `9.80665` | G | Exact SI gravity constant — not 9.8, not 10 | All gravitational calculations |
| `299_792_458` | C | Speed of light — exact | Anything involving EM or timing precision |

### Strings and Comments

| Pattern | Usage |
|---|---|
| `# always 42` | Inline comment on a parameter set to 42 |
| `# don't panic` | Comment on a large or scary-looking constant |
| `# e. always e.` | Comment on THERMAL_ANOMALY_SIGMA = math.e |
| `# Not one is decorative.` | Comment on tile count or similar critical-count constant |
| `# engineers who ask why already know why` | Comment on FFT window size |
| `# The term that matters at Mach 25` | Comment on radiation in heat equations |
| `# Computes fast enough to matter.` | Module docstring closer |

### Elon-Specific References

| Reference | Context |
|---|---|
| `42` | His stated favorite number. Use freely. |
| `PICA-X` | SpaceX's own ablative material. Always preferred over generic in SpaceX repos. |
| `Starship` vs `Shuttle` | 18,000 tiles vs 24,000. The person who knows the difference will notice. |
| `reusability` | Never explain it. It's either the point or it isn't. |
| `ABORT_TRAJECTORY` | Named action. More honest than `EMERGENCY`. |

### Douglas Adams References

| Reference | Usage |
|---|---|
| `42` | The answer to life, the universe, and everything |
| `# don't panic` | On anything that looks alarming but is fine |
| `MAX_PREDICTION_HORIZON_S = ANSWER * 2` | 84 seconds. The math is the joke. |

### Physics Constants Used as Easter Eggs

When a constant *could* be approximated, use the exact value.
The precision is the signal.

```python
STEFAN_BOLTZMANN = 5.670374419e-8   # not 5.67e-8
G = 9.80665                          # not 9.8
C = 299_792_458                      # not 3e8
math.e                               # never 2.718
math.pi                              # never 3.14159
```

## What Easter Eggs Are NOT

- `"Fun fact: The Space Shuttle had ~24,000 tiles"` — teacher voice, forbidden
- Emoji in docstrings — unprofessional
- Explained references — if you explain it, it's not an Easter egg
- Forced references — if it doesn't fit the code, don't put it in

## The Test

Ask: *would a senior SpaceX engineer reading this code stop,*
*smile slightly, and keep reading?*

If yes: ship it.
If it would make them roll their eyes: cut it.
