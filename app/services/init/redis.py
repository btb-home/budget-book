import asyncio
from app.common.logging.logger import LOGGER
from app.utils.extensions.redis import lock, unlock, ping

async def init_redis_data():
    # 동기적으로 lock을 확인하고 처리
    if ping():
        LOGGER.info("Redis Ping OK")
    else:
        raise Exception("Redis Ping Fail")

    
    LOGGER.info("Redis Locking")
    if lock():
        LOGGER.info("Redis Lock acquired")
        try:
            # 데이터 초기화 작업을 위한 더미 async 작업 추가
            await load_init_redis_data()  # 비동기적으로 처리되는 부분
        except Exception as e:
            LOGGER.error(f"Locking error: {e}")
            raise e
        finally:
            unlock()  # 동기적으로 unlock
            LOGGER.info("Redis Unlock")
                
async def load_init_redis_data():
    """
    Redis에 초기 데이터를 로드하는 함수
    """
    LOGGER.info("Loading initial data to Redis")
    # Redis에 초기 데이터를 로드하는 비동기 작업
    await asyncio.sleep(1)
    
async def load_init_data(data_id):
    
    return 