### Manual process

Start the VM and ssh into it
```
vagrant init generic/centos7
vagrant up
vagrant ssh
```

Install nginx
```
yum install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx
```

Open the needed ports in the firewall
```
sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload
```

Run test
```
curl 127.0.0.1
curl 192.168.56.2
```

Configure nginx
```
sudo vi /etc/nginx/nginx.conf
# Do the necessary things in order to enable https, use let's encrypt
```

Restart nginx
```
sudo systemctl restart nginx
```

Run test with https
```
curl https://domain.com
```

Create app_simple.py
```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```

Install requirements
```
pip install flask
pip install uwsgi
```

Run app_simple.py with python
```
python app.py
curl 127.0.0.1:5000
```

Create uwsgi.py
```
from app_simple import app

if __name__ == "__main__":
    app.run()
```

Run app with uwsgi
```
uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
curl 127.0.0.1:5000
```

Create app_simple.ini uwsgi file
```
[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = app_simple.sock
chmod-socket = 660
vacuum = true

die-on-term = true
```

Run app with uwsgi and ini file. Validate that the output of the command is similar to the previous
uwsgi execution
```
uwsgi --ini app_simple.ini
```

Create a systemd service for launching app_simple 
/etc/systemd/system/app_simple.service
```
[Unit]
Description=uWSGI instance to serve app
After=network.target

[Service]
User=vagrant
Group=vagrant
WorkingDirectory=/home/vagrant/app_simple
ExecStart=/home/vagrant/.local/bin/uwsgi --ini app_simple.ini --uid vagrant --gid vagrant

[Install]
WantedBy=multi-user.target
```

Configure nginx site configuration
```
```

Create a symbolic link
```
```

Update nginx.conf
```
```

Add an entry to /etc/hosts
```
```

Test integration
```
curl http://app_simple.com
```

Check nginx logs after doing some requests
```
sudo tail -30 /var/log/nginx/error.log
```

See Problem 3 in troubleshooting section to fix the issue

### Ansible process

pip install --user ansible  
pip install --user paramiko

```
vagrant up
ansible-playbook -i hosts playbooks/nginx.yml
ansible-playbook -i hosts playbooks/python.yml
```

### Activities
* Create a new user instead of doing the nginx and app_simple configurations for the vagrant user

### Troubleshoot (MacOS)

Problem 1

```
==> nginxServer: Clearing any previously set network interfaces...
There was an error while executing `VBoxManage`, a CLI used by Vagrant
for controlling VirtualBox. The command and stderr is shown below.

Command: ["hostonlyif", "create"]

Stderr: 0%...
Progress state: NS_ERROR_FAILURE
VBoxManage: error: Failed to create the host-only adapter
VBoxManage: error: VBoxNetAdpCtl: Error while adding new interface: failed to open /dev/vboxnetctl: No such file or directory
VBoxManage: error: Details: code NS_ERROR_FAILURE (0x80004005), component HostNetworkInterfaceWrap, interface IHostNetworkInterface
VBoxManage: error: Context: "RTEXITCODE handleCreate(HandlerArg *)" at line 94 of file VBoxManageHostonly.cpp
```

Solution 1

```
sudo "/Library/Application Support/VirtualBox/LaunchDaemons/VirtualBoxStartup.sh" restart
```

Reference 1
 
```
https://github.com/hashicorp/vagrant/issues/1671
```

Problem 2
```
[root@nginxServer vagrant]# sudo cat /var/log/audit/audit.log | grep nginx | grep denied
type=AVC msg=audit(1562220943.922:4788): avc:  denied  { name_connect } for  pid=7322 comm="nginx" dest=5000 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:commplex_main_port_t:s0 tclass=tcp_socket permissive=0
```

Problem 3
```
2019/07/03 23:58:39 [crit] 7875#0: *34 connect() to unix:/home/vagrant/app_simple/app_simple.sock failed (13: Permission denied) while connecting to upstream, client: 127.0.0.1, server: app_simple.com, request: "GET / HTTP/1.1", upstream: "uwsgi://unix:/home/vagrant/app_simple/app_simple.sock:", host: "app_simple.com"
```

Solution 3
```
yum install policycoreutils-python
sudo setenforce Permissive
# to see what permissions are needed.
sudo grep nginx /var/log/audit/audit.log | audit2allow
# to fix misslabeled error
restorecon -R -v /home/vagrant/app_simple/app_simple.sock
# to create a nginx.pp policy file
sudo grep nginx /var/log/audit/audit.log | audit2allow -M nginx
# to apply the new policy
sudo semodule -i nginx.pp
sudo setenforce Enforcing
```

### References

* https://letsencrypt.org/
* https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
* https://docs.ansible.com/ansible/latest/modules/ec2_module.html
* https://www.linuxschoolonline.com/use-ansible-to-build-and-manage-aws-ec2-instances/
* https://arkit.co.in/aws-ec2-instance-creation-using-ansible/
* http://www.mydailytutorials.com/ansible-add-line-to-file/
* https://github.com/andreif/uwsgi-tools
* https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html
* https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/security-enhanced_linux/sect-security-enhanced_linux-fixing_problems-allowing_access_audit2allow
* https://docs.ansible.com/ansible/latest/modules/script_module.html
* https://medium.com/@abhijeet.kamble619/10-things-you-should-start-using-in-your-ansible-playbook-808daff76b65

* https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-on-centos-7
* https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html
* https://www.gab.lc/articles/flask-nginx-uwsgi/
* https://stackoverflow.com/questions/21820444/nginx-error-13-permission-denied-while-connecting-to-upstream
* https://stackoverflow.com/questions/23948527/13-permission-denied-while-connecting-to-upstreamnginx


