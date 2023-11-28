import unittest


class TestsResult:

    _results = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._results = unittest.TextTestRunner()._makeResult()

    def error_add(self):
        test = TestCaseSub()
        err = (None, None, None)
        self._results.errors.append(
            (
                test,
                self._results._exc_info_to_string(err, test)
            )
        )

    def failure_add(self):
        test = TestCaseSub()
        err = (None, None, None)
        self._results.failures.append(
            (
                test,
                self._results._exc_info_to_string(err, test)
            )
        )

    @property
    def results(self):
        return self._results

    def skip_add(self):
        test = TestCaseSub()
        self._results.skipped.append(
            (
                test,
                'intentionally skipped for unit test'
            )
        )

    def success_add(self):
        test = TestCaseSub()
        self._results.addSuccess(test)


class TestCaseSub(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def runTest(self):
        pass


if __name__ == '__main__':
    unittest.main()
