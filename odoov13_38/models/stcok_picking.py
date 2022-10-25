from odoo import api, exceptions, fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_download_attachment(self):
        tab_id = []
        for rec in self:
            attachment = self.env['ir.attachment'].search([('res_id', '=', rec.id),('res_model','=','stock.picking')])
            if attachment:
                for recs in attachment:
                    tab_id.append(recs.id)
        url = '/web/binary/download_document?tab_id=%s' % tab_id
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }


class Attachment(models.Model):
    _inherit = 'ir.attachment'


    # @api.model
    # def write(self, vals):
    #     print('**************************************8')
    #     if self.res_model == 'stock.picking':
    #         if self.res_id:
    #             stock_rec = self.env['stock.picking'].search([('id','=',self.res_id)])
    #             name = self.name
    #             name_split = name.split('.')
    #             new_name = stock_rec.name +'.'+name_split[1]
    #             vals['name'] = new_name

    #     return super(Attachment, self).write(vals)


    # @api.model
    # def create(self, vals):
    #     res = super(Attachment, self).create(vals)
    #     if self.res_model == 'stock.picking':
    #         if self.res_id:
    #             stock_rec = self.env['stock.picking'].search([('id','=',self.res_id)])
    #             name = self.name
    #             name_split = name.split('.')
    #             new_name = stock_rec.name +'.'+name_split[1]
    #             vals['name'] = new_name

    #     return res
    #     