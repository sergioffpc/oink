FROM internetsystemsconsortium/bind9:9.16

COPY conf/ /etc/bind/

CMD /usr/sbin/named -c /etc/bind/named.conf -g -u bind
