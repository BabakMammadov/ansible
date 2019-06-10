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


1) Lets Create a Directory Structure as,
[root@vx111a roles]# tree tomcat/
tomcat /
├── files
├── handlers
├── meta
├── tasks
├── templates
└── vars
2) Lets start creating the variable files first tomcat/vars
[root@vx111a vault]# cat main.yml
version: 8.0.32
http_port: 8084
3) Now lets create the tasks file. We will write 3 tasks files
Configure_java.yml – configure Java for Tomcat Server
Configure_tomcat.yml – Configure Tomcat
Update_path.yml – set JAVA_HOME and add java location to PATH in .bashrc file
Main.yml – this contains all the above files using include
