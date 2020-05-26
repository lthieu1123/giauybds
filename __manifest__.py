# -*- coding: utf-8 -*-
{
    'name': "Quản lý BĐS",
    'summary': """
        Quản lý BĐS""",
    'description': """
        Quản lý các BĐS và nhân viên
    """,
    'author': "Hiếu Lâm",
    'website': "https://www.facebook.com/lthieu37",
    "contributors": [
        "Hieu Lam <lt.hieu37@gmail.com>",
    ],
    'category': 'bds',
    'version': '1.0.0',
    'depends': ['base','web','mail','decimal_precision'],
    'data': [
        'data/res.country.state.csv',
        'data/vn_district_default.xml',
        'data/crm_sequence.xml',
        'static/src/xml/custom_render_formview_template.xml',
        
        'security/ir_group_rule.xml',
        'security/ir.model.access.csv',
        'views/crm_product_view.xml',
        'views/menu_views.xml'
    ],
    'demo': [],
    'qweb': [
        'static/src/xml/inherit_button_action.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}