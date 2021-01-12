# Ansible is an open-source configuration management, application deployment, intraservice orchestration and provisioning automation tool.
## Topics
* About ansible  
* Ad-hoc commands, find info about modules
* Playbooks
* Handlers
* Conditions
* Loops
* How to store playbook result in variables
* Inventory, dynamic inventories
* Tags
* Delegation
* Variables(var,set_fact,special vars) and lookups
* URI module
* Paralel executions
* Error handling
* Vault
* Ansible Templating Jinja2 examples
* Ansible roles
* Tips_Tricks
* Service discovery and managing multi enviroment
* Application deployment, rolling updates 
* VM Provisioning
* Custom module and plugins  shell/python
* Testing Ansible roles with Molecule
* Ansible galaxy

### About Ansible
What can you do with ansible <br />
- provisioning VM or cloud instance<br />
- automate all  linux tasks <br />
- automate routine network operation<br />
- application deployment(Continuous Delivery)<br />

It work over ssh protocol and agentless it means you don't need install any agent  remote system <br />
Prepare yaml file, execute it and REACH YOUR GOALS! <br />

Let’s have a look at some of the terminology used in ansible: <br />
- Controller Machine: Machine where Ansible is installed <br />
- Inventory: Information regarding servers to be managed<br />
- Playbook: Automation is defined using tasks defined in YAML format<br />
- Task: Procedure to be executed<br />
- Module: Predefined commands executed directly on remote hosts<br />
- Play: Execution of a playbook<br />
- Role: a Pre-defined way for organizing playbooks<br />
- Handlers: Tasks with unique names that will only be executed if notified by another task<br />

