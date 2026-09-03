mod conditions;
mod generate_prolog;
mod situation;
use std::fs::File;
use std::io::Write;

use prolog2::{Config, app::{App, TopProg}};
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
        "dcpa_le/3"
];


fn main() {
    let situations = Situation::load_situations();
    generate_prolog(situations);

    // iterate_max_clause_pred("setup_avoid.json", 2, 4);

    let mut app = App::from_setup_json("setup_side.json")
        .unwrap()
        .config(Config {
            max_depth: 5,
            max_clause: 3,
            max_pred: 1,
            debug: false,
    });
    // app.run();

    learn_waypoint();
}

fn iterate_max_clause_pred(setup_path: &str, mut max_max_pred: usize, mut max_max_clause: usize) {
    max_max_pred += 1;
    max_max_clause += 1;
    for max_clause in 1..max_max_clause {
        for max_pred in 1..max_max_pred {
            println!("=================================");
            println!("Try max_clause: {max_clause}, max_pred: {max_pred}");
            println!("=================================");
            let app = App::from_setup_json(setup_path).unwrap().config(Config {
                max_depth: 5,
                max_clause,
                max_pred,
                debug: false,
            });
            app.run();
        }
    }
}

fn learn_waypoint() {
    let mut hypothesis = String::new();
    let mut log_file = File::create("learning_waypoint_log").unwrap();
    for target in ["turn", "side", "avoid", "resume"] {

        println!("====================================");
        println!("========= Learn {target} ===========");
        println!("====================================");
        let mut app = App::from_setup_json(format!("setup_{target}.json"))
            .unwrap()
            .config(Config {
                max_depth: 5,
                max_clause: 4,
                max_pred: 2,
                debug: false,
        })
        .top_prog(TopProg::True(true))
        .add_body_predicates(BODY_PREDICATES).unwrap();
        // match  app.query_session_from_examples().unwrap().next(){
        //     Some(solution) => {
        //         writeln!(log_file, "====================================").unwrap();
        //         writeln!(log_file, "========= Learn {target} ===========").unwrap();
        //         writeln!(log_file, "====================================").unwrap();
        //         writeln!(log_file, "{}", &solution.hypothesis).unwrap();
        //         hypothesis += &solution.hypothesis
        //     },
        //     None => println!("No solution for {target}")
        // }

        // let h = app.run_top_prog();
        // writeln!(log_file, "====================================").unwrap();
        // writeln!(log_file, "========= Learn {target} ===========").unwrap();
        // writeln!(log_file, "====================================").unwrap();
        // writeln!(log_file, "{h}").unwrap();
        // hypothesis += &h;
    }

    println!("====================================");
    println!("======== Final Hypothesis ==========");
    println!("====================================");
    println!("{hypothesis}");
}
