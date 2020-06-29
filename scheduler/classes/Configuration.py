import toml
import logging

logger = logging.getLogger(__name__)


class Configuration:
    """
    Wrapper for toml configuation.

    A default configuration is provided.
    Settings can be overriden in user-config.toml.

    A user can also specify a different configuration file
    using the -c|--config <filename> CLI option

    TODO: isntance exists check
    """

    __instance = None
    __defaults_filename = "defaults.toml"
    __override_filename = "user-config.toml"
    __config = None

    @staticmethod
    def __set_config(filename=None):
        """
        Sets the instance configuration
        """

        Configuration.__config = toml.load(Configuration.__defaults_filename)
        user_override = toml.load(Configuration.__override_filename)

        if not filename == None:
            override = toml.load(filename)
            Configuration.__config.update(override)
        else:
            Configuration.__config.update(user_override)

    def __init__(self, config_file=None):
        if Configuration.__instance != None:
            raise Exception("Configuration error")
        else:
            if not config_file == None and not config_file == "":
                logger.info("Override configuration provided: %s", config_file)
                self.__set_config(config_file)
            else:
                logger.info("No override configuration provided. Using defaults")
                self.__set_config()

            Configuration.__instance = self

    @staticmethod
    def config(filename=None):
        """
        Get instance of this client
        """

        if Configuration.__instance == None:
            Configuration(filename)
        return Configuration.__instance.__config
