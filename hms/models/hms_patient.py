from odoo import models,fields,api,exceptions
from dateutil.relativedelta import relativedelta
import re
from odoo import models,fields,api,exceptions
from dateutil.relativedelta import relativedelta
import re

class HmsPatient(models.Model):
    _name = "hms.patient"
    _rec_name = 'first_name'

    first_name = fields.Char(required = True)
    last_name = fields.Char(required = True)
    email = fields.Char(required = True)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB','AB')])
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Char()
    age = fields.Integer(compute="calc_age",store=True)
    department_id = fields.Many2one('hms.department','department')
    department_capacity = fields.Integer(related='department_id.capacity')
    department_open = fields.Boolean(related='department_id.is_opened')
    doctors = fields.Many2many('hms.doctor')
    logs = fields.One2many('hms.logs','patient_id','Logs')
    state = fields.Selection([
        ('u', 'Undetermined'),
        ('g', 'Good'),
        ('f', 'Fair'),
        ('s', 'Serious'),
    ], default='u')


    def next_state(self):
        if self.state == 'u':
            self.state = 'g'
            self.changeState('Good')
        elif self.state == 'g':
            self.state = 'f'
            self.changeState('Fair')

        elif self.state == 'f':
            self.state = 's'
            self.changeState('Serious')

        elif self.state == 's':
            self.state = 'u'
            self.changeState('Undetermined')

    
    def changeState(self,state):
        self.env['hms.logs'].create({
            'details': "Patient State Changed To " + state,
            'patient_id': self.id
        })


    @api.onchange('age')
    def onchange_age(self):
        if self.first_name and self.age < 30:
            self.pcr = True
            return {
                'warning':{'message':'The PCR option has been checked because age > 30.'}
            }


    @api.depends('birth_date')
    def calc_age(self):
        for record in self:
            if record.birth_date and record.birth_date <= fields.Date.today():
                record.age = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.birth_date)).years
            else:
                record.age = 0


    @api.constrains('email')
    def check_email(self):
        if self.email:
            match = re.match('^([A-Z|a-z|0-9](\.|_){0,1})+[A-Z|a-z|0-9]\@([A-Z|a-z|0-9])+((\.){0,1}[A-Z|a-z|0-9]){2}\.[a-z]{2,3}$', self.email)
            if match == None:
                raise exceptions.ValidationError('Not a valid E-mail')

    _sql_constraints = [
        ('Duplicate_Email','UNIQUE(email)','Email already exists'),
    ]