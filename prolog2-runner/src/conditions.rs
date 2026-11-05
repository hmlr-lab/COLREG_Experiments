use std::cmp::Ordering::Equal;

#[derive(Debug, PartialEq, Eq, Hash, PartialOrd)]
pub enum Turn {
    VeryLarge,
    Large,
    Moderate,
    Small,
    Insubstantial,
}

#[derive(Debug, PartialEq, Eq, Hash)]
pub enum Side {
    Port,
    Starboard,
}

#[derive(Debug, PartialEq, Eq, Hash, PartialOrd)]
pub enum Risk {
    NoRisk,
    RiskDeveloping,
    ImminentCritical,
    ImminentVeryclose,
    ImminentClose,
    ShortCritical,
    ShortVeryclose,
    ShortClose,
    MediumCritical,
    MediumVeryclose,
    MediumClose,
}

#[derive(Debug, PartialEq, Eq, Hash)]
pub enum Condition {
    Turn(Turn),
    Side(String, Side),
    Avoid(String, Risk),
    Resume(String, Risk),
}

impl Ord for Risk {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.to_int().cmp(&other.to_int())
    }
}

impl Risk {
    fn to_int(&self) -> usize {
        match self {
            Risk::ImminentCritical => 10,
            Risk::ImminentVeryclose => 9,
            Risk::ImminentClose => 8,
            Risk::ShortCritical => 7,
            Risk::ShortVeryclose => 6,
            Risk::ShortClose => 5,
            Risk::MediumCritical => 4,
            Risk::MediumVeryclose => 3,
            Risk::MediumClose => 2,
            Risk::RiskDeveloping => 1,
            Risk::NoRisk => 0,
        }
    }
}

impl From<&str> for Risk {
    fn from(value: &str) -> Self {
        match value {
            "no_risk" => Risk::NoRisk,
            "risk_developing" => Risk::RiskDeveloping,
            "imminent_critical" => Risk::ImminentCritical,
            "imminent_veryclose" => Risk::ImminentVeryclose,
            "imminent_close" => Risk::ImminentClose,
            "short_critical" => Risk::ShortCritical,
            "short_veryclose" => Risk::ShortVeryclose,
            "short_close" => Risk::ShortClose,
            "medium_critical" => Risk::MediumCritical,
            "medium_veryclose" => Risk::MediumVeryclose,
            "medium_close" => Risk::MediumClose,
            _ => panic!("Unrecognised risk value: {value}"),
        }
    }
}

impl ToString for Risk {
    fn to_string(&self) -> String {
        match self {
            Risk::NoRisk => "no_risk".into(),
            Risk::RiskDeveloping => "risk_developing".into(),
            Risk::ImminentCritical => "imminent_critical".into(),
            Risk::ImminentVeryclose => "imminent_veryclose".into(),
            Risk::ImminentClose => "imminent_close".into(),
            Risk::ShortCritical => "short_critical".into(),
            Risk::ShortVeryclose => "short_veryclose".into(),
            Risk::ShortClose => "short_close".into(),
            Risk::MediumCritical => "medium_critical".into(),
            Risk::MediumVeryclose => "medium_veryclose".into(),
            Risk::MediumClose => "medium_close".into(),
        }
    }
}

impl From<&str> for Turn {
    fn from(value: &str) -> Self {
        match value {
            "very_large" => Turn::VeryLarge,
            "large" => Turn::Large,
            "moderate" => Turn::Moderate,
            "small" => Turn::Small,
            "insubstantial" => Turn::Insubstantial,
            _ => panic!("Unrecognised turn value: {value}"),
        }
    }
}

impl ToString for Turn {
    fn to_string(&self) -> String {
        match self {
            Turn::VeryLarge => "very_large".into(),
            Turn::Large => "large".into(),
            Turn::Moderate => "moderate".into(),
            Turn::Small => "small".into(),
            Turn::Insubstantial => "insubstantial".into(),
        }
    }
}

impl Turn {
    fn to_int(&self) -> usize {
        match self {
            Turn::VeryLarge => 1,
            Turn::Large => 2,
            Turn::Moderate => 3,
            Turn::Small => 4,
            Turn::Insubstantial => 5,
        }
    }
}

