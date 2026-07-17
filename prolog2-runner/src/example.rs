use std::{fmt::Write, sync::atomic::{AtomicUsize, Ordering::Acquire}};

#[derive(Debug)]
pub struct Example {
    id: usize,
    pub agent_sector: String,
    pub other_sector: String,
    pub range: String,
    pub dcpa: String,
    pub tcpa: String,
    pub waypoint: String,
}
static ID_COUNTER: AtomicUsize = AtomicUsize::new(0);

impl Example {
    pub fn new() -> Self {
        let id = ID_COUNTER.fetch_add(1, Acquire);
        Self {
            id,
            agent_sector: String::new(),
            other_sector: String::new(),
            range: String::new(),
            dcpa: String::new(),
            tcpa: String::new(),
            waypoint: String::new(),
        }
    }

    pub fn push_literal(&mut self, mut literal: String) {
        literal = literal.replace("agent", &format!("agent_{}", self.id));
        if literal.contains("sector") {
            if literal.contains("sector(agent") {
                self.agent_sector = literal
            } else {
                self.other_sector = literal
            }
        } else if literal.contains("range") {
            self.range = literal
        } else if literal.contains("dcpa") {
            self.dcpa = literal
        } else if literal.contains("tcpa") {
            self.tcpa = literal
        } else if literal.contains("waypoint") {
            self.waypoint = literal
        }
    }

    pub fn write_bk(&self, bk: &mut String) {
        write!(bk, "{}.\n", self.agent_sector);
        write!(bk, "{}.\n", self.other_sector);
        write!(bk, "{}.\n", self.range);
        write!(bk, "{}.\n", self.dcpa);
        write!(bk, "{}.\n", self.tcpa);
    }
}