import re

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYGOL_DIR = ROOT / "PyGol_Files"
PROLOG = ROOT / "prolog"
PROLOG_GENERATED = ROOT / "prolog/generated"
EXAMPLES = ROOT / "examples"

sys.path.insert(0, str(PYGOL_DIR))

import PyGol as pygol
from python.janus_test import *
from python.bc_pruner import *

mode_declarations =  [
    "modeb(*, port_forward(A,B)).",
    "modeb(*, port_aft(A,B)).",
    "modeb(*, starboard_forward(A,B)).",
    "modeb(*, starboard_aft(A,B)).",
    "modeb(*, port(A,B)).",
    "modeb(*, starboard(A,B)).",
    "modeb(*, forward(A,B)).",
    "modeb(*, aft(A,B)).",

    "modeb(*, less_than(R1,R2)).",
    "modeb(*, less_or_equal(R1,R2)).",
    "modeb(*, greater_than(R1,R2)).",
    "modeb(*, greater_or_equal(R1,R2)).",

    "modeb(*, dcpa_unacceptable(A,B)).",
    "modeb(*, dcpa_acceptable(A,B)).",

    "modeb(*, tcpa_closing(A,B)).",
    "modeb(*, actionable_range(A,B)).",

    "modeb(*, ample_time(A,B)).",

    "modeb(*, collision_risk(A,B)).",

    "modeb(*, close_quarters_developing(A,B)).",
    "modeb(*, close_quarters(A,B)).",

    "modeb(*, encounter(A,B,R)).",
    "modeb(*, encounter_and_duty(A,B,R,D)).",

    "modeb(*, conduct(A,B,R)).",

    "modeb(*, rule2_extremis(A,B)).",

    "modeb(*, sector(A,B,S)).",
    "modeb(*, range(A,B,R)).",
    "modeb(*, dcpa(A,B,D)).",
    "modeb(*, tcpa(A,B,T)).",
    "modeb(*, arc_overtaking(A,B)).",
]

# mode_declarations = [
#     # Heads
#     #"modeb(*, applies(A,B,R)).",
#     #"modeb(*, role(A,B,R)).",
#     #"modeb(*, priority(A,B,R1,R2,W)).",

#     # Primitive facts
#     "modeb(*, sector(A,B,S)).",
#     "modeb(*, range(A,B,R)).",
#     "modeb(*, dcpa(A,B,D)).",
#     "modeb(*, tcpa(A,B,T)).",
#     "modeb(*, bearing(A,B,V)).",
#     "modeb(*, distance(A,B,V)).",
#     "modeb(*, status(A,S)).",
#     "modeb(*, waterway(A,W)).",
#     "modeb(*, constraint_draught(A)).",
#     "modeb(*, clock(C)).",

#     # Geometric abstractions
#     "modeb(*, arc_overtaking(A,B)).",
#     "modeb(*, port_forward(A,B)).",
#     "modeb(*, port_aft(A,B)).",
#     "modeb(*, starboard_forward(A,B)).",
#     "modeb(*, starboard_aft(A,B)).",
#     "modeb(*, port(A,B)).",
#     "modeb(*, starboard(A,B)).",
#     "modeb(*, forward(A,B)).",
#     "modeb(*, aft(A,B)).",

#     # Derived concepts
#     "modeb(*, dcpa_unsafe(A,B)).",
#     "modeb(*, dcpa_safe(A,B)).",
#     "modeb(*, tcpa_closing(A,B)).",
#     "modeb(*, range_actionable(A,B)).",
   
#     "modeb(*, risk_collision(A,B)).",
#     "modeb(*, close_quarters(A,B)).",
#     "modeb(*, close_quarters_developing(A,B)).",

#     # Recursive predicates
#     "modeb(*, encounter(A,B,R)).",
#     "modeb(*, encounter_and_duty(A,B,R,D)).",
#     "modeb(*, conduct(A,B,R,D)).",

#     "modeb(*, time_ample(A,B)).",
#     #"modeb(*, role(A,B,R)).",
#     #"modeb(*, priority(A,B,R1,R2,W))."
#     "range_nearer(*, time_ample(A,B)).",
#     "range_nearer_similar(*, time_ample(A,B)).",
#     "range_farther(*, time_ample(A,B)).",
#     "range_farther_similar(*, time_ample(A,B)).",
#     ]

