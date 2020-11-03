#!/usr/bin/env bash

docker-compose exec couchdb curl -vvv -X PUT localhost:5984/_node/couchdb@couchdb.oink/_config/admins/couchdb -d '"couchdb"'

docker-compose exec kazoo-apps sup kazoo_media_maintenance import_prompts /opt/kazoo/sounds/en/us/

# Create the master account and super admin user, substituting in your own values.  Account realm is used to identify
# individual accounts and needs to be a unique valid local or global FQDN.  If account realm is DNS resolvable, devices
# can access the account by using realm instead of IP + realm.
#
# Account name, realm, and password can be changes afterwards via Monster UI.
docker-compose exec kazoo-apps sup crossbar_maintenance create_account oink oink oink oink

docker-compose exec kazoo-apps sup crossbar_maintenance init_apps /var/www/html/monster-ui/apps http://kazoo.oink:8000/v2

docker-compose exec kazoo-ecallmgr sup -n ecallmgr ecallmgr_maintenance add_fs_node freeswitch@freeswitch.oink
docker-compose exec kazoo-ecallmgr sup -n ecallmgr ecallmgr_maintenance allow_sbc kamailio kamailio.oink
