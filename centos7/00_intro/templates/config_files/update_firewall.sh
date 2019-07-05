#!/bin/sh
curl http://app_simple.com
setenforce Permissive
grep nginx /var/log/audit/audit.log | audit2allow
restorecon -R -v /home/vagrant/app_simple/app_simple.sock
grep nginx /var/log/audit/audit.log | audit2allow -M nginx
semodule -i nginx.pp
setenforce Enforcing