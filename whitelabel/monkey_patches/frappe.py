import frappe

old_ = frappe._

def custom_(msg: str, lang: str | None = None, context: str | None = None) -> str:
    # Create a translation dictionary with replacements
    replacements = {
        'Almacéns': 'Almacenes',
        'inventarioss': 'inventarios',
        '(ventas)s': '(ventas)'
    }

    if "whitelabel" in frappe.get_installed_apps():
        configuracion = frappe.get_single("Whitelabel Setting")
        configuracion.whitelabel_app_name = configuracion.whitelabel_app_name or 'ERP'
        old_result = old_(msg, lang, context)
        old_result = old_result or ""

        # Apply the replacements using a loop
        for key, value in replacements.items():
            old_result = old_result.replace(key, value)

        old_result = old_result.replace("ERPNext", configuracion.whitelabel_app_name)
        
        return old_result
    else:
        msg = msg or ""
        old_result = old_(msg, lang, context)
        old_result = old_result or ""

        # Apply the replacements using a loop
        for key, value in replacements.items():
            old_result = old_result.replace(key, value)
        
        return old_result



frappe._ = custom_
frappe.utils.caching._ = custom_
# frappe.desk.desktop._ = custom_
