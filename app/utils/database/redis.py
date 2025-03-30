import json
from typing import List, Optional

from app.core.databases import redis_db


class RedisClient:
    def __init__(self, db=redis_db):
        self.db = db

    def delete(self, key: str) -> None:
        """
        주어진 키에 해당하는 Redis 데이터를 삭제합니다.

        :param key: 삭제할 Redis 키
        """
        if self.db.exists(key):
            self.db.delete(key)

    def set(self, key: str, value: dict) -> None:
        """
        주어진 키에 데이터를 JSON 형식으로 Redis에 저장합니다.

        :param key: 저장할 Redis 키
        :param value: 저장할 데이터 (딕셔너리)
        """
        self.db.set(key, json.dumps(value))

    def get(self, key: str) -> Optional[List[dict]]:
        """
        주어진 키에 해당하는 데이터를 Redis에서 가져옵니다.
        데이터가 없으면 None을 반환합니다.

        :param key: 가져올 Redis 키
        :return: Redis에서 가져온 데이터 (없으면 None)
        """
        if self.db.exists(key):
            return json.loads(self.db.get(key))
        return None

    def next_seq(self, seq_name: str) -> int:
        """
        주어진 시퀀스 이름에 대해 Redis에서 값을 증가시켜 반환합니다.

        :param seq_name: 시퀀스 이름
        :return: 증가된 시퀀스 값
        """
        return self.db.incr(seq_name)

    def lock(self) -> bool:
        """
        Redis에 'lock' 키가 없으면 설정하여 락을 걸고, 있으면 False를 반환합니다.

        :return: 락을 설정할 수 있으면 True, 아니면 False
        """
        return self.db.setnx("lock", 1)

    def unlock(self) -> None:
        """
        Redis에서 'lock' 키를 삭제하여 락을 해제합니다.
        """
        self.delete("lock")

    def ping(self) -> str:
        """
        Redis 서버에 ping을 보내어 응답을 확인합니다.

        :return: Redis 서버 응답
        """
        return self.db.ping()


# RedisClient 인스턴스 생성
redis_client = RedisClient()
