#[derive(Debug, PartialEq, Eq, Hash)]
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

#[derive(Debug, PartialEq, Eq, Hash)]
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

impl From<&str> for Side {
    fn from(value: &str) -> Self {
        match value {
            "port" => Side::Port,
            "starboard" => Side::Starboard,
            _ => panic!("Unrecognised side value: {value}"),
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
            "side" => Condition::Side(args[0].into(), args[1].into()),
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
            Condition::Side(_, _) => "side",
            Condition::Avoid(_, _) => "avoid",
            Condition::Resume(_, _) => "resume",
        }
    }

    pub fn is_pred(&self, pred: &str) -> bool {
        self.pred_symbol() == pred
    }

    pub fn to_string(&self, id: usize) -> String {
        match self {
            Condition::Turn(turn) => format!("turn(agent{id},{}).", turn.to_string()),
            Condition::Side(vessel, side) => {
                format!("side(agent{id},{vessel}_{id},{}).", side.to_string())
            }
            Condition::Avoid(vessel, risk) => {
                format!("avoid(agent{id},{vessel}_{id},{}).", risk.to_string())
            }
            Condition::Resume(vessel, risk) => {
                format!("resume(agent{id},{vessel}_{id},{}).", risk.to_string())
            }
        }
    }
}
