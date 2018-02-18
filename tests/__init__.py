def run_once(func):
    """
        A function decorator to ensure load_tests() is ran only once. Otherwise the test discovery
        will discover the load_tests() functions more than once and add the tests to the test suite.
        run_once runs the wrapped function once, and then on subsequent runs it calls an empty
        function with three arguments that returns the second argument. This is necessary because
        load_tests() takes in the current tests as its second argument and returns the updated
        tests.
        Example:
        >>> @run_once
        ... def f(a, b, c):
        ...     return b + 2
        >>> f(1, 2, 3)
        4
        >>> f(1, 2, 3)
        2
        >>> f(1, 2, 3)
        2
    """

    def pass_through(loader, tests, ignore):
        """Pass through the TestSuite without adding test cases"""
        return tests

    def wrapper(*args, **kwargs):
        """Wraps `func` to ensure it is only called once"""
        if not wrapper.has_run:
            wrapper.has_run = True
            return func(*args, **kwargs)
        # Otherwise return an empty function
        return pass_through(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


def runtests(processes=4):
    """
        Run the hexgrid library's unit tests. Will run tests in parallel if the `concurrencytest`
        module is installed. Defaults to four processes.
        Example:
        >>> from tests import runtests
        >>> runtests()
        ...
    """
    import unittest
    loader = unittest.TestLoader()
    # Discover all tests in the current directory that are prefixed with `test`. Also discovers
    # the doctests loaded by defining a load_tests(...) function in each submodule's __init__.py
    suite = loader.discover('.', pattern='*test*.py')
    runner = unittest.runner.TextTestRunner()
    try:
        from concurrencytest import ConcurrentTestSuite, fork_for_tests
        concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(processes))
        runner.run(concurrent_suite)
    except ImportError:
        runner.run(suite)
    # Prevent calling sys.exit() just in case the user is running the tests from an interpreter.
    unittest.main(exit=False)
