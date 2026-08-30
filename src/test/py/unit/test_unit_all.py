from logging import LoggerAdapter
from logging import getLogger as logging_get_logger

from unittest import TestCase

from _test_utils import _TestUtils

from exqudens.example import Example

class TestUnitAll(TestCase):
    """
    TestUnitAll class.
    """
    __logger: LoggerAdapter = LoggerAdapter(logger=logging_get_logger('.'.join([__name__, __qualname__])))

    def test_1(self) -> None:
        self.__logger.info("bgn")

        project_dir: str = _TestUtils.get_project_dir()
        self.__logger.info(f"project_dir: '{project_dir}'")

        expected: int = 111
        actual: int = int(input("AAA: ").strip())

        self.assertEqual(expected, actual)

        self.__logger.info("end")

    def test_2(self) -> None:
        try:
            self.__logger.info("bgn")

            project_dir: str = _TestUtils.get_project_dir()
            self.__logger.info(f"project_dir: '{project_dir}'")

            expected: dict[str, object] = {
                'root': {
                    'item': 'Hello'
                }
            }
            self.__logger.info(f"expected: {expected}")

            actual: dict[str, object] = Example.xml_to_dict("<root><item>Hello</item></root>")
            self.__logger.info(f"actual: {actual}")

            self.assertEqual(expected, actual)

            self.__logger.info("end")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e
