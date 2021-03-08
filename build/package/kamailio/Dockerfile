FROM centos:7

RUN yum update -y
RUN yum upgrade -y
RUN yum install -y bind-utils net-tools tcpdump

RUN yum install -y https://packages.2600hz.com/centos/7/stable/2600hz-release/4.3/2600hz-release-4.3-0.el7.centos.noarch.rpm
RUN yum install -y kazoo-kamailio kamailio-postgresql postgresql

COPY system/yum.repos.d/ /etc/yum.repos.d/
RUN rpm --import http://packages.irontec.com/public.key
RUN yum install -y sngrep
RUN yum clean all

RUN setcap cap_net_raw+ep /usr/sbin/tcpdump
RUN setcap cap_net_raw+ep /usr/bin/sngrep

COPY conf/ /etc/kazoo/kamailio/
RUN /usr/sbin/kazoo-kamailio prepare

USER kamailio
CMD /usr/sbin/kazoo-kamailio foreground
