FROM erlang:19.3

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential libxslt-dev zip unzip expat zlib1g-dev    \
    libssl-dev curl libncurses5-dev git-core libexpat1-dev htmldoc python python-pip python-yaml elixir

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y bash-completion libcap2-bin dnsutils net-tools tcpdump

RUN setcap cap_net_raw+ep /usr/sbin/tcpdump

COPY conf/ /etc/kazoo/

RUN groupadd -g 1000 kazoo
RUN useradd -m -g kazoo -u 1000 kazoo
USER kazoo

WORKDIR /home/kazoo
RUN pip install --user kazoo mkdocs mkdocs-bootstrap mkdocs-bootswatch pymdown-extensions

RUN git clone --branch 4.3 https://github.com/2600hz/kazoo-sounds.git /home/kazoo/src/kazoo-sounds

RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui.git /home/kazoo/src/monster-ui
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-voip.git /home/kazoo/src/monster-ui/src/apps/voip
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-callflows.git /home/kazoo/src/monster-ui/src/apps/callflows
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-accounts.git /home/kazoo/src/monster-ui/src/apps/accounts
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-pbxs.git /home/kazoo/src/monster-ui/src/apps/pbxs
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-numbers.git /home/kazoo/src/monster-ui/src/apps/numbers
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-webhooks.git /home/kazoo/src/monster-ui/src/apps/webhooks
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-voicemails.git /home/kazoo/src/monster-ui/src/apps/voicemails
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-fax.git /home/kazoo/src/monster-ui/src/apps/fax
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-csv-onboarding.git /home/kazoo/src/monster-ui/src/apps/csv-onboarding

ENV KAZOO_ROOT=/home/kazoo/src/kazoo/_rel/kazoo
ENV PATH=$KAZOO_ROOT/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
