"""
DEVELOPERS:
~ JACKY
~ PABLO
~ JORGE ERNESTO
~ JORGE

"""
import os
import time
import datetime
import random
import json
from unittest import case
def courseError(Exception): pass
def fechaFormatError(Exception): pass
def horaFormatError(Exception): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class User:
    def __init__(self, name, dpi, address, phone, dob, password_u):
        self.name = name
        self.__dpi = dpi
        self.address = address
        self.__phone = phone
        self.dob = dob
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
            print("Este número de telefono no es válido...")
        else:
            self.__phone = new_phone
    @property
    def pass_ward(self):
        return self.__password


    def display_info(self):
        pass

class Student(User):
    def __init__(self, name, dpi, address, phone, dob, password_u, id_student, gen):
        super().__init__(name, dpi, address, phone, dob, password_u) #atributos heredados de user
        self.__id_s = id_student
        self.gen = gen #anio de ingreso del estudiante
        self.assigned_c = {} # diccionario en donde se almacenaran las clases (en las que el estudiante este inscrito)
    @property
    def carnet(self):
        return self.__id_s

    def entregar_tarea(self):
        pass

    def display_info(self):
        return f"{self.name}|Carnet:{self.carnet} | DPI: {self.documento_personal} | tel:{self.phone_u} |Año Ingreso:{self.gen}"

    def inscription(self):
        for curse in courses_db.values():
            if curse.name == course_name:
                if curse.id_course in self.assigned_c:
                    print("Ya te asignaste a este curso...")
                else:
                    self.assigned_c[curse.id_course] = curse
                    curse.roster_alumnos[self.__id_s] = self
                    print(f"Inscripción al curso {curse.name} completada con exito!")
        print("Curso no encontrado...")

    def ver_notas(self):
        for course in self.assigned_c.values():
            nota, total = course.calcular_nota_final()
            if total == 0:
                print(f"{course.name} | Sin actividades registradas.")
            else:
                print(f"{course.name} | Nota global: {nota}/{total}")

    def deploy_s_menu(self):
        while True:
            print("---MENÚ ESTUDIANTE---")
            print(f"1.Ver cursos\n2.Inscripción de cursos.\n3.Promedio General.\n4.Ver Perfil. \n5.Trayectoria de cursos. \n6. Ver notas de cursos. \n7. Salir.")
            option= input("Ingrese una opcion (1-7):")

            match option:
                case "1":
                    if not self.assigned_c:
                        print("No estas asignado a ningun curso...")
                    else:
                        print(f"{"---"*4}MOSTRANDO-CURSOS-ASIGNADOS{"---"*4}")
                        print(f"1.Entregar Tareas\n2.Ver nota de curso\n3.Ver nota de actividad\n4.Volver a menu principal")
                        sub_option= input("Ingrese una opcion (1-4): ")
                        match sub_option:
                            case "1":
                                print("---ENTREGA DE TAREAS---")
                            case "2":
                                print("---NOTA DE CURSO---")
                                self.ver_notas()

                            case "3":
                                print("---NOTA DE ACTIVIDADES---")
                                '''
                                opciones del menu de estudiantes 
                                opcion de la 1 a la 3 el menú
                                Pertenencen a Jackelin
                                esperando merge.....
                                '''


                            case "4":
                                print("Saliendo del sistema....")
                                break
                            case "5":
                                print("esperando implementacion de funcion nueva")

                            case "6":
                                print("esperando implementacion de funcion nueva")

                            case "7":
                                print("Regresando el menú anterior..........")
                            case _:
                                print("Opcion no valida, intente de nuevo.....")
                case "2":
                    print(f"{"---"*4}INSCRIPCION A CURSOS{"---"*4}")
                    if not courses_db:
                        print("No hay cursos disponibles...")
                    print("Cursos disponibles")
                    for course in courses_db.values():
                        print(f"{course.name} - Docente:{course.teacher_assigned.name}")
                    course_name= input("Ingrese nombre de curso a inscribir:")
                    self.inscription(course_name)

                case "3":
                    print("Salieno del sistema...")
                    break
                case _:
                    print("Opcion no valida...")

