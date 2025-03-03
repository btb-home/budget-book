from fastapi import Request

def get_client_host_ip(request: Request) -> str:
    """
    클라이언트의 IP 주소를 반환하는 함수.
    """
    if request.headers.get('X-Forwarded-For'):
        client_host = request.headers.get('X-Forwarded-For')
        client_host = client_host[:client_host.find(',')] if ',' in client_host else client_host
    else:
        client_host = request.client.host        
    
    return request.client.host