impl Ord for Turn {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.to_int().cmp(&other.to_int())
    }
}

impl From<&str> for Side {
    fn from(value: &str) -> Self {
        match value {
            "port" => Side::Port,
            "starboard" => Side::Starboard,
            _ => panic!("Unrecognised cpa_side value: {value}"),
        }
    }
}

impl ToString for Side {
    fn to_string(&self) -> String {
        match self {
            Side::Port => "port".into(),
            Side::Starboard => "starboard".into(),
        }
    }
}

impl From<&str> for Condition {
    fn from(value: &str) -> Self {
        let value = value.replace("agent,", "");
        let i1 = value.find('(').unwrap();
        let i2 = value.find(')').unwrap();
        let pred = &value[..i1];
        let args: Vec<&str> = value[i1 + 1..i2].split(',').collect();
        match pred {
            "turn" => Condition::Turn(args[0].into()),
            "cpa_side" => Condition::Side(args[0].into(), args[1].into()),
            "avoid" => Condition::Avoid(args[0].into(), args[1].into()),
            "resume" => Condition::Resume(args[0].into(), args[1].into()),
            _ => panic!("Unexpected predicate symbol in waypoint conditions: \"{pred}\""),
        }
    }
}

impl Condition {
    pub fn pred_symbol(&self) -> &str {
        match self {
            Condition::Turn(_) => "turn",
            Condition::Side(_, _) => "cpa_side",
            Condition::Avoid(_, _) => "avoid",
            Condition::Resume(_, _) => "resume",
        }
    }

    pub fn is_pred(&self, pred: &str) -> bool {
        self.pred_symbol() == pred
    }

    pub fn to_string(&self, id: &str) -> String {
        match self {
            Condition::Turn(turn) => format!("turn(agent_{id},{}).", turn.to_string()),
            Condition::Side(vessel, cpa_side) => {
                format!(
                    "cpa_side(agent_{id},{vessel}_{id},{}).",
                    cpa_side.to_string()
                )
            }
            Condition::Avoid(vessel, risk) => {
                format!("avoid(agent_{id},{vessel}_{id},{}).", risk.to_string())
            }
            Condition::Resume(vessel, risk) => {
                format!("resume(agent_{id},{vessel}_{id},{}).", risk.to_string())
            }
        }
    }
}

impl PartialOrd for Condition {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        match (self, other) {
            (Self::Turn(a), Self::Turn(b)) => Some(a.cmp(b)),
            (Self::Resume(o1, a), Self::Resume(o2, b)) if *o1 == *o2 => Some(a.cmp(b)),
            (Self::Avoid(o1, a), Self::Avoid(o2, b)) if *o1 == *o2 => Some(a.cmp(b)),
            (a, b) if a == b => Some(Equal),
            _ => None,
        }
    }
}

#[cfg(test)]
mod tests {
    use std::cmp::Ordering;

    use crate::conditions::{Risk::*, Turn::*};

    #[test]
    fn turn_ord() {
        let a = VeryLarge;
        let b = Moderate;
        let c = Insubstantial;

        assert_eq!(a.cmp(&b), Ordering::Less);
        assert_eq!(a.cmp(&c), Ordering::Less);

        assert_eq!(b.cmp(&a), Ordering::Greater);
        assert_eq!(b.cmp(&c), Ordering::Less);

        assert_eq!(c.cmp(&a), Ordering::Greater);
        assert_eq!(c.cmp(&b), Ordering::Greater);
    }

    #[test]
    fn risk_ord() {
        let a = NoRisk;
        let b = ShortClose;
        let c = ImminentCritical;

        assert_eq!(a.cmp(&b), Ordering::Less);
        assert_eq!(a.cmp(&c), Ordering::Less);

        assert_eq!(b.cmp(&a), Ordering::Greater);
        assert_eq!(b.cmp(&c), Ordering::Less);

        assert_eq!(c.cmp(&a), Ordering::Greater);
        assert_eq!(c.cmp(&b), Ordering::Greater);
    }
}
