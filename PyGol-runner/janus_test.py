import re
import janus_swi as janus


def split_prolog_args(s):
    args, cur, depth = [], "", 0

    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1

        if ch == "," and depth == 0:
            args.append(cur.strip())
            cur = ""
        else:
            cur += ch

    if cur.strip():
        args.append(cur.strip())

    return args


def extract_pred_args(literal):
    literal = literal.strip().rstrip(".")
    m = re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)\((.*)\)$", literal)

    if not m:
        return None, []

    return m.group(1), split_prolog_args(m.group(2))


def queries_from_modeb_declarations(mode_declarations):
    queries = []

    for m in mode_declarations:
        m = m.strip().rstrip(".")

        if not m.startswith("modeb"):
            continue

        inside = m[m.find("(") + 1:m.rfind(")")]
        parts = split_prolog_args(inside)

        if len(parts) >= 2:
            q = parts[1].strip()
            if q not in queries:
                queries.append(q)

    return queries


def normalize_agent_names(literal):
    literal = re.sub(r"\bagent[^,\)]*", "A", literal)
    literal = re.sub(r"\bcruiseliner[^,\)]*", "B", literal)
    literal = re.sub(r"\bvessel[^,\)]*", "B", literal)
    return literal


# def get_example_binding(example):
#     _, args = extract_pred_args(example)

#     if len(args) < 2:
#         return {
#                 "A": args[0]
#             }

#     return {
#         "A": args[0],
#         "B": args[1]
#     }

# def get_example_binding(example):
#     """
#     Supports both:

#         take_action(agent_1)
#         take_action(agent_1, vessel_1)

#     For unary targets, initially bind only A.
#     B will be discovered later.
#     """

#     _, args = extract_pred_args(example)

#     if not args:
#         raise ValueError(
#             f"Cannot extract arguments from example: {example}"
#         )

#     binding = {
#         "A": args[0]
#     }

#     # If target already contains B, use it directly
#     if len(args) >= 2:
#         binding["B"] = args[1]

#     return binding

def get_example_binding(example):
    _, args = extract_pred_args(example)

    if not args:
        raise ValueError(f"Cannot extract arguments from example: {example}")

    binding = {
        "A": args[0]
    }

    # Only bind B when the second argument is really a vessel
    if len(args) >= 2:
        if (
            args[1].startswith("vessel_")
            or args[1].startswith("cruiseliner_")
        ):
            binding["B"] = args[1]

    return binding



def infer_B_from_bottom_clause(
    bottom_literals,
    binding,
    debug=False
):
    """
    Infer B when the target is unary, e.g.

        take_action(agent_1)

    using an existing bottom-clause literal such as:

        sector(A,B,starboard_bow_forward)

    which becomes:

        sector(agent_1,B,starboard_bow_forward)

    and may return:

        B = vessel_1
    """

    # B already known
    if "B" in binding:
        return binding

    # Prefer predicates that are normally safe for finding B
    priority = [
        "sector",
        "starboard_forward",
        "port_forward",
        "forward",
        "arc_overtaking",
        "range",
        "dcpa",
        "tcpa"
    ]

    def priority_key(literal):
        pred, _ = extract_pred_args(literal)

        if pred in priority:
            return priority.index(pred)

        return len(priority)

    literals = sorted(
        bottom_literals,
        key=priority_key
    )

    for literal in literals:

        pred, args = extract_pred_args(literal)

        if pred is None:
            continue

        # We specifically need a literal involving B
        if "B" not in args:
            continue

        # Replace known variables, mainly A
        query_args = [
            binding.get(arg, arg)
            for arg in args
        ]

        query = (
            f"{pred}("
            + ",".join(query_args)
            + ")"
        )

        if debug:
            print("Trying to infer B:", query)

        try:
            solutions = list(janus.query(query))

        except Exception as e:

            if debug:
                print(
                    "Could not use for B:",
                    query,
                    e
                )

            continue

        for solution in solutions:

            if "B" in solution:

                B_value = str(solution["B"])

                binding["B"] = B_value

                if debug:
                    print(
                        "Found B:",
                        B_value,
                        "using",
                        query
                    )

                return binding

    # -----------------------------------------------------
    # Fallback for your COLREGS naming scheme
    #
    # agent_1  -> vessel_1
    # agent_11 -> vessel_11
    # -----------------------------------------------------

    A_value = binding.get("A")

    if A_value and A_value.startswith("agent_"):

        B_value = A_value.replace(
            "agent_",
            "vessel_",
            1
        )

        binding["B"] = B_value

        if debug:
            print(
                "B inferred from naming convention:",
                B_value
            )

    return binding

