
from pathlib import Path
import csv
import re
import tempfile
import janus_swi as janus

# ============================================================
# CONFIGURATION
# ============================================================

BK_FILE = Path("BK.pl")
HYPOTHESIS_FILE = Path("current_combined_rules.txt")

SCENARIO_DIR = Path("scenarios")
REPORT_DIR = Path("reports")

KEEP_TEMP_FILE = False

QUERIES = [
    "take_action(agent)",
    "turn(agent,B)",
    "avoid(agent,B,C)",
    "resume(agent,B,C)",
    "cpa_side(agent,B,C)",
]


# ============================================================
# QUERY PARSING
# ============================================================

def parse_query(query):

    match = re.fullmatch(
        r"([a-z][A-Za-z_0-9]*)\(([^()]*)\)",
        query.strip()
    )

    if not match:
        raise ValueError(
            f"Unsupported query format: {query}"
        )

    predicate = match.group(1)

    arguments = [
        arg.strip()
        for arg in match.group(2).split(",")
    ]

    return predicate, arguments


# ============================================================
# SCENARIO FILE SORTING
# ============================================================

def scenario_sort_key(path):
    """
    Natural sorting of scenario filenames.

    crossing1_1.pl
    crossing1_2.pl
    crossing1_10.pl
    crossing2_1.pl
    headon1_1.pl
    """

    match = re.fullmatch(
        r"(.+)_(\d+)",
        path.stem
    )

    if match:
        return (
            match.group(1),
            int(match.group(2))
        )

    return (path.stem, 0)


# ============================================================
# COMBINE BK + SCENARIO + HYPOTHESES
# ============================================================

def combine_files(scenario_file):

    sources = [
        BK_FILE,
        scenario_file,
        HYPOTHESIS_FILE
    ]

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".pl",
        encoding="utf-8",
        delete=False
    ) as handle:

        combined_path = Path(handle.name)

        for source in sources:

            handle.write(
                f"\n% ===== {source.name} =====\n"
            )

            content = source.read_text(
                encoding="utf-8"
            )

            handle.write(content)
            handle.write("\n")

    return combined_path


# ============================================================
# EVALUATE ONE QUERY
# ============================================================

def evaluate_query(module, query):

    predicate, arguments = parse_query(query)

    arity = len(arguments)

    qualified_query = f"{module}:{query}"

    try:

        predicate_check = (
            f"current_predicate("
            f"{module}:{predicate}/{arity})"
        )

        exists = janus.query_once(
            predicate_check
        )["truth"]

        if not exists:
            return {
                "status": "UNDEFINED",
                "solutions": []
            }

        found = set()

        with janus.query(qualified_query) as answers:

            for answer in answers:

                values = []

                for argument in arguments:

                    if argument in answer:
                        values.append(
                            str(answer[argument])
                        )
                    else:
                        values.append(argument)

                fact = (
                    f"{predicate}("
                    f"{','.join(values)})"
                )

                found.add(fact)

        solutions = sorted(found)

        return {
            "status": (
                "TRUE" if solutions else "FALSE"
            ),
            "solutions": solutions
        }

    except Exception as error:

        return {
            "status": "ERROR",
            "solutions": [],
            "error": str(error)
        }


# ============================================================
# EVALUATE ONE SCENARIO
# ============================================================

def evaluate_scenario(scenario_file):

    combined_file = combine_files(
        scenario_file
    )

    module = (
        "scenario_eval_" +
        re.sub(
            r"[^a-zA-Z0-9_]",
            "_",
            scenario_file.stem
        )
    )

    try:

        janus.consult(
            str(combined_file),
            module=module
        )

        results = {}

        for query in QUERIES:

            results[query] = evaluate_query(
                module,
                query
            )

        return results

    finally:

        if not KEEP_TEMP_FILE:
            combined_file.unlink(
                missing_ok=True
            )


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():

    # --------------------------------------------------------
    # Validate input files
    # --------------------------------------------------------

    for source in [
        BK_FILE,
        HYPOTHESIS_FILE
    ]:

        if not source.is_file():
            raise FileNotFoundError(
                f"Missing file: {source}"
            )

    if not SCENARIO_DIR.is_dir():
        raise FileNotFoundError(
            f"Scenario folder not found: {SCENARIO_DIR}"
        )

    # --------------------------------------------------------
    # Find all scenario files
    # --------------------------------------------------------

    scenarios = sorted(
        SCENARIO_DIR.glob("*.pl"),
        key=scenario_sort_key
    )

    if not scenarios:
        raise FileNotFoundError(
            f"No .pl files found in {SCENARIO_DIR}"
        )

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=" * 70)
    print("JANUS / PYGOL SCENARIO EVALUATION")
    print("=" * 70)

    print(f"BK         : {BK_FILE}")
    print(f"Hypotheses : {HYPOTHESIS_FILE}")
    print(f"Scenarios  : {len(scenarios)}")
    print(f"Output     : {REPORT_DIR}")

    # --------------------------------------------------------
    # Prepare reports
    # --------------------------------------------------------

    report_lines = [
        "JANUS / PYGOL SCENARIO EVALUATION",
        f"BK: {BK_FILE}",
        f"Hypotheses: {HYPOTHESIS_FILE}",
        f"Scenarios: {len(scenarios)}",
        ""
    ]

    csv_rows = []

    # --------------------------------------------------------
    # Evaluate all scenarios
    # --------------------------------------------------------

    for index, scenario in enumerate(
        scenarios,
        start=1
    ):

        print(
            f"[{index}/{len(scenarios)}] "
            f"Evaluating {scenario.name}"
        )

        results = evaluate_scenario(
            scenario
        )

        report_lines.extend([
            "=" * 72,
            f"Scenario: {scenario.name}",
            "=" * 72
        ])

        row = {
            "scenario": scenario.name
        }

        # ----------------------------------------------------
        # Store predictions
        # ----------------------------------------------------

        for query in QUERIES:

            result = results[query]

            status = result["status"]

            report_lines.append(
                f"\n{query}: {status}"
            )

            for solution in result["solutions"]:

                report_lines.append(
                    f"  {solution}."
                )

            if result.get("error"):

                report_lines.append(
                    f"  ERROR: {result['error']}"
                )

            predicate, _ = parse_query(
                query
            )

            row[
                f"{predicate}_status"
            ] = status

            row[
                f"{predicate}_values"
            ] = "; ".join(
                result["solutions"]
            )

        csv_rows.append(row)

        report_lines.append("")

    # --------------------------------------------------------
    # Save detailed text report
    # --------------------------------------------------------

    text_path = (
        REPORT_DIR /
        "scenario_report.txt"
    )

    text_path.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # Save CSV summary
    # --------------------------------------------------------

    csv_path = (
        REPORT_DIR /
        "scenario_summary.csv"
    )

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=list(csv_rows[0])
        )

        writer.writeheader()
        writer.writerows(csv_rows)

    # --------------------------------------------------------
    # Final output
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("EVALUATION COMPLETED")
    print("=" * 70)

    print(
        f"Total scenarios: {len(scenarios)}"
    )

    print(
        f"Text report: {text_path}"
    )

    print(
        f"CSV report : {csv_path}"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
