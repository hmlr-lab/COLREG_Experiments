from util import *

import sys
from pathlib import Path

# ROOT = Path(__file__).resolve().parent
# PYGOL_DIR = ROOT / "PyGol_Files"

# sys.path.insert(0, str(PYGOL_DIR))

from PyGol import *

RULES = ROOT / "rules.txt"

BK_PATH = PROLOG /"BK.pl"
EXAMPLES = PROLOG_GENERATED / "examples.pl"
FACTS = PROLOG_GENERATED / "facts.pl"
COMBINED_BK = PROLOG_GENERATED / "combined_BK.pl"


# Example log files
file_path_log = list_log_files(POS_EXAMPLES)

# Generate stage 1 BK files from log files
facts, examples =  generate_bk_from_log(file_path_log, verbose=False)

# Save the examples
write_prolog_file(examples, EXAMPLES)
# Save the generated Prolog knowledge base (facts and rules) for evaluation.
write_prolog_file(facts, FACTS)

# Combine generated facts with the background knowledge for evaluation.
merge_prolog_files(FACTS, BK_PATH, COMBINED_BK)

# Learn Rules
H, HS = learn_rules(facts, examples, BK_PATH, print_hs=False, print_h=False, seed_value=10)

# Merge duplicate hypotheses through post-processing.
all_HS, updated_rules, sub_hypotheses = merge_duplicate_body_hypotheses(H)
for rule in all_HS:
    pretty_print_prolog(rule)
    pos, neg = evaluate_rule([rule], COMBINED_BK, examples,[])
    print(f"--- TP: {pos}, TN: {neg}")

# Write the final hypotheses to a file.
with open(RULES, "w") as f:
    for rule in all_HS:
        
        f.write(rule + ".\n")

print("Rules written to rules.txt")