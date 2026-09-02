mod conditions;
mod generate_prolog;
mod situation;
use prolog2::app::App;
use situation::Situation;

use crate::generate_prolog::generate_prolog;

fn main() {
    let situations = Situation::load_situations();
    generate_prolog(situations);

    let app = App::from_setup_json("setup.json").unwrap();
    app.run();
}
