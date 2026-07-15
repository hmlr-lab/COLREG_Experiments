from util import *

# Example log files
file_path_log = list_log_files(POS_EXAMPLES)

print(file_path_log)

# Generate stage 1 BK files from log files
facts, examples =  generate_bk_from_log(file_path_log, verbose=False)

# Save the examples
write_prolog_file(examples, PROLOG_GENERATED / "examples.pl")
# Save the generated Prolog knowledge base (facts and rules) for evaluation.
write_prolog_file(facts, PROLOG_GENERATED / "facts.pl")