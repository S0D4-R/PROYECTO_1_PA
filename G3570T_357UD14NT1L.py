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
class courseError(Exception): pass
class nameDupeError(Exception): pass
class fechaFormatError(Exception): pass
class horaFormatError(Exception): pass
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
        self.gen = gen
        self.assigned_c = {}
        self.reports = []
        self.gen = gen #anio de ingreso del estudiante
        self.assigned_c = {} # diccionario en donde se almacenaran las clases (en las que el estudiante este inscrito)
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
            actividad.submission[self.carnet] = "Entregado"
            print("Actividad entregada con éxito!")
        except ValueError:
            print("Debe ingresar un número válido...")

    def display_info(self):
        return f"{self.name}|Carnet:{self.carnet} | DPI: {self.documento_personal} | tel:{self.phone_u} |Año Ingreso:{self.gen}"

    def inscription(self,faculty):
        if not faculty.courses_db:
            print("No hay cursos disponibles...")
            return

        cursos_lista = list(faculty.courses_db.values())
        print("--- CURSOS DISPONIBLES ---")
        for i, curso in enumerate(cursos_lista, start=1):
            docente = faculty.teachers_db.get(curso.teacher_assigned, "N/A")
            if docente != "N/A":
                docente = docente.name
            print(f"{i}. {curso.name} - Docente: {docente}")
        while True:
            try:
                opcion = int(input("Ingrese el número del curso al que desea inscribirse: ").strip())
                if 1 <= opcion <= len(cursos_lista):
                    curse = cursos_lista[opcion - 1]
                    break
                else:
                    print("Número de curso inválido. Intente nuevamente.")
            except ValueError:
                print("Debe ingresar un número válido. Intente nuevamente.")

        if curse.id_course in self.assigned_c:
            print("Ya te asignaste a este curso...")
            return
        self.assigned_c[curse.id_course] = curse

        if not curse.roster_alumnos:
            curse.roster_alumnos = {}
        curse.roster_alumnos[self.carnet] = self.name

        with open("estudiantes.txt", "w", encoding="utf-8") as archivo:
            for id_s, alumno in faculty.students_db.items():
                assigned_c_data = {}
                for cid, course_obj in alumno.assigned_c.items():
                    assigned_c_data[cid] = course_obj.name
                archivo.write(f"{id_s}||{alumno.name}||{alumno.documento_personal}||{alumno.address}||{alumno.phone_u}||{alumno.dob}||{alumno.pass_ward}||{alumno.carnet}||{alumno.gen}||{json.dumps(assigned_c_data)}\n")
        with open("Cursos.txt", "w", encoding="utf-8") as archivo_c:
            for id_c, curso in faculty.courses_db.items():
                archivo_c.write(
                    f"{curso.id_course}||{curso.name}||{curso.teacher_assigned}||{json.dumps(curso.roster_alumnos)}||{json.dumps([a.to_dict() for a in curso.asignaciones])}\n")
        print(f"Inscripción al curso '{curse.name}' realizada correctamente.")

    def promedio_general(self):
        punteo_obtenido=0
        posibilidad= 0

        try:
            self.assigned_c == dict(self.assigned_c)
        except Exception:
            self.assigned_c ={}

        for curso in self.assigned_c.values():
            nota, total = curso.calcular_nota(self.carnet)
            punteo_obtenido += nota
            posibilidad += total

        try:
            promedio= (punteo_obtenido / posibilidad) *100
        except ZeroDivisionError:
            promedio =0
        return promedio

    def ver_nota(self,curso_id,faculty):
        curso = faculty.courses_db.get(curso_id)
        if not curso:
            print("Curso no encontrado...")
            return

        if not curso.asignaciones:
            print("No hay actividades registradas en este curso...")
            return

        print(f"\nCurso: {curso.name}\n-----------")
        nota_final = 0
        nota_total = 0

        for indice, actividad in enumerate(curso.asignaciones, start=1):
            valor_obtenido = actividad.submission.get(self.carnet, 0)
            if valor_obtenido != 0:
                print(f"{indice}. {actividad.name} - Valor: {actividad.valor_n} - Nota obtenida: {valor_obtenido}")
                nota_final += valor_obtenido
            else:
                print(f"{indice}. {actividad.name} - Valor: {actividad.valor_n} - Nota: Pendiente")
            nota_total += actividad.valor_n

        if nota_total == 0:
            print("No se han registrado calificaciones todavía.")
        else:
            porcentaje = (nota_final / nota_total) * 100
            print(f"Nota obtenida: {nota_final}/{nota_total} ({porcentaje}%)")

    def ver_nota_actividad(self,curso_seleccionado):
        if not curso_seleccionado.asignaciones:
            print("No hay actividades en este curso...")
            return

        print(f"---NOTAS DE ACTIVIDADES EN {curso_seleccionado.name}---")
        for indice, asignacion in enumerate(curso_seleccionado.asignaciones, start=1):
            if self.carnet in asignacion.submission:
                estado = "Entregado"
            else:
                estado = "No entregado"

            punteo_obtenido = asignacion.submission.get(self.carnet, "N/A")
            print(f"{indice}. Tipo: {asignacion.type_a} | Valor: {asignacion.valor_n} | Nota: {punteo_obtenido} | Estado: {estado}")

    def deploy_s_menu(self,faculty):
        while True:
            opciones_menu = ["1.Ver cursos","2.Inscripción a cursos.","3.Ver perfil.","4.Trayectoria de cursos.","5.Ver notas de Cursos","6.Crear reporte","7.Cerrar Sesión."]
            seleccion = menu(opciones_menu, "MENÚ ESTUDIANTE")
            option = opciones_menu[seleccion].split(".")[0]

            match option:
                case "1":
                    if not self.assigned_c:
                        print("No estás asignado a ningún curso...")
                    else:
                        print("--- CURSOS ASIGNADOS ---")
                        curso_lista_ids = list(self.assigned_c.keys())
                        for indice, curso_id in enumerate(curso_lista_ids, start=1):
                            curso = faculty.courses_db.get(curso_id)
                            if curso:
                                print(f"{indice}. {curso.name}")
                        try:
                            curso_seleccion = int(input("Seleccione el número del curso: "))
                            if 1 <= curso_seleccion <= len(curso_lista_ids):
                                curso_id_seleccionado = curso_lista_ids[curso_seleccion - 1]
                                curso_selecionado = faculty.courses_db.get(curso_id_seleccionado)

                                while True:
                                    sub_opciones = ["1.Entregar Tareas", "2.Ver nota de curso",
                                                    "3.Ver nota de actividad", "4.Volver a menu principal"]
                                    print("---" * 4 + "CURSOS" + "---" * 4)
                                    sub_options = menu(sub_opciones, "---CURSOS---")
                                    sub_option = sub_opciones[sub_options].split(".")[0]

                                    match sub_option:
                                        case "1":
                                            print("---ENTREGA DE TAREAS---")
                                            self.entregar_tarea(curso_selecionado)
                                        case "2":
                                            print("---NOTA DE CURSO---")
                                            self.ver_nota(curso_selecionado.id_course, faculty)

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
                    print("---" * 4 + "INSCRIPCIÓN A CURSOS" + "---" * 4)
                    print("--- CURSOS DISPONIBLES ---")
                    self.inscription( faculty)

                case "3": # pablo
                    print("---" * 4 + "VER PERFIL" + "---" * 4)
                    print(f"---" * 3 + "DATOS PERSONALES DEL ESTUDIANTE" + "---" * 3)
                    print(f"Nombre:{self.name}")
                    print(f"DPI/CUI: {self.documento_personal}")
                    print(f"Dirección: {self.address}")
                    print(f"Número de Teléfono:{self.phone_u} ")
                    print(f"Fecha de Nacimiento: {self.dob}") #atributo dob: fehca de nacimineto del usuario
                    print(f"Carnet:{self.carnet}")
                    print(f"Año de ingreso al establecimiento: {self.gen}")# atributo gen ´año de ingreso del usuario al sistema o estblecimiento´

                    print(f"\n{"--"*2}CURSOS EN LOS QUE ESTOY INSCRITO{"--"*2}")
                    approved_courses = [] #lista de cursos ganados
                    failed_courses =[] #lista de cursos reprobados
                    if self.assigned_c:
                        for course_id, curso in self.assigned_c.items():
                            print(f"Curso: {curso.name}")
                            print(f"Asignaciones")

                            #mostrar las actividades y sus notas (ya calificados por el maestro)
                            if curso.asignaciones:
                                for actividad in curso.asignaciones:
                                    print(f""
                                          f" - Tarea: {actividad.type_a}, Nota: {actividad.valor_dc} / {actividad.valor_n}"
                                          )
                            else:
                                print(f"---SIN ACTIVIDADES REGISTRADAS---")

                            # Calculando y clasificando el promedio del curso
                            nota_promedio, _= curso.calcular_nota(self.carnet)
                            if nota_promedio >=65:
                                approved_courses.append(curso.name)
                            else:
                                failed_courses.append(curso.name)
                            print("-"*20)
                        else:
                            print(----"NO ESTAS REGISTRADO A NINGUN CURSO, CONSULTA ESTO CON TU ENCARGADO-------")

                            print("\n"+"---" * 5 + "RESUMEN DE MIS NOTAS" + "---" * 5)
                            print(f"Cursos Ganados (mayores a un 65% de la nota)")
                            if approved_courses:
                                for curso in approved_courses:
                                    print(f" - {curso}")
                            else:
                                print("Aún no has ganado ningun curso...........")

                            print(f"Cursos Perdidos(menores a un 65% de la nota)")
                            if failed_courses:
                                for failed in failed_courses:
                                    print(f" - {curso}")
                            else:
                                print(f"No tienes cursos perdidos, ¡Muchas felicidades sigue así!")
                            input("\nPresiona Enter para volver al menú principal...")

                case "4": #pablo
                    print("---" * 4 + "TRAYECTORIA ACADÉMICA" + "---" * 4)
                    print( "Mostrando Historial de todos los cursos: ")
                    approved_courses = []
                    failed_courses = []

                    if self.assigned_c:
                        for curso in self.assigned_c.values():
                            nota_promedio, _ = curso.calcular_nota()
                            if nota_promedio >= 65:
                                approved_courses.append(curso.name)
                            else:
                                failed_courses.append(curso.name)
                    print("\n---MOSTRANDO CURSOS APROBADOS---")
                    if approved_courses:
                        for curso_nombre in approved_courses:
                            print(f" - {curso_nombre}")
                    else:
                        print(f"NO HAS APROBADO NINGUN CURSO, MEJORA TU RENDIMIENTO.")

                    print(f"\n---MOSTRANDO CURSOS REPROBADOS---")
                    if failed_courses:
                        for curso_nombre in failed_courses:
                            print(f" - {curso_nombre}")
                    else:
                        print(f" NO HAS REPROBADO CURSOS, EXCELENTE RENDIMIENTO.")

                    input(f"\nPresiona Enter para volver al menú principal...")

                case "5": # pablo
                    print("---" * 4 + "VER NOTAS DE TODOS LOS CURSOS" + "---" * 4)
                    if not self.assigned_c:
                        print("NO ESTAS INSCRITO EN NINGUN CURSO......")
                    else:
                        for curso_nombre, curso in self.assigned_c.items():
                            nota_promedio, _ = curso.calcular_nota()
                            mensaje =""
                            if nota_promedio < 30:
                                mensaje = "DEBES MEJORAR TU NOTA...."
                            elif nota_promedio >= 50:
                                mensaje = "FELICIDADES, DEBES MANTENER ESTA BUENA NOTA"

                            print(f"Curso: {curso.name} | Nota Promedio: {nota_promedio} | Estado: {mensaje}")

                    input("\nPresione enter Enter para volver al menú inicial...")

                case "6": #mostrando en pantalla los reportes del estudiante que el profesor creo0
                    print("---" * 4 + "MOSTRANDO MIS REPORTES" + "---" * 4)
                    for i, reporte in enumerate(self.reports, 1):
                        print("\n"+"---" * 4 + "ENUMERACIÓN" + "---" * 4)
                        print("\n"+"---" * 4 + f"REPORTE {i}" + "---" * 4)
                        print(f" Curso: {reporte['curso']} | Profesor: {reporte['profesor']} | Fecha : {reporte['fecha']} | Descripción : {reporte['descripcion']} ")
                        print("-"*10)
                        input("\nPresione enter Enter para volver al menú inicial...")

                case "7": #pablo
                    print(f"SALIENDO DEL MENÚ DE ESTUDIANTE - VOLVIENDO AL LOGIN INICIAL...........")
                    break
                case _:
                    print("Opcion no válida, por favor intentelo de nuevo...........")

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

    def subir_notas(self, curso, faculty):
        rig = ["1. Actualizar las notas de todas las actividades","2. Actualizar notas de una actividad"]
        opciones = menu(rig, "SUBIR NOTAS")
        option = rig[opciones].split(".")[0]
        match option:
            case "1":
                if not curso.asignaciones:
                    print("Aún no hay actividades")
                    return
                for actividad in curso.asignaciones:
                    actividad.mostrar_datos()
                    for id_est in curso.roster_alumnos:
                        bool_entregado = id_est in actividad.submission and actividad.submission[id_est] == "Entregado"
                        if bool_entregado:
                            print("El estudiante realizó su entrega")
                        else:
                            print("El estudiante aún no ha entregado nada")

                        while True:
                            try:
                                punteo = int(input("Ingrese el punteo: "))
                                if punteo < 1 or punteo > actividad.valor_n:
                                    print(f"El punteo debe ser mayor a 0 y menor a {actividad.valor_n}")
                                else:
                                    actividad.submission[id_est] = punteo
                                    if not bool_entregado:
                                        actividad.submission[id_est] = "Entregado"
                                    print("Nota actualizada con éxito.")
                                    break
                            except ValueError:
                                print("Solo puede ingresar números enteros")
                            except Exception as e:
                                print("Error inesperado", e)


            case "2":
                if not curso.asignaciones:
                    print("Aún no hay actividades")
                    return
                for actividad in curso.asignaciones:
                    actividad.mostrar_datos()
                id_act = input("Ingrese la ID de la actividad: ")
                if not any(id_act == actividad.act_id for actividad in curso.asignaciones):
                    print("No se encontro la actividad")
                else:
                    for actividad in curso.asignaciones:
                        if actividad.act_id == id_act:
                            if not curso.roster_alumnos:
                                print("No hay estudiantes en este curso")
                            for id_est in curso.roster_alumnos:
                                bool_entregado = id_est in actividad.submission and actividad.submission[id_est] == "Entregado"
                                if bool_entregado:
                                    print("El estudiante realizó su entrega")
                                else:
                                    print("El estudiante aún no ha entregado nada")
                                while True:
                                    try:
                                        punteo = int(input("Ingrese el punteo: "))
                                        if punteo < 1 or punteo > actividad.valor_n:
                                            print(f"El punteo debe ser mayor a 0 y menor a {actividad.valor_n}")
                                        else:
                                            actividad.submission[id_est] = punteo
                                            if not bool_entregado:
                                                actividad.submission[id_est] = "Entregado"
                                            print("Nota actualizada con éxito.")
                                            break
                                    except ValueError:
                                        print("Solo puede ingresar números enteros")
                                    except Exception as e:
                                        print("Error inesperado", e)
            case _:
                print("Opción inválida")

    def crear_asignacion(self, curso):
        if not self.assigned_courses:
            print("Aún no está a cargo de un curso, no puede crear actividades")
        else:
            try:
                cursos = [engineering_faculty.courses_db[course_id] for course_id in self.assigned_courses if course_id in engineering_faculty.courses_db]
                curso_search = None
                for curso_obj in cursos:
                    if curso_obj.name == curso.name:
                        curso_search = curso_obj
                if not curso_search:
                    raise courseError("No se encontro el curso")

                act_id = id_creation(curso.name,"A")
                act_name = input("Ingrese el nombre de la actividad: ")
                if any(act_name.lower() == act.name.lower() for act in curso_search.asignaciones):
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
                curso.asignaciones.append(assign)

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

    def crear_reporte(self, curso):
        print("\n" + "-" * 10 + " CREAR REPORTE " + "-" * 10)
        try:
            while True:
                for id_est in curso.roster_alumnos:
                    engineering_faculty.students_db[id_est].display_info()
                id_search = input("Ingrese la ID del estudiante: ")
                if id_search not in curso.roster_alumnos:
                    print("El estudiante no está en el curso")
                else:
                    break
            for id_est, est in engineering_faculty.students_db.items():
                if id_est == id_search:
                    while True:
                        desc = input("\nIngrese la descripción del reporte: ")
                        if len(desc) < 10:
                            print("El reporte es muy corto")
                        else:
                            break

                    report = {
                        "curso": curso.name,
                        "profesor": self.name,
                        "fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "descripcion": desc
                    }
                    est.reports.append(report)
        except ValueError as e:
            print(e)
        except Exception as e:
            print("Error inesperado: ", e)

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
                        for clave, data in enumerate(self.assigned_courses, start=1):
                            print(f"{clave}.", end="")
                            faculty.courses_db[data].mostrar_datos()
                        course_select = input("Ingrese la ID del curso: ").upper()
                        if any(course_select == course.id_course for course in faculty.courses_db.values()):
                            for course_find in faculty.courses_db.values():
                                if course_find.id_course == course_select:
                                    opciones_menu = ["1. Crear Asignación.", "2. Subir Notas", "3. Generar reporte"]
                                    seleccion = menu(opciones_menu, "OPCIONES")
                                    subselect = opciones_menu[seleccion].split(".")[0]
                                    match subselect:
                                        case "1":
                                            self.crear_asignacion(course_find)
                                        case "2":
                                            self.subir_notas(course_find, engineering_faculty)
                                        case "3":
                                            self.crear_reporte(course_find)
                                        case _:
                                            print("Opción inválida")
                        else:
                            print("La clave del curso no existe")
                case "2":
                    print("Saliendo...")
                    break
                case _:
                    print("Opción inválida")

    def display_info(self, faculty):
        print(
            f"ID: {self.id_cat}\nNombre: {self.name}\nDPI: {self.documento_personal}\nNúmero telefónico: {self.phone_u}\nCursos:")
        if len(self.assigned_courses)>=1:
            for course in self.assigned_courses:
                print(f"\nID: {course}, Nombre: {faculty.courses_db[course].name}")
            return ""
        else:
            print("No hay cursos asignados")
            return ""


