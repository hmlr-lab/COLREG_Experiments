from util import *

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYGOL_DIR = ROOT / "PyGol_Files"

sys.path.insert(0, str(PYGOL_DIR))

from PyGol import *


bk_path = "../prolog/BK.pl"
fact_path = "../prolog/generated/facts.pl"
comb_bk_path = "../prolog/generated/combined_BK.pl"
hypothesis_files = "../rules.txt"
pos_exa_path = "../prolog/generated/pos_examples.pl"
neg_exa_path = "../prolog/generated/neg_examples.pl"

# Example log files
file_path_log_pos = ["../examples/positives/crossingport_1.txt",
                 "../examples/positives/crossingstbd_1.txt",
                 ]

file_path_log_neg = ["../examples/negatives/crossingport_1.txt",
                     "../examples/negatives/crossingport_2.txt",
                 "../examples/negatives/crossingstbd_1.txt",
                 ]

# Generate stage 1 BK files from log files
facts_pos, examples_pos =  generate_bk_from_log(file_path_log_pos, verbose=False)
facts_neg, examples_neg =  generate_bk_from_log(file_path_log_neg, verbose=False, neg=True)

# Save the examples
write_prolog_file(examples_pos, pos_exa_path)
write_prolog_file(examples_neg, neg_exa_path)
# Save the generated Prolog knowledge base (facts and rules) for evaluation.
write_prolog_file(facts_pos+facts_neg,fact_path)

# Combine generated facts with the background knowledge for evaluation.
merge_prolog_files(fact_path, bk_path, comb_bk_path)

# Learn Rules
H, HS = learn_rules(facts_pos+facts_neg, examples_pos, examples_neg, bk_path, print_hs=False, print_h=False, seed_value=10)

# Merge duplicate hypotheses through post-processing.
all_HS, updated_rules, sub_hypotheses = merge_duplicate_body_hypotheses(H)
for rule in all_HS:
    pretty_print_prolog(rule)
    pos, neg = evaluate_rule([rule], comb_bk_path, examples_pos+examples_neg,[])
    print(f"--- TP: {pos}, TN: {neg}")

# Write the final hypotheses to a file.
with open("rules.txt", "w") as f:
    for rule in all_HS:
        
        f.write(rule + ".\n")

print("Rules written to rules.txt")