K = [
 'ahead',
 'port_bow_forward',
 'port_bow_broad',
 'port_beam_forward',
 'port_beam',
 'port_beam_aft',
 'port_quarter_broad',
 'port_quarter_aft',
 'astern',
 'starboard_quarter_aft',
 'starboard_quarter_broad',
 'starboard_beam_aft',
 'starboard_beam',
 'starboard_beam_forward',
 'starboard_bow_broad',
 'starboard_bow_forward',
 "aft", "forward",
 'n', 'nne', 'ne', 'ene', 'e', 'ese', 'se', 'sse', 's', 'ssw', 'sw', 'wsw', 'w', 'wnw', 'nw', 'nnw',
 "far","very_far", "middle","far", "near","middle",  "very_near","near", "long", "very_long", "medium", "short", "immediate", "large", "very_large", "moderate", "small", "insubstantial", 
 "no_risk", "port", "starboard"
]


constraints={
        "starboard_forward": ["starboard", "forward",],  
        "port_forward":      ["port", "forward", ],     
        #"range_actionable":["range"],
        "collision_risk" : ["dcpa_unacceptable"],
        "encounter_and_duty":["sector", "aft", "forward", "ahead", "forward", "starboard_forward", "port_forward"],

    }

def return_substring(string):
    pred = string.split("(")[0]

    if pred in ["cpa", "tcpa", "range", "sector", "bearing", "distance", "course", "course_compass"]:
        return string.rsplit(',', 1)[0]

    if pred in ["course_compass"]:
        return string.split(',')[0]

    if pred in ["add_waypoint_seg"]:
        return "add_waypoint_seg"

    if pred in ["add_waypoint"]:
        return "add_waypoint"
    
    if pred in ["add_waypoint_bin"]:
        return "add_waypoint_bin"
    
    if pred in ["waypoint"]:
        return "waypoint"
 
    
    return None   # explicit


def replace_starting_with(lst, starts_with, new_value):
    return [
        new_value if item.startswith(starts_with) else item
        for item in lst
    ]


def contains_substring(lst, substring):
    return any(substring in item for item in lst)

def ground_facts_log_file(file_path, not_allowed=[]):
    keys = []
    with open(file_path, "r") as f:
        raw = f.read()

    lines = raw.strip().split("\n")
    clock_pattern = r'clock\((\d+)\)'
    dict = {}
    for line in lines:
        line = line.strip().rstrip(".")
        if not line:
            continue

        parts = [p.strip() for p in line.split("),")]
        parts = [p + ("" if p.endswith(")") else ")") for p in parts]
        #print(parts[0])
        key = int(parts[0].split("(")[1].rstrip(")"))
        #print("Processing time:", key)
        if len(dict)==0:
            dict[key] = parts[1:]
        else:
            #print(parts[1:])
            last_key, last_value = list(dict.items())[-1]
            
            for eachi in parts[1:]:
                substring = return_substring(eachi)
                #print(substring)
                if  substring == "waypoint" :
                    #print("I am here", substring, parts[0])
                    time = int(re.findall(r"\d+", parts[0])[0])
                    keys.append(time)
                    last_value.append(eachi)
                elif substring is not None:
                    #print("Replacing", substring, "with", eachi)
                    last_value = replace_starting_with(last_value, substring, eachi)

            if contains_substring(last_value, "waypoint")  and  not(contains_substring(parts[1:], "waypoint")) :
               
                #print("Removing add_waypoint_seg from last_value")
                lst = [item for item in last_value if not item.startswith(tuple(["waypoint"]))]
                dict[key] = lst
            else:
                dict[key] = last_value    
    return dict, keys



def generate_facts_examples(state_list_pos1, keys, ex=1, print_facts=False, skip_prefixes=[]):
    facts_new = []
    positive_examples = []
    positive_examples_1 = []
    for id1, i in enumerate(keys):
        new_agent = f"agent_{ex}_{id1+1}"
        cruiseliner = f"cruiseliner_{ex}_{id1+1}"

        for fact in state_list_pos1.get(i, []):
            #print(fact)
            # Replace ONLY standalone 'agent'
            fact = re.sub(r"\bagent\b", new_agent, fact)
            fact_1 = re.sub(r"\bagent\b", new_agent, fact)

            # Replace ONLY exact 'cruiseliner1'
            fact = re.sub(r"\bcruiseliner1\b", cruiseliner, fact)
            fact_1 = re.sub(r"\bcruiseliner1\b", new_agent, fact_1)


            # # Skip if new_agent appears 2+ times as a token
            # if len(re.findall(rf"\b{re.escape(new_agent)}\b", fact)) >= 2:
            #     positive_examples_1.append(fact)
            #     continue
            
            # Skip if fact starts with any of the skip_prefixes
            if any(p in fact for p in skip_prefixes):
                continue
            #print(fact)
            #print("\t", fact)
            

            if "waypoint" in fact: #or "add_waypoint" in fact or "add_waypoint_bin" in fact:
                
                positive_examples.append(fact)
            else:
                facts_new.append(fact)


            
        if print_facts:
            print(f"--- Facts for agent at time {i} ---")
            for fact in state_list_pos1.get(i, []):
                print(fact)
            print("\n")
    return facts_new, positive_examples