### Add-doc commands
/etc/ansible/hosts file is default inventory file for ansible. We store here server,app and network inventories and related variables. Firstly, Ansible connect to remote servers and executed commands with ssh protocol therefore ansible able to login to server without passwor and python must be installed on the remote server<br />
[use_this_link_for_passwordless_login_to_linux_servers](https://github.com/BabakMammadov/ansible_auto_ssh)<br />
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


#Using Ansible setup’s module to gather information about your hosts
ansible localhost -m setup
localhost | SUCCESS => {
  "ansible_facts": {
    "ansible_all_ipv4_addresses": [
        "10.27.12.77",
        "192.168.33.1"
    ],
    (MANY more facts)
  }

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

### How to store playbook task result on variables
Sometimes you need to store the  result of  playbook task  to variable and take to action over this. For example you can find txt file some directory and copy to another directory. For this you can  "store_result_on_variable"   yaml example.

### Inventory,  dynamic inventories
```
inventory.ini file example
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
Dynamic inventories 
Often a user of a configuration management system will want to keep inventory in a different software system. Most infrastructure or systems can be managed with a custom inventory sources likes files, database, cloud scripts…etc. Ansible easily supports all of these options via an external inventory system. For example we write python code  and connect to mysql database  and response must be  as json. We set it ansible side.<br />
[dynamic_ansible_inventory_plugin](https://docs.ansible.com/ansible/latest/user_guide/intro_dynamic_inventory.html)<br />
[dynamic_ansible_inventory_scripts](http://devopstechie.com/creating-custom-dynamic-inventory-with-ansible-using-python/)<br />

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

### Variables(var,set_fact,special vars) and lookups
Lookups are really useful for injecting dynamic data into your plays.<br />
Facts are key-value pairs gathered via the setup module if you run gather facts in a play.<br />
Vars are set by you.<br />
Special vars are special variables that only Ansible uses, that you can use in vars.<br />
Examples is given on lookupexamples directory, loops and condition and role testing <br />
[detailed_info_variables_and_fact_set_facts](https://www.oreilly.com/library/view/ansible-up-and/9781491979792/ch04.html)<br />
[Jerakia is an open source, highly flexible data lookup tool for performing hierarchical data lookups from numerous data sources.](https://www.craigdunn.org/2017/08/hierarchical-data-lookups-ansible/)<br />

###  Ansible also provides us a way to make the Rest calls using URI module.
The URI module allows us to send XML or JSON payload and get the necessary details. In this article we will see how we can use the URI module and make the Rest calls. As for the article I will be using the Nexus artifactory to connect which run on the 8081 Port. The URL are specified in the vars/main.yml file <br />
[rest_api_examples](http://jagadesh4java.blogspot.com/2016/09/ansible-rest-calls.html)

###  Paralel executions
strategy: free      # run all task same time  <br />
strategy: linear    # run task as sequency <br />
strategy: debug     # run task of playbook as degug  mode <br />

```
- name: a play to run all tasks as fast as we can
  hosts: servers
  strategy: free
  tasks:

  ...

- name: a play to run each task on each server before going to the next one    
  hosts: servers
  strategy: linear
  tasks:
```

###  Error handling


### Ansible vault example
Sometimes you  need to store your password, ssh keys, tokens in your playbooks and roles and you don't want the public to see it's common to store Ansible configurations in version control, we need a way to store secrets securely that's way we use ansible vault<br />
Examples are given vault directory<br/>
```
# Create users.yml  and set user password here for creating user on remote server(Actually we don't set plaintext password for user module on ansible playbook) just for example.

# Encrypt users.yml  with vault and set any password but keep in mind
ansible-vault encrypt users.yml
Confirm New Vault password: 
Encryption successful

# You can set password from file not with prompt
ansible-vault encrypt users.yml  --vault-password-file=./vault-passwd


# Look at users.yml  you will see encrypted file
cat  users.yml 
$ANSIBLE_VAULT;1.1;AES256
35663436373264386131633839383035396265396463333135396239356566373638323333653533
6132646230336664373461333863323737303232396230360a636663323533366530316631613137
35636662663665653461626632363365326439376231323633646234653130363132663061326665
6636656437623030630a336631333164393439623766623562653637633436333830393734386635
6634

# If you revert encrypted file to back
ansible-vault decrypt users.yml 

# If you look at encrypted file
ansible-vault view users.yml 

# If you edit encrypted file 
ansible-vault edit users.yml 

# Change exist vault pass for secret yaml
ansible-vault rekey users.yml

# If you run ansible-playbook users.yml with simple way you won't be because it was encrypted
ansible-playbook users.yml  --ask-vault-pass

# Write ansible vault pass to file and read from it
 ansible-playbook users.yml --vault-password-file ./vault-passwd
```
In this example we just encrypt playbook and run it but is isn't practical because every time we must decrypt playbook file for read and change. Practical version is create another properties  yaml file and  encrypt it with vault. then prepare ansible  playbook file and insert encryped variable yamls files and read encrypted properties file from encryped variable yaml <br/>
```
# Create variable file
echo "vault_a: aaa" > touch vault.yml

# Encrypt it and set password
ansible-vault encrypt  vault.yml

# See encrypted file
cat vault.yml
$ANSIBLE_VAULT;1.1;AES256
39356336323836656332666130363936623364656631373737363035383133633736333562333036
3137636566646237386639313463623062643137636565320a613638303936633361653931336362
33663438343338393534306166343865336566343366633264653032366638333034373463323339
3366626230656162390a373365663865303362313732653961663933636461376434316566333864
39346338363332613631333166366435313237636538656363643233633365326437

# Create main variables file and inject  vault_a variable  it as below
cat vars.tml
---
a: "{{ vault_a }}"
b: bbb

# Prepare playbook file  but there you must insert encryped vault.yml and vars.yml 
cat test.yml
---
- hosts: localhost
  vars_files:
    - "vars.yml"
    - "vault.yml"
  tasks:
  - name: execute a shell command
    shell: >
      ls
  - debug: msg="{{ a }} / {{ b }}"

# Execute it 
ansible-playbook test.yml  --ask-vault-pass

result is so: test.yml playbook read  "a" variable from  vars.yml and vars.yml read it from encrypted vault.yml

```
[encryped_string_and_use_playbook](https://medium.com/@schogini/ansible-vault-variables-a-tiny-demonstration-to-handle-secrets-a36132971015) <br/>

###  Ansible Templating Jinja2 examples

###  Ansible roles 
Examples are given ansible_role_testing directory

###  Custom module and plugins  shell/python

###  Testing Ansible roles with Molecule

## Tips_Tricks
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
     dest: "users.yml {{nexus_iq_dir}}/nexus-iq.sh"
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
[ansible_for_devops_book](https://www.mindg.cn/download/ansible-for-devops.pdf) <br/>
[ansible_advanced_hands_on_video_course](https://www.udemy.com/learn-ansible-advanced/?ranMID=39197&ranEAID=Fh5UMknfYAU&ranSiteID=Fh5UMknfYAU-paxAYXcjWsHvM7wcRKoEeg&LSNPUBID=Fh5UMknfYAU)<br/>
[ansible_bootcamp_video_course](https://www.udemy.com/ultimate-ansible-bootcamp/?ranMID=39197&ranEAID=Fh5UMknfYAU&ranSiteID=Fh5UMknfYAU-biqDz.TdNUci.NVIxeECjg&LSNPUBID=Fh5UMknfYAU)<br/>
[mastering_ansible_video_course](https://www.udemy.com/mastering-ansible-x/?ranMID=39197&ranEAID=Fh5UMknfYAU&ranSiteID=Fh5UMknfYAU-TwxNzZ1w5DAhWas0NlR1zQ&LSNPUBID=Fh5UMknfYAU)
[Step by step basic tutorial](http://jagadesh4java.blogspot.com/p/ansible.html) <br/>
[Top Tutorials on ansible](https://medium.com/quick-code/top-tutorials-to-learn-ansible-33afd23ea160)<br/>



Readable
https://blog.crisp.se/2018/01/27/maxwenzin/how-to-run-ansible-tasks-in-parallel
https://medium.com/@ibrahimgunduz34/parallel-playbook-execution-in-ansible-30799ccda4e0
https://shadow-soft.com/turbo-charge-your-ansible/
https://blog.knoldus.com/ansible-playbook-using-templates/
https://medium.com/@abhijeet.kamble619/ansible-molecule-test-using-docker-79a2e3e527a0
https://www.digitalocean.com/community/tutorials/how-to-manage-multistage-environments-with-ansible

SSH bastion host
https://blog.scottlowe.org/2015/12/24/running-ansible-through-ssh-bastion-host/
https://blog.keyboardinterrupt.com/ansible-jumphost/