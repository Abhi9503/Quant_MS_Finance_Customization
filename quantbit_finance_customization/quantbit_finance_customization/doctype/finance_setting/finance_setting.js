// Copyright (c) 2024, Quanbit Tech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Finance Setting', {
	setup: function(frm) {
  		frm.set_query("default_deduction_account", function(doc) {
			return {
				filters: [
					['Account', 'is_group', '=', false],
					['Account','company','=',frm.doc.company]
				]
			};
		});
		frm.set_query("default_discount_account", function(doc) {
			return {
				filters: [
					['Account', 'is_group', '=', false],
					['Account','company','=',frm.doc.company]
				]
			};
		});
	},
});


