# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime

class StockMoveReport(models.TransientModel):
	_name = 'stock.move.report'

	company_id = fields.Many2one('res.company', string="Company", default= lambda self: self.env.user.company_id)
	start = fields.Date(string='Star Date', required=True, default=date.today())
	end = fields.Date(string='End Date', required=True)

	def print_excel_report(self):
		self.ensure_one()
		return self.env['report'].get_action(self, 'stock_move_report.accounting_report_sales_excel')

