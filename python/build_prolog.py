from python.util import *

# Example log files
file_path_log = ["260709_examples/log_0.txt",
                 "260709_examples/log_1.txt",
                "260709_examples/log_2.txt",
                "260709_examples/log_3.txt",
                "260709_examples/log_4.txt",
                 ]

# Generate stage 1 BK files from log files
facts, examples =  generate_bk_from_log(file_path_log, verbose=False)

# Save the examples
write_prolog_file(examples, PROLOG_GENERATED / "examples.pl")
# Save the generated Prolog knowledge base (facts and rules) for evaluation.
write_prolog_file(facts, PROLOG_GENERATED / "facts.pl")