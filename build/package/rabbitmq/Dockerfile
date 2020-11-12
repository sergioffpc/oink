FROM centos:7

RUN yum update -y
RUN yum upgrade -y
RUN yum install -y bind-utils net-tools

RUN yum install -y https://packages.2600hz.com/centos/7/stable/2600hz-release/4.3/2600hz-release-4.3-0.el7.centos.noarch.rpm
RUN yum install -y kazoo-rabbitmq
RUN yum clean all

RUN /usr/sbin/kazoo-rabbitmq prepare

USER rabbitmq
CMD /usr/sbin/kazoo-rabbitmq start