class Curso:
    def __init__(self, id_course, name, docente):
        self.id_course = id_course
        self.name = name
        self.teacher_assigned = docente
        self.roster_alumnos = []
        self.asignaciones = []

        '''
        Este método se encarga de convertir el objeto y sus atributos en un diccionario de Python. 
        ya que no se puede guardar un objeto como tal en un archivo 'json'
        entonces los objetos los convertimos en 'diccionarios' que si se puedan almacenar
        como clave valor.
        '''

    def to_dict(self): #pablo_ implementacion de un nuevo método
        return {
            "id_course":self.id_course,
            "name":self.name,
            "teacher_assigned":self.teacher_assigned,
            "roster_alumnos":self.roster_alumnos,
            "asignaciones":[a.to_dict() for a in self.asignaciones]
        }

    '''
    Este método se encarga propiamente de revertir el metodo de 'to_dict'
    ya que como un archivo json guarda los objetos por clave/valor 
    necesitamos volver a convertir estos objetos almacenados en atributos de la 
    clase 'cuso' y 'actividad'
    '''
    @staticmethod
    def from_dict(data):
        curso = Curso(data['id_course'], data['name'], data['teacher_assigned'])
        curso.roster_alumnos = data['roster_alumnos']
        for act_data in data['asignaciones']:
            actividad = Actividad.from_dict(act_data)
            curso.asignaciones.append(actividad)
        return curso

    def mostrar_datos(self, faculty):
        print(
            f"=========================\nID: {self.id_course}\n Nombre: {self.name}\n Docente: {self.teacher_assigned}\n Alumnos:")
        if self.roster_alumnos:
            for id in self.roster_alumnos:
                student = faculty.students_db.get(id)
                if student:
                    print(student.display_info())
        else:
            print("No hay alumnos asignados")
        print("\nAsignaciones: ")
        if self.asignaciones:
            for asignacion in self.asignaciones:
                asignacion.mostrar_datos()
        else:
            print("No hay asignaciones asignadas")

    def calcular_nota(self, carnet):
        nota_obtenida = 0
        nota_total_posible = 0
        for asignacion in self.asignaciones:
            nota_obtenida += asignacion.submission.get(carnet, 0)
            nota_total_posible += asignacion.valor_n
        return nota_obtenida, nota_total_posible

