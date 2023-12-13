import os
import sys
import platform
import logging
from loguru import logger


log_level = "INFO"
retention_time = "14 days"


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = log_level

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# 配置日志路径
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "SteganographyExtraction")
# 配置日志格式
log_format = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | Process: {process} | {file}:{line} | {message}"
log_config = {"rotation": "00:00:00", "format": log_format, "enqueue": True,
              "retention": retention_time, "compression": "zip"}
# 设置日志输出
logger.add("{}_{{time:YYYY-MM-DD}}.log".format(log_path), backtrace=True, diagnose=True,
           level=log_level, **log_config)


if __name__ == "__main__":
    logger.debug('this is a debug message')
    logger.info('this is info message')
    logger.success('this is success message!')
    logger.warning('this is warning message')
    logger.error('this is error message')
    logger.critical('this is critical message!')
