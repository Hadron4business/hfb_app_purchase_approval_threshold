# Purchase Approval Levels

Define approval levels with a minimum amount and approvers. Purchase orders wait in To Approve until every required level has approved them.

## What it does

- **Unlimited levels** - Each level has a name, a minimum order amount and its approvers: chosen users and/or any member of a user group.
- **One after another** - Levels approve in order of amount. Or switch to "only the highest level reached" if one signature is enough.
- **Total or untaxed** - Compare thresholds with the total including taxes (default) or with the untaxed amount. Foreign currencies are converted.
- **Activities for approvers** - The approvers of the next level get an activity. One click on Approve, and the next level is notified.
- **Reject with a reason** - Rejected orders go back to draft and the buyer is notified with the reason.
- **Full history** - The Approvals tab of the order shows every level, who approved it and when. Everything is also logged in the chatter.

## How to use it

1. Go to Purchase > Configuration > Settings and enable Purchase Approval Levels. Choose the amount to compare (total or untaxed) and the required levels (all or only the highest).
2. Open Purchase > Configuration > Approval Levels and create your levels, e.g. Team leader from 0, Director from 5,000, CEO from 50,000, with their approvers.
3. Confirm a purchase order. If it reaches a level, it goes to To Approve and the approvers get an activity. The Approvals tab shows the steps.
4. The approver opens the order and clicks Approve (or Reject with a reason). When the last level approves, the order is confirmed automatically.

## Good to know

- When the feature is on, the native single-amount "Order Approval" setting is replaced (hidden) and the native "Approve Order" button is hidden.
- Orders below the lowest level are confirmed directly. Without any level defined, all orders are confirmed directly.
- A user who is an approver of several consecutive levels approves them with one click.
- Levels are defined per company; thresholds are in the company currency.

## Technical

- Depends only on `purchase`.
- Models: `purchase.approval.level`, `purchase.order.approval` (steps), wizard `purchase.approval.reject`.
- Overrides `purchase.order._approval_allowed()` (used by `button_confirm` / `button_approve`).
- Activity type `Purchase Approval` for the approvers.

## Status

Odoo 17 build. Missing before publication: icon, banner, tests on 18/19/20.
