from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from datetime import datetime

class Volunteer(models.Model):
    _name = 'collection.volunteer'
    _description = 'Volunteer information'

    @api.constrains('lastName')
    def check_lastname(self):
        for rec in self:
            if not str(rec.lastName).isalpha():
                raise ValidationError(_('Last name contains non-alphabetical characters'))

    @api.model
    def create(self, vals):
        user_vals = {
            'name': vals.get('firstName')+" "+vals.get('lastName'),
            'login': vals.get('email'),
            'password': 'password', # atm for testing default password
        }
        user_id = self.env['res.users'].create(user_vals)
        vals["user_id"] = user_id
        return super(Volunteer, self).create(vals)

    firstName = fields.Char(string="First Name", required=True)
    lastName = fields.Char(string="Last Name")
    birth = fields.Integer(string="Birth Year")
    email = fields.Char(string="E-mail")
    mobileNumber = fields.Char(string="Mobile number")
    address = fields.Text(string="Address")
    photo = fields.Image(string="Image")
    memo = fields.Text(string="Memo")
    registration = fields.Date(readonly=True,default=datetime.today())
    user_id = fields.Integer(string="User_ID")


class Logs(models.Model):
    _name = 'collection.logs'
    _description = 'Volunteer rubbish collection logs'

    volunteer_id = fields.Many2one('res.users', readonly=True, index=True, required=True, default=lambda self: self.env.user)
    date = fields.Date(default=datetime.today())
    type = fields.Selection([('glass','Glass'),
                             ('paper','Paper'),
                             ('plastic','Plastic')],
                            string="Type of rubbish")

    weight = fields.Float(required=True, default=0, digits = (12,3))
    volume = fields.Float(required=True, default=0, digits = (12,3))
    density = fields.Float(compute='_calc_density', default=0, readonly=True, digits = (12,3))

    @api.depends('weight', 'volume')
    def _calc_density(self):
        for logs in self:
            if logs.volume > 0:
                logs.density = logs.weight / logs.volume
            else:
                logs.density = 0