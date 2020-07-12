""" A collection of utilties needed by several modules.

    Typical Usage Example:

    from util import get_version
    get_version()
"""

import logging
import json

logger = logging.getLogger(__name__)


def get_version() -> str:
    """ Return the version number of the program.
    
    Reads from the VERSION file for this information

    Returns:
        Returns a string of the version number or an error message
    """
    try:
        with open('VERSION') as version_file:
            version = version_file.read().strip()
    except:
        return "Error Getting Version Number"
    return version