from util import *

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYGOL_DIR = ROOT / "PyGol_Files"

sys.path.insert(0, str(PYGOL_DIR))

from PyGol import *


bk_path = "BK.pl"
hypothesis_files = "rules.txt"

# Example log files
file_path_log = ["260630_examples/log_0.txt",
                 "260630_examples/log_1.txt",
                "260630_examples/log_2.txt",
                "260630_examples/log_3.txt",
                "260630_examples/log_4.txt",
                 ]

# Generate stage 1 BK files from log files
facts, examples =  generate_bk_from_log(file_path_log, verbose=False)

# Save the generated Prolog knowledge base (facts and rules) for evaluation.
write_prolog_file(facts,"facts.pl")

# Combine generated facts with the background knowledge for evaluation.
merge_prolog_files("facts.pl", "BK.pl", "combined_BK.pl")

# Learn Rules
H, HS = learn_rules(facts, examples, bk_path, print_hs=False, print_h=False, seed_value=10)

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