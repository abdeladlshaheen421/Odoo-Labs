from odoo import models,fields,api,exceptions

class HmsCustomerInheritance(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient')

    def unlink(self):
        if self.related_patient_id:
            raise exceptions.UserError('can not delete patient realted to partner')
        return super().unlink()


    @api.constrains('related_patient_id')
    def check_email(self):
        if self.related_patient_id.email != self.email and not self.env['hms.patient'].search([('email','=',self.email)]):
            raise exceptions.ValidationError('email exists for a patient')