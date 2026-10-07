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

	Purchase Approval Levels - rejection
	Asks for the reason of a rejection and sends the order back to draft.
"""
from odoo import fields, models


class PurchaseApprovalReject(models.TransientModel):
    _name = 'purchase.approval.reject'
    _description = "Reject Purchase Order"

    order_id = fields.Many2one('purchase.order', required=True)
    reason = fields.Text(string="Reason", required=True)

    def action_reject(self):
        self.ensure_one()
        self.order_id.action_po_level_reject()  # access check
        self.order_id._po_level_reject(self.reason)
        return {'type': 'ir.actions.act_window_close'}

#EoF
