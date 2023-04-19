use std::fs;
use std::path::Path;
use chrono::{DateTime, FixedOffset, Local, Utc};
use rusqlite::{Connection, Result, params};
use log::{info, warn, error};
use reqwest;
//use std::collections::HashMap;
use serde_json::Value;
use serde::{Serialize, Deserialize};

static DB: &str = "cxtk.db";

pub fn init() -> Result<()>{
    //初始化数据库
    get_time();
    print!("初始化数据库 ... ");
    let conn = Connection::open(DB)?;
    // 创建题目和答案表
    conn.execute(
        "CREATE TABLE IF NOT EXISTS problems (
             id INTEGER PRIMARY KEY,
             question TEXT NOT NULL,
             answer TEXT NOT NULL
         )",
        [],
    )?;
    // 创建用户表
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY,
             name TEXT NOT NULL,
             num_of_problems INTEGER NOT NULL
         )",
        [],
    )?;
    Ok(())
}

pub fn add_qa<'a>(question: &String, answer: &String) -> Result<String, rusqlite::Error>{
    // 添加问题答案
    //(question: &str, answer: &str) -> Result<&str, rusqlite::Error>{
    let conn = Connection::open(DB)?;
    let mut stmt = conn.prepare("SELECT answer FROM problems WHERE question = ?1")?;
    let mut rows = stmt.query(&[question.as_str()])?;
    // 清洗答案
    let answer = clean_answer(&answer);
    //判断 question 是否存在
    if let Some(row) = rows.next()? {
        //判断库中 answer 是否为None
        if let Ok(a) = get_qa(&question) {
            if a == String::from("None") {
                //更新库answer
                if let Ok(an) = update_qas(&conn, &question, &answer) {
                    return Ok(an);
                }
                return Ok(String::from("None"));
            }
        }
        //如果 question 存在且 answer 不为None，返回相应的 answer
        let existing_answer: String = row.get(0)?;
        /*info!(
            "Problems 读取:\n\tQuestion: {}\n\tAnswer: {}\t[Return]",
            question, existing_answer
        );*/
        return Ok(existing_answer);
    }
    //如果 question 不存在，将其插入 problems 表
    conn.execute(
        "INSERT INTO problems (question, answer) VALUES (?1, ?2)",
        params![question, answer],
    )?;
    warn!(
        "Problems 写入:\n\tQuestion: {}\n\tAnswer: {}\t[Return]",
        question, answer
    );
    Ok(answer.to_string())
}

#[allow(dead_code)]
pub fn update_qa(question: &String, answer: &String) -> Result<String, rusqlite::Error> {
    // 更新答案
    let conn= Connection::open(DB)?;
    if let Ok(a) = get_qa(question) {
        warn!(
            "Problems 更新:\n\tQuestion: {}\n\tOld_Answer: {}\n\tNew_answer: {}",
            &question, &a, &answer
        );
        conn.execute(
            "UPDATE problems SET answer = ?1 WHERE question = ?2",
            params![answer, question],
        )?;
        return Ok(answer.to_string());
    };
    return Ok("None".to_string());
}

pub fn update_qas(conn: &Connection, question: &String, answer: &String) -> Result<String, rusqlite::Error> {
    // 清洗更新答案
    if let Ok(a) = get_qa(question) {
        warn!(
            "Problems 更新:\n\tQuestion: {}\n\tOld_Answer: {}\n\tNew_answer: {}",
            &question, &a, &answer
        );
        conn.execute(
            "UPDATE problems SET answer = ?1 WHERE question = ?2",
            params![answer, question],
        )?;
        return Ok(answer.to_string());
    };
    return Ok("None".to_string());
}

pub fn clean_answer(answer: &str) -> String {
    // 清洗函数
    let mut cleaned_answer = answer.trim();
    // 清洗 答案 首尾 #
    while cleaned_answer.starts_with('#') {
        cleaned_answer = &cleaned_answer[1..];
    }
    while cleaned_answer.ends_with('#') {
        cleaned_answer = &cleaned_answer[..cleaned_answer.len() - 1];
    }
    while cleaned_answer.starts_with(' ') {
        cleaned_answer = &cleaned_answer[1..];
    }
    while cleaned_answer.ends_with(' ') {
        cleaned_answer = &cleaned_answer[..cleaned_answer.len() - 1];
    }
    while cleaned_answer.starts_with("<p>") {
        cleaned_answer = &cleaned_answer[1..];
    }
    while cleaned_answer.ends_with("</p>") {
        cleaned_answer = &cleaned_answer[..cleaned_answer.len() - 1];
    }
    // 清洗 答案 \n
    let cleaned_answer = cleaned_answer.replace("\n", "");
    let cleaned_answer = cleaned_answer.replace("\t", "");
    let cleaned_answer = cleaned_answer.replace("javascript:void(0);", "");
    cleaned_answer.to_owned()
}

