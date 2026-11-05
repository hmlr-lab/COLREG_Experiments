use std::collections::{HashMap, HashSet};
use std::fmt;

struct Literal {
    name: String,
    args: Vec<String>,
}

struct Clause {
    head: Literal,
    body: Vec<Literal>,
}

impl Literal {
    fn parse(s: &str) -> Literal {
        let s = s.trim();
        match s.find('(') {
            Some(open) => Literal {
                name: s[..open].to_string(),
                args: split_top_level(&s[open + 1..s.rfind(')').unwrap_or(s.len())]),
            },
            None => Literal {
                name: s.to_string(),
                args: Vec::new(),
            },
        }
    }

    fn indicator(&self) -> (String, usize) {
        (self.name.clone(), self.args.len())
    }

    fn substitute(&self, map: &HashMap<String, String>) -> Literal {
        Literal {
            name: self.name.clone(),
            args: self.args.iter().map(|a| substitute(a, map)).collect(),
        }
    }
}

impl Clause {
    fn parse(s: &str) -> Clause {
        let s = s.trim().trim_end_matches('.');
        let (head, body) = s.split_once(":-").unwrap_or((s, ""));
        Clause {
            head: Literal::parse(head),
            body: split_top_level(body)
                .iter()
                .map(|l| Literal::parse(l))
                .collect(),
        }
    }

    fn vars(&self) -> HashSet<String> {
        std::iter::once(&self.head)
            .chain(&self.body)
            .flat_map(|l| l.args.iter().flat_map(|a| vars(a)))
            .collect()
    }
}

impl fmt::Display for Literal {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        if self.args.is_empty() {
            write!(f, "{}", self.name)
        } else {
            write!(f, "{}({})", self.name, self.args.join(","))
        }
    }
}

impl fmt::Display for Clause {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.head)?;
        if !self.body.is_empty() {
            let body: Vec<String> = self.body.iter().map(|l| l.to_string()).collect();
            write!(f, ":-{}", body.join(","))?;
        }
        write!(f, ".")
    }
}

/// Inline every non recursive, single clause invented predicate (e.g. turn_0, named
/// {target}_n where {target} is also defined) into the clauses that call it, then
/// remove its definition
pub fn inline_invented(h: &str) -> String {
    let mut clauses: Vec<Clause> = h
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(Clause::parse)
        .collect();

    // Each pass inlines and removes one predicate, so this terminates
    while let Some(def_idx) = find_inlinable(&clauses) {
        let def = clauses.remove(def_idx);
        let ind = def.head.indicator();
        for clause in clauses.iter_mut() {
            let mut taken = clause.vars();
            let mut body = Vec::new();
            for lit in clause.body.drain(..) {
                if lit.indicator() == ind {
                    body.extend(instantiate(&def, &lit, &mut taken));
                } else {
                    body.push(lit);
                }
            }
            clause.body = body;
        }
    }

    // Inlining can make clauses identical, keep only the first of each
    let mut seen = HashSet::new();
    let mut out = String::new();
    for clause in clauses {
        let clause = clause.to_string();
        if seen.insert(clause.clone()) {
            out += &clause;
            out.push('\n');
        }
    }
    out
}

/// Index of the definition of an invented predicate that is safe to inline: defined by
/// one clause whose head args are distinct variables, not calling itself, and called
/// from at least one other clause
fn find_inlinable(clauses: &[Clause]) -> Option<usize> {
    let mut defs: HashMap<(String, usize), Vec<usize>> = HashMap::new();
    for (i, c) in clauses.iter().enumerate() {
        defs.entry(c.head.indicator()).or_default().push(i);
    }
    let defined_names: HashSet<&str> = clauses.iter().map(|c| c.head.name.as_str()).collect();

    defs.iter()
        .filter(|(_, idx)| idx.len() == 1)
        .find_map(|(ind, idx)| {
            let def = &clauses[idx[0]];
            let invented = ind.0.rsplit_once('_').is_some_and(|(target, n)| {
                !n.is_empty()
                    && n.chars().all(|c| c.is_ascii_digit())
                    && defined_names.contains(target)
            });
            let head_vars: HashSet<&String> = def.head.args.iter().collect();
            let simple_head =
                head_vars.len() == def.head.args.len() && def.head.args.iter().all(|a| is_var(a));
            let recursive = def.body.iter().any(|l| l.indicator() == *ind);
            let called = clauses
                .iter()
                .any(|c| c.body.iter().any(|l| l.indicator() == *ind));
            (invented && simple_head && !recursive && called).then_some(idx[0])
        })
}

/// The body of `def` with its head unified against `call`, renaming any variables only
/// in its body apart from those already `taken` in the calling clause
fn instantiate(def: &Clause, call: &Literal, taken: &mut HashSet<String>) -> Vec<Literal> {
    let mut map: HashMap<String, String> = def
        .head
        .args
        .iter()
        .cloned()
        .zip(call.args.iter().cloned())
        .collect();

    taken.extend(def.vars());
    let mut n = 0;
    for v in def.vars() {
        if !map.contains_key(&v) {
            while taken.contains(&format!("Arg_{n}")) {
                n += 1;
            }
            let fresh = format!("Arg_{n}");
            taken.insert(fresh.clone());
            map.insert(v, fresh);
        }
    }

    def.body.iter().map(|l| l.substitute(&map)).collect()
}

/// Split on commas not nested inside brackets
fn split_top_level(s: &str) -> Vec<String> {
    let mut parts = Vec::new();
    let mut depth = 0;
    let mut start = 0;
    for (i, c) in s.char_indices() {
        match c {
            '(' | '[' => depth += 1,
            ')' | ']' => depth -= 1,
            ',' if depth == 0 => {
                parts.push(s[start..i].trim().to_string());
                start = i + 1;
            }
            _ => {}
        }
    }
    let last = s[start..].trim();
    if !last.is_empty() {
        parts.push(last.to_string());
    }
    parts
}

/// Identifier tokens in a term
fn tokens(s: &str) -> impl Iterator<Item = &str> {
    s.split(|c: char| !(c.is_alphanumeric() || c == '_'))
        .filter(|t| !t.is_empty())
}

fn is_var(s: &str) -> bool {
    s.starts_with(|c: char| c.is_uppercase() || c == '_')
}

fn vars(s: &str) -> Vec<String> {
    tokens(s).filter(|t| is_var(t)).map(String::from).collect()
}

/// Replace variables in a term according to `map`
fn substitute(s: &str, map: &HashMap<String, String>) -> String {
    let mut out = String::new();
    let mut token = String::new();
    for c in s.chars().chain(std::iter::once('\0')) {
        if c.is_alphanumeric() || c == '_' {
            token.push(c);
        } else {
            if !token.is_empty() {
                out += map.get(&token).unwrap_or(&token);
                token.clear();
            }
            if c != '\0' {
                out.push(c);
            }
        }
    }
    out
}