class Teacher(User):
    def __init__(self, name, dpi, address, phone, dob, password_u, id_cat): # name, dpi, address, phone, dob, password_u, id_cat, assigned_courses
        super().__init__(name, dpi, address, phone, dob, password_u)
        self.__id_cat = id_cat
        self.assigned_courses = []
    @property
    def codigo_catredatico(self):
        return self.__id_cat

    def display_info(self):
        return f"{self.name}|Código de catedrático:{self.__id_cat} | DPI: {self.documento_personal} | tel:{self.phone_u}"

    def subir_notas(self):
        pass
    def crear_asignacion(self, curso=None):
        if not self.assigned_courses.values():
            print("Aún no está a cargo de un curso, no puede crear actividades")
        else:
            try:
                if not curso:
                    curso = input("Ingrese el nombre del curso de la asignación: ")
                if not any(curso == course.name for course in self.assigned_courses.values()):
                    raise courseError("El curso asignado no existe")
                for id, curso_option in self.assigned_courses.items():
                    if curso_option.name == curso:
                        curso_search = self.assigned_courses[id]


                val_net = int(input("Ingrese el valor neto de la asignación:"))
                val_clasif = 0
                fecha = input("Ingrese la fecha límite (formato dd-mm-aaaa): ")
                if "-" in fecha:
                    secciones = fecha.split("-")
                    if len(secciones) != 3:
                        raise fechaFormatError("Debe ingresar el formato dd-mm-aaaa")
                    if any(False == seccion.isdigit() for seccion in secciones):
                        raise fechaFormatError("Solo puede ingresar números (además de los guiones de separación)")
                    if len(secciones[0]) != 2:
                        raise fechaFormatError("El día debe tener 2 valores")
                    if len(secciones[1]) != 2:
                        raise fechaFormatError("El mes debe tener 2 valores")
                    if len(secciones[2]) != 4:
                        raise fechaFormatError("El año debe tener 4 valores")
                    secciones[0] = int(secciones[0])
                    secciones[1] = int(secciones[1])
                    secciones[2] = int(secciones[2])
                else:
                    raise fechaFormatError("Debe ingresar el formato dd-mm-aaaa")

                hora_open = input("Ingrese la hora de apertura de la asignación (formato hh:mm): ")
                if ":" in hora_open:
                    secciones2 = hora_open.split(":")
                    if len(secciones2) != 2:
                        raise horaFormatError("Debe ingresar el formato hh:mm")
                    if any(False == seccion.isdigit() for seccion in secciones2):
                        raise horaFormatError("Solo puede ingresar números (además de los dos puntos)")
                    if len(secciones2[0]) != 2:
                        raise horaFormatError("La hora debe tener 2 valores")
                    if len(secciones2[1]) != 2:
                        raise horaFormatError("Los deben tener 2 valores")
                    secciones2[0] = int(secciones2[0])
                    secciones2[1] = int(secciones2[1])
                hora_close = input("Ingrese la hora de apertura de la asignación (formato hh:mm): ")
                if ":" in hora_close:
                    secciones3 = hora_close.split(":")
                    if len(secciones3) != 2:
                        raise horaFormatError("Debe ingresar el formato hh:mm")
                    if any(False == seccion.isdigit() for seccion in secciones3):
                        raise horaFormatError("Solo puede ingresar números (además de los dos puntos)")
                    if len(secciones3[0]) != 2:
                        raise horaFormatError("La hora debe tener 2 valores")
                    if len(secciones3[1]) != 2:
                        raise horaFormatError("Los deben tener 2 valores")
                    secciones3[0] = int(secciones3[0])
                    secciones3[1] = int(secciones3[1])
                else:
                    raise horaFormatError("Debe ingresar el formato hh:mm")
                tipo = input("Ingrese el tipo de asignación: ")
                assign = Actividad(val_net, val_clasif, fecha, hora_open, hora_close, tipo)
                curso_search.asignaciones.append(assign)


            except ValueError:
                print("Ingrese solo números enteros")
            except fechaFormatError as e:
                print(e)
            except horaFormatError as e:
                print(e)
            except courseError as e:
                print(e)


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
                                    pass#self.crear_asignacion(course)
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

    def calcular_nota(self):
        nota_final=0
        nota=0
        for asignacion in self.asignaciones:
            if asignacion.valor_dc is not None:
                nota_final +=asignacion.valor_dc
            nota += asignacion.valor_dc
        return nota_final, nota


