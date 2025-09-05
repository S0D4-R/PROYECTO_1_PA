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

    def deploy_s_menu(self):
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

    def deploy_t_menu(self):
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




def deploy_admin_menu():
    admin_key = True
    while admin_key:
        print("~"*15, "BIENVENIDO", "~"*15)
        admin_ops = input("\n\n1. Crear Curso\n2. Crear Usuario\n3. Ver cursos\n4. Ver alumnos\n5. Ver maestros\n6. Salir")
        match admin_ops:
            case "1":
                pass
            case "2":
                pass
            case "3":
                pass
            case "6":
                print("Gracias por usar el programa...")
                admin_key = False
                return False
""" 

class Facultad:
    def __init__(self):
        self.students_db = {}
"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
students_db = {}
teachers_db = {}
courses_db = {}

key = True
while key:
    try:
        user_pass = input("> User:")
        password_pass = input("> Password: ")
        if user_pass == "ruler" and password_pass == "admin01":
            key = deploy_admin_menu()
        elif user_pass in students_db and password_pass == students_db[user_pass].pass_ward:
            students_db[user_pass].deploy_s_menu()
        elif user_pass in teachers_db and password_pass == teachers_db[user_pass].pass_ward:
            teachers_db[user_pass].deploy_t_menu()
        else:
            print("> Usuario o Contraseña incorrectos, por favor intente de nuevo...")

    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")