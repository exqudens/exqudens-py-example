import sys
import inspect
import subprocess
from subprocess import CompletedProcess
import shutil
import logging
from logging import LoggerAdapter
from logging import getLogger as logging_get_logger
from logging.config import dictConfig as logging_config_dict
from argparse import ArgumentParser
from argparse import Namespace
from pathlib import Path
from pip._vendor import tomli

class Project:
    """
    Project class.
    """
    __logger: None | LoggerAdapter = None
    __help_message: None | str = None
    __subprocess_timeout: None | int = None
    __commands: None | list[str] = None
    __project_dir: str = Path(__file__).parent.absolute().as_posix()

    def __init__(
        self,
        help_message: None | str | object,
        namespace: None | Namespace | object,
        logger: None | LoggerAdapter | object = None
    ) -> None:
        try:
            if logger is not None and isinstance(logger, LoggerAdapter):
                self.__logger = logger
            else:
                self.__logger = logging_get_logger('.'.join([self.__module__, self.__class__.__name__]))

            self.__help_message = help_message

            if namespace is not None:
                self.__subprocess_timeout = namespace.subprocess_timeout if namespace.subprocess_timeout > 0 else None
                self.__commands = [namespace.commands] if isinstance(namespace.commands, str) else namespace.commands
        except Exception as e:
            if self.__logger: self.__logger.error(e, exc_info=True)
            raise e

    def help(self) -> None:
        try:
            self.__logger.info(self.__help_message)
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def env(self) -> None:
        try:
            project_dir: str = Path(self.__project_dir).as_posix()
            build_dir: str = Path(project_dir).joinpath('build').as_posix()
            env_dir: str = Path(build_dir).joinpath('env').as_posix()

            if Path(env_dir).exists():
                return None

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ...")

            # create env
            cmd: list[str] = [
                sys.executable,
                '-m', 'venv',
                env_dir
            ]
            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] execute: {cmd}")
            subprocess.run(
                cmd,
                cwd=project_dir,
                text=True,
                check=True,
                capture_output=False,
                timeout=self.__subprocess_timeout
            )

            # install dependencies
            project_toml: dict[str, object] = tomli.loads(Path(project_dir).joinpath('pyproject.toml').read_bytes().decode())
            requirements: list[str] = project_toml.get('project', dict()).get('dependencies', list())
            if not requirements:
                return None
            requirements_content: str = '\n'.join(requirements)
            requirements_file: str = Path(env_dir).joinpath('requirements.txt').as_posix()
            Path(requirements_file).write_bytes(requirements_content.encode())
            python_file: str = self._find_python(dir=env_dir)
            cmd = [
                python_file,
                '-m', 'pip', 'install',
                '--trusted-host', 'pypi.org',
                '--trusted-host', 'pypi.python.org',
                '--trusted-host', 'files.pythonhosted.org',
                '-r', requirements_file
            ]
            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] execute: {cmd}")
            subprocess.run(
                cmd,
                cwd=project_dir,
                text=True,
                check=True,
                capture_output=False,
                timeout=self.__subprocess_timeout
            )

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ... done")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def clean_env(self) -> None:
        try:
            project_dir: str = Path(self.__project_dir).as_posix()
            build_dir: str = Path(project_dir).joinpath('build').as_posix()
            env_dir: str = Path(build_dir).joinpath('env').as_posix()

            if not Path(env_dir).exists():
                return None

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ...")

            shutil.rmtree(env_dir)

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ... done")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def package(self) -> None:
        try:
            project_dir: str = Path(self.__project_dir).as_posix()
            build_dir: str = Path(project_dir).joinpath('build').as_posix()
            env_dir: str = Path(build_dir).joinpath('env').as_posix()
            dist_dir: str = Path(build_dir).joinpath('dist').as_posix()

            if Path(dist_dir).exists():
                return None

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ...")

            # create package
            python_file: str = self._find_python(dir=env_dir)
            cmd = [
                python_file,
                '-m', 'pip', 'wheel',
                '--no-deps',
                '-w', dist_dir,
                '--trusted-host', 'pypi.org',
                '--trusted-host', 'pypi.python.org',
                '--trusted-host', 'files.pythonhosted.org',
                '.'
            ]
            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] execute: {cmd}")
            subprocess.run(
                cmd,
                cwd=project_dir,
                text=True,
                check=True,
                capture_output=False,
                timeout=self.__subprocess_timeout
            )

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ... done")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def clean_package(self) -> None:
        try:
            project_dir: str = Path(self.__project_dir).as_posix()
            build_dir: str = Path(project_dir).joinpath('build').as_posix()
            dist_dir: str = Path(build_dir).joinpath('dist').as_posix()

            if not Path(dist_dir).exists():
                return None

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ...")

            shutil.rmtree(dist_dir)

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ... done")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def test_env(self) -> None:
        try:
            project_dir: str = Path(self.__project_dir).as_posix()
            build_dir: str = Path(project_dir).joinpath('build').as_posix()
            test_dir: str = Path(build_dir).joinpath('test').as_posix()
            env_dir: str = Path(test_dir).joinpath('env').as_posix()

            if Path(env_dir).exists():
                return None

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ...")

            # create env
            cmd: list[str] = [
                sys.executable,
                '-m', 'venv',
                env_dir
            ]
            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] execute: {cmd}")
            subprocess.run(
                cmd,
                cwd=project_dir,
                text=True,
                check=True,
                capture_output=False,
                timeout=self.__subprocess_timeout
            )

            # install dependencies
            project_toml: dict[str, object] = tomli.loads(Path(project_dir).joinpath('pyproject.toml').read_bytes().decode())
            requirements: list[str] = project_toml.get('project', dict()).get('dependencies', list())
            requirements.extend(project_toml.get('project', dict()).get('optional-dependencies', dict()).get('test', list()))
            if not requirements:
                return None
            requirements_content: str = '\n'.join(requirements)
            requirements_file: str = Path(env_dir).joinpath('requirements.txt').as_posix()
            Path(requirements_file).write_bytes(requirements_content.encode())
            python_file: str = self._find_python(dir=env_dir)
            cmd = [
                python_file,
                '-m', 'pip', 'install',
                '--trusted-host', 'pypi.org',
                '--trusted-host', 'pypi.python.org',
                '--trusted-host', 'files.pythonhosted.org',
                '-r', requirements_file
            ]
            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] execute: {cmd}")
            subprocess.run(
                cmd,
                cwd=project_dir,
                text=True,
                check=True,
                capture_output=False,
                timeout=self.__subprocess_timeout
            )

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ... done")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def update_test_env(self) -> None:
        try:
            project_dir: str = Path(self.__project_dir).as_posix()
            build_dir: str = Path(project_dir).joinpath('build').as_posix()
            test_dir: str = Path(build_dir).joinpath('test').as_posix()
            env_dir: str = Path(test_dir).joinpath('env').as_posix()
            dist_dir: str = Path(build_dir).joinpath('dist').as_posix()

            if not Path(env_dir).exists():
                raise Exception(f"not exists '{env_dir}'")

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ...")

            # install dependencies
            python_file: str = self._find_python(dir=env_dir)
            package_files: list[str] = [v.as_posix() for v, _, _ in Path(dist_dir).rglob('*.whl')]
            cmd = [
                python_file,
                '-m', 'pip', 'install',
                '--no-deps',
                '--trusted-host', 'pypi.org',
                '--trusted-host', 'pypi.python.org',
                '--trusted-host', 'files.pythonhosted.org'
            ]
            cmd.extend(package_files)
            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] execute: {cmd}")
            subprocess.run(
                cmd,
                cwd=project_dir,
                text=True,
                check=True,
                capture_output=False,
                timeout=self.__subprocess_timeout
            )

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ... done")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def clean_test_env(self) -> None:
        try:
            project_dir: str = Path(self.__project_dir).as_posix()
            build_dir: str = Path(project_dir).joinpath('build').as_posix()
            test_dir: str = Path(build_dir).joinpath('test').as_posix()
            env_dir: str = Path(test_dir).joinpath('env').as_posix()

            if not Path(env_dir).exists():
                return None

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ...")

            shutil.rmtree(env_dir)

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ... done")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def test(self) -> None:
        try:
            project_dir: str = Path(self.__project_dir).as_posix()
            build_dir: str = Path(project_dir).joinpath('build').as_posix()
            test_dir: str = Path(build_dir).joinpath('test').as_posix()
            env_dir: str = Path(test_dir).joinpath('env').as_posix()

            if not Path(env_dir).exists():
                raise Exception(f"not exists '{env_dir}'")

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ...")

            # test
            python_file: str = self._find_python(dir=env_dir)
            cmd = [
                python_file,
                '-m', 'pytest'
            ]
            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] execute: {cmd}")
            subprocess.run(
                cmd,
                cwd=project_dir,
                text=True,
                check=True,
                capture_output=False,
                timeout=self.__subprocess_timeout
            )

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ... done")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def clean_test(self) -> None:
        try:
            project_dir: str = Path(self.__project_dir).as_posix()
            build_dir: str = Path(project_dir).joinpath('build').as_posix()
            test_dir: str = Path(build_dir).joinpath('test').as_posix()
            out_dir: str = Path(test_dir).joinpath('out').as_posix()

            if not Path(out_dir).exists():
                return None

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ...")

            shutil.rmtree(out_dir)

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ... done")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def clean(self) -> None:
        try:
            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ...")

            self.clean_test()
            self.clean_test_env()
            self.clean_package()
            self.clean_env()

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ... done")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def vscode(self) -> None:
        try:
            self.env()
            self.test_env()

            project_dir: str = Path(self.__project_dir).as_posix()
            build_dir: str = Path(project_dir).joinpath('build').as_posix()
            test_dir: str = Path(build_dir).joinpath('test').as_posix()
            env_dir: str = Path(test_dir).joinpath('env').as_posix()
            launch_template_file: str = Path(project_dir).joinpath('src', 'test', 'resources', 'vscode', 'launch.json').as_posix()
            launch_target_file: str = Path(project_dir).joinpath('.vscode', 'launch.json').as_posix()

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ...")

            launch_json: str = Path(launch_template_file).read_bytes().decode()
            python_file: str = self._find_python(dir=env_dir)
            launch_json = launch_json.replace('@_PYTHON@', Path(python_file).relative_to(project_dir).as_posix())

            # list tests
            cmd = [
                python_file,
                '-m', 'pytest', '-q', '--co'
            ]
            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] execute: {cmd}")
            list_tests_out: CompletedProcess[str] = subprocess.run(
                cmd,
                cwd=project_dir,
                text=True,
                check=True,
                capture_output=True,
                timeout=self.__subprocess_timeout
            )
            test_entries: list[str] = [
                "src/test/py"
            ]
            for v in list_tests_out.stdout.splitlines():
                line: str = str(v).strip()
                if not line:
                    break
                test_entries.append(line)
            if not test_entries:
                raise Exception(f"no tests found")
            launch_json = launch_json.replace('@_OPTIONS@', '",\n                "'.join(test_entries))
            launch_json = launch_json.replace('@_DEFAULT@', test_entries[0])

            Path(launch_target_file).parent.mkdir(parents=True, exist_ok=True)
            Path(launch_target_file).write_bytes(launch_json.encode())

            self.__logger.info(f"-- [{inspect.currentframe().f_code.co_name}] ... done")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def _run(self) -> int:
        try:
            for command in self.__commands:
                method = getattr(self, command)
                if not method:
                    raise Exception(f"command not found: '{command}'")
                method()
            return 0
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def _find_python(self, dir: None | str | object) -> str:
        try:
            if dir is None:
                raise Exception("'dir' is none")
            if not isinstance(dir, str):
                raise Exception("'dir' is not an instance of 'str'")
            if len(dir) == 0:
                raise Exception("'dir' is empty")
            if not Path(dir).exists():
                raise Exception(f"not exists: '{dir}'")
            if not Path(dir).is_dir():
                raise Exception(f"is not a directory: '{dir}'")

            if Path(dir).joinpath('Scripts', 'python.exe').exists():
                return Path(dir).joinpath('Scripts', 'python.exe').as_posix()
            elif Path(dir).joinpath('bin', 'python').exists():
                return Path(dir).joinpath('bin', 'python').as_posix()
            else:
                raise Exception(f"unexpected condition")
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

