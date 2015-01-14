# Course Tester
---
Syntax checker and validator for edX Courses.
---
This repo builds a docker image of a minimal edx-platform install
capable of doing in memory course imports, along with `xmllint` to
do syntax checking of all course xml.

## Usage

Simply run `docker_test /path/to/course/folder` where the course
folder has exactly one course in it.  This will need to be run on
a system that has docker installed and enough ram to run the
import (probably about 3GiB).

