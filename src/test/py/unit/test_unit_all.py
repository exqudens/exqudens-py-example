from logging import LoggerAdapter
from logging import getLogger as logging_get_logger

from utils_for_test import UtilsForTest

from exqudens.example import Example

class TestUnitAll:
    """
    TestUnitAll class.
    """
    __logger: LoggerAdapter = LoggerAdapter(logger=logging_get_logger('.'.join([__name__, __qualname__])))

    def test_1(self) -> None:
        try:
            self.__logger.info("bgn")

            project_dir: str = UtilsForTest.get_project_dir()
            self.__logger.info(f"project_dir: '{project_dir}'")

            actual: dict[str, object] = Example.xml_to_dict("<root><item>Hello</item></root>")
            self.__logger.info(f"actual: {actual}")

            self.__logger.info("end")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e
