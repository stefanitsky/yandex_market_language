class YMLException(Exception):
    """
    Basic error for the whole module.
    """
    pass


class ValidationError(YMLException):
    """
    Data validation exception.
    """
    pass


class ParseError(YMLException):
    """
    Base parse exception.
    """
    pass


# class UnsupportedField(ParseError):
#     """
#     Unsupported field exception for parsing.
#     """
#     def __init__(self, cls, field):
#         self.cls = cls
#         self.field = field
#
#     def __str__(self):
#         return "{cls} contains unsupported field {field}".format(
#             cls=self.cls.__name__, field=self.field
#         )