class Actividad:
    # CLASE QUE NOS SRIVE PARA LA GESTIONAR LAS ACTIVIDADES ACADEMICAS
    def __init__(self, act_id, name, valor_neto, valor_de_calificacion, date_str, h_apertura_str, h_cierre_str, type_a):
        self.__act_id = act_id
        self.name = name
        self.valor_n = valor_neto
        self.valor_dc = valor_de_calificacion
        self.date = date_str
        self.h_apertura = h_apertura_str
        self.h_cierre = h_cierre_str
        self.type_a = type_a
        self.status = False
        self.submission = {}
        self.set_status()

    @property
    def act_id(self):
        return self.__act_id

    def to_dict(self):
        return {
            "act_id": self.__act_id,
            "name":self.name,
            "valor_n":self.valor_n,
            "valor_dc":self.valor_dc,
            "date":self.date,
            "h_apertura":self.h_apertura,
            "h_cierre":self.h_cierre,
            "type_a":self.type_a,
            "status":self.status,
            "submission": self.submission

        }
    @staticmethod
    def from_dict(data):
        actividad = Actividad(
            data["act_id"], data["name"], data["valor_n"], data["valor_dc"],
            data["date"], data["h_apertura"], data["h_cierre"], data["type _a"]
        )
        actividad.submission = data.get("submission", {})
        actividad.status = data.get("status", False)
        return actividad

    def set_status(self):
        try:
            ahora= datetime.datetime.now()
            fecha_cierre = datetime.datetime.strptime(f"{self.date}{self.h_cierre}", "%d-%m-%Y %H:%M" )
            self.status = ahora <= fecha_cierre
        except ValueError:
            self.status = False

    def mostrar_datos(self):
        print(
            f"------------------------------\nNombre: {self.name}\n Valor: {self.valor_n}\nFecha Limite: {self.date}\nApertura: {self.h_apertura}\nCierre: {self.h_cierre}\nTipo: {self.type_a}\nEstado:{'Abierta' if self.status else 'Cerrada'}")


