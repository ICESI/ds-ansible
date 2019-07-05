#!/bin/bash
echo "Deleting VMs ..."
vagrant destroy -f
echo "Creating VMs ..."
vagrant up
echo "Deploying playbooks ..."
ansible-playbook -i hosts playbooks/nginx.yml
ansible-playbook -i hosts playbooks/python.yml
echo "Done"