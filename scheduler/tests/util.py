"""
Test utilities
"""


def sort_by_name(dct):
    """
    Sort the dictionary of members by name
    """
    return sorted(dct, key=lambda k: k["name"])