if __name__ == '__main__':
    logger: None | LoggerAdapter = None
    try:
        sys_argv: None | list[str] | object = sys.argv[1:]
        avilable_commands: list[str] = [name for name, _ in inspect.getmembers(Project, predicate=inspect.isfunction) if not name.startswith('_')]
        parser: ArgumentParser = ArgumentParser()
        parser.add_argument(
            '-ll', '--log-level',
            nargs='?',
            type=str,
            choices=[
                logging.getLevelName(logging.DEBUG),
                logging.getLevelName(logging.INFO),
                logging.getLevelName(logging.WARNING),
                logging.getLevelName(logging.ERROR),
                logging.getLevelName(logging.FATAL)
            ],
            default=logging.getLevelName(logging.DEBUG),
            help=f"log level (default: %(default)s)"
        )
        parser.add_argument(
            '-st', '--subprocess-timeout',
            nargs='?',
            type=int,
            default=0,
            help=f"subprocess timeout in seconds (default: %(default)s)"
        )
        parser.add_argument(
            'commands',
            nargs='*',
            type=str,
            choices=avilable_commands,
            default='help',
            help='commands (default: %(default)s)'
        )
        namespace: Namespace = parser.parse_args(sys_argv)
        logging_config_dict({
            'version': 1,
            'formatters': {
                'formatter': {
                    'format': '%(message)s' # '%(asctime)s %(levelname)-4.4s [%(threadName)s] %(name)s %(funcName)s(%(filename)s:%(lineno)d): %(message)s'
                }
            },
            'handlers': {
                'handler': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'formatter',
                    'stream': 'ext://sys.stdout'
                }
            },
            'loggers': {
                'root': {
                    'level': logging.getLevelName(namespace.log_level),
                    'handlers': ['handler']
                }
            }
        })
        logger = logging_get_logger()
        project: Project = Project(
            help_message=parser.format_help(),
            namespace=namespace,
            logger=logger
        )
        raise SystemExit(project._run())
    except Exception as e:
        if logger: logger.error(e, exc_info=True)
        raise e
    except SystemExit as e:
        raise e
