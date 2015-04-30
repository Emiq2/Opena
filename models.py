# -*- coding: utf-8 -*-
from datetime import timedelta
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
		('name_unique', 'UNIQUE(name)', "The course title must be unique"),
	]

class Session(models.Model):	
	_name= 'openacademy.session'

	name= fields.Char("Nombre", required=True)
	start_date = fields.Date("Fecha de inicio", default=fields.Date.today)
	duration = fields.Float(digits=(1, 2), help="Duracion en horas")
	seats = fields.Integer(string="Numero de asientos")
	active = fields.Boolean(default=True)
	color = fields.Integer()

	instructor_id = fields.Many2one('res.partner', string="Instructor",domain=['|', ('instructor', '=', True),
	 ('category_id.name', 'ilike', "teacher")])
	course_id = fields.Many2one('cursos.course', ondelete='cascade', string="Curso")
	alumnos_ids = fields.Many2many('res.partner', string="Asistentes")

	taken_seats = fields.Float(string="Asientos Ocupados", compute='_taken_seats')
	end_date = fields.Date(string="End Date", store=True, compute='_get_end_date', inverse='_set_end_date')

	@api.one
	@api.depends('seats', 'alumnos_ids')
	def _taken_seats(self):
		if not self.seats:
			self.taken_seats = 0.0
		else:
			self.taken_seats = 100.0 * len(self.alumnos_ids) / self.seats

	#Advertencia si ocurre algo inesperado en el campo seats

	@api.onchange('seats', 'alumnos_ids')
	def _verify_valid_instructor(self):
		if self.instructor_id and self.instructor_id in self.alumnos_ids:
			raise exceptions.ValidationError("El Intructor de la sesion no puede ser un alumno")
		if self.seats < 0 or self.seats < len(self.alumnos_ids):
			return {
				'warning': {
					'title': "Valor de 'Asientos' incorrecto",
					'message': "El número de asientos es menor al número de Alumnos",
				},
			}

	#functions to calculate the functioning

	@api.one
	@api.depends('start_date', 'duration')
	def _get_end_date(self):
		if not (self.start_date and self.duration):
			self.end_date = self.start_date
			return

		#add duration to start_dtate, but: monday + 5 days = Saturday, so
		#subtract one second to get on Friday instead
		start = fields.Datetime.from_string(self.start_date)
		duration = timedelta(days=self.duration, seconds=-1)
		self.end_date = start + duration

	@api.one
	def _set_end_date(self):
		if not (self.start_date and self.end_date):
			return

		start_date = fields.Datetime.from_string(self.start_date)
		end_date = fecha.Datetime.from_string(self.end_date)
		self.duration = (end_date - start_date).days + 1
		

	@api.one
	@api.constrains('seats', 'alumnos_ids')
	def _check_instructor_not_in_attendees(self):
		if self.instructor_id and self.instructor_id in self.alumnos_ids:
			raise exceptions.ValidationError("El Intructor de la sesion no puede ser un alumno")
		
		if self.seats < 0 or self.seats < len(self.alumnos_ids):
				raise exceptions.ValidationError("El número de asientos es menor al número de Alumnos")



