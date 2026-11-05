mod conditions;
mod examples;
mod generate_prolog;
mod inline;
mod situation;
use chrono::Utc;
use std::collections::HashSet;
use std::fs::File;
use std::io::Write;

use prolog2::{Config, Examples, ParallelConfig, app::App, heap::SymbolDB};
use situation::Situation;

use crate::{examples::gen_examples, generate_prolog::generate_prolog};

/// Largest max_clause the learner will try
const MAX_CLAUSE: usize = 4;

const BODY_PREDICATES: &[&str] = &[
    "sector/3",
    "rule2_extremis/2",
    "duty/3",
    "encounter_and_conduct/4",
    "mutual_ahead/2",
    "encounter/3",
    "close_quarters/2",
    "close_quarters_developing/2",
    "collision_risk/2",
    "ample_time/2",
    "actionable_range/2",
    "tcpa_closing/2",
    "dcpa_unacceptable/2",
    "dcpa_acceptable/2",
    "port_forward/2",
    "port_aft/2",
    "starboard_forward/2",
    "starboard_aft/2",
    "port_aft/2",
    "port/2",
    "starboard/2",
    "forward/2",
    "aft/2",
    "range_gt/3",
    "range_lt/3",
    "range_ge/3",
    "range_le/3",
    "tcpa_gt/3",
    "tcpa_lt/3",
    "tcpa_ge/3",
    "tcpa_le/3",
    "dcpa_gt/3",
    "dcpa_lt/3",
    "dcpa_ge/3",
    "dcpa_le/3",
];

fn main() {
    let situations = Situation::load_situations();
    generate_prolog(&situations);
    let mut log_file = File::create(format!("prolog2{}.log", Utc::now().to_string())).unwrap();
    let mut final_h = String::new();
    // Predicates defined in final_h, e.g. "turn/2" or "turn_0/1", usable as body predicates
    let mut learnt_preds = HashSet::new();
    learn_take_action(&mut final_h, &mut learnt_preds, &mut log_file);
    learn_waypoint(&situations, &mut final_h, &mut learnt_preds, &mut log_file);
    let final_h = inline::inline_invented(&final_h);

    log_heading("Final Hypothesis", true, &mut log_file);
    log(&final_h, &mut log_file);
}

fn learn_take_action(
    final_h: &mut String,
    learnt_preds: &mut HashSet<String>,
    log_file: &mut File,
) {
    log_heading("Learn take_action", true, log_file);

    let mut app = build_app("take_action", MAX_CLAUSE, final_h, learnt_preds);
    if let Some(hypotheses) = app.run_parallel() {
        add_hypothesis(&hypotheses[0], "take_action", final_h, learnt_preds);
        for (i, h) in hypotheses.iter().enumerate() {
            writeln!(
                log_file,
                "================= Hypothesis {i} ================="
            )
            .unwrap();
            writeln!(log_file, "{h}").unwrap();
        }
    }
}

fn learn_waypoint(
    situations: &[Situation],
    final_h: &mut String,
    learnt_preds: &mut HashSet<String>,
    log_file: &mut File,
) {
    for pred in ["turn", "cpa_side", "avoid", "resume"] {
        // for pred in ["cpa_side"] {
        let examples = gen_examples(situations, pred);
        log_heading(&format!("Learn {pred}"), true, log_file);

        // Try with all negatives first, starting from small clause counts
        let mut hypotheses = run_learner(pred, examples.clone(), 2, final_h, learnt_preds);

        // Otherwise build up the negatives one at a time, keeping each one only if a
        // hypothesis can still be found with it, filtering out the bad negatives
        if hypotheses.is_none() {
            log(
                "No valid Hypothesis with all negatives, building negative set incrementally",
                log_file,
            );
            let mut reduced = examples.clone();
            reduced.neg.clear();
            hypotheses = run_learner(pred, reduced.clone(), MAX_CLAUSE, final_h, learnt_preds);

            if hypotheses.is_some() {
                let mut filtered = Vec::new();
                for neg in examples.neg.iter() {
                    reduced.neg.push(neg.clone());
                    match run_learner(pred, reduced.clone(), MAX_CLAUSE, final_h, learnt_preds) {
                        Some(h) => {
                            log(&format!("Kept negative {neg}"), log_file);
                            hypotheses = Some(h);
                        }
                        None => {
                            log(&format!("Filtered negative {neg}"), log_file);
                            filtered.push(reduced.neg.pop().unwrap());
                        }
                    }
                }
                log(
                    &format!(
                        "Kept {} of {} negatives, filtered {filtered:?}",
                        reduced.neg.len(),
                        examples.neg.len()
                    ),
                    log_file,
                );
            }
        }

        match hypotheses {
            Some(hypotheses) => {
                add_hypothesis(&hypotheses[0], pred, final_h, learnt_preds);
                for (i, h) in hypotheses.iter().enumerate() {
                    log_heading(&format!("Hypothesis {i}"), false, log_file);
                    log(h, log_file);
                }
            }
            None => log(
                "No valid Hypothesis Found, even with no negatives",
                log_file,
            ),
        }
    }
}

