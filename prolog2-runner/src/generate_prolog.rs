use std::{
    io::Write, fs::{File, read_dir, read_to_string},
};

use crate::example::Example;

const GENERATED_DIR: &str = "../prolog/generated/";
const EXAMPLE_DIR: &str = "../examples/";
const BK_PATH: &str = "../prolog/BK.pl";
const DELIMINATORS: [char; 4] = [',', '(', ')', '.'];
const PREDICATES: [&'static str; 5] = ["sector", "range", "dcpa", "tcpa", "waypoint"];

pub fn generate_prolog() {
    let (pos_examples, neg_examples) = get_examples();
    let mut bk: String = read_to_string(BK_PATH)
        .unwrap()
        .lines()
        .filter(|line| line.find(":-") != Some(0))
        .map(|line| [line, "\n"].concat())
        .collect();
    let mut pos_ex_file = String::new();
    let mut neg_ex_file = String::new();

    for ex in pos_examples.iter() {
        ex.write_bk(&mut bk);
        pos_ex_file += &ex.waypoint;
        pos_ex_file += ".\n";
    }
    for ex in neg_examples.iter() {
        ex.write_bk(&mut bk);
        neg_ex_file += &ex.waypoint;
        neg_ex_file += ".\n";
    }

    let mut file = File::create([GENERATED_DIR,"pos.pl"].concat()).unwrap();
    file.write_all(&pos_ex_file.into_bytes()).unwrap();

    let mut file = File::create([GENERATED_DIR,"neg.pl"].concat()).unwrap();
    file.write_all(&neg_ex_file.into_bytes()).unwrap();

    let mut file = File::create([GENERATED_DIR,"bk.pl"].concat()).unwrap();
    file.write_all(&bk.into_bytes()).unwrap();
}

fn get_examples() -> (Vec<Example>, Vec<Example>) {
    let pos_examples: Vec<Example> = list_log_files(&(EXAMPLE_DIR.to_string() + "positives/"))
        .unwrap()
        .into_iter()
        .map(|example_path| path_to_example(example_path))
        .collect();
    let neg_examples: Vec<Example> = list_log_files(&(EXAMPLE_DIR.to_string() + "negatives/"))
        .unwrap()
        .into_iter()
        .map(|example_path| path_to_example(example_path))
        .collect();
    (pos_examples, neg_examples)
}

fn list_log_files(dir: &str) -> std::io::Result<Vec<String>> {
    let mut files = Vec::new();
    let entries = read_dir(dir)?;

    for entry in entries {
        let entry = entry?;
        let path = entry.path();

        if path.extension().map_or(false, |ext| ext == "txt") {
            files.push(path.display().to_string());
        }
    }
    Ok(files)
}

fn path_to_example(path: String) -> Example {
    let mut example = Example::new();
    let file = read_to_string(path).unwrap();
    for literal in tokens_to_literals(tokenise(file)) {
        example.push_literal(literal);
    }
    example
}

fn tokenise(file: String) -> Vec<String> {
    let mut tokens = Vec::new();
    let mut li = 0;
    let mut hi = 0;
    let mut next_token = String::new();
    for ch in file.chars() {
        if DELIMINATORS.contains(&ch) {
            tokens.push(next_token.clone());
            tokens.push(ch.to_string());
            next_token.clear();
            continue;
        }
        if !ch.is_whitespace() {
            next_token.push(ch);
        }
    }
    tokens
}

fn tokens_to_literals(tokens: Vec<String>) -> Vec<String> {
    let mut literals = Vec::new();
    let mut i = 0;
    // println!("{tokens:?}");
    while i < tokens.len() {
        if PREDICATES.contains(&tokens[i].as_str()) {
            let mut literal = tokens[i].clone();
            let done = &literal == "waypoint";
            loop {
                i += 1;
                literal += &tokens[i];
                if tokens[i] == ")" {
                    literals.push(literal);
                    if done {
                        i = tokens.len();
                    }
                    break;
                }
            }
        } else {
            i += 1;
        }
    }

    literals
}

fn example_from_literals(literals: Vec<String>) -> Example {
    let mut example = Example::new();
    for literal in literals {}
    example
}
