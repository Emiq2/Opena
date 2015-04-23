# -*- coding utf -8 -*-
from openerp import fields, models

class Partner(models.Model):
	"""docstring for Parner"""
	_inherit = 'res.partner'

	instructor = fields.Boolean("Tildar si es Instructor de Clase", default=False)

	session_ids = fields.Many2many('openacademy.session', 
		string="Attended Sessions", readonly=True)

