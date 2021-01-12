# Async Actions
```
 Run a process and check on it later
 Run multiple process at once and check it on them later
 Run process and forget
 Async(How long to run)  
 Pool(How frequently to check default is 10 sec). Pool=0 It means ansible won't be watin complete first task , immediately move forward to second task
 async_status - check status of the an async task
 ```

# Strategy - how to playbook is executed
```
Default is linear strategy and run same tasks the  paralel in servers
Free - Host tasks runs  without regarding each other
Serial 1(batch) - Run host1 all tasks, then host2 and etc
Serial 2(batch) - Firstly run two host tasks same time and then continue host 3 and host 4
```


# Forks Maximum number of simultaneous connections Ansible made on each Task. , ansible default run paralel only 5 host(if you set 100 hosts). It declate in ansible.cfg
[fork_serial](https://medium.com/devops-srilanka/difference-between-forks-and-serial-in-ansible-48677ebe3f36)


# If ansible run tasks in multiple hosts and one of the task fail in node2. What happen ? Node1 and Node3 continue run . 
If you want to stop tasks all hosts for consistency you can use "any_errors_fatal=true" option

# ignore_errors, failed_when - fail on condition
```
- command: cat /var/log/ansible.log
  register: command_output
  failed_when: "'ERROR' in command_output.stdout"
```

# force_handlers: true , When we force handlers to run, the handlers will run when notified even if a task has failed on the host
https://medium.com/@knoldus/handling-errors-in-ansible-606ccc4d9833

# Block,rescue&always similar to catch&finally
https://blog.opstree.com/2019/11/19/error-handling-in-ansible/

# Fail_task
```
- name: 'This installation script knows only gateway.'
  fail:
    msg: "This host {{ inventory_hostname }} is not in a 'gateway' group, this script can not still install a worker."
  when: "'gateway' not in group_names"
```