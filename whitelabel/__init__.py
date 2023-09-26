# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import importlib

import frappe

patches_loaded = False

__version__ = '0.0.2'

if frappe.conf and frappe.conf.get("app_logo_url"):
    __logo__ = frappe.conf.get("app_logo_url") or '/assets/whitelabel/images/whitelabel_logo.jpg'
else:
    __logo__ = '/assets/whitelabel/images/whitelabel_logo.jpg'



def console(*data):
    frappe.publish_realtime("out_to_console", data, user=frappe.session.user)


def load_monkey_patches():
    global patches_loaded

    if (
        patches_loaded
        or not getattr(frappe, "conf", None)
        or not "whitelabel" in frappe.get_installed_apps()
    ):
        return

    for app in frappe.get_installed_apps():
        if app in ['frappe', 'erpnext']: continue

        folder = frappe.get_app_path(app, "monkey_patches")
        if not os.path.exists(folder): continue

        for module_name in os.listdir(folder):
            if not module_name.endswith(".py") or module_name == "__init__.py":
                continue

            importlib.import_module(f"{app}.monkey_patches.{module_name[:-3]}")

    patches_loaded = True


connect = frappe.connect


def custom_connect(*args, **kwargs):
    out = connect(*args, **kwargs)

    if frappe.conf.auto_commit_on_many_writes:
        frappe.db.auto_commit_on_many_writes = 1

    load_monkey_patches()
    return out


frappe.connect = custom_connect