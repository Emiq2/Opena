# -*- coding: utf-8 -*-

from openerp import models, fields, api

class cursos(models.Model):
	_name = 'cursos.course'
	
	name = fields.Char("Titulo", required=True)
	Horas = fields.Integer(long=3, help='Ingrese solo números')
	description = fields.Text("Descripcion")
	temas = fields.Text()
	profesor_id = fields.Many2many('res.users', ondelete="set null", string="Profesor", index=True)
	session_ids = fields.One2many('openacademy.session','course_id', string="Sesiones", required=True)


class Session(models.Model):
	_name= 'openacademy.session'

	name= fields.Char("Nombre", required=True)
	fecha_inicio = fields.Date(default=fields.Date.today)
	duracion = fields.Float(digits=(6, 2), help="Duracion en horas")
	asientos = fields.Integer(string="Numero de asientos")
	active = fields.Boolean(default=True)

	instructor_id = fields.Many2one('res.partner', string="Instructor",domain=['|', ('Instructor', '=', True),
	 ('category_id_name', 'ilike', "teacher")])
	course_id = fields.Many2one('cursos.course', ondelete='cascade', string="Curso")
	alumnos_ids = fields.Many2many('res.partner', string="Asistentes")

	taken_seats = fields.Float(string="Asientos Ocupados", compute='_taken_seats')

	


	@api.one
	@api.depends('asientos', 'alumnos_ids')
	def _taken_seats(self):
		if not self.asientos:
			self.taken_seats = 0.0
		else:
			self.taken_seats = 100.0 * len(self.alumnos_ids) / self.asientos

	@api.onchange('asientos', 'alumnos_ids')
	def _asientos(self):
		if self.asientos < 0:
			return {
				'warging': {
					'title': "Incorrectos 'asientos' value",
					'message': "el numero de asientos no puede ser negativo",
				},
			}
		if self.asientos < len(self.alumnos_ids):
			return {
				'warging': {
					'title': "Demasiados alumnos",
					'message': "incremente los asientos o remueva algunos alumnos",
				},
			}
			#probando ahora desde archivo online



