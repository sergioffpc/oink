BEGIN TRANSACTION;

INSERT INTO version VALUES('version',1);
INSERT INTO version (table_name, table_version) values ('acc','5');
INSERT INTO version (table_name, table_version) values ('acc_cdrs','2');
INSERT INTO version (table_name, table_version) values ('missed_calls','4');
INSERT INTO version (table_name, table_version) values ('dbaliases','1');
INSERT INTO version (table_name, table_version) values ('subscriber','7');
INSERT INTO version (table_name, table_version) values ('usr_preferences','2');
INSERT INTO version (table_name, table_version) values ('carrierroute','3');
INSERT INTO version (table_name, table_version) values ('carrierfailureroute','2');
INSERT INTO version (table_name, table_version) values ('carrier_name','1');
INSERT INTO version (table_name, table_version) values ('domain_name','1');
INSERT INTO version (table_name, table_version) values ('cpl','1');
INSERT INTO version (table_name, table_version) values ('dialog','7');
INSERT INTO version (table_name, table_version) values ('dialog_vars','1');
INSERT INTO version (table_name, table_version) values ('dialplan','2');
INSERT INTO version (table_name, table_version) values ('dispatcher','4');
INSERT INTO version (table_name, table_version) values ('domain','2');
INSERT INTO version (table_name, table_version) values ('domain_attrs','1');
INSERT INTO version (table_name, table_version) values ('domainpolicy','2');
INSERT INTO version (table_name, table_version) values ('dr_gateways','3');
INSERT INTO version (table_name, table_version) values ('dr_rules','3');
INSERT INTO version (table_name, table_version) values ('dr_gw_lists','1');
INSERT INTO version (table_name, table_version) values ('dr_groups','2');
INSERT INTO version (table_name, table_version) values ('grp','2');
INSERT INTO version (table_name, table_version) values ('re_grp','1');
INSERT INTO version (table_name, table_version) values ('htable','2');
INSERT INTO version (table_name, table_version) values ('imc_rooms','1');
INSERT INTO version (table_name, table_version) values ('imc_members','1');
INSERT INTO version (table_name, table_version) values ('lcr_gw','3');
INSERT INTO version (table_name, table_version) values ('lcr_rule_target','1');
INSERT INTO version (table_name, table_version) values ('lcr_rule','3');
INSERT INTO version (table_name, table_version) values ('matrix','1');
INSERT INTO version (table_name, table_version) values ('mohqcalls','1');
INSERT INTO version (table_name, table_version) values ('mohqueues','1');
INSERT INTO version (table_name, table_version) values ('silo','8');
INSERT INTO version (table_name, table_version) values ('mtree','1');
INSERT INTO version (table_name, table_version) values ('mtrees','2');
INSERT INTO version (table_name, table_version) values ('pdt','1');
INSERT INTO version (table_name, table_version) values ('trusted','6');
INSERT INTO version (table_name, table_version) values ('address','6');
INSERT INTO version (table_name, table_version) values ('pl_pipes','1');
INSERT INTO version (table_name, table_version) values ('presentity','5');
INSERT INTO version (table_name, table_version) values ('active_watchers','12');
INSERT INTO version (table_name, table_version) values ('watchers','3');
INSERT INTO version (table_name, table_version) values ('xcap','4');
INSERT INTO version (table_name, table_version) values ('pua','7');
INSERT INTO version (table_name, table_version) values ('purplemap','1');
INSERT INTO version (table_name, table_version) values ('aliases','8');
INSERT INTO version (table_name, table_version) values ('rls_presentity','1');
INSERT INTO version (table_name, table_version) values ('rls_watchers','3');
INSERT INTO version (table_name, table_version) values ('rtpengine','1');
INSERT INTO version (table_name, table_version) values ('rtpproxy','1');
INSERT INTO version (table_name, table_version) values ('sca_subscriptions','2');
INSERT INTO version (table_name, table_version) values ('sip_trace','4');
INSERT INTO version (table_name, table_version) values ('speed_dial','2');
INSERT INTO version (table_name, table_version) values ('topos_d','1');
INSERT INTO version (table_name, table_version) values ('topos_t','1');
INSERT INTO version (table_name, table_version) values ('uacreg','3');
INSERT INTO version (table_name, table_version) values ('uid_credentials','7');
INSERT INTO version (table_name, table_version) values ('uid_user_attrs','3');
INSERT INTO version (table_name, table_version) values ('uid_domain','2');
INSERT INTO version (table_name, table_version) values ('uid_domain_attrs','1');
INSERT INTO version (table_name, table_version) values ('uid_global_attrs','1');
INSERT INTO version (table_name, table_version) values ('uid_uri','3');
INSERT INTO version (table_name, table_version) values ('uid_uri_attrs','2');
INSERT INTO version (table_name, table_version) values ('uri','1');
INSERT INTO version (table_name, table_version) values ('userblacklist','1');
INSERT INTO version (table_name, table_version) values ('globalblacklist','1');
INSERT INTO version (table_name, table_version) values ('location','9');
INSERT INTO version (table_name, table_version) values ('location_attrs','1');
INSERT INTO event_list VALUES('dialog');
INSERT INTO event_list VALUES('presence');
INSERT INTO event_list VALUES('message-summary');
INSERT INTO version VALUES('event_list',1);
INSERT INTO version (table_name, table_version) values ('active_watchers_log','1');
INSERT INTO version (table_name, table_version) values ('keepalive','4');
INSERT INTO version (table_name, table_version) select 'auth_cache', table_version from version where table_name = 'htable';
INSERT INTO version (table_name, table_version) select 'block_cache', table_version from version where table_name = 'htable';

COMMIT;