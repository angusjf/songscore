#![feature(proc_macro_hygiene, decl_macro)]
#[macro_use] extern crate rocket; #[macro_use] extern crate rocket_contrib; #[macro_use] extern crate serde_derive;

use std::sync::Mutex;
use std::collections::HashMap;
use rocket_cors;

use rocket::http::Method;
use rocket::State;
use rocket_contrib::json::{Json, JsonValue};
use rocket_cors::{AllowedHeaders, AllowedOrigins};

// The type to represent the ID
type ID = usize;

// We're going to store all of No need for a DB.
type ReviewMap = Mutex<HashMap<ID, Review>>;

#[derive(Serialize, Deserialize, Clone)]
struct Review {
    id: Option<ID>,
    text: Option<String>,
    stars: u8,
    user: User,
    subject: Subject
}

#[derive(Serialize, Deserialize, Clone)]
struct User {
    id: Option<ID>,
    username: String,
    image: Option<String>
}

#[derive(Serialize, Deserialize, Clone)]
struct Subject {
    id: Option<ID>,
    title: String,
    artist: Option<String>,
    image: Option<String>,
    kind: Option<SubjectKind>
}

#[derive(Serialize, Deserialize, Clone)]
enum SubjectKind {
    Album,
    Song
}

// TODO: This example can be improved by using `route` with multiple HTTP verbs.
#[post("/", format = "json", data = "<review>")]
fn new(mut review: Json<Review>, map: State<'_, ReviewMap>) -> Option<Json<Review>> {
    let mut hashmap = map.lock().expect("map lock.");
    let mut id : usize = 1;
    for i in hashmap.keys() {
        if i >= &id {
            id = i + 1;
        }
    }
    review.0.id = Some(id);
    hashmap.insert(id, review.0);
    hashmap.get(&id).map(|review| Json(review.clone()))
}

#[put("/<id>", format = "json", data = "<review>")]
fn update(id: ID, review: Json<Review>, map: State<'_, ReviewMap>) -> Option<JsonValue> {
    let mut hashmap = map.lock().unwrap();
    if hashmap.contains_key(&id) {
        hashmap.insert(id, review.0);
        Some(json!({ "status": "ok" }))
    } else {
        None
    }
}

#[get("/<id>", format = "json")]
fn get(id: ID, map: State<'_, ReviewMap>) -> Option<Json<Review>> {
    let hashmap = map.lock().unwrap();
    hashmap.get(&id).map(|review| Json(review.clone()))
}

#[get("/", format = "json")]
fn get_all(map: State<'_, ReviewMap>) -> Json<Vec<Review>> {
    let hashmap = map.lock().unwrap();
    let mut vals = Vec::new();
    for v in hashmap.values() {
        vals.push(v.clone());
    }
    Json(vals)
}

#[catch(404)]
fn not_found() -> JsonValue {
    json!({
        "status": "error",
        "reason": "Resource was not found."
    })
}

fn main() {

    let allowed_origins = AllowedOrigins::all();

    // You can also deserialize this
    let cors_options = rocket_cors::CorsOptions {
        allowed_origins,
        allowed_methods: vec![Method::Get, Method::Post].into_iter().map(From::from).collect(),
        allowed_headers: AllowedHeaders::all(),
        allow_credentials: true,
        ..Default::default()
    };

    let cors = match cors_options.to_cors() {
        Ok(c)  => c,
        Err(_e) => return,
    };

    rocket::ignite()
        .mount("/review", routes![new, update, get, get_all])
        .register(catchers![not_found])
        .manage(Mutex::new(HashMap::<ID, Review>::new()))
        .attach(cors)
        .launch();
}

