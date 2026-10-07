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

	Purchase Approval Levels - company settings
	Company switch for multi-level purchase approval, the amount compared with
	the thresholds (total or untaxed) and whether all levels up to the amount or
	only the highest one must approve.
"""
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    po_level_approval = fields.Boolean(string="Purchase Approval Levels")
    po_level_approval_amount = fields.Selection(
        [('total', "Total (taxes included)"), ('untaxed', "Untaxed amount")],
        string="Compare Thresholds With", default='total', required=True)
    po_level_approval_mode = fields.Selection(
        [('all', "Every level up to the order amount, one after another"),
         ('highest', "Only the highest level reached")],
        string="Required Levels", default='all', required=True)

#EoF
