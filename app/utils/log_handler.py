import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from datetime import datetime
from rich.logging import RichHandler  # RichHandler를 사용하여 콘솔 로그에 색상 추가

class SafeRotatingFileHandler(TimedRotatingFileHandler):
    """
    TimedRotatingFileHandler를 기반으로 하는 커스텀 로그 핸들러입니다.
    로그 디렉토리가 존재하지 않으면 생성하는 기능을 추가합니다.
    """
    def __init__(
        self, 
        log_dir: str,  # 로그 파일을 저장할 디렉토리 경로
        when: str = "midnight",  # 로그 롤오버 시점 (기본값: 자정)
        interval: int = 1,  # 롤오버 주기 (기본값: 1)
        backupCount: int = 30,  # 백업된 로그 파일의 개수 (기본값: 30)
        encoding: str | None = "utf-8",  # 로그 파일 인코딩 (기본값: utf-8)
        delay: bool = False,  # 로그 롤오버 지연 여부 (기본값: False)
        utc: bool = True,  # UTC 시간 사용 여부 (기본값: True)
        atTime: datetime | None = None  # 특정 시간에 롤오버를 수행하도록 지정 (기본값: None)
    ):
        # 로그 디렉토리가 존재하지 않으면 생성
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        filename = os.path.join(log_dir, "app.log")  # 로그 파일 경로 설정

        # 부모 클래스인 TimedRotatingFileHandler 초기화
        TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay, utc, atTime)

    def _format_filename(self) -> str:
        """
        로그 파일 이름을 포맷팅합니다.
        """
        return self.baseFilename
    
    def doRollover(self):
        """
        로그 파일을 롤오버하는 작업을 확장합니다.
        로그 파일을 새로 생성하고, 기존 로그 파일을 백업합니다. 
        또한, 서머타임(DST) 변경을 고려하여 롤오버 시점을 조정하며,
        지정된 백업 개수에 따라 오래된 로그 파일을 삭제합니다.
        """
        # 로그 파일 롤오버 시 기존 스트림을 닫고, 
        # 새로운 로그 파일로 기록을 시작하기 위한 준비 작업
        if self.stream:
            self.stream.close()
            self.stream = None

        # 롤오버 시점을 계산하여 새 로그 파일 이름을 결정하고, 
        # 서머타임(DST) 상태를 고려한 시간 조정을 수행하기 위한 과정        
        current_time = int(time.time())
        dst_now = time.localtime(current_time)[-1]  # 현재 시간의 DST 상태 (서머타임 여부)
        t = self.rolloverAt - self.interval
        
        if self.utc:
            # UTC 시간 사용 여부에 따른 시간 계산
            time_tuple = time.gmtime(t)
        else:
            # 로컬 시간과 DST(서머시간) 계산
            time_tuple = time.localtime(t)
            dst_then = time_tuple[-1]
            
            # DST 상태가 다르면 조정
            if dst_now != dst_then:
                if dst_now:
                    addend = 3600  # 서머타임이 적용되면 1시간 추가
                else:
                    addend = -3600  # 서머타임이 해제되면 1시간 차감
                time_tuple = time.localtime(t + addend)
        
        # 파일 이름 포맷을 바탕으로 새 롤오버된 파일 이름 생성
        dfn = self._format_filename() + "." + time.strftime(self.suffix, time_tuple)
        
        # 롤오버된 파일이 아직 없으면 기본 파일을 새 파일로 이름 변경
        if not os.path.exists(self.baseFilename) and not os.path.lexists(self.baseFilename):
            os.rename(self.baseFilename, dfn)

        # 롤오버된 파일 삭제
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)

        # 로그 스트림을 지연없이 엶
        if not self.delay:  
            self.mode = "a"
            self.stream = self._open()
        
        # 다음 롤오버 시점 계산
        # 다음 롤오버 시점이 현재보다 이전이면 다시 계산
        new_rollover_at = self.computeRollover(current_time)
        while new_rollover_at <= current_time:  
            new_rollover_at = new_rollover_at + self.interval
        
        # 자정 및 주간 롤오버 시 서머타임에 맞게 조정
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dst_at_rollover = time.localtime(new_rollover_at)[-1]
            # 서머타임 상태가 다르면 롤오버 시점 조정
            if dst_now != dst_at_rollover:  
                if not dst_now:
                    addend = -3600  # 서머타임 해제되면 1시간 차감
                else:
                    addend = 3600  # 서머타임 시작되면 1시간 추가
                new_rollover_at += addend

        # 새로운 롤오버 시점 설정
        self.rolloverAt = new_rollover_at  
