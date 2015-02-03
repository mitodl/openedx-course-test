#!/bin/env python
# -*- coding: utf-8 -*-
"""
Import a course using the XMLModuleStore object given the
directory passed in. Attempt to parse the logging output
and print out a nice report of the results.

.. note::
  This needs to be run from wihtin the ``edx-platform``
  directory to function properly.
"""
from __future__ import print_function
from cStringIO import StringIO
import logging
import os
import sys

from xmodule.modulestore.xml import XMLModuleStore

from common import TestResult, TestResultList
from alt import check_alt_tags
from image import check_image
from captions import check_captions
from links import check_links
from report import report_results, render_report_results


def test_course(directory):

    """Import the course, run tests that require the course objects, and
    generate reports

    Args:
        directory (str): Path to directory that contains the course folders

    """

    # Add in student modules and settings
    sys.path.append('/build/edx-platform/')
    sys.path.append('/build/edx-platform/lms/djangoapps/')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lms.envs.test'

    # Setup logging level and capture stream
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    output = StringIO()
    handler = logging.StreamHandler(output)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(levelname)s|%(message)s'))
    root.addHandler(handler)

    modulestore = XMLModuleStore(directory)
    courses = modulestore.get_courses()
    # Validate we have one and only one course
    results = []

    import_test = TestResultList('Test Importability')
    result = TestResult('Course import success', True)
    if len(courses) != 1:
        result.result = False
    import_test.append(result)
    results.append(import_test)

    # Course import is dep for all further tests, so just fail out
    if not result.result:
        report_results(results)
        sys.exit(1)

    course = modulestore.courses.get(modulestore.courses.keys()[0])
    results.append(check_image(directory, course))
    results.append(check_alt_tags(course))
    results.append(check_captions(course))
    results.append(check_links(course))

    if report_results(results):
        sys.exit(1)

    render_report_results(course, output.getvalue())

if __name__ == '__main__':
    test_course(sys.argv[1])
