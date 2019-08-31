# -*- coding: utf-8 -*-
{
    'name': "Stock Move Report",

    'description': """
        Use of wizards to generate excel files with Stock moves information
    """,

    'author': "Abraham J Febres, Globalitec GT",
    'website': "http://globalitec.gt",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'account_accountant', 'report_xlsx', 'stock', 'sale', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/action_report.xml',
        'wizard/accouting_report_sales_views.xml',
        'views/menu_items_views.xml',
    ],
    # only loaded in demonstration mode
}