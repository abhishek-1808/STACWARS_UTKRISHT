# STAC Wars PS3: Exoplanet Hunters

Transit analysis of three stars (STAC-1, STAC-2, STAC-3): detection, planet size, orbital distance and a habitability ranking. The write-up is an IEEE-style two-column report.

## Results

| | STAC-1 b | STAC-2 b | STAC-3 b |
|---|---|---|---|
| Period | ~4.25 d | 80 d | ~38 d |
| Depth | 0.0030 | 0.0010 | 0.00088 |
| Radius | 5.98 Re (Neptune-sized) | 2.76 Re (Super-Earth) | 1.62 Re (Super-Earth) |
| Orbit | 0.0513 AU | 0.337 AU | 0.176 AU |

Most promising candidate: **STAC-3 b**.

## Layout

```
report/report.pdf    final report (submit this)
report/report.tex    LaTeX source
figures/lc.pdf       light curves
src/                 calculations.py, make_figure.py
data/                brightness observations as CSV
```

## Reproduce

```
make calc      # prints all numbers
make           # rebuilds figure and PDF (needs matplotlib, pdflatex)
```

## Notes

- The brief's depth formula is inverted; the report uses depth = (Rp/Rs)^2.
- Periods for STAC-1 and STAC-3 are estimates because of sparse sampling; see Section II of the report.
