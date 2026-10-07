# -*- coding: utf-8 -*-
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
"""	@version	18.0.1.0.0
	@owner  Hadron for Business
	@author Hadron for Business sp. z o.o.
	@date   2026.10.07

	Purchase Approval Levels - approval steps
	One approval step of a purchase order: a copy of the level (name, amount)
	taken when the order was submitted, its state and who approved it when.
"""
from odoo import fields, models


class PurchaseOrderApproval(models.Model):
    _name = 'purchase.order.approval'
    _description = "Purchase Order Approval Step"
    _order = 'order_id, min_amount, sequence, id'

    order_id = fields.Many2one('purchase.order', required=True, index=True, ondelete='cascade')
    company_id = fields.Many2one(related='order_id.company_id', store=True)
    level_id = fields.Many2one('purchase.approval.level', string="Level", ondelete='set null')
    name = fields.Char(string="Level", required=True)
    sequence = fields.Integer()
    min_amount = fields.Monetary(string="Orders From", currency_field='company_currency_id')
    company_currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection(
        [('pending', "Waiting"), ('approved', "Approved")], default='pending', required=True)
    user_id = fields.Many2one('res.users', string="Approved By")
    date = fields.Datetime(string="Approved On")

#EoF
