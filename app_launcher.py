# launcher.py

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", 
        host="127.0.0.1",
        port=8031,
        reload=True,
        log_config="conf/local/log.ini"
    )