def ground_bottom_literal(literal, binding):
    pred, args = extract_pred_args(literal)

    if pred is None:
        return None

    grounded_args = [binding.get(a, a) for a in args]

    return f"{pred}({','.join(grounded_args)})."


def bind_query_with_example(query, binding):
    """
    applies(A,B,R)
    -> applies(agent_1_1,cruiseliner_1_1,R)

    tcpa_closing(A,B)
    -> tcpa_closing(agent_1_1,cruiseliner_1_1)
    """

    pred, args = extract_pred_args(query)

    if pred is None:
        return query

    new_args = [binding.get(a, a) for a in args]

    return f"{pred}({','.join(new_args)})"


def subst_to_literal(query, sol):
    pred, args = extract_pred_args(query)

    grounded_args = [str(sol.get(a, a)) for a in args]

    return f"{pred}({','.join(grounded_args)})"


_LOADED_BK_FILES = set()


def consult_bk_once(bk_path, debug=False):
    global _LOADED_BK_FILES

    if bk_path in _LOADED_BK_FILES:
        return

    if debug:
        print("CONSULTING BK ONCE:", bk_path)

    janus.query_once(f"consult('{bk_path}')")
    _LOADED_BK_FILES.add(bk_path)


# def assert_bottom_facts(bottom_facts, debug=False):
#     for fact in bottom_facts:
#         fact = fact.strip().rstrip(".")

#         if not fact:
#             continue
        
        
#         query = f"assertz(({fact}))"

#         if debug:
#             print("ASSERT:", query)
        
#         janus.query_once(query)


def contains_prolog_variable(term):
    """
    Return True when a Prolog term contains an unbound variable.

    Examples
    --------
    range(agent_1,ship_1,far)       -> False
    less_than(R,far)                -> True
    encounter(agent_1,ship_1,R)     -> True
    tcpa(agent_1,ship_1,short)      -> False
    """

    term = term.strip().rstrip(".")

    # Prolog variables begin with an uppercase letter or underscore.
    variable_pattern = r"(?<![A-Za-z0-9_])(?:[A-Z][A-Za-z0-9_]*|_[A-Za-z0-9_]*)\b"

    return re.search(variable_pattern, term) is not None


def assert_bottom_facts(bottom_facts, debug=False):
    """
    Assert only fully ground bottom-clause literals.

    Literals containing variables are query templates and must not be
    inserted as Prolog facts.
    """

    asserted_facts = []

    for fact in bottom_facts:
        fact = fact.strip().rstrip(".")

        if not fact:
            continue

        if contains_prolog_variable(fact):
            if debug:
                print("SKIP NON-GROUND:", fact)
            continue

        query = f"assertz(({fact}))"

        if debug:
            print("ASSERT:", query)

        try:
            janus.query_once(query)
            asserted_facts.append(fact)

        except Exception as exc:
            print("\nFAILED TO ASSERT:", fact)
            print("PROLOG QUERY:", query)
            print("ERROR:", exc)
            raise

    return asserted_facts


def clear_bottom_facts(bottom_facts, debug=False):
    for fact in bottom_facts:
        pred, args = extract_pred_args(fact)

        if pred is None:
            continue

        query = f"retractall({pred}({','.join(['_'] * len(args))}))"

        if debug:
            print("RETRACT:", query)

        janus.query_once(query)


# def modify_bcrl_janus_from_bk(
#     bk_path,
#     bottom_clause_dict,
#     mode_declarations,
#     normalize=True,
#     debug=False
# ):
#     consult_bk_once(bk_path, debug=debug)

#     query_literals = queries_from_modeb_declarations(mode_declarations)

#     output = {}

#     for example, bottom_literals in bottom_clause_dict.items():

#         binding = get_example_binding(example)

#         bottom_facts = []

#         for lit in bottom_literals:
#             grounded = ground_bottom_literal(lit, binding)
#             if grounded:
#                 bottom_facts.append(grounded)

#         if debug:
#             print("\n================================")
#             print("Example:", example)
#             print("Binding:", binding)
#             print("Modeb queries:", query_literals)
#             print("Ground bottom facts:")
#             for f in bottom_facts:
#                 print("  ", f)

#         assert_bottom_facts(bottom_facts, debug=debug)

