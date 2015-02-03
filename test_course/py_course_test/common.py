#!/bin/env python
# -*- coding: utf-8 -*-
"""
Common classes and properties for tests
"""


class TestResultList(list):
    """
    Wrap a list of tests into an categorical list
    """
    def __init__(self, list_description, *args):
        """
        Initialize class with list_description property fo
        display in test results
        """
        self.list_description = list_description
        super(TestResultList, self).__init__(args)


class TestResult(object):
    """Simple class to wrap test results in.
    """
    def __init__(
            self, test_description=None, result=False, fail=True, value=None
    ):
        """Initialize the class with optional properties

        Args:
            test_description (str): String to use display describing test
            result (bool): Whether the test was successfull
            fail (bool): Whether the failure should fail everything,
                         or just warn.
            value (str): Optional string to show
        """
        self.test_description = test_description
        self.result = result
        self.fail = fail
        self.value = value


