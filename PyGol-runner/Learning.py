from datetime import datetime
from pathlib import Path

from util import *
from PyGol import *

# Resolve all project files relative to this script, not the shell's working directory.
BASE_DIR = Path(__file__).resolve().parent
output_dir = BASE_DIR / "rules"
output_dir.mkdir(parents=True, exist_ok=True)

combined_rules = {}
facts = str(BASE_DIR / "bk_files" / "facts.pl")
bk_path = str(BASE_DIR / "bk_files" / "BK.pl")
output_path = BASE_DIR / "bk_files" / "combined_BK.pl"
output_path.parent.mkdir(parents=True, exist_ok=True)


def example_path(kind, filename):
    return str(BASE_DIR / kind / filename)


def save_rules(filename, rules):
    file_path = output_dir / filename
    with open(file_path, "w") as f:
        for rule in rules:
            pretty_print_prolog(rule)
            f.write(rule + ".\n")
    print(f"Rules written to {file_path}")


def prepare_examples(positive_path, negative_path):
    pos_all = read_example(positive_path)
    neg_all = read_example(negative_path)
    pos_examples = sorted(set(pos_all))
    neg_examples = sorted(set(neg_all) - set(pos_all))
    return pos_examples, neg_examples


# Merge facts and background knowledge once for subsequent evaluation.
merge_prolog_files(facts, bk_path, str(output_path))

print("\n" + "=" * 60)
print("        Learning Take Action")
print("=" * 60)

pos_example = example_path("positive_examples", "take_action.pl")
neg_example = example_path("negative_examples", "take_action.pl")

H, HS = learn_rules(
    facts, pos_example, neg_example, bk_path,
    print_hs=False, print_h=False, seed_value=10
)
pos_example_list = pygol.read_example(pos_example)
neg_example_list = pygol.read_example(neg_example)
pygol.evaluate_theory_prolog(
    H, str(output_path), sorted(pos_example_list), sorted(neg_example_list)
)
save_rules("rules_take_action.txt", H)
combined_rules["take_action"] = H


print("\n" + "=" * 60)
print("        Learning Turning Magnitude")
print("=" * 60)

pos_example, neg_example = prepare_examples(
    example_path("positive_examples", "turn.pl"),
    example_path("negative_examples", "turn.pl"),
)
H = learn_rules_muti_label(
    facts, pos_example, neg_example, bk_path,
    print_hs=False, print_h=False, seed_value=10, label_literal=1
)
print(f"Positive Examples: {len(pos_example)}")
print(f"Negative Examples: {len(neg_example)}")
pygol.evaluate_theory_prolog(H, str(output_path), pos_example, neg_example)
save_rules("rules_turning_magnitude.txt", H)
combined_rules["turning_magnitude"] = H


print("\n" + "=" * 60)
print("        Learning Avoid")
print("=" * 60)

pos_example, neg_example = prepare_examples(
    example_path("positive_examples", "avoid.pl"),
    example_path("negative_examples", "avoid.pl"),
)
H = learn_rules_muti_label(
    facts, pos_example, neg_example, bk_path,
    print_hs=False, print_h=False, seed_value=10
)
print(f"Positive Examples: {len(pos_example)}")
print(f"Negative Examples: {len(neg_example)}")
pygol.evaluate_theory_prolog(H, str(output_path), pos_example, neg_example)
save_rules("rules_avoid.txt", H)
combined_rules["avoid"] = H


print("\n" + "=" * 60)
print("        Learning Resume")
print("=" * 60)

pos_example, neg_example = prepare_examples(
    example_path("positive_examples", "resume.pl"),
    example_path("negative_examples", "resume.pl"),
)
H = learn_rules_muti_label(
    facts, pos_example, neg_example, bk_path,
    print_hs=False, print_h=False, seed_value=10
)
pygol.evaluate_theory_prolog(H, str(output_path), pos_example, neg_example)
save_rules("rules_resume.txt", H)
combined_rules["resume"] = H


print("\n" + "=" * 60)
print("        Learning Side")
print("=" * 60)

pos_example, neg_example = prepare_examples(
    example_path("positive_examples", "cpa_side.pl"),
    example_path("negative_examples", "cpa_side.pl"),
)
H = learn_rules_muti_label(
    facts, pos_example, neg_example, bk_path,
    print_hs=False, print_h=False, seed_value=10
)
pygol.evaluate_theory_prolog(H, str(output_path), pos_example, neg_example)
save_rules("rules_side.txt", H)
combined_rules["side"] = H


combined_rules_file = output_dir / "rules.txt"
with open(combined_rules_file, "w") as f:
    for category, rules in combined_rules.items():
        f.write(f"% Rules for {category}\n")
        for rule in rules:
            f.write(rule + ".\n")
        f.write("\n")

# Append a timestamped record of all learned rules.
final_rules_file = output_dir / "log_rules.txt"
with open(final_rules_file, "a") as f:
    f.write(f"% Timestamp: {datetime.now()}\n")
    for category, rules in combined_rules.items():
        f.write(f"% Rules for {category}\n")
        for rule in rules:
            f.write(rule + ".\n")
        f.write("\n")
