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
"""	@version	17.0.1.0.0
	@owner  Hadron for Business
	@author Hadron for Business sp. z o.o.
	@date   2026.10.07

	Purchase Approval Levels - levels
	Approval level: minimum order amount in the company currency and the users
	(or the user group) allowed to approve purchase orders reaching it.
"""
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseApprovalLevel(models.Model):
    _name = 'purchase.approval.level'
    _description = "Purchase Approval Level"
    _order = 'company_id, min_amount, sequence, id'

    name = fields.Char(string="Level", required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company', string="Company", required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    min_amount = fields.Monetary(
        string="Orders From", required=True, default=0.0,
        help="Orders of this amount or more (in the company currency) need the approval of this level.")
    user_ids = fields.Many2many(
        'res.users', string="Approvers", domain="[('share', '=', False)]",
        help="Any of these users can approve the level.")
    group_id = fields.Many2one(
        'res.groups', string="Or Any Member Of",
        help="Any internal user of this group can approve the level too.")

    @api.constrains('user_ids', 'group_id')
    def _check_approvers(self):
        for level in self:
            if not level.user_ids and not level.group_id:
                raise ValidationError(_("Approval level %s needs at least one approver or a group.", level.name))

    @api.constrains('min_amount')
    def _check_min_amount(self):
        for level in self:
            if level.min_amount < 0:
                raise ValidationError(_("The amount of approval level %s cannot be negative.", level.name))

    def _get_approvers(self):
        """Internal, active users allowed to approve this level."""
        self.ensure_one()
        users = self.user_ids | self.group_id.sudo().users
        return users.filtered(lambda u: u.active and not u.share)

    def _can_approve(self, user):
        self.ensure_one()
        return user in self._get_approvers()

#EoF
