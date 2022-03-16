#!/usr/bin/python

from ansible.errors import AnsibleFilterTypeError
import re


def mac_filter(mac: str) -> str:
    '''
        mac address conversion 
    '''
    if not isinstance(mac, str):
        raise AnsibleFilterTypeError("String type is expected, "
                                     "got type %s instead" % type(mac))

    regex = r"^([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})$"
    match = re.match(regex, mac)
    if match is None:
        raise AnsibleFilterTypeError("Expected hex string of length 12 ")
    return ":".join(match.groups())


class FilterModule(object):
    def filters(self):
        return {
            'mac_filter': mac_filter,
        }
