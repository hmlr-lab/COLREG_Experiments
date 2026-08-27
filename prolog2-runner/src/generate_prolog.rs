use std::{
    fs::{File, create_dir_all, read_to_string},
    io::Write,
};

use crate::situation::Situation;

const BK_PATH: &str = "../prolog/BK.pl";
const GENERATED_DIR: &str = "../prolog/generated/";

pub fn generate_prolog(situations: Vec<Situation>) {
    create_dir_all(format!("{GENERATED_DIR}pos")).unwrap();
    create_dir_all(format!("{GENERATED_DIR}neg")).unwrap();
    combine_bk(&situations);
    gen_take_action(&situations);
    gen_waypoint_examples(&situations);
}

/// Take BK file and combine with facts from situations
/// Write output to GENERATED_DIR + "bk.pl"
fn combine_bk(situations: &Vec<Situation>) {
    //Load BK.pl file and remove directives
    let mut bk: String = read_to_string(BK_PATH)
        .unwrap()
        .lines()
        .filter(|line| line.find(":-") != Some(0))
        .map(|line| [line, "\n"].concat())
        .collect();
    // Add situation facts to bk
    for sit in situations {
        for fact in &sit.facts {
            bk += fact;
            bk += ".\n";
        }
    }
    let mut file = File::create([GENERATED_DIR, "bk.pl"].concat()).unwrap();
    file.write_all(&bk.into_bytes()).unwrap();
}

/// Generate positve and negative example files for take action predicate
/// Write ouput to GENERATED_DIR + "pos/take_action.pl" or "neg/take_action.pl"
fn gen_take_action(situations: &Vec<Situation>) {
    let mut pos = String::new();
    let mut neg = String::new();

    for sit in situations {
        if sit.take_action {
            pos += &format!("take_action(agent{}).\n", sit.id);
        } else {
            neg += &format!("take_action(agent{}).\n", sit.id);
        }
    }

    let mut file = File::create([GENERATED_DIR, "pos/", "take_action.pl"].concat()).unwrap();
    file.write_all(&pos.into_bytes()).unwrap();

    let mut file = File::create([GENERATED_DIR, "neg/", "take_action.pl"].concat()).unwrap();
    file.write_all(&neg.into_bytes()).unwrap();
}

/// Generate examples for each target predicate of waypoint examples
/// Write output to GENERATED_DIR + "pos" + "{target predicate}" or,
/// GENERATED_DIR + "neg" + "{target predicate}.pl"
fn gen_waypoint_examples(situations: &Vec<Situation>) {
    for pred in ["turn", "side", "avoid", "resume"] {
        let mut pos = String::new();
        let mut neg = String::new();

        for sit in situations {
            for cond in &sit.pos_conds {
                if cond.is_pred(pred) {
                    pos += &cond.to_string(sit.id);
                    pos += "\n";
                }
            }
            for cond in &sit.neg_conds {
                if cond.is_pred(pred) {
                    neg += &cond.to_string(sit.id);
                    neg += "\n";
                }
            }
        }

        let mut file = File::create([GENERATED_DIR, "pos/", pred, ".pl"].concat()).unwrap();
        file.write_all(&pos.into_bytes()).unwrap();
        let mut file = File::create([GENERATED_DIR, "neg/", pred, ".pl"].concat()).unwrap();
        file.write_all(&neg.into_bytes()).unwrap();
    }
}
