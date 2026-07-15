# BMT_Experiments -PyGol

This example demonstrates how to generate symbolic facts from simulation logs and learn logical rules automatically.

## Usage

### Setup Enviroment

From project root move to PyGol-runner `cd PyGol-runner`
Install requirements: `pip3 install -r requirements.txt`

From within the `PyGol-runner/PyGol_Files/` directory run the command 
```bash
    python3 generate_so.py build_ext --inplace
```

### Learning

    File Name: Learning.py
    Execution : python3 Learning.py

```python
from util import *
from PyGol import merge_duplicate_body_hypotheses, evaluate_rule

bk_path = "BK.pl"
hypothesis_files = "rules.txt"

# Example log files
file_path_log = ["260605_examples/log_0.txt",
                 "260605_examples/log_1.txt",
                "260605_examples/log_2.txt",
                "260605_examples/log_3.txt",
                "260605_examples/log_4.txt",
                 ]

# Generate stage 1 BK files from log files
facts, examples =  generate_bk_from_log(file_path_log, verbose=False)

# Save the generated Prolog knowledge base (facts and rules) for evaluation.
write_prolog_file(facts,"facts.pl")

# Combine generated facts with the background knowledge for evaluation.
merge_prolog_files("facts.pl", "BK.pl", "combined_BK.pl")

# Learn Rules
H, HS = learn_rules(facts, examples, bk_path, print_hs=False, print_h=False)

# Merge duplicate hypotheses through post-processing.
all_HS, updated_rules, sub_hypotheses = merge_duplicate_body_hypotheses(H)
for rule in all_HS:
    pretty_print_prolog(rule)
    pos, neg = evaluate_rule([rule], "combined_BK.pl", examples,[])
    print(f"--- TP: {pos}, TN: {neg}")

# Write the final hypotheses to a file.
with open("rules.txt", "w") as f:
    for rule in all_HS:
        
        f.write(rule + ".\n")

print("Rules written to rules.txt")
```

## Input

* `BK.pl` – Background knowledge.
* `log_*.txt` – Simulation log files.

## Output

* `rules.txt` – Learned Prolog rules.

## Workflow

```text
Log Files
    ↓
generate_bk_from_log()
    ↓
Facts + Examples
    ↓
learn_rules()
    ↓
Learned Rules
    ↓
rules.txt
```

# BMT_Expreiments - Prolog<sup>2</sup>

Must have rust installed [Rust Installation Guide](https://doc.rust-lang.org/cargo/getting-started/installation.html)

```bash
    cd prolog2-runner
    cargo run --release
```