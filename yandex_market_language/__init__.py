"""
Top-level package for Yandex Market Language (YML) for Python.
"""

__author__ = """Alexandr Stefanitsky-Mozdor"""
__email__ = "stefanitsky.mozdor@gmail.com"
__version__ = "__version__ = '0.6.0'"


from .yml import parse, convert


__all__ = ["parse", "convert"]