def deploy_admin_menu(faculty):
    admin_key = True
    while admin_key:
        print("\n", "~" * 15, "BIENVENIDO", "~" * 15)
        ops = ["1. Crear Curso", "2. Crear Usuario", "3. Ver cursos", "4. Ver alumnos", "5. Ver maestros",
               "6. Asignar Maestros", "7. Guardar", "8. Salir"]
        seleccion = menu(ops, "MENÚ ADMIN")
        admin_ops = ops[seleccion].split(".")[0]
        match admin_ops:

            # Creación de cursos
            case "1":
                print("-" * 15, "COURSE CREATION", "-" * 15)
                course_name = ""
                while len(course_name) <= 3:
                    course_name = input("> Nombre del curso (mínimo 4 caracteres): ")
                    if len(course_name) <= 3:
                        print("> El nombre no es válido.....")


                teacher = "N/A"
                if not faculty.teachers_db:
                    print("> No hay maestros disponibles...\n> Curso ha sido creado con éxito...")

                else:
                    for temp_cont, teacher_x in enumerate(faculty.teachers_db.values(), start=1):
                        print(f"{temp_cont}|{teacher_x.name}|{teacher_x.id_cat} ~ ID")
                    search_work_id = input("> Coloque el ID del maestro que desea asignar (o '0' para ninguno): ")
                    if search_work_id in faculty.teachers_db:
                        teacher_id = search_work_id
                    elif search_work_id == "0":
                        print("> Ningún maestro seleccionado. Curso creado sin maestro asignado.")
                    else:
                        print("> ID de maestro no válido. Curso creado sin maestro asignado.")


                course_id = id_creation(course_name, "C")
                faculty.courses_db[course_id] = Curso(course_id, course_name, teacher)
                if teacher_id != "N/A":
                    faculty.teachers_db[teacher].assigned_courses.append(course_id)
                print(f"Curso '{course_name}' creado con ID: {course_id}")

            # Creación de usuarios ; dpi, address, phone, dob, password_u
            case "2":

                user_name = input("> Coloque el nombre del Usuario: ")
                user_address = input("> Coloque la dirección del Usuario: ")
                user_phone = input("> Coloque el teléfono del Usuario: ")
                user_dob = b_day_check(input("> Coloque la fecha de nacimiento del Usuario DD/MM/AAAA: "))
                user_pass = input("> Coloque la contraseña del Usuario: ")
                user_dpi = doc_check(input("> Coloque el DPI del Usuario: "), faculty)
                user_inscr_year = input("> Coloque el año de inscripción: ")

                user_type = input("> Seleccione el tipo de usuario:\n1. Estudiante\n2. Docente\n")
                if user_type == "1":
                    user_type = "S"
                    user_id = id_creation("", user_type)
                    faculty.students_db[user_id] = Student(user_name, user_dpi, user_address, user_phone, user_dob,
                                                           user_pass, user_id, user_inscr_year)
                    print(f"Estudiante {user_name} creado con ID: {user_id}")

                 elif user_type == "2":
                    user_type = "T"
                    user_id = id_creation("", user_type)
                    faculty.teachers_db[user_id] = Teacher(user_name, user_dpi, user_address, user_phone, user_dob,
                                                               user_pass, user_id)
                    print(f"Docente {user_name} creado con ID: {user_id}")
                else:
                    print("Opción de tipo de usuario no válida.")


            case "3":
                print("-" * 17, "CURSOS DISPONIBLES", "-" * 17)
                print("No.".ljust(8) + "Nombre del curso".ljust(30) + "Maestro asignado".ljust(20) +f"\n" + "---"*18)
                for index, course in enumerate(faculty.courses_db.values(), start=1):
                    print(str(index).ljust(8) + course.name.ljust(30) + faculty.teachers_db[course.teacher_assigned].name.ljust(20))

            case "4":
                print("-" * 15, "ALUMNOS REGISTRADOS", "-" * 15)
                for index, student in enumerate(faculty.students_db.values(), start=1):
                    print(student.display_info())

            case "5":
                print("-" * 15, "MAESTROS REGISTRADOS", "-" * 15)
                for index, teacher_x in enumerate(faculty.teachers_db.values(), start=1):
                    print(teacher_x.display_info(faculty))

            case "6":
                if not faculty.teachers_db:
                    print("> No hay maestros disponibles...")
                else:
                    print("-" * 15, "CURSOS DISPONIBLES", "-" * 15)
                    for index, course in enumerate(faculty.courses_db.values(), start=1):
                        if course.teacher_assigned == "N/A":
                            print(f"> {index}. {course.name}|ID: {course.id_course}")

                    calss_conmf = False
                    while not calss_conmf:
                        class_assignment = input("> Coloque el ID del curso al que quieres asignar un maestro: ")
                        if class_assignment not in faculty.courses_db.keys():
                            print("> Ese ID no es válido...")
                        else:
                            calss_conmf = True

                    print("-" * 15, f"{faculty.courses_db[class_assignment].name}", "-" * 15)
                    print("> Lista de maestros disponibles: ")
                    for index_x, teacher_y in enumerate(faculty.teachers_db.values(), start=1):
                        print(f"{index_x}. {teacher_y.name}|ID: {teacher_y.id_cat}")

                    teach_conf = False
                    while not teach_conf:
                        teacher_assignment = input("> Coloque el ID del maestro al que quiere agregar: ")
                        if teacher_assignment not in faculty.teachers_db.keys():
                            print("> Ese ID no es válido...")
                        else:
                            teach_conf = True
                    faculty.courses_db[class_assignment].teacher_assigned = faculty.teachers_db[teacher_assignment].id_cat
                    faculty.teachers_db[teacher_assignment].assigned_courses.append(
                        class_assignment)
                    print("Maestro asignado con éxito...\n\n")

            case "7":
                """
                opciones_menu = ["1.Alumnos.","2.Maestros.","3.Cursos."]
                seleccion = menu(opciones_menu, "GUARDADO DE INFORMACIÓN")
                save_ops = opciones_menu[seleccion].split(":")[0]
                match save_ops:
                    case "1":
                """
                try:
                    with open("estudiantes.txt", "w", encoding="utf-8") as courses_file:
                        for id_s, alumni in faculty.students_db.items():
                            assigned_c_data = {}
                            for cid, course_obj in alumni.assigned_c.items():
                                assigned_c_data[cid] = course_obj.name
                            courses_file.write(f"{id_s}||{alumni.name}||{alumni.documento_personal}||{alumni.address}||{alumni.phone_u}||{alumni.dob}||{alumni.pass_ward}||{alumni.carnet}||{alumni.gen}||{json.dumps(assigned_c_data)}\n")

                    with open("Profesores.txt", "w", encoding="utf-8") as teachers_file:
                        for id_t, teacher_temp in faculty.teachers_db.items():
                            teachers_file.write(f"{id_t}||{teacher_temp.name}||{teacher_temp.documento_personal}||{teacher_temp.address}||{teacher_temp.phone_u}||{teacher_temp.dob}||{teacher_temp.pass_ward}||{teacher_temp.id_cat}||{json.dumps(teacher_temp.assigned_courses)}\n")

                    with open("Cursos.txt", "w", encoding="utf-8") as courses_file:
                        for course_id, course_x in faculty.courses_db.items():
                            courses_file.write(f"{course_x.id_course}||{course_x.name}||{course_x.teacher_assigned}||{json.dumps(course_x.roster_alumnos)}||{json.dumps([a.to_dict() for a in course_x.asignaciones])}\n")

                    print("> Datos Guardados con éxito")
                except Exception as e:
                    print(f"Error al guardar datos: {e}")
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
            with open("estudiantes.txt", "r", encoding="utf-8") as archivo_estudiantes:
                for linea in archivo_estudiantes:
                    linea = linea.strip()
                    if linea:
                        id_s, name, dpi, address, phone, dob, password, carnet, gen, assigned_c_file = linea.split("||",9)
                        alumno = Student(name, dpi, address, phone, dob, password, carnet, gen)
                        assigned_cl = json.loads(assigned_c_file)

                        for course_id, data in assigned_cl.items():
                            course_obj = self.courses_db.get(course_id)
                            if course_obj:
                                alumno.assigned_c[course_id] = course_obj

                        self.students_db[id_s] = alumno
                print("Estudiantes importados desde el archivo estudiantes.txt")
        except FileNotFoundError:
            print("No existe estudiantes.txt, se creará al guardar...")
        except Exception as e:
            print(f"Error al cargar estudiantes: {e}")

    def cargar_profesores(self):
        try:
            with open("Profesores.txt", "r", encoding="utf-8") as archivo_profesores:
                for linea in archivo_profesores:
                    linea = linea.strip()
                    if linea:
                        id_t, name, dpi, address, phone, dob, password, id_cat, assigned_courses_str = linea.split("||", 8)
                        maestro = Teacher(name, dpi, address, phone, dob, password, id_t)
                        maestro.assigned_courses = json.loads(assigned_courses_str)
                        self.teachers_db[id_t] = maestro
                print("Maestros importados desde el archivo profesores.txt")
        except FileNotFoundError:
            print("No existe profesores.txt, se creará al guardar")
        except Exception as e:
            print(f"Error al cargar profesores: {e}")

    def cargar_cursos(self):
        try:
            with open("Cursos.txt", "r", encoding="utf-8") as archivo_cursos:
                for linea in archivo_cursos:
                    linea = linea.strip()
                    if linea:
                        id_c, name, teacher_id, roster_alumnos_str, asignaciones_str = linea.split("||", 4)
                        curso = Curso(id_c, name, teacher_id)
                        curso.roster_alumnos = json.loads(roster_alumnos_str)

                        asignaciones_data = json.loads(asignaciones_str)
                        for act_data in asignaciones_data:
                            actividad = Actividad.from_dict(act_data)
                            curso.asignaciones.append(actividad)

                        self.courses_db[id_c] = curso
                print("Cursos importados...")
        except FileNotFoundError:
            print("No existe Cursos.txt, se creará al guardar...")
        except Exception as e:
            print(f"Error al cargar cursos: {e}")

