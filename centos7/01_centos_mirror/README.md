### CentOS7 Custom Mirror

#### Server
```
mkdir /var/repo
cd /var/repo
yum install httpd
systemctl start httpd
systemctl enable httpd
yum install createrepo
yum install yum-plugin-downloadonly
yum install --downloadonly --downloaddir=/var/repo nmap
createrepo /var/repo/
ln -s /var/repo /var/www/html/repo 
yum install policycoreutils-python
semanage fcontext -a -t httpd_sys_content_t "/var/repo(/.*)?" && restorecon -rv /var/repo
```

#### Client
```
vi /etc/hosts
---
192.168.131.23 icesi.mirror.edu.co
---
```

```
vi /etc/yum.repos.d/icesi.repo
--
[icesirepo]
name=My RPM System Package Repo
baseurl=http://icesi.mirror.edu.co/repo/
enabled=1
gpgcheck=0
--
yum repolist
yum update
yum --disablerepo="*" --enablerepo="icesirepo" list available
yum --disablerepo="*" --enablerepo="icesirepo" install nmap
```

### References
* https://g4greetz.wordpress.com/2016/10/12/how-to-run-a-yum-update-from-a-specific-repository/
* https://www.ostechnix.com/download-rpm-package-dependencies-centos/
* https://www.digitalocean.com/community/tutorials/how-to-set-up-and-use-yum-repositories-on-a-centos-6-vps

### FAQ
* I'm not able to execute the yum update command 
R/ setenforce 0 (use with caution)

#### Alternatives (Not recommended)
```
vi /etc/selinux/config
---
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#       enforcing - SELinux security policy is enforced.
#       permissive - SELinux prints warnings instead of enforcing.
#       disabled - No SELinux policy is loaded.
SELINUX=disabled
# SELINUXTYPE= can take one of these two values:
#       targeted - Targeted processes are protected,
#       mls - Multi Level Security protection.
SELINUXTYPE=targeted
---
reboot
getenforce
> Disabled
```

