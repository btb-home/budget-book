from fastapi import Request


def get_client_ip(request: Request) -> str:
    """
    클라이언트의 IP 주소를 반환하는 함수.
    """
    if request.headers.get("X-Forwarded-For"):
        client_ip = request.headers.get("X-Forwarded-For")
        client_ip = client_ip[: client_ip.find(",")] if "," in client_ip else client_ip
    else:
        client_ip = request.client.host

    return client_ip
