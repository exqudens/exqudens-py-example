from logging import LoggerAdapter
from logging import getLogger as logging_get_logger

from xmltodict import parse as xmltodict_parse

class XmlService:
    """
    XmlService class.
    """
    __logger: None | LoggerAdapter = None

    def __init__(
        self,
        logger: None | LoggerAdapter | object = None
    ) -> None:
        try:
            if isinstance(logger, LoggerAdapter):
                self.__logger = logger
            else:
                self.__logger = LoggerAdapter(logger=logging_get_logger(f"{self.__module__}.{self.__class__.__name__}"))
        except Exception as e:
            if isinstance(self.__logger, LoggerAdapter): self.__logger.error(e, exc_info=True)
            raise e

    def xml_to_dict(self, input: str) -> dict[str, object]:
        try:
            if not isinstance(input, str):
                raise Exception("'input' is not an instance of 'str'")
            return xmltodict_parse(input)
        except Exception as e:
            if isinstance(self.__logger, LoggerAdapter): self.__logger.error(e, exc_info=True)
            raise e
