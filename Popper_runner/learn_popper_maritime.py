from pathlib import Path
import shutil

def read_examples(kind, filename):
    file_path = BASE_DIR / kind / filename

    with open(file_path, "r", encoding="utf-8") as f:
        examples = [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("%")
        ]

    return examples


def write_examples(foldername, filename, examples):

    folder_path = BASE_DIR / foldername

    folder_path.mkdir(parents=True, exist_ok=True)

    file_path = folder_path / filename

    with open(file_path, "w", encoding="utf-8") as f:
        for example in examples:
            f.write(str(example).strip().rstrip(".") + ".\n")

    #print(f"Saved {len(examples)} examples to {file_path}")
    return str(file_path)




def combine_files(file1, file2, destination):
    file1 = Path(file1)
    file2 = Path(file2)
    destination = Path(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)

    with open(destination, "w", encoding="utf-8") as outfile:
        for file in [file1, file2]:
            with open(file, "r", encoding="utf-8") as infile:
                content = infile.read()
                outfile.write(content)
                if content and not content.endswith("\n"):
                    outfile.write("\n")

    print(f"Combined files saved to: {destination}")
    return str(destination)

BASE_DIR = Path(__file__).resolve().parent
PYGOL_DIR = BASE_DIR.parent / "PyGol-runner"

source = PYGOL_DIR / "bk_files" / "combined_BK.pl"
#destination = BASE_DIR / "bk_files" / "bk.pl"






print("\n" + "=" * 60)
print("        Learning Take Action")
print("=" * 60)

predicate = "take_action"

destination = BASE_DIR / predicate / "bk.pl"
destination.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(source, destination)

pos_example = read_examples(PYGOL_DIR / "positive_examples", predicate + ".pl")
neg_example = read_examples(PYGOL_DIR / "negative_examples", predicate + ".pl")


popper_examples = []

for i in range(len(pos_example)):
    popper_examples.append(f"pos({pos_example[i][0:-1]}).")

for i in range(len(neg_example)):
    popper_examples.append(f"neg({neg_example[i][0:-1]}).")

print(f"Popper formatted examples for {predicate}: {popper_examples}")


write_examples(predicate, "exs.pl", popper_examples)


combined_file = combine_files(
        BASE_DIR / f"bias_{predicate}.pl",
        BASE_DIR /  "bias_bk.pl",
        BASE_DIR / predicate / "bias.pl"
    )




import subprocess

task_dir = BASE_DIR / "take_action"

code = """
from popper.util import Settings, print_prog_score
from popper.loop import popper

settings = Settings.from_args()
prog, score = popper(settings)

if prog:
    print_prog_score(prog, score, settings, settings.noisy)
else:
    print("No solution found")
"""

result = subprocess.run(
    [
        "/opt/homebrew/bin/python3.14",
        "-c",
        code,
        str(task_dir)
    ],
    cwd=str(BASE_DIR.parent),
    capture_output=True,
    text=True
)

print(result.stdout)
print(result.stderr)
