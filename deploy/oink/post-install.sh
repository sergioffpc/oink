#!/usr/bin/env bash

docker-compose exec kazoo-couchdb curl -vvv -X PUT localhost:5984/_node/kazoo_couchdb@kazoo-couchdb.oink_app_net/_config/admins/couchdb -d '"couchdb"'

# Wait for Kazoo to start up.
sleep 15

# Import all prompts for a given language.
docker-compose exec kazoo-apps sup kazoo_media_maintenance import_prompts /home/kazoo/src/kazoo-sounds/kazoo-core/en/us/ en-us

# Create the master account and super admin user, substituting in your own values.  Account realm is used to identify
# individual accounts and needs to be a unique valid local or global FQDN.  If account realm is DNS resolvable, devices
# can access the account by using realm instead of IP + realm.
#
# Account name, realm, and password can be changes afterwards via Monster UI.
docker-compose exec kazoo-apps sup crossbar_maintenance create_account oink oink oink oink

docker-compose exec kazoo-apps sup crossbar_maintenance init_apps /home/kazoo/src/monster-ui/src/apps/ http://localhost:8000/v2

docker-compose exec kazoo-apps sup ecallmgr_maintenance add_fs_node freeswitch@kazoo-freeswitch-alpha.oink_app_net
docker-compose exec kazoo-apps sup ecallmgr_maintenance add_fs_node freeswitch@kazoo-freeswitch-beta.oink_app_net
docker-compose exec kazoo-apps sup ecallmgr_maintenance allow_sbc kamailio kazoo-kamailio.oink_app_net
docker-compose exec kazoo-apps sup ecallmgr_maintenance reload_acls

# It can be a good idea to run a refresh over the installed databases - there are sporadic reports of partial
# installations hanging at this point.
docker-compose exec kazoo-apps sup kapps_maintenance refresh

docker-compose exec kazoo-apps sup ecallmgr_maintenance get_fs_nodes
docker-compose exec kazoo-apps sup ecallmgr_maintenance acl_summary

docker-compose exec kazoo-kamailio kazoo-kamailio status
docker-compose exec kazoo-apps sup kz_nodes status