#[allow(dead_code)]
pub fn clean_database() -> Result<(), rusqlite::Error> {
    // 清洗数据库答案
    warn!("清洗数据库初始化...");
    let conn = Connection::open(DB)?;
    let mut stmt = conn.prepare("SELECT question, answer FROM problems")?;
    let problem_iter = stmt.query_map([], |row| {
        let question: String = row.get(0)?;
        let answer: String = row.get(1)?;
        /*warn!(
            "清洗数据:\n\tQuestion: {}\n\tAnswer: {}",
            &question, &answer
        );*/
        let cleaned_answer = clean_answer(&answer);
        Ok((question, cleaned_answer))
    })?;
    let mut stmt = conn.prepare("SELECT answer FROM problems WHERE question = ?")?;
    for problem in problem_iter {
        let (cleaned_question, cleaned_answer) = problem?;
        let rows = stmt.query_map(&[&cleaned_question], |row| {
            let answer: String = row.get(0)?;
            Ok(answer)
        })?;
        if let Some(Ok(old_answer)) = rows.into_iter().next() {
            if old_answer == cleaned_answer {
                continue;
            }
        };
        /*if let Ok(a) = update_qa(&cleaned_question, &cleaned_answer) {
            info!("清洗结果: {}", a);
        } else {
            error!("更新错误！");
        };*/
        match update_qas(&conn, &cleaned_question, &cleaned_answer) {
            Ok(a) => info!("清洗结果: {}", a),
            Err(e) => error!("更新错误: {}", e),
        }
    }
    Ok(())
}

#[allow(dead_code)]
pub fn get_id(question: &String) -> Result<String, rusqlite::Error> {
    // question 获取 ID
    let conn = Connection::open(DB)?;
    let mut stmt = conn.prepare("SELECT ID FROM problems WHERE question = ?1")?;
    let mut rows = stmt.query(&[question.as_str()])?;
    if let Some(row) = rows.next()? {
        let existing_answer: String = row.get(0)?;
        info!(
            "Problems 读取:\n\tQuestion: {}\n\tID: {}",
            question, &existing_answer
        );
        return Ok(existing_answer);
    };
    error!(
        "Problems 读取:\n\tQuestion: {}\n\tID None",
        question
    );
    Ok("None".to_string())
}

pub fn get_qa(question: &String) -> Result<String, rusqlite::Error> {
    // question 获取答案
    let conn = Connection::open(DB)?;
    let mut stmt = conn.prepare("SELECT answer FROM problems WHERE question = ?1")?;
    let mut rows = stmt.query(&[question.as_str()])?;
    if let Some(row) = rows.next()? {
        let existing_answer: String = row.get(0)?;
        /*info!(
            "Problems 读取:\n\tQuestion: {}\n\tAnswer: {}",
            question, &existing_answer
        );*/
        return Ok(existing_answer);
    };
    /*error!(
        "Problems 读取:\n\tQuestion: {}\n\tAnswer: None",
        question
    );*/
    Ok("None".to_string())
    //Err(rusqlite::Error::InvalidParameterName("None".to_string()))
}

pub fn file_db() -> bool{
    // 判断数据库是否存在
    let file_path = Path::new(DB);
    if let Ok(metadata) = fs::metadata(file_path) {
        if metadata.is_file() {
            info!("数据库已初始化");
            return true;
        } else {
            warn!("存在同名文件夹");
            return false;
        }
    } else {
        warn!("数据库不存在");
    };
    false
}

pub fn get_time() -> String {
    // 获取当前+8区时间
    let local: DateTime<Local> = Local::now();
    let utc_time = DateTime::<Utc>::from_utc(local.naive_utc(), Utc);
    let china_timezone = FixedOffset::east_opt(8 * 3600).unwrap();
    //::east_opt(8 * 3600);
    let s = utc_time.with_timezone(&china_timezone).format("%m-%d|%H:%M:%S");
    print!("[{}] ", s);
    s.to_string()
}

// 将格式转化为enncy题库类型(code改为version)
//  {"code": 1, "data": {"question": question, "answer": res_}}
pub fn enncy(v: u8, question: &String, answer: &String) -> String {
    match v {
        0 => r#"{"v": 0, "data": {"question": ""#.to_owned() + question + r#"", "answer": ""# + &answer + r#""}}"#,
        _ => {
            if let Ok(answer) = add_qa(question, answer) {
                r#"{"v": "#.to_owned() + &v.to_string() + r#", "data": {"question": ""# + question + r#"", "answer": ""# + &answer + r#""}}"#
            } else { "None".to_string() }
        },
    }
}

#[derive(Debug, Serialize, Deserialize)]
struct V1 {
    code: u8,
    data: String,
    name: String,
    msg: String,
    question: String,
}

