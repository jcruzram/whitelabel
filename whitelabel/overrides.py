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

# from typing import TYPE_CHECKING, Any, Callable, Literal, Optional, overload

# import click
# from werkzeug.local import Local, release_local

# from frappe import as_unicode

# controllers = {}
# local = Local()

# def _(msg: str, lang: str | None = None, context: str | None = None) -> str:
#     """Returns translated string in current lang, if exists.
#     Usage:
#             _('Change')
#             _('Change', context='Coins')
#     """
#     # frappe.log_error('overrides',msg)
#     from frappe.translate import get_all_translations
#     from frappe.utils import is_html, strip_html_tags

#     if not hasattr(local, "lang"):
#         local.lang = lang or "en"

#     if not lang:
#         lang = local.lang

#     non_translated_string = msg

#     if is_html(msg):
#         msg = strip_html_tags(msg)

#     # msg should always be unicode
#     msg = as_unicode(msg).strip()

#     translated_string = ""

#     all_translations = get_all_translations(lang)
#     if context:
#         string_key = f"{msg}:{context}"
#         translated_string = all_translations.get(string_key)

#     if not translated_string:
#         translated_string = all_translations.get(msg)

#     if translated_string:
#         translated_string = translated_string.replace("ERPNext","My ERP**")
#     non_translated_string = non_translated_string.replace("ERPNext","My ERP**")

#     return translated_string or non_translated_string

def get_all_translations(lang: str) -> dict[str, str]:
	"""Load and return the entire translations dictionary for a language from apps + user translations.

	:param lang: Language Code, e.g. `hi`
	"""
	if not lang:
		return {}
	def _merge_translations():
		all_translations = get_translations_from_apps(lang).copy()
		try:
			# get user specific translation data
			user_translations = get_user_translations(lang)
			all_translations.update(user_translations)

		except Exception:
			pass

		return all_translations

	try:
		return frappe.cache().hget(MERGED_TRANSLATION_KEY, lang, generator=_merge_translations)
	except Exception:
		# People mistakenly call translation function on global variables
		# where locals are not initalized, translations dont make much sense there
		return {}