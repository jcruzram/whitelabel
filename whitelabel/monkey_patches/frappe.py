import frappe

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