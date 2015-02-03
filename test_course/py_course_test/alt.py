#!/bin/env python
# -*- coding: utf-8 -*-
"""
Check that all img tags in the course have an alt
tag
"""
import HTMLParser

from BeautifulSoup import BeautifulStoneSoup

from common import TestResult, TestResultList


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
        except HTMLParser.HTMLParseError:
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
    results = TestResultList('Checks for Image Alt Tags')
    recurse_for_alt(course, results)
    # If no results, no failures, make a pass test result
    if len(results) == 0:
        results.append(TestResult('All images have `alt` attributes', True))
    return results