def generate_bk_from_log(path, verbose=False):
    facts = []
    examples = []
    for count, eachpath in enumerate(path):
        state_list_pos_1, key_1 = ground_facts_log_file(eachpath)
        
        facts_new_1, examples_1 = generate_facts_examples(state_list_pos_1, key_1, ex=count+1, print_facts=verbose, skip_prefixes=[])

        facts = facts+facts_new_1
        examples = examples + examples_1
    return facts, examples




def modify_bcrl_1(P1,Col_Reg_Rules, py_function):
    head_literals = []
    P2 ={}
    for i in Col_Reg_Rules:
        head= pygol.Meta(i).head
        if head not in head_literals:
            head_literals.append(head)
    for k,v in P1.items():
        #print("Processing:", k)
        kb_bcrl = pl.KnowledgeBase()
        if py_function:
            for fname, f in py_function.items():
                kb_bcrl.register_py_function(fname, f)
        kb_bcrl.add_clauses(Col_Reg_Rules)
        kb_bcrl.add_clauses(v)

        for j in head_literals:
        
            #print("Querying:", j)

            # Query the knowledge base for the head literal
            results = pl.show_results_1(kb_bcrl.query(j)).sub
            #print("r", results)
            status= pl.show_results_1(kb_bcrl.query(j)).stat
            proof= pl.show_results_1(kb_bcrl.query(j)).proof
            #print("\t",proof)
            
            #v = substitute_rules_with_values(results, proof)
            #print(v)
            if status and results:
                if type(results)==dict:
                    results = [results]
                clause_1=""
                #print(results)
                for eachr in results:
                    #print(eachr)
                    args = []
                    for l in pygol.Clause(j).args():
                        #print(l)
                        
                        if l in eachr.keys():
                            #print(1)
                            #if "Var" in eachr[l]:
                                #print("dany", sub[eachr[l]])
                            if "_" in eachr[l]:
                                val = pygol.Clause(eachr[l]).args()[0]
                                args.append(val.split("_")[0])
                            else:
                                args.append(eachr[l])
                        else:
                            #print(2)
                            args.append(l)
                    #print(len(set(args)), len(args))
                    if len(set(args))==len(args):
                        clause_1 = pygol.generate_clause(pygol.Clause(j).predicate, args)
                    #print("\t",j, clause_1)
                if clause_1:
                    
                    if clause_1 not in P1[k]:
                        P1[k].append(clause_1)
    return P1





def pretty_print_prolog(rule_str):
    head, body = rule_str.split(":-", 1)

    literals = re.split(r',(?![^()]*\))', body.rstrip('.'))

    print(f"{head} :-")
    for i, lit in enumerate(literals):
        lit = lit.strip()
        if i < len(literals) - 1:
            print(f"    {lit},")
        else:
            print(f"    {lit}.")

import janus_swi as janus

def heads_from_mode_declarations(mode_declarations):
    """
    Converts mode declarations into query heads.

    Example:
        modeh(*, applies(+ship,+ship,#rule)).
    becomes:
        applies(X,Y,Rule)
    """

    heads = []

    for m in mode_declarations:
        m = m.strip().rstrip(".")

        if not m.startswith("modeh"):
            continue

        inside = m[m.find("(")+1 : m.rfind(")")]

        # remove recall part before first comma
        _, pred_part = inside.split(",", 1)
        pred_part = pred_part.strip()

        pred = pred_part.split("(")[0]
        args_raw = pred_part[pred_part.find("(")+1 : pred_part.rfind(")")]

        args = []
        var_count = 0

        for a in args_raw.split(","):
            a = a.strip()

            if a.startswith("+") or a.startswith("-"):
                var_count += 1
                args.append(chr(87 + var_count))  # X,Y,Z...

            elif a.startswith("#"):
                const_name = a[1:]
                args.append(const_name.capitalize())

            else:
                var_count += 1
                args.append(chr(87 + var_count))

        head = pygol.generate_clause(pred, args)

        if head not in heads:
            heads.append(head)

    return heads


