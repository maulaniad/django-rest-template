from logging import getLogger

from rest_framework.test import APITestCase as _APITestCase


logger = getLogger(__name__)

class APITestCase(_APITestCase):
    fixtures = []

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self):
        outcome = self._outcome  # type: ignore
        test_result = outcome.result

        errors = self._get_error_list(test_result.errors)
        failures = self._get_error_list(test_result.failures)

        if errors:
            logger.error(f">> {self._testMethodName}: ERROR")
        elif failures:
            logger.warning(f">> {self._testMethodName}: FAIL")
        else:
            logger.info(f">> {self._testMethodName}: PASS")

    def _get_error_list(self, error_list):
        current_test = self._testMethodName
        return [error for test, error in error_list if test._testMethodName == current_test]
