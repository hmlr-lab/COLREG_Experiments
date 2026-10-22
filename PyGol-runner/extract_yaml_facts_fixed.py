
from pathlib import Path
import re
import yaml

YAML_DIR = Path("../examples/take_action/")
OUTPUT_DIR = Path("scenarios")


def main():
    files = sorted(
        set(YAML_DIR.glob("*.yaml")) |
        set(YAML_DIR.glob("*.yml"))
    )

    if not files:
        raise FileNotFoundError(
            f"No YAML files found in {YAML_DIR}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total = 0

    for source in files:
        data = yaml.safe_load(
            source.read_text(encoding="utf-8")
        )

        if not isinstance(data, list):
            raise ValueError(
                f"Expected a list of scenarios in {source}"
            )

        # crossing1(1).yaml -> crossing1_1.pl
        stem = re.sub(r"\(\d+\)$", "", source.stem)

        for i, item in enumerate(data, 1):
            facts = item.get("facts", [])

            if not isinstance(facts, list):
                raise ValueError(
                    f"Invalid facts in {source}, scenario {i}"
                )

            dest = OUTPUT_DIR / f"{stem}_{i}.pl"

            dest.write_text(
                "".join(
                    str(f).strip().rstrip(".") + ".\n"
                    for f in facts
                ),
                encoding="utf-8"
            )

            total += 1

            print(
                f"Created: {dest.name} "
                f"({len(facts)} facts)"
            )

    print(f"\nTotal: {total} files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
