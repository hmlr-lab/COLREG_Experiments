mod conditions;
mod generate_prolog;
mod situation;
use prolog2::{Config, app::App};
use situation::Situation;

use crate::generate_prolog::generate_prolog;

fn main() {
    let situations = Situation::load_situations();
    generate_prolog(situations);

    iterate_max_clause_pred("setup.json", 2, 4);
}

fn iterate_max_clause_pred(setup_path: &str, max_max_pred: usize, max_max_clause: usize) {
    for max_clause in 0..max_max_clause {
        for max_pred in 0..max_max_pred {
            println!("=================================");
            println!("Try max_clause: {max_clause}, max_pred: {max_pred}");
            let app = App::from_setup_json(setup_path).unwrap().config(Config {
                max_depth: 20,
                max_clause,
                max_pred,
                debug: false,
            });
            app.run();
            println!("=================================");
            println!("");
        }
    }
}
