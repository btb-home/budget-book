import json
from typing import List, Optional
from app.core.databases import redis_db

def delete_redis(key: str) -> None:
    """
    주어진 키에 해당하는 Redis 데이터를 삭제합니다.
    
    :param key: 삭제할 Redis 키
    """
    if redis_db.exists(key):
        redis_db.delete(key)

def set_redis(key: str, value: dict) -> None:
    """
    주어진 키에 데이터를 JSON 형식으로 Redis에 저장합니다.
    
    :param key: 저장할 Redis 키
    :param value: 저장할 데이터 (딕셔너리)
    """
    redis_db.set(key, json.dumps(value))

def get_redis(key: str) -> Optional[List[dict]]:
    """
    주어진 키에 해당하는 데이터를 Redis에서 가져옵니다.
    데이터가 없으면 None을 반환합니다.
    
    :param key: 가져올 Redis 키
    :return: Redis에서 가져온 데이터 (없으면 None)
    """
    if redis_db.exists(key):
        return json.loads(redis_db.get(key))
    return None

def next_seq(seq_name: str) -> int:
    """
    주어진 시퀀스 이름에 대해 Redis에서 값을 증가시켜 반환합니다.
    
    :param seq_name: 시퀀스 이름
    :return: 증가된 시퀀스 값
    """
    return redis_db.incr(seq_name)

def lock() -> bool:
    """
    Redis에 'lock' 키가 없으면 설정하여 락을 걸고, 있으면 False를 반환합니다.
    
    :return: 락을 설정할 수 있으면 True, 아니면 False
    """
    return redis_db.setnx("lock", 1)

def unlock() -> None:
    """
    Redis에서 'lock' 키를 삭제하여 락을 해제합니다.
    """
    delete_redis("lock")

def ping() -> str:
    """
    Redis 서버에 ping을 보내어 응답을 확인합니다.
    
    :return: Redis 서버 응답
    """
    return redis_db.ping()