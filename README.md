* About Ansible, terminilogy and Install
* Ad-hoc commands, find info about modules
* Conditins
* Loops
* How to store playbook result in variables
* Inventory, dynamic inventories
* Tags
* Delegation
* Monitor - alert
* Vault
* Ansible Templating Jinja2 examples
* Ansible roles
* To do things
* Custom module and plugins  shell/python
* Testing Ansible roles with Molecule
* Yaml lint and ansible lint.  YAML syntax 
* Ansible galaxy
## Inventory
```
inventory.init file example
# Single
172.16.202.96 ansible_ssh_user=root
172.16.202.97 ansible_ssh_user=root

# Groups
[dev]
172.16.202.96 ansible_ssh_user=root

[test]
172.16.202.97 ansible_ssh_user=root

#Groups of Groups
[dev]
172.16.202.96 ansible_ssh_user=root
[test]
172.16.202.97 ansible_ssh_user=root

[testing:children]
dev
test

$ ansible testing -i hosts -m ping
```
## Tags
###  tags allow us execute only a subset of tasks defining them with tag attribute. example given tags_sample.yml files, If you set sample  then execute only  run echo command task and etc
```
ansible-playbook sample-playbook.yml --tags sample
ansible-playbook sample-playbook.yml --tags create
```
## Local_action module allow youexecute commands  local ansible server

## Delegation , Say if you are patching a package on a machine and you need to continue until a certain file is available on another machine. This is done in Ansible using the delegation option. For example  detegate_sample.yml  execute all task  groups of cent server  but  Tell Master and  writing hostname_output in ansible node in file on ansible node

