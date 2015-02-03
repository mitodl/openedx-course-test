#!/bin/env python
# -*- coding: utf-8 -*-
"""
Check links within the course. Specifically these link types:
- Internal jump_to links
- Internal static links
- External links
"""
import HTMLParser
import os

from BeautifulSoup import BeautifulStoneSoup
from opaque_keys import InvalidKeyError
import requests
from xmodule.modulestore.exceptions import ItemNotFoundError
from xmodule.modulestore.search import path_to_location

from common import TestResult, TestResultList


def check_jump_to(course, element, location):
    """Verify that the location in the jumpto exists

    """
    result_msg = ''
    try:
        usage_key = course.id.make_usage_key_from_deprecated_string(
            location
        )
    except InvalidKeyError:
        result_msg = 'Invalid usage key'
    else:
        try:
            path_to_location(course.runtime.modulestore, usage_key)
        except ItemNotFoundError:
            result_msg = 'Nothing at this location (404)'
    if result_msg:
        return TestResult(
            'jump_to link /jump_to/{} in {} invalid. {}'.format(
                location, element.location, result_msg
            ),
            False
        )


def check_jump_to_id(course, element, module_id):
    """Verify that the location in the jumpto exists

    """
    items = course.runtime.modulestore.get_items(
        course.id, qualifiers={'name': module_id}
    )
    if len(items) != 1:
        return TestResult(
            'jump_to_id link /jump_to_id/{} in {} wrong.'
            ' {} items found'.format(
                module_id, element.location, len(items)
            ),
            False
        )


def check_static(course, element, href):
    """Verify that magic /static links have files that exist on disk

    """
    path = os.path.join(
        course.runtime.modulestore.data_dir,
        course.data_dir,
        'static',
        href
    )
    if not os.path.isfile(path):
        return TestResult(
            'Linked static asset {} in {} not found'.format(
                href, element.location
            ),
            False
        )


def check_external(element, href):
    """
    This will go ahead and try and get the URL linked to
    and if it is a 404 returns a failed test result.
    """
    result_msg = None
    try:
        status_code = requests.head(
            href, timeout=1, allow_redirects=True,
        ).status_code
        if status_code != 200:
            result_msg = "Status code was {}, expected 200".format(status_code)
    except requests.exceptions.RequestException, ex:
        result_msg = "Request exception occurred, {}".format(ex)
    if result_msg:
        return TestResult(
            'External link {} in {} invalid. {}'.format(
                href, element.location, result_msg
            ),
            False
        )


def recurse_for_links(course, element, results, counter):

    """
    Depth first recursor for going through children, finding
    links, and validating them
    """
    if hasattr(element, 'data'):
        # Try and parse data as XML
        try:
            soup = BeautifulStoneSoup(element.data)
            for link in soup.findAll('a'):
                if link.get('href', None):
                    counter += 1
                    href = link.get('href')
                    if href.startswith('/jump_to/'):
                        # use module store to verify link
                        check = check_jump_to(
                            course, element, href.replace('/jump_to/', '')
                        )
                        if check:
                            results.append(check)
                    elif href.startswith('/jump_to_id/'):
                        # use module store to verify link
                        check = check_jump_to_id(
                            course, element, href.replace('/jump_to_id/', '')
                        )
                        if check:
                            results.append(check)
                    elif href.startswith('/static/'):
                        # use file system to find file or not
                        check = check_static(
                            course, element, href.replace('/static/', '')
                        )
                        if check:
                            results.append(check)
                    elif href.startswith('http'):
                        # Use urlparse and requests to ping the URL
                        check = check_external(element, href)
                        if check:
                            results.append(check)
        except HTMLParser.HTMLParseError:
            pass
    # And recurse
    if not hasattr(element, 'get_children'):
        return counter
    if len(element.get_children()) == 0:
        return counter
    for child in element.get_children():
        counter = recurse_for_links(course, child, results, counter)
    return counter


def check_links(course):
    """
    Run through entire course tree looking for <img> tags
    that don't have alt attributes
    """
    # walk the tree for data in nodes and check them
    results = TestResultList('Check Links')
    counter = 0
    counter = recurse_for_links(course, course, results, counter)
    # If no results, no failures, make a pass test result
    if len(results) == 0:
        results.append(
            TestResult(
                'All links({}) are valid'.format(counter), True
            )
        )
    return results