def _janus_all_solutions(query_literal):
    """
    Query Prolog and return all substitutions as Python dictionaries.
    Example:
        applies(X,Y,rule17a2_standon_may_act)
    returns:
        [{'X': 'a', 'Y': 'b'}, ...]
    """
    q = query_literal.strip().rstrip(".")

    vars_in_query = []
    for v in pygol.Clause(q).args():
        if re.match(r"^[A-Z_]", v):
            vars_in_query.append(v)

    solutions = []

    for sol in janus.query(q):
        one = {}
        for v in vars_in_query:
            if v in sol:
                one[v] = str(sol[v])
        solutions.append(one)

    return solutions

def _clear_dynamic_predicates(clauses):
    """
    Remove predicates loaded for one BCRL example.
    """
    seen = set()

    for c in clauses:
        try:
            head = pygol.Meta(c).head if ":-" in c else c
            pred = pygol.Clause(head).predicate
            arity = len(pygol.Clause(head).args())
            seen.add((pred, arity))
        except Exception:
            pass

    for pred, arity in seen:
        janus.query_once(f"retractall({pred}({','.join(['_'] * arity)}))")

def _consult_clauses_in_janus(clauses):
    """
    Assert Prolog clauses dynamically into SWI-Prolog using Janus.
    """
    for c in clauses:
        c = c.strip()
        if not c:
            continue
        if not c.endswith("."):
            c += "."
        janus.query_once(f"assertz(({c[:-1]}))")

def modify_bcrl_1_janus(P1, Col_Reg_Rules, mode_declarations):
    head_literals = heads_from_mode_declarations(mode_declarations)

    for k, bcrl_literals in P1.items():

        all_loaded_clauses = [
            c for c in (Col_Reg_Rules + bcrl_literals)
            if c is not None and str(c).strip()
        ]

        _consult_clauses_in_janus(all_loaded_clauses)

        for head_query in head_literals:
            results = _janus_all_solutions(head_query)

            if not results:
                continue

            for sub in results:
                args = []

                for arg in pygol.Clause(head_query).args():
                    if arg in sub:
                        val = sub[arg]
                        if "_" in val:
                            val = val.split("_")[0]
                        args.append(val)
                    else:
                        args.append(arg)

                if len(set(args)) != len(args):
                    continue

                grounded_clause = pygol.generate_clause(
                    pygol.Clause(head_query).predicate,
                    args
                )

                if grounded_clause not in P1[k]:
                    P1[k].append(grounded_clause)

        _clear_dynamic_predicates(all_loaded_clauses)

    return P1



