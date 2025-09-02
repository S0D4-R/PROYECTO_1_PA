"""
DEVELOPERS:
~ JACKY
~ PABLO
~ JORGE
"""
import os
import time
import random
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class User:
    def __init__(self, name, dpi, address, phone, dob, password_u):
        self.name = name
        self.__dpi = dpi
        self.address = address
        self.__phone = phone
        self.dob__ = dob
        self.__password = password_u
    @property
    def documento_personal(self):
        return self.__dpi
    @property
    def phone_u(self):
        return self.__phone
    @phone_u.setter
    def phone_u(self, new_phone):
        if len(new_phone) > 8 or len(new_phone) < 8:
            print("Ese número no es válido...")
        else:
            self.__phone = new_phone
    @property
    def pass_ward(self):
        return self.__password


class Student(User):
    def __init__(self, name, dpi, address, phone, dob, password_u, id_student, gen):
        super.__init__(name, dpi, address, phone, dob, password_u)
        self.__id_s = id_student
        self.gen = gen
        self.assigned_c = {}
    @property
    def carnet(self):
        return self.__id_s

    def entregar_tarea(self):
        pass
    def inscription(self):
        pass


class Teacher(User):
    def __init__(self, name, dpi, address, phone, dob, password_u, id_cat):
        super().__init__(name, dpi, address, phone, dob, password_u)
        self.__id_cat = id_cat
        self.assigned_courses = {}
    @property
    def codigo_catredatico(self):
        return self.__id_cat

    def subir_notas(self):
        pass
    def crear_asignacion(self):
        pass


class Curso:
    def __init__(self, id_course, name, docente):
        self.id_course = id_course
        self.name = name
        self.teacher_assigned = docente
        self.roster_alumnos = {}
        self.asignaciones = []

    def reporte_x(self):
        pass


class Actividad:
    def __init__(self, valor_neto, valor_de_calificacion, date, h_apertura, h_cierre, type_a, status):
        self.valor_n = valor_neto
        self.valor_dc = valor_de_calificacion
        self.date = date
        self.h_apertura = h_apertura
        self.h_cierre = h_cierre
        self.type_a = type_a
        self.status = status

    def auto_cierre(self):
        pass
    def asignar_punteo(self):
        pass
    def assignment_modification(self):
        pass
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~