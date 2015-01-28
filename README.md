# Course Tester
---
Syntax checker and validator for edX Courses.
---
This repo builds a docker image of a minimal edx-platform install
capable of doing in memory course imports, along with `xmllint` to
do syntax checking of all course xml.

## Quick Start

If you have docker installed and a course to test, you don't even need
to grab this repository, just run: `docker run -v
"/path/to/course_dir":"/course" -w /course-test
mitodl/openedx-course-test bash -e 'test_course'` replacing
`path/to/course_dir` with the file path to a folder above where you
have your course.

## Full Usage

Simply run `course_test /path/to/course/folder` where the course
folder has exactly one course in it.  This will need to be run on
a system that has docker installed and enough ram to run the
import (probably about 2GiB).


By default this will get the latest public docker image.  If you want
to build your own locally instead, you can run `course_test -l
/path/to/course/folder` and it will build it if you don't already have
the image.  You can also manually build just the image with `docker
build -t=mitodl/openedx-course-test .` and build from scratch
(no-cache) with `docker build --no-cache -t=mitodl/openedx-course-test
.`
