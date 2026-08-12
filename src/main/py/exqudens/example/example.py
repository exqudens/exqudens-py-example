from logging import LoggerAdapter
from logging import getLogger as logging_get_logger

from xmltodict import parse as xmltodict_parse

class Example:
    """
    Example class.
    """
    __logger: LoggerAdapter = LoggerAdapter(logger=logging_get_logger('.'.join([__name__, __qualname__])))

    @classmethod
    def xml_to_dict(cls, input: str) -> dict[str, object]:
        try:
            if not isinstance(input, str):
                raise Exception("'input' is not an instance of 'str'")

            return xmltodict_parse(input)
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e