def read_modes(file_path, strip_empty=True):
    """
    Read a text file and return a list of lines.

    Parameters
    ----------
    file_path : str
        Path to the text file.
    strip_empty : bool, optional
        If True, remove empty lines and strip whitespace.

    Returns
    -------
    list
        List of lines from the file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        if strip_empty:
            return [line.strip() for line in f if line.strip()]
        else:
            return [line.rstrip("\n") for line in f]
        


def simplify(file_name = "BK.pl", strings =[]):
    #strings = P_inter[pos]
    prefixes = ["range(", "tcpa(", "dcpa("]
    remove_list = ["less_than(", "less_or_equal(", "greater_than(", "greater_or_equal(", "sector(",
                   "port_forward", "port", "forward", "starboard"] 
    result_1 = [s for s in strings if s.startswith(tuple(prefixes))]
    result = add_comparisons_from_bk(
    literals=result_1,
    bk_path=file_name,
    include_original=True,
    )
    result_2 = [
    x for x in strings
    if not any(x.startswith(prefix) for prefix in remove_list+prefixes)
    ]
    # print("---R2")
    # print(result_2)
    # print("---Res")
    # print(result)
    new_strings = result_2 + result

    #print(new_strings)
    return new_strings


def learn_rules(facts, examples, bk_path, print_hs=True, print_h=True, seed_value=42):
    Hypothesis = []
    Hypothesis_space = []
    for i, pos in enumerate(examples):
        #print(pos)
        neg = []
        for j, item in enumerate(examples):
            if i != j:
                neg.append(item)

        P, N = pygol.bottom_clause_generation(file=facts,  
                                        constant_set = K ,  
                                        container = "memory",
                                        positive_example=[pos], 
                                        negative_example=neg,tqdm_disable=True)
        

        P_inter = modify_bcrl_janus_from_bk(
        bk_path=bk_path,
        bottom_clause_dict=P,
        mode_declarations=mode_declarations,
        debug=False
        )
        
        # Included BK
        #print(P_inter)
        # print()
        
        N_inter = modify_bcrl_janus_from_bk(
        bk_path=bk_path,
        bottom_clause_dict=N,
        mode_declarations=mode_declarations,
        debug=False
    )

        P1 = prune_bottom_clauses_from_file(
        bk_file=bk_path,
        bottom_clauses=P_inter,
        verbose=False,  explicit_constraints=  constraints      # set True to see why each literal was removed/kept
        )
        # print("Pruning")
        # print("===============")
        # print(P1)
        # print("===============")



        N1 = prune_bottom_clauses_from_file(
        bk_file=bk_path,
        bottom_clauses=N_inter,
        verbose=False,  explicit_constraints=  constraints      # set True to see why each literal was removed/kept
        )




        # strings = P_inter[pos]
        # prefixes = ["range(", "tcpa(", "dcpa("]
        # remove_list = ["less_than(", "less_or_equal(", "greater_than(", "greater_or_equal("] 
        # result_1 = [s for s in strings if s.startswith(tuple(prefixes))]
        # result = add_comparisons_from_bk(
        # literals=result_1,
        # bk_path="BK.pl",
        # include_original=True,
        # )
        # result_2 = [
        # x for x in strings
        # if not any(x.startswith(prefix) for prefix in remove_list)
        # ]

        
        # print("----", result_1)

        # print("---", result)

        
        #new_list = simplify(file_name="BK.pl", strings=P_inter[pos])
        #print("--new ", new_list)
        
        #print(new_list)

        

        Train_P = {i:simplify(file_name="BK.pl", strings=P_inter[i]) for i,j in P1.items()}
        Train_N = {i:simplify(file_name="BK.pl", strings=N_inter[i]) for i,j in N1.items()}
        #print("pos")
        print(Train_P)
        

        #print("---", Train_N)

        H, HS = pygol.pygol_learn_hypo_space(Train_P, Train_N,  constant_set = K,  max_literals=4,  exact_literals=True, distinct=False, key_size=len(Train_P), min_pos=1, max_neg = 1, verbose=True, seed_value=seed_value)
        
        print("\n" + "=" * 80)
        print(len(HS))
        for i in HS[0:10]:
            print(i)
        print("\n" + "=" * 80)


        if print_hs:
            print("\n" + "=" * 80)
            print(f"HYPOTHESIS SPACE ({len(HS)} hypotheses)")
            print("=" * 80)

            for idx, h in enumerate(HS, start=1):
                print(f"[{idx}]")
                pretty_print_prolog(h)

            print("=" * 80)
        if print_h:
            print("\n" + "=" * 80)
            print("HYPOTHESIS")
            print("=" * 80)
            for i in H:
                pretty_print_prolog(i)
                Hypothesis.append(i)
                Hypothesis_space.append(HS)
            print("\n" + "=" * 80)

        else:
            for i in H:
                Hypothesis.append(i)
                Hypothesis_space.append(HS)
    return Hypothesis, Hypothesis_space



def parse_predicate(s):
    name = s[:s.index("(")]
    args = s[s.index("(")+1:-1].split(",")
    return name, args

def unify_predicates(predicates):
    parsed = [parse_predicate(p) for p in predicates]

    names = [p[0] for p in parsed]
    if len(set(names)) != 1:
        raise ValueError("Predicates have different names")

    args_list = [p[1] for p in parsed]

    if len(set(len(args) for args in args_list)) != 1:
        raise ValueError("Predicates have different arity")

    unified_args = []
    var_count = 1

    for col in zip(*args_list):
        if len(set(col)) == 1:
            unified_args.append(col[0])
        else:
            unified_args.append(f"X{var_count}")
            var_count += 1

    return f"{names[0]}({','.join(unified_args)})"




# def generate_hypo(head,args):
#     start=""
#     for i in args:
#         start=start+i+","
#     body=start[0:-1]
#     clause=head+":-"+body
#     return clause


# def merge_duplicate_body_hypotheses(Hypothesis):
#     """
#     Find hypotheses with identical body clauses and unify their heads.

#     If two or more hypotheses have the same body, this function:
#     1. Collects their heads
#     2. Unifies the heads
#     3. Generates a new hypothesis using the unified head and shared body

#     Parameters
#     ----------
#     Hypothesis : list
#         List of hypothesis clauses.

#     Returns
#     -------
#     merged_rules : list
#         List of newly generated merged hypotheses.
#     """

