# pip install pyyaml

import os
import yaml

with open("all_scenarios.yaml") as f:
    data = yaml.safe_load(f)


def rename_fact(fact, idx):
    # e.g. "sector(agent,vessel1,starboard_bow_forward)" -> "sector(agent_0,vessel_0,starboard_bow_forward)"
    functor, args_str = fact.split('(', 1)
    args = args_str.rstrip(')').split(',')
    renamed_args = [
        f'agent_{idx}' if arg == 'agent' else
        f'vessel_{idx}' if arg == 'vessel1' else
        f'vessel_{idx}' if arg == 'cruiseliner1' else
        arg
        for arg in args
    ]
    return f"{functor}({','.join(renamed_args)})"


facts = []
examples = {
    ('pos', 'take_action'): [],
    ('neg', 'take_action'): [],
    ('pos', 'turn'): [],
    ('neg', 'turn'): [],
    ('pos', 'avoid'): [],
    ('neg', 'avoid'): [],
    ('pos', 'resume'): [],
    ('neg', 'resume'): [],
    ('pos', 'cpa_side'): [],
    ('neg', 'cpa_side'): [],
}

for i, example in enumerate(data):
    for fact in example['facts']:
        facts.append(rename_fact(fact, i))

    label = example['take_action']
    examples[(label, 'take_action')].append(f"take_action(agent_{i})")

    for branch in ('pos', 'neg'):
        for step_facts in example['waypoints'].get(branch, {}).values():
            for wfact in step_facts:
                renamed = rename_fact(wfact, i)
                predicate = renamed.split('(', 1)[0]
                examples[(branch, predicate)].append(renamed)


import os

# Create folder if it doesn't exist
os.makedirs("bk_files", exist_ok=True)

# Write facts.pl inside the folder
with open("bk_files/facts.pl", "w") as f:
    for fact in facts:
        f.write(f"{fact}.\n")




folder_names = {
    "pos": "positive_examples",
    "neg": "negative_examples"
}

for (label, predicate), fact_list in examples.items():
    folder = folder_names[label]
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, f"{predicate}.pl"), "w") as f:
        for fact in fact_list:
            f.write(f"{fact}.\n")