pub fn v0(title: String) -> Result<String, rusqlite::Error> {
    match get_qa(&title) {
        Ok(a) => {
            if a!="None" {
                info!("SQL 查询 v0:\n\tQ: {}\n\tA: {}", &title, &a);
            } else {
                error!("SQL 查询 v0:\n\tQ: {}\n\tA: {}", &title, &a);
            }
            Ok(enncy(0, &title, &a))
        }
        Err(err) => Err(err),
    }
}

pub async fn v1(title: String) -> Result<String, Box<dyn std::error::Error>> {
    let resp = reqwest::get(format!("专属群内一个人的接口", &title))
        .await?
        .text()
        .await?;
    let res: V1= serde_json::from_str(&resp).unwrap();
    info!("API 查询 v1:\n\tQ: {}\n\tA: {:#?}", &title, &res);
    Ok(enncy(1, &res.question, &clean_answer(&res.data)))
}

#[derive(Debug)]
struct V2 {
    id: u64,
    atype: String,
}

pub fn v2(title: String) -> Result<String, rusqlite::Error> {
    let conn2 = Connection::open("questionbank.db")?;
    let mut stmt = conn2.prepare("SELECT answer_id, type FROM questions WHERE title = ?1")?;
    let rows = stmt.query_map(&[title.as_str()], |row| {
        Ok(V2 {
            id: row.get(0)?,
            atype: row.get(1)?,
        })
    })?;
    // 将所有行组成的 vector 返回
    let vec_a = rows.collect::<Vec<_>>();
    //println!("{:#?}", vec_a);
    if vec_a.is_empty() {
        error!("SQL 查询 v2(a):\n\tQ: {}\n\tA: None", &title);
        return Ok(enncy(0, &title, &"None v3a".to_string()));
    }
    if let Ok(a) = &vec_a[0] {
        let answer_id = a.id;
        let answer_type = a.atype.as_str();
        match answer_type {
            // 单选 single_choice_answers
            "1" => {
                let mut stmt2 = conn2.prepare("SELECT correct_option_text FROM single_choice_answers WHERE question_id = ?1")?;
                let mut rows2 = stmt2.query(params![answer_id])?;
                if let Some(row2) = rows2.next()? {
                    let row2: String = row2.get(0)?;
                    info!("SQL 查询 v2(s):\n\tQ: {}\n\tA: {}", &title, &row2);
                    return Ok(enncy(2, &title, &row2.to_string()));
                };
                error!("SQL 查询 v2(s):\n\tQ: {}\n\tA: None", &title);
            },
            // 多选 multiple_choice_answers
            "2" => {
                let mut stmt2 = conn2.prepare("SELECT correct_option FROM multiple_choice_answers WHERE question_id = ?1")?;
                let mut rows2 = stmt2.query(params![answer_id])?;
                if let Some(row2) = rows2.next()? {
                    let row2: String = row2.get(0)?;
                    info!("SQL 查询 v2(m):\n\tQ: {}\n\tA: {}", &title, &row2);
                    let v: Vec<Value> = serde_json::from_str(&row2).unwrap();
                    let mut result = String::new();
                    for item in v {
                        if let Value::Object(dict) = item {
                            for value in dict.values() {
                                if let Value::String(s) = value {
                                    result.push_str(s);
                                    result.push_str("###");
                                }
                            }
                        }
                    }
                    //println!("{} {}", result, enncy(2, &title, &result[..&result.len() - 3].to_string()));
                    return Ok(enncy(2, &title, &result[..&result.len() - 3].to_string()));
                };
                error!("SQL 查询 v2(m):\n\tQ: {}\n\tA: None", &title);
                return Ok(enncy(2, &title, &"None v3m".to_string()));
            },
            // 判断 true_or_false_answers
            "3" => {
                let mut stmt2 = conn2.prepare("SELECT correct_option FROM true_or_false_answers WHERE question_id = ?1")?;
                let mut rows2 = stmt2.query(params![answer_id])?;
                if let Some(row2)= rows2.next()? {
                    let row2: u8 = row2.get(0)?;
                    //let row2 = row2.as_str();
                    info!("SQL 查询 v2(o):\n\tQ: {}\n\tA: {}", &title, &row2);
                    match row2 {
                        0 => return Ok(enncy(2, &title, &"错误".to_string())),
                        1 => return Ok(enncy(2, &title, &"正确".to_string())),
                        _ => return Ok(enncy(2, &title, &"None v3o".to_string())),
                    }
                };
                error!("SQL 查询 v2(o):\n\tQ: {}\n\tA: None", &title);
                return Ok(enncy(2, &title, &"None v3o".to_string()));
            },
            _ => return Ok(enncy(2, &title, &"None v3a".to_string())),
        }
    };
    Ok(enncy(2, &title, &"None v3a".to_string()))
}