#     body_clauses = []

#     # Extract body clauses from each hypothesis
#     for hypo in Hypothesis:
#         body = pygol.Meta(hypo).get_body_clauses()
#         body_clauses.append(body)

#     # Store positions of hypotheses with the same body
#     positions = {}

#     for index, body in enumerate(body_clauses):
#         # Sorting makes comparison independent of literal order
#         key = tuple(sorted(body))
#         positions.setdefault(key, []).append(index)

#     # Keep only bodies that appear more than once
#     duplicates = {
#         body_key: indices
#         for body_key, indices in positions.items()
#         if len(indices) > 1
#     }

#     merged_rules = []

#     # Process each group of duplicate bodies
#     for body_key, indices in duplicates.items():

#         heads_to_unify = []

#         # Use the body from any one hypothesis in the duplicate group
#         reference_index = indices[0]
#         shared_body = pygol.Meta(Hypothesis[reference_index]).get_body_clauses()

#         # Collect heads from all hypotheses with the same body
#         for index in indices:
#             head = pygol.Meta(Hypothesis[index]).head
#             heads_to_unify.append(head)

#         # Unify heads into a single generalised head
#         unified_head = unify_predicates(heads_to_unify)

#         # Generate new hypothesis using unified head and shared body
#         merged_rule = generate_hypo(unified_head, shared_body)

#         merged_rules.append(merged_rule)

#     return merged_rules



def write_prolog_file(prolog_list, filename):
    """
    Write a list of Prolog facts/rules to a file.

    Parameters
    ----------
    prolog_list : list
        List of Prolog facts/rules.
    filename : str
        Output .pl filename.
    """

    with open(filename, "w") as f:
        for clause in prolog_list:
            clause = str(clause).strip()

            # Ensure each clause ends with '.'
            if not clause.endswith("."):
                clause += "."

            f.write(clause + "\n")


def merge_prolog_files(file1, file2, output_file):
    """
    Merge two Prolog files into one.
    """

    with open(output_file, "w") as out:

        with open(file1, "r") as f1:
            out.write(f1.read())

        out.write("\n\n")

        with open(file2, "r") as f2:
            out.write(f2.read())


import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import janus_swi as janus


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

# Source predicate -> variable used for its ordered third argument
ORDERED_PREDICATES = {
    "range": "R",
    "dcpa": "D",
    "tcpa": "T",
}

COMPARISON_PREDICATES = [
    "less_than",
    "less_or_equal",
    "greater_than",
    "greater_or_equal",
]


# ---------------------------------------------------------------------
# BK loading
# ---------------------------------------------------------------------

def consult_bk(bk_path: str) -> None:
    """
    Consult the Prolog background-knowledge file.
    """

    path = Path(bk_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"BK file not found: {path}")

    prolog_path = (
        str(path)
        .replace("\\", "/")
        .replace("'", "\\'")
    )

    janus.query_once(f"consult('{prolog_path}')")


# ---------------------------------------------------------------------
# Prolog literal parsing
# ---------------------------------------------------------------------

def parse_prolog_literal(
    literal: str,
) -> Tuple[Optional[str], List[str]]:
    """
    Parse a simple Prolog literal.

    Example
    -------
    range(A,B,far)

    Returns
    -------
    ("range", ["A", "B", "far"])
    """

    literal = literal.strip().rstrip(".")

    match = re.fullmatch(
        r"([a-zA-Z_]\w*)\((.*)\)",
        literal,
    )

    if not match:
        return None, []

    predicate = match.group(1)

    arguments = [
        argument.strip()
        for argument in match.group(2).split(",")
    ]

    return predicate, arguments


def make_prolog_literal(
    predicate: str,
    arguments: List[str],
) -> str:
    """
    Construct a Prolog literal from a predicate and argument list.
    """

    return f"{predicate}({','.join(arguments)})"


# ---------------------------------------------------------------------
# Read ordering from BK
# ---------------------------------------------------------------------

def get_adjacency_edges() -> List[Tuple[str, str]]:
    """
    Read all less_and_adjacent(Smaller,Larger) relations from the BK.

    Example:
        less_and_adjacent(very_near,near)

    means:
        very_near < near
    """

    edges = []

    for solution in janus.query(
        "less_and_adjacent(Smaller,Larger)"
    ):
        smaller = str(solution["Smaller"])
        larger = str(solution["Larger"])

        edge = (smaller, larger)

        if edge not in edges:
            edges.append(edge)

    return edges


