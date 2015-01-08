FROM ubuntu:precise
MAINTAINER ODL DevOps <mitx-devops@mit.edu>
RUN mkdir /build
COPY requirements.txt /build/
COPY docker_build /build/
RUN bash -ex /build/docker_build
