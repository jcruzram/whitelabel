$(document).ready(function() {
    frappe.after_ajax(function () {
        if (frappe.boot.whitelabel_setting.show_help_menu) {
            // $('.dropdown-help').css('display','block');
            $('.dropdown-help').attr('style', 'display: block !important');
        }
        if (frappe.boot.whitelabel_setting.logo_width) {
            $('.app-logo').css('width',frappe.boot.whitelabel_setting.logo_width+'px');
        }
        if (frappe.boot.whitelabel_setting.logo_height) {
            $('.app-logo').css('height',frappe.boot.whitelabel_setting.logo_height+'px');
        }
        if (frappe.boot.whitelabel_setting.navbar_background_color) {
            $('.navbar').css('background-color',frappe.boot.whitelabel_setting.navbar_background_color)
        }
        if (frappe.boot.whitelabel_setting.custom_navbar_title_style && frappe.boot.whitelabel_setting.custom_navbar_title) {
            $(`<span style=${frappe.boot.whitelabel_setting.custom_navbar_title_style.replace('\n','')} class="hidden-xs hidden-sm">${frappe.boot.whitelabel_setting.custom_navbar_title}</span>`).insertAfter("#navbar-breadcrumbs")
        }
    })
})
frappe.underscore = function (txt, replace, context = null) {
    const replacements = {
        'Almacéns': 'Almacenes',
        'inventarioss': 'inventarios',
        '\\(ventas\\)s': '(ventas)'
    };
	if (!txt) return txt;

    if (typeof txt != "string") return txt;

    // if(txt.includes('Create an Item')){
    //     alert(txt);
    // }
	let translated_text = "";

	let key = txt; // txt.replace(/\n/g, "");
	if (context) {
		translated_text = frappe._messages[`${key}:${context}`];
	}

	if (!translated_text) {
		translated_text = frappe._messages[key] || txt;
	}

	if (replace && typeof replace === "object") {
		translated_text = $.format(translated_text, replace);
	}
    frappe.boot.whitelabel_setting.whitelabel_app_name = frappe.boot.whitelabel_setting.whitelabel_app_name || 'ERP'
    let modifiedString = translated_text.replace("ERPNext", frappe.boot.whitelabel_setting.whitelabel_app_name);
    for (const key in replacements) {
        if (replacements.hasOwnProperty(key)) {
            const regex = new RegExp(key, 'g');
            modifiedString = modifiedString.replace(regex, replacements[key]);
        }
    }
	return modifiedString;
};
frappe._ = frappe.underscore;
window.__ = frappe._;