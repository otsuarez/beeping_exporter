FROM phusion/baseimage:0.9.22
MAINTAINER Osvaldo <osvaldo.toja@gmail.com>

ADD . /pd_build
RUN /pd_build/install.sh

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]
EXPOSE 8080

