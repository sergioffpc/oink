FROM node:15

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git-core

USER node

WORKDIR /home/node
RUN npm install gulp-cli

RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui.git /home/node/src/monster-ui
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-voip.git /home/node/src/monster-ui/src/apps/voip
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-callflows.git /home/node/src/monster-ui/src/apps/callflows
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-accounts.git /home/node/src/monster-ui/src/apps/accounts
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-pbxs.git /home/node/src/monster-ui/src/apps/pbxs
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-numbers.git /home/node/src/monster-ui/src/apps/numbers
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-webhooks.git /home/node/src/monster-ui/src/apps/webhooks
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-voicemails.git /home/node/src/monster-ui/src/apps/voicemails
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-fax.git /home/node/src/monster-ui/src/apps/fax
RUN git clone --branch 4.3 https://github.com/2600hz/monster-ui-csv-onboarding.git /home/node/src/monster-ui/src/apps/csv-onboarding

WORKDIR /home/node/src/monster-ui
RUN npm install

COPY conf/ /home/node/src/monster-ui/src/js/
CMD /home/node/node_modules/.bin/gulp