class Actividad:
    def __init__(self, valor_neto, valor_de_calificacion, date, h_apertura, h_cierre, type_a):
        self.valor_n = valor_neto
        self.valor_dc = valor_de_calificacion
        self.date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        self.h_apertura = datetime.datetime.strptime(h_apertura, "%H:%M").time()
        self.h_cierre = datetime.datetime.strptime(h_cierre, "%H:%M").time()
        self.type_a = type_a
        self.status = False

    def set_status(self):
        ahora = datetime.datetime.now()
        ahora_fecha = ahora.date()
        ahora_hora = ahora.time()
        if ahora_fecha > self.date:
            self.status = False
        elif ahora_fecha == self.date:
            if self.h_apertura <= ahora_hora <= self.h_cierre:
                self.status = True
            else:
                self.status = False
        else:
            if ahora_hora > self.h_apertura:
                self.status = True
            else:
                self.status = False


    def auto_cierre(self):
        pass
    def asignar_punteo(self):
        pass
    def assignment_modification(self):
        pass
    def mostrar_datos(self):
        print(f"------------------------------\nValor: {self.valor_n}\n fecha: {self.date}\n apertura: {self.h_apertura}\n cierre: {self.h_cierre}\n tipo: {self.type_a}\n status: {self.status}")


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
        print("\n", "~"*15, "BIENVENIDO", "~"*15)
        admin_ops = input("\n\n1. Crear Curso\n2. Crear Usuario\n3. Ver cursos\n4. Ver alumnos\n5. Ver maestros\n6. Asignar Maestros\n7. Guardar\n8. Salir\n")
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
                teacher= "N/A"
                if not faculty.teachers_db:
                    print("> No hay maestros disponibles...\n> Curso ha sido creado con éxito...")

                else:
                    for temp_cont, teacher_x in enumerate(faculty.teachers_db.values(), start=1):
                        print(f"{temp_cont}|{teacher_x.name}|{teacher_x.codigo_catredatico} ~ ID")
                    chose_teach = False
                    while not chose_teach:
                        search_work_id = input("> Coloque el ID del maestro que desea asignar: ")
                        teacher = faculty.teachers_db[search_work_id]
                        chose_teach = True


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
                    type_conf = True


            case "3":
                print("-"*15, "CURSOS DISPONIBLES", "-"*15)
                for index, course in enumerate(faculty.courses_db.values(), start=1):
                    print(f"> {index}. {course.name}|Maestro asignado: {faculty.teachers_db[course.teacher_assigned].name}")


            case "4":
                print("-" * 15, "ALUMNOS REGISTRADOS", "-" * 15)
                for index, student in enumerate(faculty.students_db.values(), start=1):
                    print(student.display_info())

            case "5":
                print("-" * 15, "MAESTROS REGISTRADOS", "-" * 15)
                for index, teacher_x in enumerate(faculty.teachers_db.values(), start=1):
                    print(teacher_x.display_info())

            case "6":
                if not faculty.teachers_db:
                    print("> No hay maestros disponibles...")
                else:
                    print("-" * 15, "CURSOS DISPONIBLES", "-" * 15)
                    for index, course in enumerate(faculty.courses_db.values(), start=1):
                        if course.teacher_assigned == "N/A":
                            print(f"> {index}. {course.name}|ID: {course.id_course}")

                    calss_conmf = False
                    while not  calss_conmf:
                        class_assignment = input("> Coloque el ID del curso al que quieres asignar un maestro: ")
                        if class_assignment not in faculty.courses_db:
                            print("> Ese ID no es válido...")
                        else:
                            calss_conmf = True

                    print("-"*15, f"{faculty.courses_db[class_assignment].name}", "-"*15)
                    print("> Lista de maestros disponibles: ")
                    for index_x, teacher_y in enumerate(faculty.teachers_db.values(), start=1):
                        print(f"{index_x}. {teacher_y.name}|ID: {teacher_y.codigo_catredatico}")

                    teach_conf = False
                    while not  teach_conf:
                        teacher_assignment = input("> Coloque el ID del maestro al que quiere agregar: ")
                        if teacher_assignment not in faculty.teachers_db:
                            print("> Ese ID no es válido...")
                        else:
                            teach_conf = True
                    faculty.courses_db[class_assignment].teacher_assigned = faculty.teachers_db[teacher_assignment].codigo_catredatico
                    faculty.teachers_db[teacher_assignment].assigned_courses.append(class_assignment)
                    print("Maestro asignado con éxito...\n\n")


            case "7":
                print("-"*15, "GUARDADO DE INFORMACIÓN", "-"*15)
                save_ops = input("> 1. Alumnos...\n> 2. Maestros...\n> 3. Cursos...\n")
                match save_ops:
                    case "1":
                        with open("estudiantes.txt","w",encoding="utf-8") as courses_file:
                            for id_s, alumni in faculty.students_db.items():
                                courses_file.write(f"{id_s}:{alumni.name}:{alumni.documento_personal}:{alumni.address}:{alumni.phone_u}:{alumni.dob}"
                                                   f":{alumni.pass_ward}:{alumni.carnet}:{alumni.gen}:{json.dumps(alumni.assigned_c)}\n"
                                                   )
                                #id_s, name, dpi, address, phone, dob, passward, carnet, gen, dic(clases)
                    case "2":
                        with open("Profesores.txt","w",encoding="utf-8") as teachers_file:
                            for id_t, teacher_temp in faculty.teachers_db.items():
                                # name, dpi, address, phone, dob, password_u, id_cat, assigned_courses
                                teachers_file.write(
                                    f"{id_t}:{teacher_temp.name}:{teacher_temp.documento_personal}:{teacher_temp.address}:{teacher_temp.phone_u}:{teacher_temp.dob}"
                                    f":{teacher_temp.pass_ward}:{teacher_temp.codigo_catredatico}:{json.dumps(teacher_temp.assigned_courses)}\n"
                                )
                    case "3":
                        with open("Cursos.txt","w",encoding="utf-8") as courses_file:
                            for id_cs, course_x in faculty.courses_db.items():
                                #id_course, name, docente, roster_alumnos, asignaciones
                                courses_file.write(f"{course_x.id_course};{course_x.name};{course_x.teacher_assigned};{json.dumps(course_x.roster_alumnos)};{json.dumps(course_x.asignaciones)}")
                    case _:
                        pass



            case "8":
                print("> Gracias por usar el programa...")
                admin_key = False
                return False


