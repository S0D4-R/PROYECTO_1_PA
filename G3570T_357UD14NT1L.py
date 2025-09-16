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
import msvcrt
from colorama import Fore, init
from unittest import case #Pa que sirve este import tmr
def courseError(exception): pass
def nameDupeError(exception): pass
def fechaFormatError(exception): pass
def horaFormatError(exception): pass
init(autoreset=True)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def menu(opciones, titulo="MENÚ"):
    seleccion = 0
    while True:
        for caracter in f"--- {titulo} ---":
            print(Fore.CYAN + caracter, end='', flush=True)
            time.sleep(0.03)
        print("\n" + Fore.CYAN + "═" * 40)
        time.sleep(0.03)

        for i, opcion in enumerate(opciones):
            if i == seleccion:
                print(Fore.LIGHTMAGENTA_EX + f"→ {opcion}")
            else:
                print(f"  {opcion}")
        print("\nUsa ↑/↓ para mover, ENTER para seleccionar.")

        tecla = msvcrt.getch()
        if tecla == b'\xe0':
            tecla2 = msvcrt.getch()
            if tecla2 == b'H' and seleccion > 0:
                seleccion -= 1
            elif tecla2 == b'P' and seleccion < len(opciones) - 1:
                seleccion += 1
        elif tecla == b'\r':
            time.sleep(1.5)
            return seleccion

        os.system('cls' if os.name == 'nt' else 'clear')

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
        super().__init__(name, dpi, address, phone, dob, password_u)
        self.__id_s = id_student
        self.gen = gen
        self.assigned_c = {}
    @property
    def carnet(self):
        return self.__id_s

    def entregar_tarea(self, curso_seleccionado):
        if not curso_seleccionado.asignaciones:
            print("No hay actividades en este curso...")
            return

        print("---ACTIVIDADES DEL CURSO---")
        for indice, asignacion in enumerate(curso_seleccionado.asignaciones, start=1):
            print(f"{indice}. Tipo: {asignacion.type_a} | Valor: {asignacion.valor_n} | Fecha: {asignacion.date}")

        try:
            seleccion = int(input("Ingrese el número de la actividad a entregar: "))
            if not 1 <= seleccion <= len(curso_seleccionado.asignaciones):
                print("Número de asignación no válido.")
                return

            actividad = curso_seleccionado.asignaciones[seleccion - 1]
            actividad.submissions[self.carnet] = "Entregado"
            print("Actividad entregada con éxito!")
        except ValueError:
            print("Debe ingresar un número válido...")

    def display_info(self):
        return f"{self.name}|Carnet:{self.carnet} | DPI: {self.documento_personal} | tel:{self.phone_u} |Año Ingreso:{self.gen}"

    def inscription(self,course_name,faculty):
        for curse in faculty.courses_db.values():
            if curse.name == course_name:
                if curse.id_course in self.assigned_c:
                    print("Ya te asignaste a este curso...")
                    return
                else:
                    self.assigned_c[curse.id_course] = curse

                    try:
                        curse.roster_alumnos = json.loads(curse.roster_alumnos)
                    except Exception:
                        curse.roster_alumnos = {}
                    try:
                        curse.roster_alumnos = dict(curse.roster_alumnos)
                    except Exception:
                        curse.roster_alumnos = {}

                    curse.roster_alumnos[self.__id_s] = self.name

                    print(f"Inscripción al curso {curse.name} completada con éxito!")

                    with open("estudiantes.txt", "w", encoding="utf-8") as archivo:
                        for id_s, alumno in faculty.students_db.items():
                            assigned_ids = list(alumno.assigned_c.keys())
                            archivo.write(f"{id_s}:{alumno.name}:{alumno.documento_personal}:{alumno.address}:{alumno.phone_u}:{alumno.dob}:{alumno.pass_ward}:{alumno.carnet}:{alumno.gen}:{json.dumps(assigned_ids)}\n")

                    with open("Cursos.txt", "w", encoding="utf-8") as archivo_c:
                        for id_c, curso in faculty.courses_db.items():
                            archivo_c.write(f"{curso.id_course};{curso.name};{curso.teacher_assigned};{json.dumps(curso.roster_alumnos)};{json.dumps(curso.asignaciones)}\n")

                    return

        print("Curso no encontrado...")

    def promedio_general(self):
        punteo_obtenido=0
        posibilidad= 0

        for curso in self.assigned_c.values():
            nota,total= curso.calcular_nota(self.carnet)
            punteo_obtenido += nota
            posibilidad += total

        try:
            promedio= (punteo_obtenido / posibilidad) *100
        except ZeroDivisionError:
            promedio =0
        return promedio

    def ver_notas(self):
        for course in self.assigned_c.values():
            nota, total = course.calcular_nota_final()
            if total == 0:
                print(f"{course.name} | Sin actividades registradas.")
            else:
                print(f"{course.name} | Nota global: {nota}/{total}")

    def ver_nota_actividad(self,curso_seleccionado):
        if not curso_seleccionado.asignaciones:
            print("No hay actividades en este curso...")
            return
        print(f"---NOTAS DE ACTIVIDADES EN {curso_seleccionado.name}---")
        for indice, asignacion in enumerate(curso_seleccionado.asignaciones, start=1):
            try:
                try:
                    estado= asignacion.submissions[self.carnet]
                except KeyError:
                    estado= "No entregado"
            except AttributeError:
                estado= "No entregado"
            print(
                f"{indice}. Tipo: {asignacion.type_a} | Valor: {asignacion.valor_n} | Fecha: {asignacion.date} | Estado: {estado}")

    def deploy_s_menu(self,faculty):
        while True:
            opciones_menu = ["1.Ver cursos","2.Inscripción a cursos.","3.Promedio General.","4.Ver perfil.","5.Trayectoria de cursos.","6.Ver notas de Cursos","7.Cerrar Sesión."]
            seleccion = menu(opciones_menu, "MENÚ ESTUDIANTE")
            option = opciones_menu[seleccion].split(".")[0]

            match option:
                case "1":
                    if not self.assigned_c:
                        print("No estas asignado a ningun curso...")
                        print("Presione ENTER para volver")
                    else:
                        for indice, curso in enumerate(self.assigned_c.values(), start=1):
                            print(f"{indice}. {curso.name}")

                        try:
                            curso_seleccion = int(input("Seleccione el número del curso: "))
                            curso_lista = list(self.assigned_c.values())

                            if 1 <= curso_seleccion <= len(curso_lista):
                                curso_selecionado = curso_lista[curso_seleccion - 1]

                                while True:
                                    sub_opciones = ["1.Entregar Tareas", "2.Ver nota de curso",
                                                    "3.Ver nota de actividad", "4.Volver a menu principal"]
                                    print(f"{"---" * 4}CURSOS{"---" * 4}")
                                    sub_option = menu(sub_opciones, "---CURSOS---")

                                    match sub_option:
                                        case "1":
                                            print("---ENTREGA DE TAREAS---")
                                            self.entregar_tarea(curso_selecionado)
                                        case "2":
                                            print("---NOTA DE CURSO---")
                                            nota, total = curso_selecionado.calcular_nota_final()
                                            if total == 0:
                                                print("Sin actividades registradas.")
                                            else:
                                                print(f"Nota global: {nota}/{total}")

                                        case "3":
                                            print("---NOTA DE ACTIVIDADES---")
                                            self.ver_nota_actividad(curso_selecionado)
                                        case "4":
                                            print("Volviendo a menú principal...")
                                            break
                                        case _:
                                            print("Opcion no valida...")
                            else:
                                print("Número de curso no válido...")

                        except ValueError:
                            print("Se debe ingresar un número válido...")
                case "2":
                    print(f"{"---"*4}INSCRIPCION A CURSOS{"---"*4}")
                    if not faculty.courses_db:
                        print("No hay cursos disponibles...")
                    print("Cursos disponibles")
                    for curso in faculty.courses_db.values():
                        print(f"{curso.name} - Docente: {curso.teacher_assigned}")
                    course_name = input("Ingrese nombre del curso a inscribir: ")
                    self.inscription(course_name, faculty)

                case "3":
                    print("---PROMEDIO GENERAL---")
                    promedio= self.promedio_general()
                    print(f"Su promedio general es de:{promedio}")
                case "4":
                    print("---PERFIL DE USUARIO---")
                case "5":
                    print("----TRAYECTORIA DE CURSOS---")
                case "6":
                    print("---NOTAS DE CURSOS---")
                case "7":
                    print("Saliendo del sistema...")
                    break
                case _:
                    print("Opcion no valida...")

