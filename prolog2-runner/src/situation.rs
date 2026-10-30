use crate::conditions::Condition;
use core::panic;
use indexmap::IndexMap;
use rust_yaml::{Value, Yaml};
use std::{
    cmp::Ordering::{Equal, Greater},
    collections::HashSet,
    fs::{read_dir, read_to_string},
};

const EXAMPLES_PATH: &str = "../examples/take_action/";

#[derive(Debug)]
pub struct Situation {
    pub id: String,
    pub facts: Vec<String>,
    pub take_action: bool,
    pub pos_conds: Vec<Condition>,
    pub neg_conds: Vec<Condition>,
}

impl Situation {
    pub fn load_situations() -> Vec<Self> {
        let yaml = Yaml::new();
        let mut res = Vec::new();
        for file in read_dir(EXAMPLES_PATH).unwrap().map(Result::unwrap) {
            let file_name = file
                .file_name()
                .to_str()
                .unwrap()
                .split('.')
                .next()
                .unwrap()
                .to_string();
            let mut id_counter = 0;

            let parsed = yaml
                .load_str(&read_to_string(file.path()).unwrap())
                .unwrap();

            for parsed_sit in parsed.as_sequence().unwrap().iter() {
                match Self::from_yaml(parsed_sit, format!("{file_name}_{id_counter}")) {
                    Ok(sit) => res.push(sit),
                    Err(err) => panic!(
                        "
                    {err}
                    Failed to parse situation yaml:\n{}",
                        yaml.dump_str(&parsed_sit).unwrap()
                    ),
                }
                id_counter += 1;
            }
        }
        res
    }

    pub fn from_yaml(yaml: &Value, id: String) -> Result<Self, String> {
        let mapping = yaml.as_mapping().unwrap();

        let facts = parse_facts(mapping, &id)?;
        let take_action = parse_take_action(mapping)?;
        let (pos_conds, neg_conds) = parse_waypoints(mapping)?;

        Ok(Self {
            id,
            facts,
            take_action,
            pos_conds,
            neg_conds,
        })
    }
}

fn parse_waypoints(
    mapping: &IndexMap<Value, Value>,
) -> Result<(Vec<Condition>, Vec<Condition>), String> {
    let mut pos_conds = HashSet::new();
    let mut neg_conds = HashSet::new();

    let waypoints = mapping
        .get(&Value::String("waypoints".into()))
        .ok_or("waypoints not present".to_string())?
        .as_mapping()
        .ok_or("waypoints not valid mapping".to_string())?;

    let pos_waypoints = waypoints
        .get(&Value::String("pos".into()))
        .ok_or("pos not present in waypoints".to_string())?
        .as_mapping()
        .unwrap();
    let neg_waypoints = waypoints
        .get(&Value::String("neg".into()))
        .ok_or("pos not present in waypoints".to_string())?
        .as_mapping()
        .unwrap();

    for (_, wp) in pos_waypoints {
        for cond in wp
            .as_sequence()
            .ok_or(format!("waypoint not valid sequence {wp:?}"))?
        {
            pos_conds.insert(
                cond.as_str()
                    .ok_or(format!("condition not string: {cond:?}"))?
                    .into(),
            );
        }
    }

    for (_, wp) in neg_waypoints {
        for cond in wp
            .as_sequence()
            .ok_or(format!("waypoint not valid sequence {wp:?}"))?
        {
            let cond: Condition = cond
                .as_str()
                .ok_or("condition not string: {cond:?}")?
                .into();

            // Only add negative condition if all positives of the same type are less risk
            if pos_conds
                .iter()
                .all(|pos_cond: &Condition| match pos_cond.partial_cmp(&cond) {
                    Some(Greater) | Some(Equal) => false,
                    _ => true,
                })
            {
                neg_conds.insert(cond);
            }
        }
    }

    Ok((
        pos_conds.into_iter().collect(),
        neg_conds.into_iter().collect(),
    ))
}

fn parse_facts(mapping: &IndexMap<Value, Value>, id: &str) -> Result<Vec<String>, String> {
    Ok(mapping
        .get(&Value::String("facts".into()))
        .ok_or("facts not present".to_string())?
        .as_sequence()
        .ok_or("facts not valid sequence".to_string())?
        .iter()
        .map(|value| {
            let fact = value.as_str().unwrap().to_owned();
            fact.replace("agent", &format!("agt_{id}"))
                .replace("cruiseliner1", &format!("cl_{id}"))
                .replace("vessel1", &format!("vsl_{id}"))
        })
        .collect())
}

fn parse_take_action(mapping: &IndexMap<Value, Value>) -> Result<bool, String> {
    let value = mapping
        .get(&Value::String("take_action".into()))
        .ok_or("take_action not present")?
        .as_str()
        .ok_or("take_action not a string")?;
    match value {
        "pos" => Ok(true),
        "neg" => Ok(false),
        _ => Err(format!("{value} not valid take action string")),
    }
}