class Database:
    def __init__(self):
        self.students_db = {}
        self.teachers_db = {}
        self.courses_db = {}


    def cargar_estudiantes(self):
        try:
            with open("estudiantes.txt","r",encoding="utf-8") as archivo_estudiantes:
                for linea in archivo_estudiantes:
                    linea= linea.strip()
                    if linea:
                        # id_s, name, dpi, address, phone, dob, passward, carnet, gen, dic(clases)
                        id_s, name, dpi, address, phone, dob, password, carnet, gen, assigned_c_file = linea.split(":",9)
                        assigned_cl = json.loads(assigned_c_file)
                        alumno= Student(name,dpi,address,phone,dob,password,carnet, gen)
                        alumno.assigned_c = assigned_cl
                        self.students_db[id_s] = alumno
                print("Estudiantes importados desde el archivo estudiantes.txt")
        except FileNotFoundError:
            print("No existe estudiantes.txt, se creara al guardar...")

    def cargar_profesores(self):
        try:
            with open("Profesores.txt","r",encoding="utf-8" ) as archivo_profesores:
                for linea in archivo_profesores:
                    linea = linea.strip()
                    if linea:
                        # id_t, name, dpi, address, phone, dob, password_u, id_cat, assigned_courses
                        id_t, name, dpi, address, phone, dob, password, id_cat, assigned_courses = linea.split(":",8)
                        maestro = Teacher(name, dpi, address, phone, dob, password, id_t)
                        maestro.assigned_courses = json.loads(assigned_courses)
                        self.teachers_db[id_t]=maestro
                print("Maestros inportados desde el archivo profesores.txt")
        except FileNotFoundError:
            print("No existe profesores.txt, se creara al guardar")

    def cargar_cursos(self):
        try:
            with open("Cursos.txt","r",encoding="utf-8") as archivo_cursos:
                for linea in archivo_cursos:
                    linea = linea.strip()
                    if linea:
                        #id_course, name, docente, roster_alumnos, asignaciones
                        id_c, name, teacher_id, roster_alumnos, asignaciones = linea.split(";")
                        #teacher = self.teachers_db.get(teacher_id)
                        curso = Curso(id_c, name, teacher_id)
                        curso.roster_alumnos = roster_alumnos
                        curso.asignaciones = asignaciones
                        self.courses_db[id_c] = curso
                print("Cursos importados...")
        except FileNotFoundError:
            print("No existe Cursos.txt, se creara al guardar...")


#OlA
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
engineering_faculty = Database()
engineering_faculty.cargar_cursos()
engineering_faculty.cargar_profesores()
engineering_faculty.cargar_estudiantes()

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
        elif user_pass == "0" and password_pass == "0":
            key = False
        else:
            print("> Usuario o Contraseña incorrectos, por favor intente de nuevo...")

    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")