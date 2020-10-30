FROM centos:7

RUN yum update
RUN yum upgrade -y
RUN yum install -y bind-utils net-tools tcpdump sysvinit-tools

RUN yum install -y https://packages.2600hz.com/centos/7/stable/2600hz-release/4.3/2600hz-release-4.3-0.el7.centos.noarch.rpm
RUN yum install -y httpd monster-ui
RUN yum clean all

COPY system/httpd/ /etc/httpd/

CMD /usr/sbin/httpd -DFOREGROUND
