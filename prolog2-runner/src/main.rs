mod conditions;
mod examples;
mod generate_prolog;
mod situation;
use std::fs::File;
use std::io::Write;

use prolog2::{Config, Examples, app::App};
use situation::Situation;

use crate::{examples::gen_examples, generate_prolog::generate_prolog};

/// Largest max_clause the learner will try
const MAX_CLAUSE: usize = 3;

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
    let mut log_file = File::create("prolog2.log").unwrap();
    let mut final_h = String::new();
    learn_take_action(&mut final_h, &mut log_file);
    learn_waypoint(&situations, &mut final_h, &mut log_file);

    log_heading("Final Hypothesis", true, &mut log_file);
    log(&final_h, &mut log_file);
}

fn learn_take_action(final_h: &mut String, log_file: &mut File) {
    log_heading("Learn take_action", true, log_file);

    let mut app = App::from_setup_json(format!("setup/take_action.json"))
        .unwrap()
        .config(Config {
            max_depth: 7,
            max_clause: MAX_CLAUSE,
            debug: false,
            protect_h_preds: true,
        })
        // .top_prog(TopProg::True(true))
        .add_body_predicates(BODY_PREDICATES)
        .unwrap();
    if let Some(hypotheses) = app.run_parallel() {
        *final_h += &hypotheses[0];
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

fn learn_waypoint(situations: &[Situation], final_h: &mut String, log_file: &mut File) {
    for pred in ["turn", "cpa_side", "avoid", "resume"] {
        // for pred in ["cpa_side"] {
        let examples = gen_examples(situations, pred);
        log_heading(&format!("Learn {pred}"), true, log_file);

        // Try with all negatives first, starting from small clause counts
        let mut hypotheses = run_learner(pred, examples.clone(), 2);

        // Otherwise build up the negatives one at a time, keeping each one only if a
        // hypothesis can still be found with it, filtering out the bad negatives
        if hypotheses.is_none() {
            log(
                "No valid Hypothesis with all negatives, building negative set incrementally",
                log_file,
            );
            let mut reduced = examples.clone();
            reduced.neg.clear();
            hypotheses = run_learner(pred, reduced.clone(), MAX_CLAUSE);

            if hypotheses.is_some() {
                let mut filtered = Vec::new();
                for neg in examples.neg.iter() {
                    reduced.neg.push(neg.clone());
                    match run_learner(pred, reduced.clone(), MAX_CLAUSE) {
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
                *final_h += &hypotheses[0];
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
fn run_learner(pred: &str, examples: Examples, min_clause: usize) -> Option<Vec<String>> {
    (min_clause..=MAX_CLAUSE).find_map(|max_clause| {
        App::from_setup_json(format!("setup/{pred}.json"))
            .unwrap()
            .config(Config {
                max_depth: 7,
                max_clause,
                debug: false,
                protect_h_preds: true,
            })
            // .top_prog(TopProg::True(true))
            .add_body_predicates(BODY_PREDICATES)
            .unwrap()
            .examples(examples.clone())
            .run_parallel()
    })
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
