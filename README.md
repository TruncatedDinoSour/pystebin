# Pystebin

Simple, open source and minimal self-hosted pastebin

# Installing dependencies
```bash
python3 -m pip install --user -r requirements.txt
```

# Running
```bash
python3 app.py
```

# Configuring
- Configuration file
```bash
vim pysb/config.py
```

- Configuration options
    - **WEBSITE_NAME** is the displayed website name, by default it's dynamic and decides based on the directory name
    - **PASTE_DIR** is the directory name where all pastes go into, by default it's `pastes`
    - **MAX_PASTE_SIZE_B** is the max request size, by default it's one milion bytes
    - **HOST** is the host IP of the server, by default it's 127.0.0.1
    - **PORT** is the host IPs port of the server, by default it's 5050
    - **DEBUG** decides whether the server is in debug mode or not, by default it's `True`
    - **SECRET_KEY** is used to encrypt the connection and cookies, by default it's 20 milion random bytes
    - **MAX_PASTE_COUNT** is the maximum paste count which will destroy all pastes if a limit is reached, default there is no limit
    - **RequestLimiterConfig** is the configuration for [flask rate limiting](https://github.com/tabotkevin/flask_limit)

Other configuration options can be found in [pysb/config.py](/pysb/config.py)

# Screenshots
## Home page
![Home page](/screenshots/home.png)

## Paste page
![Paste](/screenshots/paste.png)

