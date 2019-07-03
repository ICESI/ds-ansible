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

### Ansible process

pip install --user ansible
pip install --user paramiko

```
vagrant up
ansible-playbook playbooks/nginxServer.yml
```

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

### References
```
https://letsencrypt.org/
``