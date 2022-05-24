from odoo import models, fields

class Log(models.Model):
    _name = "hms.logs"
    
    user = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)
    patient_id = fields.Many2one('hms.patient','Patient')
    date = fields.Datetime('DateTime', default=lambda self: fields.datetime.now())
    details = fields.Text()