def find_connected_component(
    source_value: str,
    edges: List[Tuple[str, str]],
) -> Set[str]:
    """
    Find the ordered scale containing source_value.

    This prevents range, DCPA, and TCPA values from being mixed.
    """

    graph: Dict[str, Set[str]] = {}

    for smaller, larger in edges:
        graph.setdefault(smaller, set()).add(larger)
        graph.setdefault(larger, set()).add(smaller)

    if source_value not in graph:
        return {source_value}

    component: Set[str] = set()
    stack = [source_value]

    while stack:
        current = stack.pop()

        if current in component:
            continue

        component.add(current)

        for neighbour in graph.get(current, set()):
            if neighbour not in component:
                stack.append(neighbour)

    return component


def build_ordered_scale(
    source_value: str,
    edges: List[Tuple[str, str]],
) -> List[str]:
    """
    Build the complete ordered scale from smallest to largest.

    Examples
    --------
    range:
        very_near < near < middle < far < very_far

    dcpa:
        critical < very_close < close < marginal < safe

    tcpa:
        immediate < short < medium < long < very_long
    """

    component = find_connected_component(
        source_value=source_value,
        edges=edges,
    )

    next_value: Dict[str, str] = {}

    incoming_count: Dict[str, int] = {
        value: 0
        for value in component
    }

    for smaller, larger in edges:
        if smaller in component and larger in component:
            next_value[smaller] = larger
            incoming_count[larger] += 1

    starts = [
        value
        for value in component
        if incoming_count[value] == 0
    ]

    if not starts:
        return []

    current = starts[0]
    ordered_scale = []

    while current not in ordered_scale:
        ordered_scale.append(current)

        if current not in next_value:
            break

        current = next_value[current]

    return ordered_scale


# ---------------------------------------------------------------------
# Generalise original source literals
# ---------------------------------------------------------------------

def generalise_source_literal(
    literal: str,
) -> str:
    """
    Replace the concrete third argument with its corresponding variable.

    Examples
    --------
    range(A,B,far)
        -> range(A,B,R)

    dcpa(A,B,very_close)
        -> dcpa(A,B,D)

    tcpa(A,B,medium)
        -> tcpa(A,B,T)
    """

    predicate, arguments = parse_prolog_literal(literal)

    if predicate not in ORDERED_PREDICATES:
        return literal.strip().rstrip(".")

    if len(arguments) != 3:
        return literal.strip().rstrip(".")

    arguments[2] = ORDERED_PREDICATES[predicate]

    return make_prolog_literal(
        predicate=predicate,
        arguments=arguments,
    )


def generalise_source_literals(
    literals: List[str],
) -> List[str]:
    """
    Generalise every supported source literal.
    """

    output = []

    for literal in literals:
        generalised = generalise_source_literal(literal)

        if generalised not in output:
            output.append(generalised)

    return output


# ---------------------------------------------------------------------
# Generate comparison literals
# ---------------------------------------------------------------------

def generate_less_than_literals(
    source_value: str,
    variable: str,
    ordered_scale: List[str],
) -> List[str]:
    """
    Generate strict less_than literals.

    For source_value='far' and variable='R':

        less_than(very_near,R)
        less_than(near,R)
        less_than(middle,R)
        less_than(R,very_far)
    """

    if source_value not in ordered_scale:
        return []

    index = ordered_scale.index(source_value)

    smaller_values = ordered_scale[:index]
    larger_values = ordered_scale[index + 1:]

    output = []

    for smaller in smaller_values:
        output.append(
            f"less_than({smaller},{variable})"
        )

    for larger in larger_values:
        output.append(
            f"less_than({variable},{larger})"
        )

    return output


def generate_less_or_equal_literals(
    source_value: str,
    variable: str,
    ordered_scale: List[str],
) -> List[str]:
    """
    Generate less_or_equal literals following the orientation
    used in your current BK.

    For source_value='far' and variable='R':

        less_or_equal(R,middle)
        less_or_equal(R,near)
        less_or_equal(R,very_near)
        less_or_equal(very_far,R)
    """

    if source_value not in ordered_scale:
        return []

    index = ordered_scale.index(source_value)

    smaller_values = ordered_scale[:index]
    larger_values = ordered_scale[index + 1:]

    output = []

    # Observed value is on the left
    for smaller in reversed(smaller_values):
        output.append(
            f"less_or_equal({variable},{smaller})"
        )

    # Observed value is on the right
    for larger in larger_values:
        output.append(
            f"less_or_equal({larger},{variable})"
        )

    return output


