FROM couchdb:2.3.1

COPY system/sbin/ /usr/sbin/
RUN chmod 755 /usr/sbin/kazoo-couchdb
RUN chmod 755 /usr/sbin/kazoo-run-couchdb

COPY system/security/limits.d/ /etc/security/limits.d/

COPY conf/ /etc/kazoo/couchdb/
RUN /usr/sbin/kazoo-couchdb prepare

USER couchdb
CMD /usr/sbin/kazoo-couchdb background
