# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
# import whitelabel.overrides



__version__ = '0.0.1'

if frappe.conf and frappe.conf.get("app_logo_url"):
    __logo__ = frappe.conf.get("app_logo_url") or '/assets/whitelabel/images/whitelabel_logo.jpg'
else:
    __logo__ = '/assets/whitelabel/images/whitelabel_logo.jpg'

# Replace frappe function with custom function
# frappe._ = whitelabel.overrides._