##  Ansible also provides us a way to make the Rest calls using URI module.The URI module allows us to send XML or JSON payload and get the necessary details. In this article we will see how we can use the URI module and make the Rest calls. As for the article I will be using the Nexus artifactory to connect which run on the 8081 Port. The URL are specified in the vars/main.yml file
[rest_api_examples](http://jagadesh4java.blogspot.com/2016/09/ansible-rest-calls.html)


## Ansible vault example ??????????????????????????????????????????????????????????????????????????????

# Things to do with ansible 
## 1. Obtain a Environment Variable – To retrieve a Environment variable we can use
```
- name: Copy JAVA_HOME location to variable
  command:  bash -c -l "echo $JAVA_HOME"
  register: java_loc
- name: show debug
  debug: var=java_loc
```
## 2. Retrieve executables – In order to retrieve executables available in remote machine. Ex- to get where bash resides we can use
```
 - name: Where is Bash
   command: bash -c -l "which bash"
   register: whereis_bash

 - name: show Bash
   debug: var=whereis_bash
```
## 3. Wait for Port – When ever we run a script and wait for particular port to start we can use
```
- name: Wait for the nexus-iq Port to start
   wait_for: port=8070 delay=60
```
## 4. Template Variables – When ever we want to pass variables to template we can use
```
 - name: copy nexus-iq.sh start script
   template:
     src: nexus-iq.j2
     dest: "{{nexus_iq_dir}}/nexus-iq.sh"
     mode: "0755"
   vars:
     java_path: "{{java_loc.stdout}}"
     nexus_iq_path: "{{nexus_deploy_location}}"
     bash_is: "{{whereis_bash.stdout}}"
```
## 5. Update environment variables – We use source command to update environment variables .this can be done in Ansible as

- name: Source Bashrc to Update Env Variables
  shell: source {{ installation_user_home }}/.bashrc

## 6. Replace – There are some cases where we might need to replace things in the obtained values from remote hosts. We can do that in anisble as,
```
- name: Copy the jetty-https Template to the Remote Machine
    template:
       src: jetty-https.j2
       dest: "{{nexus_dir}}/nexus-{{nexus_version}}/conf/jetty-https.xml"
       mode: "0644"
       backup: "yes"
    vars:
      OBF: "{{ generated_password.stdout | replace('\n', '') | replace('^M', '') }}"
```
## 7. Pipelining - pipelining reduces the number of ssh connections required to execute a module on the remote server, by piping scripts to the ssh session instead of copying it.
This results in the performance improvement.
Note - pipe ling will only work if the option requiretty is disabled on all remote machines in the sudoers file
[ssh_connection]
pipelining = True

## 8. Turn off Facts -if you are not using any facts in your playbook ,we can disable that using the
```
- hosts: dev
  gather_facts: False
```
## 9. Step by Step Task - an ansible playbook will run all the tasks in a sequential way. What if we want to check before running the task. --step in Ansible will let you decide which tasks you want to run
```
ansible-playbook sample.yml --step
```
## 10. Dry Run – Some time we want our Ansible scripts to run but with out making any changes. This is something like testing our Scripts. We can do this as
```
ansible-playbook playbook.yml –check
```
## 11. Pause a Playbook – In Some cases we want out playbook to pause until some other action on the remote machine is done. We can do this by adding,
```
pause: prompt="waiting 60 Seconds" minutes=1 seconds=30
```
## 12. List Tasks – There may be cases where we want to check the tasks available before running them. This can done by
```
[root@cent delegate]# ansible-playbook --list-tasks sample-playbook.yml
playbook: sample-playbook.yml
  play #1 (cent):       TAGS: []
  Install zenity        TAGS: []
  configure zenity      TAGS: []
  Tell Master           TAGS: []
```
## 13. Syntax Checking – In order to check the syntax of the playbook we can use
```
[root@cent delegate]# ansible-playbook --syntax-check sample-playbook.yml
```
## 14. Verbose Mode – Run Ansible playbook in verbose mode as,
```
[root@cent delegate]# ansible-playbook --verbose sample-playbook.yml
```
## 15. install one more thing using from loop with_items module
```
- name: Installing Packages
  apt:
    name: "{{ item }}"
    update_cache: yes
  with_items:
    - git
    - nginx
    - memcached
```
## 16. You know ansible gather_fact module take all info from remote server but you can't want ot take all info example only take network info. To do this, you have to keep gather_facts to True and also pass one more attribute named gather_subset to fetch specific remote information. Ansible supports network, hardware, virtual, facter, ohai as subset
```
- hosts: web
  gather_facts: True
  gather_subset: network,virtual
```
## 17. any_errors_fatal ,  Sometime it is desired to abort the entire play on failure of any task on any host, mainly needed as deploy any app
```
---
- hosts: web
  any_errors_fatal: true
```
## 18. max_fail_percentage,think about you can  deploy app to 100 server if one of the servers deploy fail  all playbook failed  thats way we use this option.  If 30 of the servers to fail out of 100. Ansible will abort the rest of the play.
```
---
- hosts: web
  max_fail_percentage: 30
  serial: 30
```
## 19.  run_once, it is usefull you want to do some task step at once and delegate to specific host , yeni siz playbook icra edende normal olaraq bu birinci  hostun host faylinda oxuyur ve orda hansi task icra edir amma sen isteyir ki soecific hosta birncin bu emeliyyat getsin sonra basqa tasklar ishlesin
```
---
- hosts: web
    tasks:
    - name: Initiating Database
        script: initalize_wp_database.sh
        run_once: true
        delegate_to: 172.16.202.97
```
## 20. no_log option you want ot add log log option specific task on playbook
```
---
- hosts: web

  tasks:
  - include_vars: group_vars/encrypted_data.yml
    no_log: true

  - name: Printing encrypted variable
    debug:
      var: vault_db_password
    no_log: true
```
## 21. Debugging playbook
```
---
- hosts: web
  strategy: debug

  tasks:

  ...
```
## 22. Include multiple playbook to one playbook for that we use include option on playbook
```
---
- hosts: cent
  tasks:
    - include:  playbook1.yml
    - include:  playbook2.yml 
    - include:  playbook3.yml 
```

[General-Info](http://jagadesh4java.blogspot.com/p/ansible.html)