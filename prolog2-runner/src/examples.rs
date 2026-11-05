use prolog2::Examples;

use crate::situation::Situation;

pub fn gen_examples(situations: &[Situation], pred: &str) -> Examples {
    let mut pos = Vec::new();
    let mut neg = Vec::new();

    for sit in situations {
        for cond in sit.pos_conds.iter() {
            if cond.is_pred(pred) {
                pos.push(cond.to_string(&sit.id));
            }
        }
        for cond in sit.neg_conds.iter() {
            if cond.is_pred(pred) {
                neg.push(cond.to_string(&sit.id));
            }
        }
    }

    Examples { pos, neg }
}
