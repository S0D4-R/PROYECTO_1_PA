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


    def display_info(self):
        pass

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

    def display_info(self):
        return f"{self.name}|Carnet: "

    def inscription(self):
        pass

    def deploy_s_menu(self):
        pass

class Teacher(User):
    def __init__(self, name, dpi, address, phone, dob, password_u, id_cat):
        super().__init__(name, dpi, address, phone, dob, password_u)
        self.__id_cat = id_cat
        self.assigned_courses = []
    @property
    def codigo_catredatico(self):
        return self.__id_cat

    def subir_notas(self):
        pass
    def display_info(self):
        return f"{self.name}|Carnet: "
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


def id_creation(name_x, typeP):
    ran_code1 = random.randint(1000, 9999)
    ran_code2 = random.randint(0, 9)
    if typeP == "C":
        id_p1 = name_x.strip()

        id_gen = id_p1[0].upper() + id_p1[1].upper() + id_p1[2].upper() + str(ran_code1) + str(ran_code2)
        return id_gen
    elif typeP == "S":
        id_gen = "STU" + str(ran_code1) + str(ran_code2)
        return id_gen
    elif typeP == "T":
        id_gen = "DOC" + str(ran_code1) + str(ran_code2)
        return id_gen
    else:
        return  None

def deploy_admin_menu(faculty):
    admin_key = True
    while admin_key:
        print("\n~"*15, "BIENVENIDO", "~"*15)
        admin_ops = input("\n\n1. Crear Curso\n2. Crear Usuario\n3. Ver cursos\n4. Ver alumnos\n5. Ver maestros\n6. Asignar Maestros\n7. Salir\n")
        match admin_ops:


            #Creación de cursos
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
                if not faculty.teachers_db:
                    print("> No hay maestros disponibles...\n> Curso ha sido creado con éxito...")
                else:
                    for temp_cont, workid, teacher_x in enumerate(faculty.teachers_db.keys(), start=1):
                        print(f"{temp_cont}|{teacher_x.name}|{workid} ~ ID")
                    chose_teach = False
                    while not chose_teach:
                        search_work_id = input("> Coloque el ID del maestro que desea asignar: ")
                        teacher = faculty.teachers_db[search_work_id]


                course_id = id_creation(course_name, "C")
                faculty.courses_db[course_id] = Curso(course_id, course_name, teacher)
                if teacher is not None:
                    teacher.assigned_courses.append(course_id)


            # Creación de usuarios ; dpi, address, phone, dob, password_u
            case "2":

                user_name = input("> Coloque el nombre del Usuario: ")
                user_address = input("> Coloque la dirección del Usuario: ")
                user_phone = input("> Coloque el teléfono del Usuario: ")
                user_dob = input("> Coloque la fecha de nacimiento del Usuario: ")
                user_pass = input("> Coloque la contraseña del Usuario: ")
                user_dpi = input("> Coloque el DPI del Usuario: ")
                user_inscr_year = input("> Coloque el año de inscripción: ")

                type_conf = False
                while not  type_conf:
                    user_type = input("> Seleccione el tipo de usuario:\n1. Estudiante\n2. Docente\n")
                    if user_type == "1":
                        user_type = "S"
                        user_id = id_creation("", user_type)
                        faculty.students_db[user_id] = Student(user_name,user_dpi,user_address,user_phone,user_dob,user_pass,user_id,user_inscr_year)
                    elif user_type == "2":
                        user_type = "T"
                        user_id = id_creation("", user_type)
                        faculty.teachers_db[user_id] = Teacher(user_name, user_dpi, user_address, user_phone, user_dob, user_pass, user_id)


            case "3":
                print("-"*15, "CURSOS DISPONIBLES", "-"*15)
                for index, course in enumerate(faculty.courses_db.values(), start=1):
                    print(f"> {index}. {course.name}|Maestro asignado: {course.teacher_assigned}")


            case "4":
                print("-" * 15, "ALUMNOS REGISTRADOS", "-" * 15)
                for index, student in enumerate(faculty.students_db.values(), start=1):
                    print(student.display_info())

            case "5":
                print("-" * 15, "MAESTROS REGISTRADOS", "-" * 15)
                for index, teacher_x in enumerate(faculty.teachers_db.values(), start=1):
                    print(teacher_x.display_info())

            case "6":
                print("-" * 15, "CURSOS DISPONIBLES", "-" * 15)
                for index, course in enumerate(faculty.courses_db.values(), start=1):
                    print(f"> {index}. {course.name}|Maestro asignado: {course.teacher_assigned}")


            case "7":
                print("> Gracias por usar el programa...")
                admin_key = False
                return False


class Database:
    def __init__(self):
        self.students_db = {}
        self.teachers_db = {}
        self.courses_db = {}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
engineering_faculty = Database()

key = True
while key:
    try:
        user_pass = input("> User: ")
        password_pass = input("> Password: ")
        if user_pass == "ruler" and password_pass == "admin01":
            key = deploy_admin_menu(engineering_faculty)
        elif user_pass in engineering_faculty.students_db and password_pass == engineering_faculty.students_db[user_pass].pass_ward:
            engineering_faculty.students_db[user_pass].deploy_s_menu(engineering_faculty)
        elif user_pass in engineering_faculty.teachers_db and password_pass == engineering_faculty.teachers_db[user_pass].pass_ward:
            engineering_faculty.teachers_db[user_pass].deploy_t_menu(engineering_faculty)
        else:
            print("> Usuario o Contraseña incorrectos, por favor intente de nuevo...")

    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")