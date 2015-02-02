#!/bin/env python
# -*- coding: utf-8 -*-
"""
Test the course image
"""
from __future__ import division
import os

from PIL import Image

from common import TestResult, TestResultList


ASPECT_RATIO = 1.75


def check_image(directory, course):
    """Take a course and check that it's course image exists and is an image

    Args:
        course (modulestore course object): The course to check.

    Returns:
        list: TestResult objects
    """
    results = TestResultList('Course Image Tests')
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
