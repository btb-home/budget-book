# launcher.py

import uvicorn

if __name__ == "__main__":
    try:
        host = "127.0.0.1"
        port = 8031
        print("Start the py app launcher at http://{}:{}".format(host, port))

        uvicorn.run(
            "app.main:app", 
            host=host,
            port=port,
            reload=True,
            log_config="conf/local/log.ini"
        )
    except KeyboardInterrupt as e:
        print("Exit the app launcher by KeyboardInterrupt")
    finally:
        exit(0)
