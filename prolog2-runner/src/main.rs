mod generate_prolog;
mod example;
use prolog2::app::App;

use crate::generate_prolog::generate_prolog;

fn main() {
    generate_prolog();
    let app = App::from_setup_json("setup.json").unwrap();
    app.run();
}
