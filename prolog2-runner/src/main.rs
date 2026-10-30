mod conditions;
mod generate_prolog;
mod situation;
use std::fs::File;
use std::io::Write;

use prolog2::{Config, app::App};
use situation::Situation;

use crate::generate_prolog::generate_prolog;

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
    generate_prolog(situations);
    let mut log_file = File::create("prolog2.log").unwrap();
    learn_take_action(&mut log_file);
    learn_waypoint(&mut log_file);
}

fn learn_take_action(log_file: &mut File) {
    log_heading("Learn take_action", true, log_file);

    let mut app = App::from_setup_json(format!("setup/take_action.json"))
        .unwrap()
        .config(Config {
            max_depth: 5,
            max_clause: 4,
            debug: false,
            protect_h_preds: true,
        })
        // .top_prog(TopProg::True(true))
        .add_body_predicates(BODY_PREDICATES)
        .unwrap();
    if let Some(hypotheses) = app.run_parallel() {
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

fn learn_waypoint(log_file: &mut File) {
    let mut hypothesis = String::new();
    for target in ["turn", "cpa_side", "avoid", "resume"] {
        // for target in ["cpa_side"] {
        log_heading(&format!("Learn {target}"), true, log_file);
        let mut app = App::from_setup_json(format!("setup/{target}.json"))
            .unwrap()
            .config(Config {
                max_depth: 5,
                max_clause: 3,
                debug: false,
                protect_h_preds: true,
            })
            // .top_prog(TopProg::True(true))
            .add_body_predicates(BODY_PREDICATES)
            .unwrap();

        if let Some(hypotheses) = app.run_parallel() {
            hypothesis += &hypotheses[0];

            for (i, h) in hypotheses.iter().enumerate() {
                log_heading(&format!("Hypothesis {i}"), false, log_file);
                log(h, log_file);
            }
        } else {
            log("No valid Hypothesis", log_file);
        }
    }

    log_heading("Final Hypothesis", true, log_file);
    log(&hypothesis, log_file);
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
