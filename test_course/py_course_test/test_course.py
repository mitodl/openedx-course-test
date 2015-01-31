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
from __future__ import print_function, division
from cStringIO import StringIO
import codecs
import logging
import os
import sys

from BeautifulSoup import BeautifulStoneSoup
from jinja2 import Environment
from PIL import Image

from xmodule.modulestore.xml import XMLModuleStore


ASPECT_RATIO = 1.75


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


def check_image(directory, course):
    """Take a course and check that it's course image exists and is an image

    Args:
        course (modulestore course object): The course to check.

    Returns:
        list: TestResult objects
    """
    results = []
    image_path = os.path.join(
        directory, course.data_dir, 'static', course.course_image
    )
    result = TestResult("Course image file exists", True)
    results.append(result)
    if not os.path.isfile(image_path):
        # Handle that lovely default of images_course_image.jpg problem
        # by trying the _ to folder expansion
        if course.course_image == 'images_course_image.jpg':
            image_path = os.path.join(
                directory, course.data_dir, 'static', 'images/course_image.jpg'
            )
            if not os.path.isfile(image_path):
                result.result = False
                result.value = 'no file at {}'.format(image_path)
                return results

    result = TestResult("Course image is an image", True)
    results.append(result)
    try:
        image = Image.open(image_path)
    except IOError:
        result.result = False
        result.value = '{} is not an image'.format(image_path)
        return results

    result = TestResult("Course image is allowed type (JPG or PNG)", True)
    results.append(result)
    if image.format not in ['JPEG', 'PNG']:
        result.result = False
        result.value = 'Got format of {}'.format(image.format)
        return results

    result = TestResult("Course image is correct aspect ratio", True, False)
    results.append(result)
    ratio = image.size[0]/image.size[1]
    if ratio != ASPECT_RATIO:
        result.result = False
        result.value = '{} not desired {}'.format(ratio, ASPECT_RATIO)
    return results


def recurse_for_alt(element, results):
    """
    Depth first recursor for going through children and finding
    images
    """
    # Check
    if hasattr(element, 'data'):
        # Try and parse data as XML
        try:
            soup = BeautifulStoneSoup(element.data)
            for img in soup.findAll('img'):
                if not img.get('alt', False):
                    results.append(
                        TestResult(
                            'Image missing alt tag for `{}` in {} ({})'.format(
                                img,
                                element.xml_attributes['filename'][0],
                                element.location
                            ),
                            False
                        )
                    )
        except Exception:
            pass
    # And recurse
    if not hasattr(element, 'get_children'):
        return
    if len(element.get_children()) == 0:
        return
    for child in element.get_children():
        recurse_for_alt(child, results)


def check_alt_tags(course):
    """
    Run through entire course tree looking for <img> tags
    that don't have alt attributes
    """
    # walk the tree for data in nodes and check them
    results = []
    recurse_for_alt(course, results)
    # If no results, no failures, make a pass test result
    if len(results) == 0:
        results.append(TestResult('All images have `alt` attributes', True))
    return results


def recurse_for_captions(element, results, counter):
    """
    Depth first recursor for going through children and finding
    images
    """
    # Check
    if element.xml_element_name().lower() == 'video':
        counter += 1
        if not element.show_captions:
            results.append(
                TestResult(
                    'Video named {} has captions disabled at'
                    '`{}`'.format(
                        element.display_name_with_default,
                        element.location,
                    ),
                    False,
                    False
                )
            )
    # And recurse
    if not hasattr(element, 'get_children'):
        return counter
    if len(element.get_children()) == 0:
        return counter
    for child in element.get_children():
        counter = recurse_for_captions(child, results, counter)
    return counter


def check_captions(course):
    """Check that all video blocks have ``show_captions`` enabled
    """
    # walk the tree for data in nodes and check them
    results = []
    counter = 0
    counter = recurse_for_captions(course, results, counter)
    # If no results, no failures, make a pass test result
    if len(results) == 0:
        results.append(
            TestResult(
                'All videos({}) have captions enabled'.format(counter),
                True
            )
        )
    return results


def report_results(results):
    """Output from a list of `class:TestResult` objects and return false
    if any of them are critical.

    Args:
        results (list): List of `class:TestResult` classes

    Returns:
        bool: True if a critical failure was detected
    """
    print("\033[0;34mPython Test Results\033[0m")

    failed = False
    for result in results:
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

    return failed


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

    result = TestResult('Course import success', True)
    if len(courses) != 1:
        result.result = False
    results.append(result)

    course = modulestore.courses.get(modulestore.courses.keys()[0])
    course_key = u'{}'.format(
        course.location.course_key.to_deprecated_string()
    )
    results.extend(check_image(directory, course))
    results.extend(check_alt_tags(course))

    if report_results(results):
        sys.exit(1)

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
    for line in output.getvalue().split('\n'):
        split_msg = line.split('|')
        if split_msg[0] in ('WARNING', 'ERROR', 'CRITICAL'):
            print(split_msg[1])

if __name__ == '__main__':
    test_course(sys.argv[1])
