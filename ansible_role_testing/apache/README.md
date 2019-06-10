Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).


## How to create role 
ansible-galaxy init /etc/ansible/roles/apache --offline

## How to run role as two variant
cd ansible_role_testing
ansible-playbook runsetup.yml  # it read general ansible hosts file 
ansible-playbook apache/tests/test.yml -i apache/tests/inventory  # it read custom role inventory files



## How to define variables on ansible roles, playbook itself, inventory files, For host variables – /etc/ansible/host_vars , For group variables – /etc/ansible/group_vars , also yiu can set  runtime variables 

### For roles you can add  defaults or vars  directory to main.yml, For example apache/defaults/main.yml 
```
---
webserver_package: tomcat
http_server_port: 80
```
### OR  apache/vars/main.yml
```
---
webserver_package: httpd
```
### playbook itself
```
---
- hosts: linuxservers
  vars:
    http_server_port: 80
    webserver_package: httpd
  tasks:
    - name: Install Apache Web Server
      yum: name={{webserver_package}} state=latest
      notify:
        - openport
        - startwebserver
  handlers:
    - name: openport
      service: name=httpd state=started
    - name: startwebserver
      firewalld: port={{http_server_port}}/tcp permanent=true state=enabled immediate=yes

- hosts: ansibleclient2
  tasks:
    - name: upload index page
      get_url: url=http://www.purple.com/faq.html dest=/var/www/html/index.html
```
### Inventory files
```
[test]
ansibleclient1 
# ansibleclient2    http_server_port=80   webserver_package=httpd

[linuxservers:vars]
http_server_port=80
webserver_package=httpd
webserver_package=httpd
```

### Runtimes variables
```
ansible-playbook webserver-roles.yml –e ‘webserver_package=httpd http_server_port=80’

And plaubook as above

```
