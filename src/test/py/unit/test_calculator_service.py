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

        expected_months: int = 12
        schedule: list[dict[str, str]] = calculator_service.generate_amortization(
            principal=1000,
            annual_rate=10.0,
            months=expected_months,
            extra_principal_schedule={
                3: 10,
                6: 20,
                9: 30
            }
        )
        self.__logger.info(f"schedule.size: {len(schedule)}")
        schedule_as_string: str = ''
        for i, v in enumerate(schedule):
            schedule_as_string += '\n'
            schedule_as_string += f"[{i}]: {v}"

        self.__logger.info(f"schedule: {schedule_as_string}")

        self.assertTrue(len(schedule) == expected_months)

        self.__logger.info("end")
