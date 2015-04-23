# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

class cursos(models.Model):
	_name = 'cursos.course'
	
	name = fields.Char("Titulo", required=True)
	Horas = fields.Integer(long=3, help='Ingrese solo números')
	description = fields.Text("Descripcion")
	temas = fields.Text()
	profesor_id = fields.Many2one('res.users', ondelete="set null", string="Profesor", index=True)
	session_ids = fields.One2many('openacademy.session','course_id', string="Sesiones", required=True)
	
	_sql_contraints = [
		('name_description_check', 'CHECK(name != description)',
		 "The title of the course should not be the description"),

		('name_unique',
		 'UNIQUE(name)',
		 "The course title must be unique"),
	]

class Session(models.Model):
	_name= 'openacademy.session'

	name= fields.Char("Nombre", required=True)
	fecha_inicio = fields.Date(default=fields.Date.today)
	duracion = fields.Float(digits=(6, 2), help="Duracion en horas")
	seats = fields.Integer(string="Numero de asientos")
	active = fields.Boolean(default=True)

	instructor_id = fields.Many2one('res.partner', string="Instructor",domain=['|', ('instructor', '=', True),
	 ('category_id.name', 'ilike', "teacher")])
	course_id = fields.Many2one('cursos.course', ondelete='cascade', string="Curso")
	alumnos_ids = fields.Many2many('res.partner', string="Asistentes")

	taken_seats = fields.Float(string="Asientos Ocupados", compute='_taken_seats')
	


	@api.one
	@api.depends('seats', 'alumnos_ids')
	def _taken_seats(self):
		if not self.seats:
			self.taken_seats = 0.0
		else:
			self.taken_seats = 100.0 * len(self.alumnos_ids) / self.seats

	#Advertencia si ocurre algo inesperado en el campo seats

	@api.onchange('seats', 'alumnos_ids')
	def _verify_valid_seats(self):
		if self.seats < 0:
			return {
				'warning': {
					'title': "Valor de 'Asientos' incorrecto",
					'message': "El numero de asientos no puede ser negativo",
				},
			}
		if self.seats < len(self.alumnos_ids):
		        return {
		            'warning': {
		                'title': "Demasiados Alumnos",
		                'message': "Incremente los asientos o puede reducir numero de Alumnos",
		            },
		        }
	

	@api.one
	@api.constrains('instructor_id', 'alumnos_ids')
	def _check_instructor_not_in_attendees(self):
		if self.instructor_id and self.instructor_id in self.alumnos_ids:
			raise exceptions.ValidationError("a session's instructor cant ' be an attendee")


