#!/bin/env python
# -*- coding: utf-8 -*-
"""
Check that video xblocks have captions enabled
"""
from common import TestResult, TestResultList


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
    results = TestResultList('Test for Disabled Video Captions')
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
