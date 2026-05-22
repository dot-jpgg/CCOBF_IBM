# CCOBF IBM: The individual-based model from the *Compounding costs of being female in academia*

A simple implementation of the IBM described in:

> Gibson, L., Brower, A., MacDonald, L. & James, A. (2026). *The compounding costs of being female in academia: Individual-based modelling of career progression and interventions*.

> A pre-print is available on the [bioRxiv](https://www.biorxiv.org/content/biorxiv/early/2026/05/03/2026.04.29.721520.full.pdf).

## Overview

This repository contains an implementation of the individual-based model described in the manuscript.

The code is intended to demonstrate the model structure, rather than act as a finished software package.

## Data

Data confidentially does not allow us to release the IBM parameterised with the data set used in the paper.

However, we provide a fabricated data set which has been generated using ChatGPT-5 for demonstrative purposes.

## Structure

- `src/` — model implementation
- `scripts/` — sample scripts
- `data/` — toy data and output simulations

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Example

A simulation can be generated using the provided sample data set. This can be run using the file

```bash
python scripts/run_ibm.py
```

The example simulation can be visualised using the plotting file

```bash
python scripts/make_example_figure.py
```
