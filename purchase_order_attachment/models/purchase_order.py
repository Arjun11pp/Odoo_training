# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _description = "Inherits Purchase Order"

    def button_confirm(self):
        """ super the button_confirm function from purchase order and check with attachments """
        for attachment in self:
            icp_sudo = self.env['ir.config_parameter'].sudo()
            require_attachment = icp_sudo.get_param('res.config.settings.require_attachment')
            if require_attachment:
                if attachment.message_attachment_count != 0 :
                    attachment_type=len(self.env['ir.attachment'].search([('res_model','=','purchase.order'),('res_id','=',attachment.id),('mimetype','in',['image/png', 'application/pdf'])]).ids)
                    if attachment_type != 0 :
                        return super(PurchaseOrder,self).button_confirm()
                    else:
                        raise ValidationError('Minimum one attachment of type PDF/image is required.')
                else:
                    raise ValidationError('Minimum one attachment of type PDF/image is required.')
            else:
                return super(PurchaseOrder, self).button_confirm()