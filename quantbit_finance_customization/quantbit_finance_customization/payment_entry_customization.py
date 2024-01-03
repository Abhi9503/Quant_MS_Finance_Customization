import frappe

@frappe.whitelist()
def get_payment_references(party,party_type):
    doctype_li = ["Sales Invoice","Purchase Invoice","Journal Entry"]
    updated_doc = []
    for doctype in doctype_li:
        if doctype != "Journal Entry":
            field_list=[]
            if doctype == "Sales Invoice":
                doctype_name ="customer" 
                field_list=['name','grand_total','outstanding_amount',"return_against","base_net_total"]
            else:
                doctype_name="Supplier"
                field_list=['name','grand_total','outstanding_amount',"return_against","taxes_and_charges_deducted"]
            doc = frappe.get_all(doctype, {doctype_name: party, 'docstatus': 1},field_list)
            if doc:
                for entry in doc:
                    entry["doctype"] = doctype
                    entry["ref_doctype"]=entry["return_against"] if entry["return_against"] else None
                    if doctype =="Sales Invoice":
                        entry["base_net_total"]=entry["base_net_total"] if entry["base_net_total"] else None
                    else:
                        entry["base_net_total"]=None
                    if doctype =="Purchase Invoice":
                        entry["taxes_and_charges_deducted"]=entry["taxes_and_charges_deducted"] if entry["taxes_and_charges_deducted"] else None
                    else:
                        entry["taxes_and_charges_deducted"]=None  
                    updated_doc.append(entry)
        else:
            doc = frappe.get_all("Journal Entry Account", {"party": party, "party_type":party_type, 'docstatus': 1},
                                 ['parent', 'debit_in_account_currency', 'credit_in_account_currency',"reference_name","account"])
            if doc:
                for entry in doc:
                    outstanding_amt=0
                    if(entry["credit_in_account_currency"]):
                        account_doc=frappe.get_value("Account",{"name":entry["account"]},"account_type")
                        outstanding_amt=-entry["credit_in_account_currency"] if(account_doc=="Receivable") else entry["credit_in_account_currency"]
                    if(entry["debit_in_account_currency"]):
                        account_doc=frappe.get_value("Account",{"name":entry["account"]},"account_type")
                        outstanding_amt=-entry["debit_in_account_currency"] if(account_doc=="Payable") else entry["debit_in_account_currency"]
                        
                    entry["doctype"] = doctype
                    entry["name"] = entry["parent"]
                    entry["grand_total"] = entry["credit_in_account_currency"] or entry["debit_in_account_currency"]
                    entry["outstanding_amount"] = outstanding_amt
                    entry["ref_doctype"]=entry["reference_name"] if entry["reference_name"] else None
                    entry["base_net_total"]=None
                    entry["taxes_and_charges_deducted"]=None  
                    updated_doc.append(entry)
    return updated_doc


