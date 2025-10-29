from logging import LoggerAdapter
from logging import getLogger as logging_get_logger

class Example:
    """
    Example class.
    """
    __logger: LoggerAdapter = logging_get_logger('.'.join([__name__, __qualname__]))

    def __init__(self) -> None:
        try:
            pass
        except Exception as e:
            self.__logger.info(e, exc_info=True)
            raise e

    def xml_to_dict(self) -> dict[str, object]:
        try:
            pass
        except Exception as e:
            self.__logger.info(e, exc_info=True)
            raise e
