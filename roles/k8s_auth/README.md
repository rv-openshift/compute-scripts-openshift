# Ansible Role: k8s_auth

Authenticate to OpenShift.

## Requirements

* Ansible Tower Credential to authenticate to OpenShift

## Role Variables

Default role variables.

```yaml
# Credentials are read from Ansible Tower credentials
k8s_auth_address: "{{ lookup('env','K8S_ADDR') }}"
k8s_auth_username: "{{ lookup('env','K8S_USERNAME') }}"
k8s_auth_password: "{{ lookup('env','K8S_PASSWORD') }}"

# Allow administration even if cert is expired or self-signed
k8s_validate_certs: no
```

## Dependencies

None.

## Example Playbook

```yaml
---
- name: Authenticate to OpenShift
  hosts: all
  gather_facts: true

  roles:
  - k8s_auth
```
