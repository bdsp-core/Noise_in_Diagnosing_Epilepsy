# LaTeX Document Structure

This document is now organized into modular sections for easier editing and management.

## Main File

**kilt_main.tex** - Compile this file in Overleaf. It contains:
- All preamble (packages, document class, metadata)
- Abstract
- `\input` commands that pull in each section

## Section Files (in /sections/)

The document is split into these files, which are assembled in order by `kilt_main.tex`:

### Main Body
1. **01_introduction.tex** - Introduction section with overview table and illustrative examples
2. **02_methods.tex** - Three models of noise and skill, interpretation, identifiability
3. **03_case_study.tex** - Epilepsy diagnosis case study (materials, methods, results, intervention roadmap)
4. **04_discussion.tex** - Relationship to existing reliability metrics + Posterior predictive checks
5. **05_conclusion.tex** - Conclusion section

### Appendices
6. **appendix_A_bayesian.tex** - Bayesian estimation details (MCMC, implementation)
7. **appendix_B_practical.tex** - Practical implementation guide for researchers

### Back Matter
8. **99_backmatter.tex** - Acknowledgements and conflict of interest statements

## Benefits of This Structure

- **Easy reordering**: Just change the order of `\input` commands in `kilt_main.tex`
- **Focused editing**: Work on one section at a time without scrolling through entire document
- **Version control**: Git diffs will be cleaner when changes are isolated to specific section files
- **Collaboration**: Different authors can work on different sections simultaneously

## Original File

**kilt.tex** - The original monolithic file is preserved but should not be edited. Use `kilt_main.tex` going forward.

## Compiling

In Overleaf:
1. Set `kilt_main.tex` as the main document
2. Compile as usual - LaTeX will automatically pull in all section files
3. All `\input` paths are relative to the location of `kilt_main.tex`
