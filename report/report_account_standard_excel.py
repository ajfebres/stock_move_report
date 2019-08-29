# -*- coding: utf-8 -*-
from datetime import datetime
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx


class AccountigReportSales(ReportXlsx):

	def generate_xlsx_report(self, workbook, data, wizard):
		stock_move = self.env['stock.move']
		sale_order =self.env['sale.order']
		purchase_order = self.env['purchase.order']

		date = datetime.strptime(wizard.start, '%Y-%m-%d')
		end_date = datetime.strptime(wizard.end, '%Y-%m-%d')
		sheet = workbook.add_worksheet('%s' % (date.strftime('%B').upper()))

		bold = workbook.add_format({'bold': True, 'font_size': 10})
		text = workbook.add_format({'font_size': 8})

		sheet.write('A2', 'Rango de Fechas', bold)
		sheet.write('C2', '%s al %s'%(date.strftime('%d %B'), end_date.strftime('%d %B')), text)

		move_ids = stock_move.search([('state', '=', 'done'), ('company_id', '=', wizard.company_id.id)]).filtered(lambda x: datetime.strptime(x.date,'%Y-%m-%d %H:%M:%S') >= date and 
													   										datetime.strptime(x.date,'%Y-%m-%d %H:%M:%S') <= end_date)
		products = {}
		for move in move_ids:
			products.setdefault(move.product_id, [])
			products[move.product_id].append(move)
		
		row = 5
		for product, moves in products.items():
			sheet.write(row, 0, 'Producto', bold)
			sheet.write(row, 1, 'No. Doc', bold)
			sheet.write(row, 2, 'No. Orden', bold)
			sheet.write(row, 3, 'Fecha', bold)
			sheet.write(row, 4, 'Salida', bold)
			sheet.write(row, 5, 'Entrada', bold)
			sheet.write(row, 6, 'Salida Costo', bold)
			sheet.write(row, 7, 'Entrada Costo', bold)
			move_row = row + 1
			total_out = total_in = 0
			for mv in moves:
				date_format = datetime.strptime(mv.date, '%Y-%m-%d %H:%M:%S').strftime('%d-%b')
				sheet.write(move_row, 0, product.name, bold)
				sheet.write(move_row, 2, mv.origin, text)
				sheet.write(move_row, 3, date_format, text)

				sale_id = sale_order.search([('name', '=', mv.origin)], limit=1)
				if sale_id:
					sale_invoices = sale_id.invoice_ids.filtered(lambda i: i.state in ['open', 'paid'])
					line_ids = []
					for inv in sale_invoices:
						for line in inv.move_id.line_ids.filtered(lambda m: '5101001' in m.account_id.name):
							line_ids.append(line)
					debit = sum([l.debit for l in line_ids])
					document = ', '.join([i.number for i in sale_invoices])
					sheet.write(move_row, 1, document, text)
					sheet.write(move_row, 6, debit, text)
				purchase_id = purchase_order.search([('name', '=', mv.origin)], limit=1)
				if purchase_id:
					purchase_invoices = purchase_id.invoice_ids.filtered(lambda i: i.state in ['open', 'paid'])
					lines_ids = []
					for inv in purchase_invoices:
						for line in inv.move_id.line_ids.filtered(lambda m: '1104001' in m.account_id.name):
							lines_ids.append(line)
					debit = sum([l.debit for l in lines_ids])
					document = ', '.join([i.number for i in purchase_invoices])
					sheet.write(move_row, 1, document, text)
					sheet.write(move_row, 7, debit, text)
				if mv.picking_type_id.code == 'outgoing':
					sheet.write(move_row, 4, mv.product_uom_qty, text)
					total_out+=mv.product_uom_qty
				elif mv.picking_type_id.code == 'incoming':
					sheet.write(move_row, 5, mv.product_uom_qty, text)
					total_in+=mv.product_uom_qty
				move_row+=1
			move_row+=1
			row=move_row


AccountigReportSales('report.stock_move_report.accounting_report_sales_excel', 'stock.move.report')