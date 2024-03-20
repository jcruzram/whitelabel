import frappe
from frappe.desk.desktop import Workspace
from frappe import _

@frappe.whitelist()
def get_workspace_sidebar_items():
	"""Get list of sidebar items for desk"""
	has_access = "Workspace Manager" in frappe.get_roles()

	# don't get domain restricted pages
	blocked_modules = frappe.get_doc("User", frappe.session.user).get_blocked_modules()
	blocked_modules.append("Dummy Module")

	filters = {
		"restrict_to_domain": ["in", frappe.get_active_domains()],
		"module": ["not in", blocked_modules],
	}

	if has_access:
		filters = []

	# pages sorted based on sequence id
	order_by = "sequence_id asc"
	fields = [
		"name",
		"title",
		"for_user",
		"parent_page",
		"content",
		"public",
		"module",
		"icon",
		"is_hidden",
	]
	all_pages = frappe.get_all(
		"Workspace", fields=fields, filters=filters, order_by=order_by, ignore_permissions=True
	)
	pages = []
	private_pages = []

	# Filter Page based on Permission
	for page in all_pages:
		try:
			page["content"] = page["content"].replace('Your Shortcuts', _('Your Shortcuts'))
			page["content"] = page["content"].replace('Quick Access', _('Quick Access'))
			page["content"] = page["content"].replace('Reports & Masters', _('Reports & Masters'))
			page["content"] = page["content"].replace('Reports &amp; Masters', _('Reports & Masters'))
			page["content"] = page["content"].replace('Masters &amp; Reports', _('Reports & Masters'))
			page["content"] = page["content"].replace('Elements', _('Elements'))
			page["content"] = page["content"].replace('Documents', _('Documents'))
			page["content"] = page["content"].replace('Settings', _('Settings'))
			page["content"] = page["content"].replace('Integrations', _('Integrations'))
			workspace = Workspace(page, True)
			if has_access or workspace.is_permitted():
				if page.public and (has_access or not page.is_hidden) and page.title != "Welcome Workspace":
					pages.append(page)
				elif page.for_user == frappe.session.user:
					private_pages.append(page)
				page["label"] = _(page.get("name"))
		except frappe.PermissionError:
			pass
	if private_pages:
		pages.extend(private_pages)

	if len(pages) == 0:
		pages = [frappe.get_doc("Workspace", "Welcome Workspace").as_dict()]
		pages[0]["label"] = _("Welcome Workspace")

	return {"pages": pages, "has_access": has_access}
