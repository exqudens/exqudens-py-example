from logging import LoggerAdapter
from logging import getLogger as logging_get_logger

from exqudens.example.service.xml_service import XmlService
from exqudens.example.service.calculator_service import CalculatorService

class Example:
    """
    Example class.
    """
    __logger: None | LoggerAdapter = None
    __xml_service: None | XmlService = None
    __calculator_service: None | CalculatorService = None

    def __init__(
        self,
        xml_service: None | XmlService | object = None,
        calculator_service: None | CalculatorService | object = None,
        logger: None | LoggerAdapter | object = None
    ) -> None:
        try:
            if isinstance(logger, LoggerAdapter):
                self.__logger = logger
            else:
                self.__logger = LoggerAdapter(logger=logging_get_logger(f"{self.__module__}.{self.__class__.__name__}"))

            if isinstance(xml_service, XmlService):
                self.__xml_service = xml_service
            else:
                self.__xml_service = XmlService()

            if isinstance(calculator_service, CalculatorService):
                self.__calculator_service = calculator_service
            else:
                self.__calculator_service = CalculatorService()
        except Exception as e:
            if isinstance(self.__logger, LoggerAdapter): self.__logger.error(e, exc_info=True)
            raise e

    def get_xml_service(self) -> XmlService:
        try:
            if not isinstance(self.__xml_service, XmlService):
                raise Exception(f"'self.__xml_service' is not an instance of '{XmlService.__class__.__name__}'")
            return self.__xml_service
        except Exception as e:
            if isinstance(self.__logger, LoggerAdapter): self.__logger.error(e, exc_info=True)
            raise e

    def get_calculator_service(self) -> CalculatorService:
        try:
            if not isinstance(self.__calculator_service, CalculatorService):
                raise Exception(f"'self.__calculator_service' is not an instance of '{CalculatorService.__class__.__name__}'")
            return self.__calculator_service
        except Exception as e:
            if isinstance(self.__logger, LoggerAdapter): self.__logger.error(e, exc_info=True)
            raise e
