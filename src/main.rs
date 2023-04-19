use actix_web::{get, web, App, HttpResponse, HttpServer, Responder,}; //middleware::Logger};
use log::{info, error};
use ice_cx_qk::*;

/*
#[derive(serde::Deserialize)]
#[serde(rename_all = "lowercase")]
struct Question {
    q: String,
}

#[derive(serde::Deserialize)]
#[serde(rename_all = "lowercase")]
struct Problems {
    q: String,
    a: String,
}
*/

#[derive(serde::Deserialize)]
#[serde(rename_all = "lowercase")]
struct Ver {
    v: u8,
    title: String,
}

#[get("/")]
async fn index() -> impl Responder {
    HttpResponse::Ok().body("Hello, ice_cx_qk!")
}

#[get("/api")]
async fn serach_v(info: web::Query<Ver>) -> impl Responder  {
    let v = info.v;
    let s = info.title.to_string();
    match v {
        0 => {
            match v0(s) {
                Ok(a) => HttpResponse::Ok().body(a),
                Err(err) => {
                    error!("{}", err);
                    HttpResponse::InternalServerError().body(err.to_string())
                },
            }
        },
        1 => {
            match v1(s).await {
                Ok(a) => HttpResponse::Ok().body(a),
                Err(err) => {
                    error!("{}", err);
                    HttpResponse::InternalServerError().body(err.to_string())
                },
            }
        },
        2 => {
            match v2(s) {
                Ok(a) => HttpResponse::Ok().body(a),
                Err(err) => {
                    error!("{}", err);
                    HttpResponse::InternalServerError().body(err.to_string())
                },
            }
        },
        _ => HttpResponse::InternalServerError().body("Version error".to_string()),
    }
}

/*#[get("/q")]
async fn question_answer(info: web::Query<Question>) -> impl Responder  {
    let question = &info.q;
    match get_qa(&question) {
        Ok(answer) => HttpResponse::Ok().body(answer),
        Err(err) => HttpResponse::InternalServerError().body(err.to_string()),
    }
}

#[get("/p")]
async fn problems_add(info: web::Query<Problems>) -> impl Responder  {
    let question = &info.q;
    let answer = &info.a;
    match add_qa(&question, &answer) {
        Ok(answer) => HttpResponse::Ok().body(answer),
        Err(err) => HttpResponse::InternalServerError().body(err.to_string()),
    }
}*/

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    if ! file_db() {
        if let Err(err) = init() {
            panic!("失败: {}", err);
        } else {
            println!("成功");
            get_time();
            info!("Web Run");
        }
    }
    env_logger::builder()
        .filter_level(log::LevelFilter::Info)
        .init();
    // 清洗数据库 
    // if let Ok(_) = clean_database() {};
    HttpServer::new(|| {
        App::new()
            //.wrap(Logger::default())
            .service(index)
            //.service(problems_add)
            //.service(question_answer)
            .service(serach_v)
    })
    .bind("0.0.0.0:8080")?
    .run()
    .await
}
