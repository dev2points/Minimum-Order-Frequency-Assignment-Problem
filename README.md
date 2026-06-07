# Minimum Order Frequency Assignment Problem

This repository contains implementations and experiment scripts for solving
the Minimum Order Frequency Assignment Problem using several backends
(CPLEX, Gurobi, SAT solvers, and solver sequences).

## Overview

This README explains how to prepare an environment and run the experimental
scripts. Each solver framework lives in its own folder (`CPLEX/`, `Gurobi/`,
`SAT/`, `sequence/`); automated runner scripts (`auto.sh`) are provided where
available to run batches of experiments on the provided datasets.

## Prerequisites

- Git
- Python 3.10 (recommended)
- System dependencies and solver licenses:
	- IBM CPLEX (if using the `CPLEX/` experiments) and `docplex` Python package
	- Gurobi (if using the `Gurobi/` experiments) and `gurobipy` Python package
	- SAT solvers used by the `SAT/` folder (the repo contains wrappers)
- Make sure shell scripts are executable: `chmod +x *.sh` in each folder

Note: This repo includes a `venv310/` virtual environment for convenience,
but creating a fresh venv is recommended on new machines.

## Quick Start (example)

1. Clone the repository:

	 git clone <repo-url>
	 cd Minimum-Order-Frequency-Assignment-Problem

2. Create and activate a Python virtual environment (example):

	 python3.10 -m venv venv310
	 source venv310/bin/activate

3. Install Python dependencies (if a `requirements.txt` exists):

	 pip install -r requirements.txt

	 If there is no `requirements.txt`, install solver SDKs as needed (CPLEX,
	 Gurobi) and common packages you expect to need (e.g., `networkx`, `numpy`).

4. Make scripts executable (if necessary):

	 find . -name "*.sh" -exec chmod +x {} +

## Running experiments

General guidance: many folders include an `auto.sh` script to run a set of
experiments using the repository's datasets. Use that for repeatable batch
runs. Example invocations below.

- CPLEX experiments

	cd CPLEX
	./auto.sh

	Or run scripts directly (for interactive or single runs):

	python3 cp.py [options]
	python3 cp_no.py [options]

	Note: CPLEX requires a valid installation and license. The `docplex` package
	is commonly used for Python + CPLEX integrations.

- Gurobi experiments

	cd Gurobi
	./auto.sh

	Or run directly:

	python3 main.py [options]

	Note: Gurobi requires a licensed installation and `gurobipy`.

- SAT experiments (pairwise)

	cd SAT/pairwise
	./auto.sh

	Or for single runs:

	python3 pairwise.py [options]

- Sequence / solver pipelines

	cd sequence
	./auto.sh

	Or run its main scripts for specific modes:

	python3 main.py [options]

## Datasets and results

- Datasets are stored under each solver's `dataset/` subfolder (e.g., `Gurobi/dataset/`).
- Results are written to the `Result/`, `Result_python/`, and `Result2/` folders
	depending on the run and pre-processing options. Inspect these folders after
	runs to collect output and logs.

## Troubleshooting

- If a script fails saying a solver library is missing, install the SDK for
	that solver and ensure the Python binding is available in the active venv.
- Ensure `runlim` (present in several folders) is executable if used by the
	auto runners.
- Check file permissions: `chmod +x auto.sh` and other `.sh` wrappers.

## Tips

- Use the `auto.sh` scripts for reproducible batch experiments.
- To run a single dataset or scenario, inspect the scripts in each solver
	folder (`*.py`) — most accept command-line options for dataset and scenario.

## Contact

If you need more specific run commands for a solver or help configuring a
license (CPLEX/Gurobi), tell me which solver and platform and I can provide
exact setup commands.

