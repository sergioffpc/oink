FROM centos:7

RUN yum update
RUN yum upgrade -y
RUN yum install -y bind-utils net-tools tcpdump sngrep

RUN yum install -y https://packages.2600hz.com/centos/7/stable/2600hz-release/4.3/2600hz-release-4.3-0.el7.centos.noarch.rpm
RUN yum install -y kazoo-kamailio
RUN yum clean all

COPY conf/ /etc/kazoo/kamailio/
RUN /usr/sbin/kazoo-kamailio prepare

USER kamailio
CMD /usr/sbin/kazoo-kamailio foreground