def generate_greater_than_literals(
    source_value: str,
    variable: str,
    ordered_scale: List[str],
) -> List[str]:
    """
    Generate strict greater_than literals.

    For source_value='far' and variable='R':

        greater_than(R,middle)
        greater_than(R,near)
        greater_than(R,very_near)
        greater_than(very_far,R)
    """

    if source_value not in ordered_scale:
        return []

    index = ordered_scale.index(source_value)

    smaller_values = ordered_scale[:index]
    larger_values = ordered_scale[index + 1:]

    output = []

    for smaller in reversed(smaller_values):
        output.append(
            f"greater_than({variable},{smaller})"
        )

    for larger in larger_values:
        output.append(
            f"greater_than({larger},{variable})"
        )

    return output


def generate_greater_or_equal_literals(
    source_value: str,
    variable: str,
    ordered_scale: List[str],
) -> List[str]:
    """
    Generate greater_or_equal literals.

    For source_value='far' and variable='R':

        greater_or_equal(R,middle)
        greater_or_equal(R,near)
        greater_or_equal(R,very_near)
        greater_or_equal(very_far,R)
    """

    if source_value not in ordered_scale:
        return []

    index = ordered_scale.index(source_value)

    smaller_values = ordered_scale[:index]
    larger_values = ordered_scale[index + 1:]

    output = []

    for smaller in reversed(smaller_values):
        output.append(
            f"greater_or_equal({variable},{smaller})"
        )

    for larger in larger_values:
        output.append(
            f"greater_or_equal({larger},{variable})"
        )

    return output


def generate_comparisons_for_value(
    source_value: str,
    variable: str,
    edges: List[Tuple[str, str]],
) -> List[str]:
    """
    Generate all comparison literals for one source value.
    """

    ordered_scale = build_ordered_scale(
        source_value=source_value,
        edges=edges,
    )

    if not ordered_scale:
        print(
            f"No ordered scale found for value: "
            f"{source_value}"
        )
        return []

    output = []

    groups = [
        generate_less_than_literals(
            source_value=source_value,
            variable=variable,
            ordered_scale=ordered_scale,
        ),
        generate_less_or_equal_literals(
            source_value=source_value,
            variable=variable,
            ordered_scale=ordered_scale,
        ),
        generate_greater_than_literals(
            source_value=source_value,
            variable=variable,
            ordered_scale=ordered_scale,
        ),
        generate_greater_or_equal_literals(
            source_value=source_value,
            variable=variable,
            ordered_scale=ordered_scale,
        ),
    ]

    for group in groups:
        for literal in group:
            if literal not in output:
                output.append(literal)

    return output


# ---------------------------------------------------------------------
# Main function
# ---------------------------------------------------------------------

def add_comparisons_from_bk(
    literals: List[str],
    bk_path: str,
    include_original: bool = True,
) -> List[str]:
    """
    Consult the BK, generalise range/dcpa/tcpa literals, and generate
    complete comparison literals.

    Input example
    -------------
    [
        "range(A,B,far)",
        "dcpa(A,B,very_close)",
        "tcpa(A,B,medium)"
    ]

    Output starts with
    ------------------
    [
        "range(A,B,R)",
        "dcpa(A,B,D)",
        "tcpa(A,B,T)",
        ...
    ]
    """

    consult_bk(bk_path)

    edges = get_adjacency_edges()

    if include_original:
        output = generalise_source_literals(literals)
    else:
        output = []

    for literal in literals:
        source_predicate, arguments = parse_prolog_literal(
            literal
        )

        if source_predicate not in ORDERED_PREDICATES:
            continue

        if len(arguments) != 3:
            continue

        source_value = arguments[2]
        variable = ORDERED_PREDICATES[source_predicate]

        generated_literals = generate_comparisons_for_value(
            source_value=source_value,
            variable=variable,
            edges=edges,
        )

        for generated_literal in generated_literals:
            if generated_literal not in output:
                output.append(generated_literal)

    return output


# ---------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------

#if __name__ == "__main__":

    # input_literals = [
    #     "range(A,B,far)",
    #     "dcpa(A,B,very_close)",
    #     "tcpa(A,B,medium)",
    # ]

    # result = add_comparisons_from_bk(
    #     literals=input_literals,
    #     bk_path="BK.pl",
    #     include_original=True,
    # )

    # print("\nGenerated literals")
    # print("=" * 80)

    # for literal in result:
    #     print(literal)

    # print("=" * 80)
    # print(f"Total literals: {len(result)}")