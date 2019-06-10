# Ansible is an open-source configuration management, application deployment, intraservice orchestration and provisioning automation tool.
## Topics
* About Ansible, terminalogy
* Ad-hoc commands, find info about modules
* Playbooks
* Handlers
* Conditions
* Loops
* How to store playbook result in variables
* Inventory, dynamic inventories
* Tags
* Delegation
* Monitor-alert
* Vault
* Ansible Templating Jinja2 examples
* Ansible roles
* To do things
* Custom module and plugins  shell/python
* Testing Ansible roles with Molecule
* Yaml lint and ansible lint.  YAML syntax
* Ansible galaxy

### Add-doc commands
/etc/ansible/hosts file is default inventory file for ansible. We store here server,app and network inventories and related variables. Firstly, Ansible connect to remote servers and executed commands with ssh protocol therefore ansible able to login to server without passwor and python must be installed on the remote server
[use_this_link_for_passwordless_to_linux_servers](https://github.com/BabakMammadov/ansible_auto_ssh)
```
# Create sample group of host and make passwordless login to these servers using above script
cat /etc/ansible/hosts
[test]
172.16.100.131 
172.20.20.13
[prod]
172.10.20.10

# List all hosts default from hosts file(/etc/ansible/hosts)
ansible all --list-hosts
# List from other inventory file
ansible all --list-hosts -i inventory.ini
# List default inventory  and inside of group
ansible test --list-hosts
# send command  specific group of servers and from  non-default inventory file
ansible -i /etc/ansible/inventory.ini local -a ‘uptime'
# Or specific hosts
ansible -i inventory.ini 172.16.100.131  -a ‘uptime'
```
Command&Shell&Raw Modules
```
# You can only execute binaries commands on the remote node with command module, but you cann't use buil-in functions or  shell redirections with command module
ansible -i inventory.ini   172.16.100.131 -m command  -a 'who‘
# Make output  on the single line
ansible -i inventory.ini   172.16.100.131  -m command -a 'who ‘  -o

# Let's suppose, python doesn't exist remote server(Ubuntu some versions). Ansible won't be execute commands on remote server  and  give us python error. Thats way we can use ansible raw module and install firstly python on remote server
ansible  -i inventory.ini  172.16.100.133  -m raw -a 'who'

# Install python to ubuntu server with raw module(After that we use another ansible module):
ansible -i inventory.ini  172.16.100.135  -m  raw  -a "apt-get install python -y"

# Use shell builtIN functions(mostly we use built in func on the shell scripts) and redirections with ansible shell module.Lets simulate redirection error with command module
ansible  -i inventory.ini   172.16.100.131  -m command -a 'df -hT| grep xfs '
172.16.100.131 | FAILED | rc=1 >>
df: invalid option -- '|'

ansible  -i inventory.ini 172.16.100.131  -m shell  -a 'df -hT| grep xfs '  
172.16.100.131 | CHANGED | rc=0 >>
/dev/mapper/centos-root xfs        17G 1003M   17G   6% /
/dev/sda1               xfs      1014M  133M  882M  14% /boot

ansible  -i inventory.ini 172.16.100.131  -m shell  -a 'df -h > /var/tmp/df.out’  
ansible  -i inventory.ini 172.16.100.131  -m shell  -a 'cat /var/tmp/df.out’ 


# By default, ansible executed commands  user on remote server with root. if we want to use  another sudo user and want to execute all tasks  with this user. For this we must be add this user to wheel group(administator group) and  sudoers file(nopassword option)

# Do it on remote system
useradd -m -d /home/user -s /bin/bash -k  /etc/skel -g user user
echo "pass" | passwd --stdin user
usermod -aG wheel user
%wheel ALL=(ALL) NOPASSWD: ALL

Defination:
-m module_name :  set it for  which module you will use
-a "command" : set it for which commands will be executed on remote server
-i inventory.ini ipOrgroup_of_servers :  set it for which servers it will be executed
-become  -u user : set it for which user will execute these commands on remote server


# In ansible server
ansible  -i inventory.ini 172.16.100.131 -become  -u user  -a “whoami"

# Install vim on the remote hosts with sudo user
ansible  -i inventory.ini 172.16.100.131 -become  -u user  -m  raw  -a "yum install vim -y “

# Use ansible default yum module
ansible -i inventory.ini 172.16.100.131 -become  -u user  -m yum -a "name=httpd state=present" 

# Connect remote server and check another server tcp port as below. We will use what_for ansible module for this in the future
ansible -m shell -a "nc -w1 -zv 1.1.1.1  8080; echo $?  " test -become  -u user -i inventory.ini

# Check internet connection on remote server
ansible -m shell -a "echo 'wget www.az; echo $? ; rm -f index.html" test -become  -u user -i inventory.ini

# File transfer(from ansible server  to remote hosts that under test group in the inventory file)
ansible test  -m copy -a "src=/etc/hosts dest=/tmp/hosts" -i inventory.ini

# File module change owner and perm
ansible test -m file -a "dest=/srv/foo/a.txt mode=600 owner=babak group=babak" -i inventory.ini

# The file module can also create directories, similar to mkdir -p:
ansible test -m file -a "dest=/path/to/c mode=755 owner=babak group=babak state=directory" -i inventory.ini

# Working with git module
ansible test -m git -a "repo=https://foo.example.org/repo.git dest=/srv/myapp version=HEAD" -i inventory.ini

# Gather  facts is using for gather infor about remote system and then you can use this info as dynamic variables
ansible  -i inventory.ini 172.16.100.131  -m setup

# Create file remote server
ansible  -i inventory.ini 172.16.100.131 -m file -a 'path=/var/tmp/ansible_test.txt state=touch'

# Remove  file remote server
ansible  -i inventory.ini 172.16.100.131  -m file -a 'path=/var/tmp/ansible_test.txt state=absent'

# Create soft link
ansible  -i inventory.ini 172.16.100.131 -m file -a 'src=/etc/hosts dest=/var/tmp/hosts state=link'

# Copy  file and Backup
ansible  -i inventory.ini 172.16.100.131  -m copy -a 'src=/etc/hosts dest=/etc/hosts backup=yes’

# Extract specific info with gather_fact module
ansible -m  setup  -i inventory.ini test -a 'filter=ansible_mounts'
ansible -m  setup  -i inventory.ini test -a 'filter=ansible_distribution'
ansible -m  setup  -i inventory.ini test  -a 'filter="ansible_kernel"'
```
### Find info about modules.
```
# List all ansible modules
ansible-doc -l
# Find specific module name f.e yum module
ansible-doc -l  | grep yum
# Look detail info about module
ansible-doc module_name
ansible-doc -s module_name
ansible-doc apt
```
### Playbook
Lets suppose  we want to executed one more commands(tasks) on remote servers. It isn't best practise every time that we use  single line ansible command for doing something. It will be boring and complex on huge tasks.Therefore we use playbook and run one more tasks inside of the  one yaml file. Example is given in "playbook_handler.yml" file
In this playbook we executed following tasks(install httpd,openssh,vim and start httpd service on under of test group servers).
```
ansible-playbook  playbook.yml  -i  inventory.ini
```
### Handlers
Ansible playbook executed tasks as sequential. If we take latest playbook.yml in there all tasks executed step by step and latest  task will execute "Start apache service" task . It isn't not proper way because we want to start httpd service at  once after installed httpd service.
For this we must use handlers. Example is given "playbook_handler.yml" file
```
ansible-playbook  playbook_handler.yml  -i  inventory.ini
```
### Conditions
Lets suppose we have different version linux os in under of test group servers and don't want to use two  playbook yaml file for every os version(Ubuntu and centos). For this we will use "when" conditions sample. Second example just check file exist or no and take action on result of this file. Examples is given  playbook_condition.yml and playbook_condition_2.yml files
In there register options using for register output of command 
```
ansible-playbook  playbook_condition.yml -i  inventory.ini
ansible-playbook  playbook_condition_2.yml -i  inventory.ini
```

### Loops
Lets suppose we want to install much more packages on remote server  and won't to write task for every new package. Therefore we use loops. Detailed example is given playbook_loop.yml file.
In there debug module using for show you information. 

### How to store playbook result in variables

### Inventory
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
### Tags
tags allow us execute only a subset of tasks defining them with tag attribute. example given tags_sample.yml files, If you set sample  then execute only  run echo command task and etc
```
ansible-playbook sample-playbook.yml --tags sample
ansible-playbook sample-playbook.yml --tags create
```
### Local_action 
allow you execute commands local ansible server

### Delegation
Say if you are patching a package on a machine and you need to continue until a certain file is available on another machine. This is done in Ansible using the delegation option. For example  detegate_sample.yml  execute all task  groups of cent server  but Tell Master and  writing hostname_output in ansible node in file on ansible node

###  Ansible also provides us a way to make the Rest calls using URI module.
The URI module allows us to send XML or JSON payload and get the necessary details. In this article we will see how we can use the URI module and make the Rest calls. As for the article I will be using the Nexus artifactory to connect which run on the 8081 Port. The URL are specified in the vars/main.yml file
[rest_api_examples](http://jagadesh4java.blogspot.com/2016/09/ansible-rest-calls.html)


### Ansible vault example ??

## Things to do with ansible
### 1. Obtain a Environment Variable – To retrieve a Environment variable we can use
```
- name: Copy JAVA_HOME location to variable
  command:  bash -c -l "echo $JAVA_HOME"
  register: java_loc
- name: show debug
  debug: var=java_loc
```
### 2. Retrieve executables 
In order to retrieve executables available in remote machine. Ex- to get where bash resides we can use
```
 - name: Where is Bash
   command: bash -c -l "which bash"
   register: whereis_bash

 - name: show Bash
   debug: var=whereis_bash
```
### 3. Wait for Port
When ever we run a script and wait for particular port to start we can use
```
- name: Wait for the nexus-iq Port to start
   wait_for: port=8070 delay=60
```
### 4. Template Variables
When ever we want to pass variables to template we can use
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
### 5. Update environment variables
We use source command to update environment variables .this can be done in Ansible as
```
- name: Source Bashrc to Update Env Variables
  shell: source {{ installation_user_home }}/.bashrc
```
### 6. Replace
There are some cases where we might need to replace things in the obtained values from remote hosts. We can do that in anisble as,
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
### 7. Pipelining
pipelining reduces the number of ssh connections required to execute a module on the remote server, by piping scripts to the ssh session instead of copying it.
This results in the performance improvement.
Note - pipe ling will only work if the option requiretty is disabled on all remote machines in the sudoers file
```
[ssh_connection]
pipelining = True
```
### 8. Turn off Facts 
if you are not using any facts in your playbook ,we can disable that using the
```
- hosts: dev
  gather_facts: False
```
### 9. Step by Step Task
ansible playbook will run all the tasks in a sequential way. What if we want to check before running the task. --step in Ansible will let you decide which tasks you want to run
```
ansible-playbook sample.yml --step
```
### 10. Dry Run 
Some time we want our Ansible scripts to run but with out making any changes. This is something like testing our [playbooks]. We can do this as
```
ansible-playbook playbook.yml –check
```
### 11. Pause a Playbook 
In Some cases we want out playbook to pause until some other action on the remote machine is done. We can do this by adding,
```
pause: prompt="waiting 60 Seconds" minutes=1 seconds=30
```
### 12. List Tasks
There may be cases where we want to check the tasks available before running them. This can done by
```
[root@cent delegate]# ansible-playbook --list-tasks sample-playbook.yml
playbook: sample-playbook.yml
  play #1 (cent):       TAGS: []
  Install zenity        TAGS: []
  configure zenity      TAGS: []
  Tell Master           TAGS: []
```
### 13. Syntax Checking – In order to check the syntax of the playbook we can use
```
[root@cent delegate]# ansible-playbook --syntax-check sample-playbook.yml
```
### 14. Verbose Mode – Run Ansible playbook in verbose mode as,
```
[root@cent delegate]# ansible-playbook --verbose sample-playbook.yml
```
### 15. install one more thing using from loop with_items module
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
### 16. gather_fact
You know ansible gather_fact module take all info from remote server but you can't want ot take all info example only take network info. To do this, you have to keep gather_facts to True and also pass one more attribute named gather_subset to fetch specific remote information. Ansible supports network, hardware, virtual, facter, ohai as subset
```
- hosts: web
  gather_facts: True
  gather_subset: network,virtual
```
### 17. any_errors_fatal
Sometimes,  it is desired to abort the entire play on failure of any task on any host, mainly needed as deploy any app
```
---
- hosts: web
  any_errors_fatal: true
```
### 18. max_fail_percentage
think about you can  deploy app to 100 server if one of the servers deploy fail  all playbook failed  thats way we use this option.  If 30 of the servers to fail out of 100. Ansible will abort the rest of the play.
```
---
- hosts: web
  max_fail_percentage: 30
  serial: 30
```
### 19. run_once
it is usefull you want to do some task step at once and delegate to specific host , yeni siz playbook icra edende normal olaraq bu birinci  hostun host faylinda oxuyur ve orda hansi task icra edir amma sen isteyir ki soecific hosta birncin bu emeliyyat getsin sonra basqa tasklar ishlesin
```
---
- hosts: web
    tasks:
    - name: Initiating Database
        script: initalize_wp_database.sh
        run_once: true
        delegate_to: 172.16.202.97
```
### 20. no_log
you want to add no log option specific task on playbook
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
### 21. Debugging playbook
```
---
- hosts: web
  strategy: debug

  tasks:

  ...
```
### 22. Include multiple playbook to one playbook for that we use include option on playbook
```
---
- hosts: cent
  tasks:
    - include:  playbook1.yml
    - include:  playbook2.yml 
    - include:  playbook3.yml 
```
[Example to shell built in command on linux:](https://www.gnu.org/software/bash/manual/html_node/Shell-Builtin-Commands.html)
[General-Info](http://jagadesh4java.blogspot.com/p/ansible.html)