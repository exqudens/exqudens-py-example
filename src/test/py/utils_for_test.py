from logging import LoggerAdapter
from logging import getLogger as logging_get_logger
from pathlib import Path

class UtilsForTest:
    """
    UtilsForTest class.
    """
    __logger: LoggerAdapter = logging_get_logger('.'.join([__name__, __qualname__]))

    @classmethod
    def get_project_dir(cls) -> str:
        try:
            return Path(__file__).parent.parent.parent.parent.as_posix()
        except Exception as e:
            cls.__logger.info(e, exc_info=True)
            raise e
