FROM ubuntu:precise
MAINTAINER ODL DevOps <mitx-devops@mit.edu>
RUN mkdir /build
COPY requirements.txt /build/
COPY docker_build /build/
RUN bash -ex /build/docker_build

# Add copies to Dockerfile incase they don't want dev mode
RUN mkdir /course-test
COPY test_course /course-test/
COPY report.j2 /course-test/
COPY import_test.py /course-test/
