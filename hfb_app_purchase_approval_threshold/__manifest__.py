# -*- coding: utf-8 -*-
# vim: tabstop=4 softtabstop=0 shiftwidth=4 smarttab expandtab fileformat=unix
#################################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2017-2026 Hadron for Business sp. z o.o. (http://hadronforbusiness.com)
#
# This program is proprietary software, licensed under the Odoo Proprietary
# License v1.0 (OPL-1). Its use is governed by the Odoo Apps terms available
# at https://www.odoo.com/documentation/user/legal/licenses.html and the
# license agreement accepted at purchase / installation.
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the
# Software or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in
# all copies or substantial portions of the Software.
#
#################################################################################
{
    'name': "Purchase Approval Levels",
    'summary': "Multi-level approval of purchase orders by amount: each level has its own threshold and approvers",
    'description': """
Purchase Approval Levels
========================

Odoo can ask a manager to approve purchase orders above one amount. Real
companies need a ladder: a team leader approves small orders, a director the
bigger ones, the CEO the biggest.

Define as many approval levels as you need (Purchase > Configuration >
Approval Levels), each with a minimum amount and its approvers (users and/or
a user group). When an order is confirmed, it waits in "To Approve" until
every required level has approved it, in order of amount. Approvers get an
activity, approve or reject (with a reason) right on the order, and the
whole history is kept on the order and in its chatter.

Settings (Purchase > Configuration > Settings): compare the thresholds with
the total including taxes (default) or the untaxed amount, and require all
levels up to the amount or only the highest one.
""",
    'version': "18.0.1.0.0",
    'author': "Hadron for Business sp. z o.o.",
    'website': "http://hadronforbusiness.com",
    'license': "OPL-1",
    'category': "Inventory/Purchase",
    'depends': [
        'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/purchase_approval_security.xml',
        'data/mail_activity_type_data.xml',
        'wizard/purchase_approval_reject_views.xml',
        'views/purchase_approval_level_views.xml',
        'views/purchase_order_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'images': [
        'static/description/banner_screenshot.png',
    ],
    'installable': True,
    'application': False,
}