#         if normalize:
#             updated_literals = [
#                 normalize_agent_names(lit)
#                 for lit in bottom_literals
#             ]
#         else:
#             updated_literals = list(bottom_literals)

#         for q in query_literals:

#             grounded_q = bind_query_with_example(q, binding)
#             #print(grounded_q)
#             if debug:
#                 print("\nQUERY:", grounded_q)

#             try:
#                 solutions = list(janus.query(grounded_q))
#             except janus.PrologError as e:
#                 if "sufficiently instantiated" in str(e):
#                     continue
#                 raise

#             for sol in solutions:
#                 lit = subst_to_literal(grounded_q, sol)

#                 if normalize:
#                     lit = normalize_agent_names(lit)

#                 if lit not in updated_literals:
#                     updated_literals.append(lit)

#                     if debug:
#                         print("  ADDED:", lit)

#         clear_bottom_facts(bottom_facts, debug=debug)

#         output[example] = updated_literals

#     return output




def modify_bcrl_janus_from_bk(
    bk_path,
    bottom_clause_dict,
    mode_declarations,
    normalize=True,
    debug=False
):

    # =====================================================
    # 1. Consult BK
    # =====================================================

    consult_bk_once(
        bk_path,
        debug=debug
    )

    query_literals = queries_from_modeb_declarations(
        mode_declarations
    )

    output = {}

    # =====================================================
    # 2. Process each example
    # =====================================================

    for example, bottom_literals in bottom_clause_dict.items():

        # ---------------------------------------------
        # Initial binding
        #
        # take_action(agent_1)
        #
        # gives:
        #
        # A = agent_1
        # ---------------------------------------------

        binding = get_example_binding(example)

        # ---------------------------------------------
        # NEW PART
        #
        # Find B using existing bottom clause / BK
        # ---------------------------------------------

        binding = infer_B_from_bottom_clause(
            bottom_literals,
            binding,
            debug=debug
        )

        if debug:

            print("\n================================")
            print("Example:", example)
            print("Final binding:", binding)

        # ---------------------------------------------
        # Example:
        #
        # A = agent_1
        # B = vessel_1
        #
        # Therefore:
        #
        # sector(A,B,...)
        #
        # becomes:
        #
        # sector(agent_1,vessel_1,...)
        # ---------------------------------------------

        bottom_facts = []

        for lit in bottom_literals:

            grounded = ground_bottom_literal(
                lit,
                binding
            )

            if grounded:
                bottom_facts.append(grounded)

        if debug:

            print("Modeb queries:")
            for q in query_literals:
                print("  ", q)

            print("Ground bottom facts:")
            for f in bottom_facts:
                print("  ", f)

        # =================================================
        # 3. Assert existing bottom-clause information
        # =================================================

        assert_bottom_facts(
            bottom_facts,
            debug=debug
        )

        # =================================================
        # 4. Start output with original bottom clause
        # =================================================

        if normalize:

            updated_literals = [
                normalize_agent_names(lit)
                for lit in bottom_literals
            ]

        else:

            updated_literals = list(
                bottom_literals
            )

        # =================================================
        # 5. Query additional predicates from BK
        # =================================================

        for q in query_literals:

            grounded_q = bind_query_with_example(
                q,
                binding
            )

            if debug:
                print(
                    "\nQUERY:",
                    grounded_q
                )

            try:

                solutions = list(
                    janus.query(grounded_q)
                )

            except Exception as e:

                print(
                    "FAILED QUERY:",
                    grounded_q
                )

                # Do not terminate learning just because one
                # derived predicate cannot be evaluated.
                if (
                    "sufficiently instantiated"
                    in str(e)
                ):

                    if debug:
                        print(
                            "Skipping insufficiently "
                            "instantiated query."
                        )

                    continue

                clear_bottom_facts(
                    bottom_facts,
                    debug=debug
                )

                raise e

            # =================================================
            # 6. Add solutions returned by BK
            # =================================================

            for sol in solutions:

                lit = subst_to_literal(
                    grounded_q,
                    sol
                )

                if normalize:
                    lit = normalize_agent_names(
                        lit
                    )

                if lit not in updated_literals:

                    updated_literals.append(
                        lit
                    )

                    if debug:
                        print(
                            "  ADDED:",
                            lit
                        )

        # =================================================
        # 7. Remove temporary facts
        # =================================================

        clear_bottom_facts(
            bottom_facts,
            debug=debug
        )

        output[example] = updated_literals

    return output