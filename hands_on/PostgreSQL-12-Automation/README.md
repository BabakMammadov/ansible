# Ansible PostgreSQL-12 Automation
<img src="https://www.redhat.com/cms/managed-files/Logotype_RH_AnsibleAutomation_RGB_Black_2.png" width="400">

## What will this playbook do?

1. Install PostgreSQL 12
2. Initialize Database
3. Create Database  # From Vars
4. Create DB Username with Password  # From Vars
5. Grant All privileges from created user to created DB
6. Update Configuration files from SCM
7. Uninstall PostgreSQL 12 (Without wipe data)

FYI: Due to credentials we encrypted `GlobalVars`.So you need to know vault password
- To decrypt it just execute the following command and input vault password:
```bash
$ ansible-vault decrypt ./vars/*
```

First of all you should edit your invertory file (hosts) and set Target SSH Credentials.
Then you should edit your variables files under `/vars/` folder
- To Install PostgreSQL 12
```bash
$ ansible-playbook playbook.yml -e please=install --ask-vault-pass
```
- To Uninstall PostgreSQL 12
```bash
$ ansible-playbook playbook.yml -e please=uninstall --ask-vault-pass
```
- To Update PostgreSQL 12 Configuration files
```bash
$ ansible-playbook playbook.yml -e please=update --ask-vault-pass
```
## What should I Do before executing?
## Make sure that your Target Server has full access to Internet
#### Successfully Tested on RHEL7/CentOS7

| Latest stable release | [![release](https://img.shields.io/badge/release-latest-green.svg)]() |
|---|---|

Copyright &copy; 2020 Team of DevOps. All Rights Reserved
