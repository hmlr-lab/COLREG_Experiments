# PyGol Runner — COLREGs Experiments



## 1. File structure

```text
PyGol-runner/
├── all_scenarios.yaml            # Combined scenario data
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
│
├── bk_files/                     # Background-knowledge Prolog files (e.g. facts.pl, BK.pl)
├── positive_examples/            # Positive training examples, grouped by predicate
├── negative_examples/            # Negative training examples, grouped by predicate
├── scenarios/                    # Individual scenario files for generating the reports
├── rules/                        # Learned Prolog rule files
├── reports/                      # Evaluation outputs and reports
│
├── merge_examples_yaml.py        # Combine example/scenario YAML data
├── extract_yaml_facts_fixed.py   # Extract or transform facts from scenario YAML
├── generate_facts_examples.py    # Generate Prolog facts and positive/negative examples
├── learning.py                   # Run PyGol rule learning
├── evaluate_all_scenarios.py     # Evaluate learned rules across scenarios
├── janus_test.py                 # Python–Prolog integration (not a main run command)
├── generate_so.py                # Generate PyGol executable file
├── util.py                       # Supporting utilities (not a main run command)
├── bc_pruner.py                  # Bottom-clause pruning helper (not a main run command)
└── PyGol.cpython-312-darwin.so   # Compiled PyGol extension
```

### Important folders

| Folder | Description |
|---|---|
| `bk_files/` | Prolog background knowledge and generated scenario facts. |
| `positive_examples/` | Positive examples such as `take_action.pl`, `turn.pl`, `avoid.pl`, `resume.pl`, and `cpa_side.pl`. |
| `negative_examples/` | Negative examples for the same target predicates. |
| `scenarios/` | Individual encounter scenarios used for validation. |
| `rules/` | Learned rules to be loaded or tested. |
| `reports/` | Outputs produced by scenario evaluation and other analyses. |

## 2. Main Python files

| Script | Intended role |
|---|---|
| `merge_examples_yaml.py` | Merge individual YAML examples into an aggregated scenario dataset (for example, `all_scenarios.yaml`). |
| `extract_yaml_facts_fixed.py` | Extract/convert facts from YAML into the format needed for the experiments. |
| `generate_facts_examples.py` | Generate background-knowledge facts and separate positive/negative `.pl` example files. |
| `learning.py` | Train PyGol to produce rules for the target predicates. |
| `evaluate_all_scenarios.py` | Apply learned rules to scenarios and produce evaluation results. |
| `generate_so.py` | Optional helper for building a native `.so` file; check the script before use. |

**`util.py`, `janus_test.py` and `bc_pruner.py` are helper files, not steps you need to run manually in the normal workflow.** They may be imported by other scripts.



## 3. How to run the project

Run commands **from the project root**, unless a script explicitly requires another working directory. The sequence below is a suggested workflow; individual scripts may use hard-coded paths or expect files produced by another step.

### Step 1 — Prepare or merge scenarios (when needed)

If your examples are still in separate YAML files, try:

```bash
python3 merge_examples_yaml.py
```

Check that `all_scenarios.yaml` contains the expected scenarios. **Skip this step** if the file is already prepared and up to date.

### Step 2 — Extract facts (when needed)

```bash
python3 extract_yaml_facts_fixed.py
```

Use this when your workflow needs the extraction/transformation performed by that script. Confirm its destination filenames before running to avoid overwriting existing data.

### Step 3 — Generate BK and positive/negative examples

```bash
python3 generate_facts_examples.py
```

Based on the shared generation code, this stage converts scenario facts into Prolog and separates examples by label and target predicate. Check the configured paths for outputs such as:

```text
bk_files/facts.pl
positive_examples/take_action.pl
positive_examples/turn.pl
positive_examples/avoid.pl
positive_examples/resume.pl
positive_examples/cpa_side.pl
negative_examples/take_action.pl
negative_examples/turn.pl
negative_examples/avoid.pl
negative_examples/resume.pl
negative_examples/cpa_side.pl
```

These are **expected/example output names**, not a guarantee that the current version of the script uses exactly these paths.

### Step 4 — Learn Prolog rules

```bash
python3 learning.py
```

Inspect the training output and check for generated rule files in `rules/`. The learned target predicates may include:

- `take_action/1`
- `turn/...`
- `avoid/...`
- `resume/...`
- `cpa_side/3`

The exact arities of predicates other than those shown explicitly depend on your example definitions.

### Step 5 — Evaluate learned rules

```bash
python3 evaluate_all_scenarios.py
```

Ensure that the evaluator is pointing to the intended **learned rules**, **background knowledge**, and **scenario files**. Review any generated output in `reports/` and compare predicted actions with the scenario expectations.

### Optional — Test Janus before the full run

```bash
python3 janus_test.py
```

This may help detect Python/SWI-Prolog integration issues before a longer experiment.

### Optional — Rebuild the native PyGol extension

```bash
python3 generate_so.py build_ext --inplace
```

Run this **only if required**, after checking the script and its build prerequisites. Do not rebuild a working `.so` unnecessarily. The `.so` shown in the project is platform- and Python-version-specific.


## 4. Example learning/evaluation pipeline

```text
Scenario YAML files
         │
         ▼
  all_scenarios.yaml
         │
         ▼
  Facts & example generation
         │
         ├── bk_files/             (Prolog facts / BK)
         ├── positive_examples/    (positive targets)
         └── negative_examples/    (negative targets)
                    │
                    ▼
                learning.py
                    │
                    ▼
                  rules/
                    │
                    ▼
        evaluate_all_scenarios.py
                    │
                    ▼
                 reports/
```


