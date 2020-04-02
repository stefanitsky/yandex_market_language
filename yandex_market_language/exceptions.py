class YMLException(Exception):
    """
    Basic error for the whole module.
    """
    pass


class ValidationError(YMLException):
    """
    Error for data validation exceptions for models.
    """
    pass
