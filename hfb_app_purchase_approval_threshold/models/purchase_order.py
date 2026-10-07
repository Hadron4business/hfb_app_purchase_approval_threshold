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

	Purchase Approval Levels - purchase orders
	Replaces the single approval threshold of Odoo with approval levels: the
	order waits in To Approve until every required level (by amount) has
	approved it; approvers get an activity, approve or reject with a reason, and
	each step is recorded on the order.
"""
from odoo import _, api, fields, models
from odoo.exceptions import UserError

ACTIVITY_TYPE = 'hfb_app_purchase_approval_threshold.mail_activity_type_po_approval'


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    po_approval_ids = fields.One2many(
        'purchase.order.approval', 'order_id', string="Approval Steps", copy=False)
    po_level_approval = fields.Boolean(related='company_id.po_level_approval')
    po_approval_next_id = fields.Many2one(
        'purchase.order.approval', string="Next Approval Step", compute='_compute_po_approval_next')
    po_approval_can_approve = fields.Boolean(string="Can Approve", compute='_compute_po_approval_next')

    @api.depends_context('uid')
    @api.depends('po_approval_ids.state', 'state')
    def _compute_po_approval_next(self):
        for order in self:
            step = order.po_approval_ids.filtered(lambda a: a.state == 'pending')[:1]
            order.po_approval_next_id = step
            order.po_approval_can_approve = bool(
                order.state == 'to approve' and step and step.level_id
                and step.level_id._can_approve(self.env.user))

    # ------------------------------------------------------------------
    # Required levels
    # ------------------------------------------------------------------
    def _po_approval_amount(self):
        self.ensure_one()
        amount = self.amount_untaxed if self.company_id.po_level_approval_amount == 'untaxed' else self.amount_total
        return self.currency_id._convert(
            amount, self.company_id.currency_id, self.company_id, self.date_order or fields.Date.today())

    def _po_required_levels(self):
        self.ensure_one()
        amount = self._po_approval_amount()
        levels = self.env['purchase.approval.level'].sudo().search([
            ('company_id', '=', self.company_id.id),
        ]).filtered(lambda l: self.company_id.currency_id.compare_amounts(l.min_amount, amount) <= 0)
        if levels and self.company_id.po_level_approval_mode == 'highest':
            top = max(levels.mapped('min_amount'))
            levels = levels.filtered(lambda l: l.min_amount == top)[-1:]
        return levels

    def _po_missing_levels(self):
        self.ensure_one()
        approved = self.po_approval_ids.filtered(lambda a: a.state == 'approved').level_id
        return self._po_required_levels() - approved

    def _approval_allowed(self):
        self.ensure_one()
        if not self.company_id.po_level_approval:
            return super()._approval_allowed()
        return not self._po_missing_levels()

    def _po_sync_approval_steps(self):
        """Create the steps still to approve and drop pending steps no longer needed."""
        Step = self.env['purchase.order.approval'].sudo()
        for order in self:
            required = order._po_required_levels()
            steps = order.po_approval_ids.sudo()
            steps.filtered(lambda a: a.state == 'pending' and a.level_id not in required).unlink()
            present = order.po_approval_ids.level_id
            Step.create([{
                'order_id': order.id,
                'level_id': level.id,
                'name': level.name,
                'sequence': level.sequence,
                'min_amount': level.min_amount,
            } for level in required if level not in present])

    # ------------------------------------------------------------------
    # Notifications
    # ------------------------------------------------------------------
    def _po_notify_next_approvers(self):
        for order in self:
            order.activity_unlink([ACTIVITY_TYPE])
            step = order.po_approval_ids.filtered(lambda a: a.state == 'pending')[:1]
            if not step or not step.level_id:
                continue
            for user in step.level_id._get_approvers():
                order.activity_schedule(
                    ACTIVITY_TYPE, user_id=user.id,
                    note=_("Level: %(level)s - %(amount)s",
                           level=step.name, amount=order.currency_id.format(order.amount_total)))

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def button_confirm(self):
        result = super().button_confirm()
        waiting = self.filtered(lambda o: o.state == 'to approve' and o.company_id.po_level_approval)
        waiting._po_sync_approval_steps()
        waiting._po_notify_next_approvers()
        for order in waiting:
            order.message_post(body=_("Order submitted for approval: %s.", ", ".join(
                order.po_approval_ids.filtered(lambda a: a.state == 'pending').mapped('name'))))
        return result

    def action_po_level_approve(self):
        """Approve the next step, and every following step the same user may approve."""
        for order in self:
            if order.state != 'to approve' or not order.company_id.po_level_approval:
                raise UserError(_("Order %s is not waiting for approval.", order.name))
            order._po_sync_approval_steps()
            approved = []
            for step in order.po_approval_ids.filtered(lambda a: a.state == 'pending'):
                if not step.level_id or not step.level_id._can_approve(self.env.user):
                    break
                step.sudo().write({'state': 'approved', 'user_id': self.env.user.id, 'date': fields.Datetime.now()})
                approved.append(step.name)
            if not approved:
                raise UserError(_("You are not an approver of the next level of order %s.", order.name))
            order.activity_feedback([ACTIVITY_TYPE], user_id=self.env.uid)
            order.message_post(body=_("Approved: %s.", ", ".join(approved)))
            if order._approval_allowed():
                order.activity_unlink([ACTIVITY_TYPE])
                order.button_approve()
            else:
                order._po_notify_next_approvers()
        return True

    def action_po_level_reject(self):
        self.ensure_one()
        if not (self.po_approval_can_approve or self.env.user.has_group('purchase.group_purchase_manager')):
            raise UserError(_("Only an approver of the next level or a purchase administrator can reject the order."))
        return {
            'name': _("Reject Purchase Order"),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.approval.reject',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id},
        }

    def _po_level_reject(self, reason):
        for order in self:
            order.activity_unlink([ACTIVITY_TYPE])
            order.po_approval_ids.sudo().unlink()
            order.write({'state': 'draft'})
            partners = order.user_id.partner_id if order.user_id else self.env['res.partner']
            order.message_post(
                body=_("Order rejected by %(user)s. Reason: %(reason)s", user=self.env.user.name, reason=reason),
                partner_ids=partners.ids)

    def button_draft(self):
        result = super().button_draft()
        self.activity_unlink([ACTIVITY_TYPE])
        self.po_approval_ids.sudo().unlink()
        return result

    def button_cancel(self):
        result = super().button_cancel()
        self.activity_unlink([ACTIVITY_TYPE])
        return result

#EoF
