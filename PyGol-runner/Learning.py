from datetime import datetime
from turtle import pos

from util import *
import os

output_dir = Path(__file__).resolve().parent / "rules"

# Create the directory if it doesn't exist
output_dir.mkdir(parents=True, exist_ok=True)



from PyGol import *

combined_rules  = {}
facts = "bk_files/facts.pl"
bk_path = "bk_files/BK.pl"
# Learn Take Action
print("\n" + "=" * 60)
print("        Learning Take Action")
print("=" * 60)

pos_example = "positive_examples/take_action.pl"
neg_example = "negative_examples/take_action.pl"

merge_prolog_files(facts, bk_path, "bk_files/combined_BK.pl")

H, HS = learn_rules(facts, pos_example, neg_example, bk_path, print_hs=False, print_h=False, seed_value=10)
pos_example_list = pygol.read_example(pos_example)
neg_example_list = pygol.read_example(neg_example)

pygol.evaluate_theory_prolog(H, "bk_files/combined_BK.pl", sorted(pos_example_list), sorted(neg_example_list))
# Write the final hypotheses to a file.
file_name_hypo = output_dir / "rules_take_action.txt"
with open(file_name_hypo, "w") as f:
    for rule in H:
        pretty_print_prolog(rule)
        #combined_rules.append(rule)
        f.write(rule + ".\n")
print(f"Rules written to {file_name_hypo}")
combined_rules["take_action"] = H


print("\n" + "=" * 60)
print("        Learning Turning Magnitude")
print("=" * 60)

pos_example_avoid = "positive_examples/turn.pl"
neg_example_avoid = "negative_examples/turn.pl"

pos_all = read_example(pos_example_avoid)
neg_all = read_example(neg_example_avoid)


#remove dupilcated from pos
pos_example = list(set(pos_all))

# remove noisy examples from neg
neg_example = [eache for eache in neg_all if eache not in pos_all]


H= learn_rules_muti_label(facts, sorted(pos_example), sorted(neg_example), bk_path, print_hs=False, print_h=False, seed_value=10, label_literal=1)

print(f"Positive Examples: {len(pos_example)}")
print(f"Negative Examples: {len(neg_example)}")
pygol.evaluate_theory_prolog(H, "bk_files/combined_BK.pl", sorted(pos_example), sorted(neg_example))
# Write the final hypotheses to a file.
file_name_hypo = output_dir / "rules_turning_magnitude.txt"
with open(file_name_hypo, "w") as f:
    for rule in H:
        pretty_print_prolog(rule)
        #combined_rules.append(rule)
        f.write(rule + ".\n")
print(f"Rules written to {file_name_hypo}")

combined_rules["turning_magnitude"] = H


print("\n" + "=" * 60)
print("        Learning Avoid")
print("=" * 60)

pos_example_avoid = "positive_examples/avoid.pl"
neg_example_avoid = "negative_examples/avoid.pl"

pos_all = read_example(pos_example_avoid)
neg_all = read_example(neg_example_avoid)


#remove dupilcated from pos
pos_example = list(set(pos_all))
# remove noisy examples from neg
neg_example = [eache for eache in neg_all if eache not in pos_all]
H= learn_rules_muti_label(facts, sorted(pos_example), sorted(neg_example), bk_path, print_hs=False, print_h=False, seed_value=10)

print(f"Positive Examples: {len(pos_example)}")
print(f"Negative Examples: {len(neg_example)}")
pygol.evaluate_theory_prolog(H, "bk_files/combined_BK.pl", sorted(pos_example), sorted(neg_example))
# Write the final hypotheses to a file.
file_name_hypo = output_dir / "rules_avoid.txt"
with open(file_name_hypo, "w") as f:
    for rule in H:
        pretty_print_prolog(rule)
        #combined_rules.append(rule)
        f.write(rule + ".\n")
print(f"Rules written to {file_name_hypo}")
combined_rules["avoid"] = H


print("\n" + "=" * 60)
print("        Learning Resume")
print("=" * 60)

pos_example_avoid = "positive_examples/resume.pl"
neg_example_avoid = "negative_examples/resume.pl"

pos_all = read_example(pos_example_avoid)
neg_all = read_example(neg_example_avoid)


#remove dupilcated from pos
pos_example = list(set(pos_all))
# remove noisy examples from neg
neg_example = [eache for eache in neg_all if eache not in pos_all]

H= learn_rules_muti_label(facts, sorted(pos_example), sorted(neg_example), bk_path, print_hs=False, print_h=False, seed_value=10)
pygol.evaluate_theory_prolog(H, "bk_files/combined_BK.pl", sorted(pos_example), sorted(neg_example))
# Write the final hypotheses to a file.
file_name_hypo = output_dir / "rules_resume.txt"
with open(file_name_hypo, "w") as f:
    for rule in H:
        pretty_print_prolog(rule)
        #combined_rules.append(rule)
        f.write(rule + ".\n")
print(f"Rules written to {file_name_hypo}")
combined_rules["resume"] = H


print("\n" + "=" * 60)
print("        Learning Side")
print("=" * 60)

pos_example_avoid = "positive_examples/cpa_side.pl"
neg_example_avoid = "negative_examples/cpa_side.pl"


pos_all = sorted(read_example(pos_example_avoid))
neg_all = sorted(read_example(neg_example_avoid))



neg_example = [eache for eache in neg_all if eache not in pos_all]
#remove dupilcated from pos
pos_example = sorted(list(set(pos_all)))
# remove noisy examples from neg
neg_example = sorted(list(set(neg_example)))


H= learn_rules_muti_label(facts, pos_example, neg_example, bk_path, print_hs=False, print_h=False, seed_value=10)

pygol.evaluate_theory_prolog(H, "bk_files/combined_BK.pl", sorted(pos_example), sorted(neg_example))
# Write the final hypotheses to a file.
file_name_hypo = output_dir / "rules_side.txt"
with open(file_name_hypo, "w") as f:
    for rule in H:
        pretty_print_prolog(rule)
        #combined_rules.append(rule)
        f.write(rule + ".\n")
print(f"Rules written to {file_name_hypo}")
combined_rules["side"] = H


combined_rules_file = output_dir / "rules.txt"
with open(combined_rules_file, "w") as f:
    #f.write(f"% Retain only pairs with a single, non-conflicting CPA side prediction.\n")
    for k, v in combined_rules.items():
        f.write(f"% Rules for {k}\n")
        for rule in v:
            f.write(rule + ".\n")
        f.write("\n")

#record all the rules over time in a file
final_rules_file = output_dir / "log_rules.txt"
with open(final_rules_file, "a") as f:
    # include timestamp in the file
    f.write(f"% Timestamp: {datetime.now()}\n")
    for k, v in combined_rules.items():
        f.write(f"% Rules for {k}\n")
        for rule in v:
            f.write(rule + ".\n")
        f.write("\n")