class Teacher(User):
    def __init__(self, name, dpi, address, phone, dob, password_u, id_cat):
        super().__init__(name, dpi, address, phone, dob, password_u)
        self.__id_cat = id_cat
        self.assigned_courses = []
    @property
    def id_cat(self):
        return self.__id_cat
    @id_cat.setter
    def id_cat(self, id_cat):
        pass

    def subir_notas(self, curso):
        rig = ["1. Actualizar las notas de todas las actividades","2. Actualizar notas de una actividad","3. Actualizar curso"]
        opciones = menu(rig, "SUBIR NOTAS")
        option = rig[opciones].split(".")[0]
        match option:
            case "1":
                if not curso.asignaciones:
                    print("Aún no hay actividades")
                    return
                for actividad in curso.asgnaciones:
                    actividad.mostrar_datos()
                    for est in curso.roster_alumnos.values():
                        for act in est.assigned_c[curso.id_course][1]:
                            act[0].set_status()
                            if act[1]:
                                print("El estudiante realizó su entrega")
                            else:
                                print("El estudiante aún no ha entregado nada")
                            while True:
                                try:
                                    punteo = int(input("Ingrese el punteo: "))
                                    if punteo <1 or punteo > act[0].valor_n:
                                        print(f"El punteo debe ser mayor a 0 y menor a {act[0].valor_n}")
                                    else:
                                        act[0].valor_dc = punteo
                                        est.assigned_c[curso.id_course][2] += punteo
                                        break
                                except ValueError:
                                    print("Solo puede ingresar números enteros")
                                except Exception as e:
                                    print("Error inesperado", e)

            case "2":
                if not curso.asignaciones:
                    print("Aún no hay actividades")
                    return
                for actividad in curso.asgnaciones:
                    actividad.mostrar_datos()
                id_act = input("Ingrese la ID de la actividad: ")
                if not any(id_act == actividad.act_id for actividad in curso.asignaciones):
                    print("No se encontro la actividad")
                else:
                    for actividad in curso.asignaciones:
                        if actividad.id == id_act:
                            for est in curso.roster_alumnos.values():
                                for act in est.assigned_c[curso.id_course][1]:
                                    act[0].set_status()
                                    if act[0].id == id_act:
                                        if act[1]:
                                            print("El estudiante realizó su entrega")
                                        else:
                                            print("El estudiante aún no ha entregado nada")

                                        while True:
                                            try:
                                                punteo = int(input("Ingrese el punteo: "))
                                                if punteo < 0 or punteo > act[0].valor_n:
                                                    print(f"El punteo debe ser mayor a 0 y menor a {act[0].valor_n}")
                                                else:
                                                    act[0].valor_dc = punteo
                                                    est.assigned_c[curso.id_course][2] += punteo
                                                    break
                                            except ValueError:
                                                print("Solo puede ingresar números enteros")
                                            except Exception as e:
                                                print("Error inesperado", e)

            case "3":
                if not curso.asignaciones:
                    print("Aún no hay actividades")
                    return
                for id, est in curso.roster_alumnos.values():
                    actividades_upd = est.assigned_c[curso.id_course][1]
                    est_base = engineering_faculty.students_db.get(id, False)
                    if est_base == False:
                        print(f"Estudiante con ID {id} no encontrado en la base de datos")
                    else:
                        est_base.assigned_c[curso.id_course][1] = actividades_upd
                print(f"Estudiantes del curso {curso.name} actualizados")
                engineering_faculty.courses_db[curso.id_course] = curso
                print("Curso actualizado en la base de datos")
            case _:
                print("Opción inválida")

    def crear_asignacion(self, curso):
        if not self.assigned_courses:
            print("Aún no está a cargo de un curso, no puede crear actividades")
        else:
            try:
                curso_search = None
                if not any(curso == course.name for course in self.assigned_courses):
                    raise courseError("El curso asignado no existe")
                for i, curso_option in enumerate(self.assigned_courses):
                    if curso_option.name == curso:
                        curso_search = self.assigned_courses[i]

                act_id = input("Ingrese la ID de la actividad: ")
                act_name = input("Ingrese el nombre de la actividad: ")
                if any(act_name.lower() == act.name.lower() for act in self.assigned_courses.asignaciones):
                    raise nameDupeError("Ya hay una actividad con ese nombre")
                val_net = int(input("Ingrese el valor neto de la asignación:"))
                if val_net<1 or val_net>100:
                    raise ValueError("El valor de la nota debe estar entre 0 y 100")
                nota_total = 0
                for actividad in curso.asignaciones:
                    nota_total += actividad.valor_n
                if (nota_total + val_net) > 100:
                    raise ValueError(f"La ponderación de esta actividad debe ser de {100-nota_total} puntos como máximo para evitar sobrepasar los 100 puntos")

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
                else:
                    raise horaFormatError("Debe ingresar el formato hh:mm")
                tipo = input("Ingrese el tipo de asignación: ")
                assign = Actividad(act_id,act_name,val_net, val_clasif, fecha, hora_open, hora_close, tipo)
                curso_search.asignaciones.append(assign)
                for estudiante in curso_search.roster_alumnos.items():
                    estudiante.assigned_c[curso_search.id_course] = {
                        "nombre" : curso_search.name,
                        "actividades": [],
                        "nota": 0
                    }
                    actividad = [assign,False]
                    estudiante.assigned_c[curso_search.id_course]["actividades"].append(actividad)

            except ValueError:
                print("Ingrese solo números enteros")
            except nameDupeError as e:
                print(e)
            except fechaFormatError as e:
                print(e)
            except horaFormatError as e:
                print(e)
            except courseError as e:
                print(e)
            except Exception as e:
                print("Error inesperado", e)


    def deploy_t_menu(self, faculty):
        while True:
            opciones_menu = ["1.Ver cursos", "2.Cerrar sesión"]
            seleccion = menu(opciones_menu, "MENÚ DOCENTE")
            select_cat = opciones_menu[seleccion].split(".")[0]
            match select_cat:
                case "1":
                    if not self.assigned_courses:
                        print("No hay cursos asignados")
                    else:
                        for clave, data in enumerate(self.assigned_courses):
                            print(f"{clave}.", end = "")
                            data.mostrar_datos()
                        course_select = input("Ingrese la ID del curso: ").upper()
                        if any(course_select == course.id_course for course in self.assigned_courses):
                            for course_find in self.assigned_courses:
                                if course_find.id_course == course_select:
                                    opciones_menu = ["1.Crear Asignación.", "2.Subir Notas"]
                                    seleccion = menu(opciones_menu, "OPCIONES")
                                    subselect = opciones_menu[seleccion].split(".")[0]
                                    match subselect:
                                        case "1":
                                            self.crear_asignacion(course_find)
                                        case "2":
                                            self.subir_notas(course_find)
                                        case _:
                                            print("Opción inválida")
                        else:
                            print("La clave del curso no existe")
                case "2":
                    print("Saliendo...")
                    break
                case _:
                    print("Opción inválida")
    def display_info(self):
        print(f"ID: {self.id_cat}\nNombre: {self.name}\nDPI: {self.dpi}\nNúmero telefónico: {self.phone}\nCursos:")
        if self.assigned_courses:
            for course in self.assigned_courses:
                print(f"\nID: {course.id_course}, Nombre: {course.name}")
        else:
            print("No hay cursos asignados")


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
    def __init__(self,act_id, name, valor_neto, valor_de_calificacion, date, h_apertura, h_cierre, type_a):
        self.__act_id = act_id
        self.name = name
        self.valor_n = valor_neto
        self.valor_dc = valor_de_calificacion
        self.date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        self.h_apertura = datetime.datetime.strptime(h_apertura, "%H:%M").time()
        self.h_cierre = datetime.datetime.strptime(h_cierre, "%H:%M").time()
        self.type_a = type_a
        self.status = False
        self.submission={}

    @property
    def act_id(self):
        return self.__act_id
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
        ops = ["1. Crear Curso","2. Crear Usuario","3. Ver cursos","4. Ver alumnos","5. Ver maestros",
               "6. Asignar Maestros","7. Guardar","8. Salir"]
        seleccion = menu(ops, "MENÚ ADMIN")
        admin_ops = ops[seleccion].split(".")[0]
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
                opciones_menu = ["1.Alumnos.","2.Maestros.","3.Cursos."]
                seleccion = menu(opciones_menu, "GUARDADO DE INFORMACIÓN")
                save_ops = opciones_menu[seleccion].split(":")[0]
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
                        time.sleep(1)


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
            key = engineering_faculty.students_db[user_pass].deploy_s_menu(engineering_faculty)


        elif user_pass in engineering_faculty.teachers_db and password_pass == engineering_faculty.teachers_db[user_pass].pass_ward:
            key = engineering_faculty.teachers_db[user_pass].deploy_t_menu(engineering_faculty)
        elif user_pass == "0" and password_pass == "0":
            key = False
        else:
            print("> Usuario o Contraseña incorrectos, por favor intente de nuevo...")

    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")