import asyncio
from app.core.logger import LOGGER
from app.utils.database.redis import redis_client
from app.common.exceptions.systems import RedisSystemException, RedisInitDataException


async def init_redis_data():
    """
    Redis 데이터 초기화 작업을 수행하는 함수입니다.

    이 함수는 Redis 서버와의 연결 상태를 확인하고, 데이터 초기화 작업을 수행하기 전에
    Redis에 락(lock)을 걸어 다른 프로세스에서 동시에 작업을 수행하지 않도록 합니다.

    초기화 작업은 비동기적으로 수행되며, 작업 도중 오류가 발생하면 예외가 발생하고
    로그에 기록됩니다. 작업이 끝나면 반드시 락을 해제하여 다른 프로세스가 Redis 작업을
    실행할 수 있도록 합니다.

    1. Redis 서버의 핑을 확인하여 연결 상태 점검
    2. 락을 설정하여 다른 프로세스와의 충돌 방지
    3. 비동기적으로 Redis 데이터 초기화 작업 수행
    4. 예외 발생 시 오류를 로그에 기록하고, 락을 해제하여 작업이 완료되었음을 알림
    """
    if not redis_client.ping():
        raise RedisSystemException("Redis Ping Fail")

    LOGGER.info("[Redis] Ping OK")

    if redis_client.lock():
        LOGGER.info("[Redis] Lock for Init Data")

        try:
            # 비동기적으로 데이터 초기화 작업 수행
            await _init_redis_data()
        except Exception as e:
            LOGGER.error(f"{e}")
            raise RedisInitDataException()
        finally:
            redis_client.unlock()
            LOGGER.info("[Redis] Unlock for Init Data")
    else:
        LOGGER.error("[Redis] Lock Fail")
        redis_client.unlock()
        LOGGER.error("[Redis] Unlockking")


async def cleanup_redis():
    """
    Redis 락을 해제하고 초기화 데이터를 위한 잠금을 풀어주는 함수.

    시스템 종료 시 락을 해제하여 다른 프로세스가 락을 얻을 수 있도록 합니다.
    """

    # Redis에서 락 해제
    redis_client.unlock()
    LOGGER.info("[Redis] Redis lock 해제 완료")


async def _init_redis_data():
    """
    Redis에 초기 데이터를 로드하는 함수
    """
    LOGGER.info("[Redis] Loading initial data to Redis")
    # Redis에 초기 데이터를 로드하는 비동기 작업
    await asyncio.sleep(1)
