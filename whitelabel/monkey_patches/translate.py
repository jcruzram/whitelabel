import frappe
from frappe import translate
from frappe.translate import get_translation_dict_from_file


old_get_user_translations = translate.get_user_translations
def get_user_translations(lang):
    if not frappe.db:
        frappe.connect()
    out = frappe.cache().hget('lang_user_translations', lang)
    if not out:
        user_translation = old_get_user_translations(lang)
        if lang == 'en' and frappe.translate.get_user_lang() == "en":
            app = 'whitelabel'
            path =frappe.get_app_path(app, "translations","en_global.csv")
            out = get_translation_dict_from_file(path, lang, app)
            # User translation has the highest priority
            out.update(user_translation)
        else:
            out = user_translation
        frappe.cache().hset('lang_user_translations', lang, out)

    return out

translate.get_user_translations = get_user_translations    