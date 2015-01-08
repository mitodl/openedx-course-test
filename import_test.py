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
from cStringIO import StringIO
import codecs
import logging
import os
import sys

from jinja2 import Environment

from xmodule.modulestore.xml import XMLModuleStore


def import_course(directory):
    """
    Setup environment and import the course.
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
    assert len(courses) == 1
    print('Course imported successfully!')

    course = modulestore.courses.get(modulestore.courses.keys()[0])
    course_key = u'{}'.format(
        course.location.course_key.to_deprecated_string()
    )
    jinja_environment = Environment()
    with open(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'report.j2'
            )
    ) as template_file:
        template = jinja_environment.from_string(template_file.read())
        UTF8Writer = codecs.getwriter('utf8')
        sys.stdout = UTF8Writer(sys.stdout)
        print(template.render({'course': course, 'course_key': course_key}))

    print('Possible issues in course:')
    print('==========================')
    for line in output.getvalue().split('\n'):
        split_msg = line.split('|')
        if split_msg[0] in ('WARNING', 'ERROR', 'CRITICAL'):
            print(split_msg[1])

if __name__ == '__main__':
    import_course(sys.argv[1])
