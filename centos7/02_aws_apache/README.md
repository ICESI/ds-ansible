### Ansible EC2 

Generate a key pair in aws and update its permissions
```
chmod 600 ~/.ssh/dbarragan.pem
```

Prepare an environment and execute the playbook
```
mkvirtualenv aws_deploy
pip install boto3 boto
ansible-vault create aws_keys.yml
cat aws_keys.yml 
ansible-playbook -i hosts --ask-vault-pass ec2_deploy.yml
```

Log in into the instance
```
ssh -i ~/.ssh/dbarragan.pem ec2-user@3.87.69.140
```

Delete en instance
```
ansible-playbook -i hosts --ask-vault-pass ec2_down.yml
```

### References
* https://docs.ansible.com/ansible/latest/modules/ec2_module.html

