from logging import LoggerAdapter
from logging import getLogger as logging_get_logger

from exqudens.example import Example

from utils_for_test import UtilsForTest

class TestUnitAll:
    """
    TestUnitAll class.
    """
    __logger: LoggerAdapter = logging_get_logger('.'.join([__name__, __qualname__]))

    def test_1(self) -> None:
        try:
            self.__logger.info("bgn")

            project_dir: str = UtilsForTest.get_project_dir()
            self.__logger.info(f"project_dir: '{project_dir}'")

            obj: Example = Example()
            obj.xml_to_dict()

            self.__logger.info("end")
        except Exception as e:
            self.__logger.info(e, exc_info=True)
            raise e
