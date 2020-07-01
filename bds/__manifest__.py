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
    'depends': ['base','web','mail','decimal_precision','document','hr','snailmail'],
    'data': [
        'data/res.country.state.csv',
        'data/vn_district_default.xml',
        # 'data/vn_sg_ward_default.xml',
        # 'data/vn_sg_street_default.xml',
        'data/crm.street.csv',
        'data/crm.ward.csv',
        'data/crm_sequence.xml',
        'data/crm_state.xml',
        'static/src/xml/custom_render_formview_template.xml',
        'security/ir_group_rule.xml',
        'security/ir.model.access.csv',
        'wizard/announce_views.xml',
        'views/crm_product_view.xml',
        'views/crm_product_request_rule.xml',
        'views/crm_product_request_rule_sheet.xml',
        'views/crm_request_view.xml',
        'views/crm_request_request_rule.xml',
        'views/crm_request_request_rule_sheet.xml',
        'views/crm_state_city_view.xml',
        'views/menu_views.xml'
    ],
    'demo': [],
    'qweb': [
        # 'static/src/xml/inherit_button_action.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}