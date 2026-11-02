from logging import LoggerAdapter
from logging import getLogger as logging_get_logger

from unittest import TestCase

from _test_utils import _TestUtils

from exqudens.example import Example, CalculatorService

class TestCalculatorService(TestCase):
    """
    TestCalculatorService class.
    """
    __logger: LoggerAdapter = LoggerAdapter(logger=logging_get_logger('.'.join([__name__, __qualname__])))

    def test_1(self) -> None:
        self.__logger.info("bgn")

        example: Example = Example()
        self.__logger.info(f"example: {isinstance(example, Example)}")

        self.assertTrue(isinstance(example, Example))

        calculator_service: CalculatorService = example.get_calculator_service()
        self.__logger.info(f"calculator_service: {isinstance(calculator_service, CalculatorService)}")

        self.assertTrue(isinstance(calculator_service, CalculatorService))

        schedule: list[dict[str, str]] = calculator_service.generate_amortization(
            principal=1000,
            annual_rate=10.0,
            months=12
        )
        self.__logger.info(f"schedule.size: {len(schedule)}")
        for i, v in enumerate(schedule):
            self.__logger.info(f"schedule[{i}]: {v}")

        self.assertTrue(len(schedule) == 12)

        self.__logger.info("end")
