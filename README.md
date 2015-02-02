# Course Tester

---
Syntax checker and validator for edX Courses.
---

This repo builds a docker image of a minimal edx-platform install
capable of doing several
[Open Learning XML (OLX)](http://engineering.edx.org/2014/10/open-learning-xml-olx-format/)
(a.k.a. [Open edX course exports](https://code.edx.org)) content checks and validations.

This is extremely useful for raw XML authored (or
[latex2edx](https://github.com/mitocw/latex2edx)) courses, but it also
has a lot of benefits for validating regular Studio edited courses as
well.  Notably link checking and some basic accessibility checks

## Quick Start

If you have docker installed and a course to test, you don't even need
to grab this repository, just run: `docker run -v
"/path/to/course_dir":"/course" -w /test_course
mitodl/openedx-course-test bash -e test_course` replacing
`path/to/course_dir` with the file path to a folder above where you
have your course.

## Current Tests

- XML syntax validation
- JSON policy file syntax validation
- Static asset file names are in the simple URL set of `^[a-zA-Z0-9_\./-]+$`
- Course imports successfully into `XMLModuleStore`
- Course image validation
  - It exists
  - It is an image
  - It is the correct image type (PNG or JPG)
  - It warns if the aspect ratio isn't correct (1.75)
- All image tags in content have `alt` attributes for accessibility
- All video units have `show_captions` set to true (warns only)


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


## Known Issues

Due to somewhat ridiculous requirements needed to import ORA problems,
they will just show up as failed in the "Possible issues in course"
section as `Error loading from xml. No module named ratelimitbackend`.
