const GENERATED_DIR: &str = "../prolog/generated";
const EXAMPLE_DIR: &str = "../examples";
const DELIMINATORS: [char; 5] = [',', '(', ')', '.', '\n'];

enum Range {
    VeryFar,
    Far,
    Middle,
    Near,
    VeryNear,
}

enum DCPA {
    Safe,
    Marginal,
    Close,
    VeryClose,
    Critical,
}

enum TCPA {
    VeryLong,
    Long,
    Medium,
    Short,
    Immediate,
}

enum Sector{
    ahead,
    port_bow_forward,
    port_beam_forward,
    port_bow_broad,
    port_beam,
    port_beam_aft,
    port_quarter_broad,
    port_quarter_aft,
    astern,
    starboard_bow_forward,
    starboard_beam_forward,
    starboard_bow_broad,
    starboard_beam,
    starboard_beam_aft,
    starboard_quarter_broad,
    starboard_quarter_aft,
}

enum AvoidResume{
    
}

struct Example{

}

pub fn generate_prolog() {}

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
