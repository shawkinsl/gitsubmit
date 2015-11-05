import binascii
import os
import requests
from SSHKeyLib import SSHKeyLib

__author__ = 'shawkins'
"""
Yes, this filename does not comply with PEP8. Thank robotframework for that.
"""

class APIClientLib(object):

    def list_classes(self, url_root):
        classes_result = requests.get(url_root+"/classes/")
        classes_obj = classes_result.json()
        return_obj = {"status_code": classes_result.status_code,
                      "data": classes_obj}
        return return_obj

    def create_randomized_class(self, url_root):
        randomized_url_name = "test_random_class_" + binascii.b2a_hex(os.urandom(15))[:8]
        long_name = "A Randomized Class for Testing"
        class_obj = {"url_name": randomized_url_name, "class_name": long_name, "description": long_name}
        result = requests.post(url_root+"/classes/", data=class_obj)
        return_obj = {"status_code": result.status_code,
                      "data": result.json()}
        return return_obj

    def create_predefined_class(self, url_root):
        randomized_url_name = "test_predef_classs"
        long_name = "A Predefined Class for Testing"
        class_obj = {"url_name": randomized_url_name, "class_name": long_name, "description": long_name}
        result = requests.post(url_root+"/classes/", data=class_obj)
        return_obj = {"status_code": result.status_code,
                      "data": result.json()}
        return return_obj

    def list_keys_for_user(self, url_root, user):
        keys_result = requests.get(url_root+"/"+user+"/ssh_keys/")
        keys_obj = keys_result.json()
        return_obj = {"status_code": keys_result.status_code,
                      "data": keys_obj}
        return return_obj

    def add_randomized_key_to_user(self, url_root, user):
        ssh = SSHKeyLib()
        key = ssh.create_bogus_key()["pubkey_contents"]
        key_obj = {"pkey_contents": key}
        post_result = requests.post(url_root+"/"+user+"/ssh_keys/", data=key_obj)
        return_obj = {"status_code": post_result.status_code,
                      "data": post_result.json()}
        return return_obj