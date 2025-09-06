"""
DEVELOPERS:
~ JACKY
~ PABLO
~ JORGE
"""
import os
import time
import random
from unittest import case

students_db = {}
teachers_db = {}
courses_db = {}
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
        super().__init__(name, dpi, address, phone, dob, password_u)
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
    def subir_notas(self, curso):
        pass
    def crear_asignacion(self, curso):
        pass
    def deploy_t_menu(self):
        while True:
            print("\n\n========== MENÚ DE CATEDRÁTICOS ==========\n1. Ver cursos\n2. Salir")
            select_cat = input("Seleccione una opción")
            match select_cat:
                case "1":
                    if not self.assigned_courses:
                        print("No hay cursos asignados")
                    else:
                        for clave, data in self.assigned_courses.items():
                            print(f"{clave}, {data.id_course}, {data.name}")
                            data.mostrar_datos()
                        course_select = input("Ingrese la ID del curso: ")
                        if course_select in self.assigned_courses.keys():
                            course = self.assigned_courses[course_select]
                            print("\nOpciones\1. Crear asignación\n2. Subir notas")
                            subselect = input("Ingrese la opción que desea elegir: ")
                            match subselect:
                                case "1":
                                    self.crear_asignacion(course)
                                case "2":
                                    self.subir_notas(course)
                                case _:
                                    print("Opción inválida")
                        else:
                            print("La clave del curso no existe")
                case "2":
                    print("Saliendo...")
                    break
                case _:
                    print("Opción inválida")

class Curso:
    def __init__(self, id_course, name, docente):
        self.id_course = id_course
        self.name = name
        self.teacher_assigned = docente
        self.roster_alumnos = {}
        self.asignaciones = []

    def reporte_x(self):
        pass
    def mostrar_datos(self):
        print(f"=========================\nID: {self.id_course}\n Nombre: {self.name}\n Docente: {self.teacher_assigned}\n Alumnos:")
        if self.roster_alumnos:
            for id, alumno in self.roster_alumnos.items():
                pass # Se llama a una función para mostrar los datos de cada alumno
        else:
            print("No hay alumnos asignados")
        print("\nAsignaciones: ")
        if self.asignaciones:
            for asignacion in self.asignaciones:
                asignacion.mostrar_datos()
        else:
            print("No hay asignaciones asignadas")


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
    def mostrar_datos(self):
        print(f"------------------------------\nValor: {self.valor_n}\n fecha: {self.date}\n apertura: {self.h_apertura}\n cierre: {self.h_cierre}\n tipo: {self.type_a}\n status: {self.status}")


def id_creation(name_x):
    ran_code1 = random.randint(0, 50)
    ran_code2 = random.randint(0, 50)
    id_p1 = name_x.strip()

    id_gen = id_p1[0].upper() + id_p1[1].upper() + id_p1[2].upper() + str(ran_code1) + str(ran_code2)
    return id_gen

def deploy_admin_menu():
    admin_key = True
    while admin_key:
        print("~"*15, "BIENVENIDO", "~"*15)
        admin_ops = input("\n\n1. Crear Curso\n2. Crear Usuario\n3. Ver cursos\n4. Ver alumnos\n5. Ver maestros\n6. Salir\n")
        match admin_ops:
            case "1":
                print("-"*15, "COURSE CREATION", "-"*15)
                name_ver = False
                while not name_ver:
                    course_name = input("> Nombre del curso: ")
                    if len(course_name) <= 3:
                        print("> El nombre no es válido")
                    else:
                        name_ver = True
                teacher= None
                if not teachers_db:
                    print("> No hay maestros disponibles...\n> Curso ha sido creado con éxito...")

                else:
                    for temp_cont, workid, teacher_x in enumerate(teachers_db.keys(), start=1):
                        print(f"{temp_cont}|{teacher_x.name}|{workid} ~ ID")
                    chose_teach = False
                    while not chose_teach:
                        pass


                course_id = id_creation(course_name)
                courses_db[course_id] = Curso(course_id, course_name, teacher)

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


key = True
while key:
    try:
        user_pass = input("> User: ")
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