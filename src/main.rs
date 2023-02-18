struct IceStudy {
    version: String,
    debug: i32,
    headers: Header,
    proxy: Option<String>,
    cookie: Option<Cookie>,
}

impl IceStudy {
    fn new(main: Option<String>, proxy: Option<String>, v: bool) -> Self {
        let res = Args::new();
        Logo(v && res.get("logo"));
        let debug = res.get("debug").parse().unwrap_or(0);
        let headers = Header::new();
        let proxy = proxy;
        let version = format!("ice-study 0.0.1(Beta LTS)");
        let mut ice_study = IceStudy { version, debug, headers, proxy, cookie: None };
        iLog_new(ice_study, iLog);
        if res.get("v") {
            ice_study.iLog(&ice_study.version);
            std::process::exit(0);
        }
        ice_study.iLog(&format!("\nVerison: {}\nHeader: {}\nProxy: {:?}\n", v, ice_study.headers, ice_study.proxy), 0);
        ice_study
    }

    fn login(&mut self, user: &str, password: &str) -> Result<Cookie, Box<dyn std::error::Error>> {
        let data = Api::Login_fn(user, password);
        self.iLog(&format!("\n[POST]: {}\nData: {}\n", Api::Login, data), 0);
        let mut req = reqwest::Client::new().post(Api::Login).headers(self.headers.clone());
        if let Some(proxy) = &self.proxy {
            req = req.proxy(reqwest::Proxy::http(proxy)?);
        }
        let res = req.json(&data).send()?;
        self.iLog(&format!("\nRes: {}\n", res.text()?), 0);
        if !res.json::<Value>()?["status"].as_bool().unwrap_or(false) {
            self.iLog("Login status... [False]", 4);
            self.iLog(&format!("Error Res: {}", res.text()?));
            std::process::exit(0);
        }
        self.iLog("Login status... [True]");
        let cookie = res.cookies().clone();
        self.cookie = Some(cookie.clone());
        self.iLog(&format!("\nCookie: {:?}\n", cookie), 0);
        Ok(cookie)
    }

    fn iLog(&self, message: &str, level: i32) {
        // Implement the iLog function here
    }
}
fn main() {
    println!("Hello world");
}
