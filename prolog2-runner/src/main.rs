use prolog2::app::App;

fn main() {
    let app = App::from_setup_json("setup.json").unwrap();
    app.run();
}
