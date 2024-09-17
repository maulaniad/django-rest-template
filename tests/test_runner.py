from types import TracebackType
from unittest import TestCase, TextTestResult

from django.test.runner import DiscoverRunner


class TestRunner(DiscoverRunner):
    def get_resultclass(self):
        class NoDotTextTestResult(TextTestResult):
            def addSuccess(self, test):
                """Supress Output"""
                pass

            def addError(self, test: TestCase, err: tuple[type[BaseException], BaseException, TracebackType] | tuple[None, None, None]) -> None:
                super().addError(test, err)

            def addFailure(self, test: TestCase, err: tuple[type[BaseException], BaseException, TracebackType] | tuple[None, None, None]) -> None:
                super().addFailure(test, err)

            def addSkip(self, test: TestCase, reason: str) -> None:
                super().addSkip(test, reason)

        return NoDotTextTestResult
