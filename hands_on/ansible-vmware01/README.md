# Ansible VMware

This repository contains a role for create, delete or to manage a Virtual Machine (VM) using VMware vSphere vCenter

## Prerequisites
* [PyVmoni](https://pypi.python.org/pypi/pyvmomi/) is the Python SDK for the VMware vSphere API that allows you to manage ESX, ESXi, and vCenter.

### Install PyVmoni
The official release is available using epel, just run `yum install python2-pyvmomi`

## Role Variables
Look the file [`defaults/main.yml`](defaults/main.yml)

## Example Playbook
```yaml
---
- hosts: localhost
  gather_facts: false
  vars_prompt:
    - name: "vmware_vcenter_username"
      prompt: "Enter your vCenter username"
      private: no

    - name: "vmware_vcenter_password"
      prompt: "Enter your vCenter password"
      private: yes
  roles:
    - vpshere_vm_ops
```

## Dependencies
Not yet.

## Licens
MIT
