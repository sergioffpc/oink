FROM debian:10-slim

RUN apt-get update
RUN apt-get install -y gnupg2 wget lsb-release
RUN wget -O - https://files.freeswitch.org/repo/deb/debian-release/fsstretch-archive-keyring.asc | apt-key add -

RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

RUN echo "deb http://files.freeswitch.org/repo/deb/debian-release/ `lsb_release -sc` main" > /etc/apt/sources.list.d/freeswitch.list
RUN echo "deb-src http://files.freeswitch.org/repo/deb/debian-release/ `lsb_release -sc` main" >> /etc/apt/sources.list.d/freeswitch.list

RUN apt-get update
RUN mkdir -p /usr/share/man/man1
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y freeswitch freeswitch-mod-console freeswitch-mod-logfile      \
    freeswitch-mod-event-socket freeswitch-mod-kazoo freeswitch-mod-dialplan-xml freeswitch-mod-loopback            \
    freeswitch-mod-av freeswitch-mod-commands freeswitch-mod-conference freeswitch-mod-dptools freeswitch-mod-expr  \
    freeswitch-mod-http-cache freeswitch-mod-spandsp freeswitch-mod-g723-1 freeswitch-mod-amr freeswitch-mod-ilbc   \
    freeswitch-mod-opus freeswitch-mod-sndfile freeswitch-mod-sofia freeswitch-mod-local-stream                     \
    freeswitch-mod-tone-stream freeswitch-mod-shout freeswitch-mod-flite freeswitch-mod-say-en

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y dnsutils net-tools

COPY system/sbin/ /usr/sbin/
RUN chmod 755 /usr/sbin/kazoo-freeswitch

COPY system/security/limits.d/ /etc/security/limits.d/

COPY conf/ /etc/kazoo/freeswitch/
RUN /usr/sbin/kazoo-freeswitch prepare

USER freeswitch
CMD /usr/sbin/kazoo-freeswitch start
