import toml
import logging

logger = logging.getLogger(__name__)


class Configuration:
    """
    Wrapper for toml configuation.

    A default configuration is provided.
    Settings can be overridden in user-config.toml.

    A user can also specify a different configuration file
    using the -c|--config <filename> CLI option

    """

    _instance = None
    _defaults_filename: str = ".defaults.toml"
    _override_filename: str = "user-config.toml"
    _config: dict = None

    @classmethod
    def _set_config(cls, filename=None) -> None:
        """
        Sets the instance configuration
        """

        # get default configuration
        cls._config = toml.load(cls._defaults_filename)
        user_override = toml.load(cls._override_filename)

        if filename is not None:
            # override with user provided file
            override = toml.load(filename)
            Configuration._config.update(override)
        else:
            # override with user-config.toml overrides
            cls._config.update(user_override)

    def __init__(self, config_file=None):
        print("test", __name__)
        if Configuration._instance is not None:
            raise Exception("Configuration error")
        else:
            if config_file is not None and config_file != "":
                logger.info("Override configuration provided: %s", config_file)
                self._set_config(config_file)
            else:
                logger.info(
                    "No override configuration provided. Using defaults")
                self._set_config()

            Configuration._instance = self

    @classmethod
    def config(cls, path=None, filename=None) -> dict:
        """
        Get instance of this client

        path: dot separated path to simplify access to nested tables
        """

        if cls._instance is None:
            Configuration(filename)

        # get nested table dictionaries
        if path is not None:
            path = path.split(".")
            data = Configuration._instance._config

            for p in path:
                data = data[p]

            return data

        return cls._instance._config
