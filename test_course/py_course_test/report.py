#!/bin/env python
# -*- coding: utf-8 -*-
"""
Reporting for the test results
"""
from __future__ import print_function
import codecs
import os
import sys

from jinja2 import Environment


def report_results(results):
    """Output from a list of `class:TestResultList` objects and return false
    if any of them are critical.

    Args:
        results (list): List of `class:TestResult` classes

    Returns:
        bool: True if a critical failure was detected
    """
    print("\033[0;34mPython Test Results\033[0m")
    print("\033[0;34m{}\033[0m".format('=' * 78))
    failed = False
    for result_list in results:
        print('\033[0;34m{}\033[0m'.format(result_list.list_description))
        for result in result_list:
            if (not result.result) and result.fail:
                failed = True
            value = ''
            if result.value:
                value = ' [{}]'.format(result.value)
            print('{}{}: '.format(result.test_description, value),
                  end='')
            if result.result:
                print('\033[0;32mOK\033[0m')
            else:
                if result.fail:
                    print('\033[0;31mFAIL\033[0m')
                else:
                    print('\033[0;33mWARNING\033[0m')

    if failed:
        print('\033[0;31mCourse has critical issues. Tests failed\033[0m')

    return failed


def render_report_results(course, import_log):
    """Render jinja report for courses that have passed tests
    """

    course_key = u'{}'.format(
        course.location.course_key.to_deprecated_string()
    )

    jinja_environment = Environment()
    with open(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'templates',
                'report.j2'
            )
    ) as template_file:
        template = jinja_environment.from_string(template_file.read())
        UTF8Writer = codecs.getwriter('utf8')
        sys.stdout = UTF8Writer(sys.stdout)
        print(template.render({'course': course, 'course_key': course_key}))

    print('\033[0;33mPossible issues in course:\033[0m')
    print('==========================')
    for line in import_log.split('\n'):
        split_msg = line.split('|')
        if split_msg[0] in ('WARNING', 'ERROR', 'CRITICAL'):
            print(split_msg[1])

