import sys
import os
import json
from logging import LoggerAdapter
from logging import getLogger as logging_get_logger
from logging.config import dictConfig as logging_config_dict
from unittest import TestSuite, TestCase, TestLoader, TextTestRunner, TextTestResult
from pathlib import Path

class _TestApplication:
    """
    _TestApplication class.
    """
    __logger: LoggerAdapter = LoggerAdapter(logger=logging_get_logger('.'.join([__name__, __qualname__])))

    @classmethod
    def get_test_suite(cls, testNamePatterns: list[str] = None) -> TestSuite:
        try:
            test_loader: TestLoader = TestLoader()
            test_loader.testNamePatterns = testNamePatterns
            test_suite: TestSuite = test_loader.discover(start_dir=Path(__file__).parent.as_posix())
            return test_suite
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def list_test_suite(cls, input: object, result: list[str] = []) -> list[str]:
        try:
            if isinstance(input, (TestSuite, TestCase)):
                for v in input:
                    if isinstance(v, TestSuite):
                        result = cls.list_test_suite(input=v, result=result)
                    elif isinstance(v, TestCase):
                        test_module_name: str = f"{v.__class__.__module__}"
                        if test_module_name not in result:
                            result.append(test_module_name)
                        test_class_name: str = f"{test_module_name}.{v.__class__.__name__}"
                        if test_class_name not in result:
                            result.append(test_class_name)
                        result.append(f"{test_class_name}.{v._testMethodName}")
            return result
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def run(cls, args: list[str] = None, logging_dict: dict[str, object] = None) -> tuple[int, str]:
        try:
            list_only: bool = False
            format_txt: bool = False
            logging_file: str = None
            patterns: list[str] = []
            if isinstance(args, list):
                list_only = '--list' in args or '-l' in args
                format_txt = '--format=txt' in args
                logging_prefix: str = '--logging-json='
                logging_prefix_len: int = len(logging_prefix)
                pattern_prefix_1: str = '-k='
                pattern_prefix_1_len: int = len(pattern_prefix_1)
                pattern_prefix_2: str = '--pattern='
                pattern_prefix_2_len: int = len(pattern_prefix_2)
                for v in args:
                    if v.startswith(logging_prefix):
                        v_sub_str: str = v[logging_prefix_len:].strip()
                        if v_sub_str:
                            logging_file = v_sub_str
                    if v.startswith(pattern_prefix_1):
                        v_sub_str: str = v[pattern_prefix_1_len:].strip()
                        if v_sub_str:
                            patterns.append(v_sub_str)
                    if v.startswith(pattern_prefix_2):
                        v_sub_str: str = v[pattern_prefix_2_len:].strip()
                        if v_sub_str:
                            patterns.append(v_sub_str)
                if not patterns:
                    patterns = None
            if isinstance(logging_dict, dict):
                logging_config_dict(logging_dict)
            else:
                if logging_file:
                    logging_content: str = Path(logging_file).read_bytes().decode()
                    logging_dict = json.loads(logging_content)
                    logging_config_dict(logging_dict)
            test_suite: TestSuite = cls.get_test_suite(testNamePatterns=patterns)
            if list_only:
                list_output: list[str] = cls.list_test_suite(input=test_suite)
                exit_code: int = 0
                output: str = os.linesep.join(list_output) if format_txt else json.dumps(list_output, indent=4)
                return (exit_code, output)
            else:
                test_runner: TextTestRunner = TextTestRunner(verbosity=2)
                test_result: TextTestResult = test_runner.run(test_suite)
                exit_code: int = 0 if test_result.wasSuccessful() else 1
                return (exit_code, None)
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

if __name__ == '__main__':
    args: list[str] = sys.argv[1:]
    exit_code, output = _TestApplication.run(args=args)
    if output:
        print(output)
    raise SystemExit(exit_code)
