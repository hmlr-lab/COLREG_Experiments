mod conditions;
mod generate_prolog;
mod situation;
use prolog2::{Config, app::App};
use situation::Situation;

use crate::generate_prolog::generate_prolog;

fn main() {
    let situations = Situation::load_situations();
    generate_prolog(situations);

    // iterate_max_clause_pred("setup_avoid.json", 2, 4);

    // let mut app = App::from_setup_json("setup_side.json")
    //     .unwrap()
    //     .config(Config {
    //         max_depth: 5,
    //         max_clause: 3,
    //         max_pred: 1,
    //         debug: false,
    //     });
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

    for target in ["turn", "side", "avoid", "resume"] {

        println!("====================================");
        println!("========= Learn {target} ===========");
        println!("====================================");
        let mut app = App::from_setup_json(format!("setup_{target}.json"))
            .unwrap()
            .config(Config {
                max_depth: 5,
                max_clause: 3,
                max_pred: 1,
                debug: false,
        });
        
        // match  app.query_session_from_examples().unwrap().next(){
        //     Some(solution) => hypothesis += &solution.hypothesis,
        //     None => println!("No solution for {target}")
        // }
        let h = app.run_top_prog();
        hypothesis += &h;
    }

    println!("====================================");
    println!("======== Final Hypothesis ==========");
    println!("====================================");
    println!("{hypothesis}");
}
