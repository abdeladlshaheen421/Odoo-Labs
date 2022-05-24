from odoo import models,fields

class HmsDepartment(models.Model):
    _name = "hms.department"

    name = fields.Char()
    capacity = fields.Integer(default=0)
    is_opened = fields.Boolean()
    patients = fields.One2many('hms.patient',
        'department_id',
        'Patients')