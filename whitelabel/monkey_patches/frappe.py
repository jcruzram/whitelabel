import frappe
import functools
import io
import itertools
import json
import operator
import os
import re
from contextlib import contextmanager
from csv import reader

from frappe.utils import cstr, get_bench_path, is_html, strip, strip_html_tags, unique
from frappe.translate import get_translations_from_apps, get_user_translations
# Cache keys
MERGED_TRANSLATION_KEY = "merged_translations"
USER_TRANSLATION_KEY = "lang_user_translations"

from typing import TYPE_CHECKING, Any, Callable, Literal, Optional, overload

import click
from werkzeug.local import Local, release_local

from frappe import as_unicode

controllers = {}
local = Local()

old_ = frappe._

def custom_(msg: str, lang: str | None = None, context: str | None = None) -> str:
    configuracion = frappe.get_single("Whitelabel Setting")
    configuracion.whitelabel_app_name = configuracion.whitelabel_app_name or 'ERP'
    old_result = old_(msg,lang,context)
    old_result = old_result or ""
    return old_result.replace("ERPNext", configuracion.whitelabel_app_name)

frappe._ = custom_
frappe.utils.caching._ = custom_
frappe.desk.desktop._ = custom_