/// Run the learner with max_clause from `min_clause` up to MAX_CLAUSE, returning the
/// first hypotheses found
fn run_learner(
    pred: &str,
    examples: Examples,
    min_clause: usize,
    final_h: &str,
    learnt_preds: &HashSet<String>,
) -> Option<Vec<String>> {
    (min_clause..=MAX_CLAUSE).find_map(|max_clause| {
        build_app(pred, max_clause, final_h, learnt_preds)
            .examples(examples.clone())
            .run_parallel()
    })
}

/// Build an app for `pred` with the previously learnt hypothesis loaded and its
/// predicates available as body predicates
fn build_app(pred: &str, max_clause: usize, final_h: &str, learnt_preds: &HashSet<String>) -> App {
    let mut app = App::from_setup_json(format!("setup/{pred}.json"))
        .unwrap()
        .config(Config {
            max_depth: 7,
            max_clause,
            debug: false,
            protect_h_preds: true,
        })
        .parallel(ParallelConfig {
            reduce: true,
            sort_by_literals: true,
            final_h_count: 5,
        });
    if !final_h.is_empty() {
        app = app.load_code(final_h).unwrap();
    }
    app.add_body_predicates(BODY_PREDICATES)
        .unwrap()
        .add_body_predicates(learnt_preds)
        .unwrap()
}

/// Rename invented predicates in `h` from pred_n to {pred}_n, append it to `final_h`
/// and record every predicate it defines in `learnt_preds`
fn add_hypothesis(h: &str, pred: &str, final_h: &mut String, learnt_preds: &mut HashSet<String>) {
    let h = rename_invented(h, pred);
    for clause in h.lines().map(str::trim).filter(|c| !c.is_empty()) {
        let head = clause.split(":-").next().unwrap().trim_end_matches('.');
        learnt_preds.insert(pred_indicator(head));
    }
    *final_h += &h;
    if !final_h.ends_with('\n') {
        final_h.push('\n');
    }
}

/// Replace invented predicate names pred_n with {pred}_n, leaving any identifier that
/// merely contains "pred_" untouched
fn rename_invented(h: &str, pred: &str) -> String {
    let mut out = String::with_capacity(h.len());
    let mut rest = h;
    while let Some(i) = rest.find("pred_") {
        let at_boundary = !rest[..i]
            .chars()
            .next_back()
            .is_some_and(|c| c.is_alphanumeric() || c == '_');
        out += &rest[..i];
        out += if at_boundary { pred } else { "pred" };
        out.push('_');
        rest = &rest[i + "pred_".len()..];
    }
    out += rest;
    out
}

/// Convert a clause head such as "turn(Arg_0,Arg_1)" into "turn/2"
fn pred_indicator(head: &str) -> String {
    let head = head.trim();
    let Some(open) = head.find('(') else {
        return format!("{head}/0");
    };
    let args = &head[open + 1..head.rfind(')').unwrap_or(head.len())];
    let mut depth = 0;
    let mut arity = 1;
    for c in args.chars() {
        match c {
            '(' | '[' => depth += 1,
            ')' | ']' => depth -= 1,
            ',' if depth == 0 => arity += 1,
            _ => {}
        }
    }
    format!("{}/{arity}", &head[..open])
}

fn log_heading(heading: &str, bold: bool, log_file: &mut File) {
    fn line(bold: bool, log_file: &mut File) {
        if bold {
            writeln!(log_file, "{:=<40}", "").unwrap();
            println!("{:=<40}", "");
        }
    }

    line(bold, log_file);
    writeln!(log_file, "========= {heading:^20} =========").unwrap();
    println!("========= {heading:^20} =========");
    line(bold, log_file);
}

fn log(text: &str, log_file: &mut File) {
    println!("{text}");
    writeln!(log_file, "{text}").unwrap();
}
