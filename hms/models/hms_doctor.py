from odoo import models,fields

class HmsDoctor(models.Model):
    _name = "hms.doctor"

    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Image()
    patients = fields.Many2many('hms.patient',
        read_only=True)