# Ol
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    elif typeP == "A":
        return "ACT" + str(ran_code1) + str(ran_code2)
    else:
        return None

def b_day_check(bday):
    try:
        datetime.datetime.strptime(, "%d/%m/%Y")
        return bday
    except ValueError:
        print(f"Formato de fecha invalido, Intentelo de nuevo.....")
        new_bday = input(">Coloque la fecha de nacimiento del Usuario DD/MM/AAAA: ")
        return b_day_check(new_bday)

def doc_check(dpi, faculty):
    if len(dpi) != 13 or not dpi.isdigit():
        print(f"El DPI no es valido, Debe contener 13 dígitos, intente de nuevo.....")
        new_dpi = input("> Coloque el DPI del Usuario: ")
        return doc_check(new_dpi, faculty)
    if any(dpi= teacher.documento_personal for teacher in faculty.teachers_db.values()) or \
            any(dpi == student.documento_personal for student in faculty.students_db.values()):
        print("> El DPI ya existe. Por favor, intente de nuevo.")
        new_dpi = input("> Coloque el DPI del Usuario: ")
        return doc_check(new_dpi, faculty)
    return dpi



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


        elif user_pass in engineering_faculty.students_db and password_pass == engineering_faculty.students_db[
            user_pass].pass_ward:
            key = engineering_faculty.students_db[user_pass].deploy_s_menu(engineering_faculty)


        elif user_pass in engineering_faculty.teachers_db and password_pass == engineering_faculty.teachers_db[
            user_pass].pass_ward:
            key = engineering_faculty.teachers_db[user_pass].deploy_t_menu(engineering_faculty)
        elif user_pass == "0" and password_pass == "0":
            key = False
        else:
            print("> Usuario o Contraseña incorrectos, por favor intente de nuevo...")

    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")