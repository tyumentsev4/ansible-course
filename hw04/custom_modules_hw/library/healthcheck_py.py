#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import requests

DOCUMENTATION = r'''
---
module: healthcheck
author: Pupkin V.
short_description: healthcheck of site
description:
  - healthcheck of site with or without TLS
version_added: 1.0.0
requirements:
  - requests
  - python >= 3.6
options:
  addr:
    description:
      - Address of site we want to check
      - This is a required parameter
    type: str
  tls:
    description:
      - Whether site using certificates or not
      - Default value is 'True'
    type: bool
'''

EXAMPLES = r'''
- name: Check availability of site
  healthcheck:
    addr: mysite.example
  connection: local

- name: Check availability of site without certs
  healthcheck:
    addr: mysite.example
    tls: false
  connection: local
'''

RETURN = r'''
msg:
  description: Errors if occured
  returned: always
  type: str
  sample: ""
site_status:
  description: State status
  returned: always
  type: str
  sample: Available
rc:
  description: Return code
  returned: always
  type: int
  sample: 200
'''


def check_site(addr, tls):
    failed = False
    if tls:
        r = requests.get("https://%s" % addr, verify=False)
    else:
        r = requests.get("http://%s" % addr)
    rc = r.status_code

    if rc == 200:
        site_status = "Available"
    else:
        site_status = "Not available"

    msg = ""
    return (failed, msg, site_status, rc)


def main():
    # Аргументы для модуля
    arguments = dict(
        addr=dict(required=True, type='str'),
        tls=dict(type='bool', default="True")
    )
    # Создаем объект - модуль
    module = AnsibleModule(
        argument_spec=arguments,
        supports_check_mode=False
    )
    # Получаем аргументы
    addr = module.params["addr"]
    tls = module.params["tls"]

    # Вызываем нашу функцию
    lc_return = check_site(addr, tls)
    # Если задача зафейлилась
    if lc_return[0]:
        module.fail_json(changed=False,
                         failed=lc_return[0],
                         msg=lc_return[1],
                         site_status=lc_return[2],
                         rc=lc_return[3])
    # Если задача успешно завершилась
    else:
        module.exit_json(changed=False,
                         failed=lc_return[0],
                         msg=lc_return[1],
                         site_status=lc_return[2],
                         rc=lc_return[3])


if __name__ == "__main__":
    main()
