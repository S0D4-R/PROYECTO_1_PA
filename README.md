Sistema de Gestión Académica
Este proyecto es un sistema de gestión académica desarrollado en Python. Permite a usuarios administradores crear y gestionar cursos, estudiantes y docentes, mientras que los estudiantes pueden inscribirse a cursos y ver sus notas, y los docentes pueden crear actividades y calificar a los alumnos.

Características Principales
El sistema cuenta con tres tipos de roles de usuario, cada uno con funcionalidades específicas:

Administrador:

Crear, ver y gestionar cursos.

Crear y ver usuarios (estudiantes y docentes).

Asignar docentes a los cursos.

Guardar todos los datos en archivos de texto para persistencia.

Docente:

Ver los cursos que tiene asignados.

Crear nuevas actividades (tareas, proyectos, exámenes) para sus cursos.

Subir y actualizar las notas de los estudiantes.

Generar reportes sobre el rendimiento de los estudiantes.

Estudiante:

Inscribirse a cursos disponibles.

Ver sus cursos asignados.

Entregar actividades y ver sus notas.

Consultar su perfil y trayectoria académica.

Ver los reportes generados por los docentes.

Estructura del Código
El proyecto está estructurado de manera modular y utiliza Programación Orientada a Objetos (POO) para manejar las diferentes entidades del sistema.

Clases Principales:

User: Clase base con atributos comunes como nombre, DPI, dirección, etc.

Student y Teacher: Clases que heredan de User e implementan funcionalidades específicas para cada rol.

Curso: Gestiona la información de cada curso, incluyendo docentes, alumnos y actividades.

Actividad: Representa una asignación o evaluación, con detalles como valor, fecha de entrega y notas de los estudiantes.

Database: Se encarga de la carga y el guardado de datos desde y hacia archivos de texto (.txt), garantizando que la información se mantenga entre sesiones.

Archivos de Datos:

estudiantes.txt

Profesores.txt

Cursos.txt
Claro, aquí tienes un archivo README.md completo para GitHub que describe tu código. Este archivo está diseñado para ser claro y fácil de entender para otros desarrolladores.

README.md
Sistema de Gestión Académica 🎓
Este proyecto es un sistema de gestión académica desarrollado en Python. Permite a usuarios administradores crear y gestionar cursos, estudiantes y docentes, mientras que los estudiantes pueden inscribirse a cursos y ver sus notas, y los docentes pueden crear actividades y calificar a los alumnos.

Características Principales
El sistema cuenta con tres tipos de roles de usuario, cada uno con funcionalidades específicas:

Administrador:

Crear, ver y gestionar cursos.

Crear y ver usuarios (estudiantes y docentes).

Asignar docentes a los cursos.

Guardar todos los datos en archivos de texto para persistencia.

Docente:

Ver los cursos que tiene asignados.

Crear nuevas actividades (tareas, proyectos, exámenes) para sus cursos.

Subir y actualizar las notas de los estudiantes.

Generar reportes sobre el rendimiento de los estudiantes.

Estudiante:

Inscribirse a cursos disponibles.

Ver sus cursos asignados.

Entregar actividades y ver sus notas.

Consultar su perfil y trayectoria académica.

Ver los reportes generados por los docentes.

Estructura del Código
El proyecto está estructurado de manera modular y utiliza Programación Orientada a Objetos (POO) para manejar las diferentes entidades del sistema.

Clases Principales:

User: Clase base con atributos comunes como nombre, DPI, dirección, etc.

Student y Teacher: Clases que heredan de User e implementan funcionalidades específicas para cada rol.

Curso: Gestiona la información de cada curso, incluyendo docentes, alumnos y actividades.

Actividad: Representa una asignación o evaluación, con detalles como valor, fecha de entrega y notas de los estudiantes.

Database: Se encarga de la carga y el guardado de datos desde y hacia archivos de texto (.txt), garantizando que la información se mantenga entre sesiones.

Archivos de Datos:

estudiantes.txt

Profesores.txt

Cursos.txt

Requisitos e Instalación
Para ejecutar este proyecto, necesitas tener Python instalado. Las librerías necesarias pueden ser instaladas usando pip:

Bash

pip install colorama msvcrt
colorama: Se usa para agregar colores en la consola, mejorando la experiencia del usuario.

msvcrt: Se utiliza para capturar las pulsaciones de teclado en tiempo real, lo que permite la navegación interactiva en los menús.

Uso
Clona el repositorio o descarga el código fuente.

Ejecuta el archivo principal:

Bash

python main.py
El programa te pedirá las credenciales de inicio de sesión.

Para Administrador:

Usuario: ruler

Contraseña: admin01

Para Usuarios:

Usa el ID de usuario y la contraseña que se generen al crear un estudiante o docente.

Una vez dentro, podrás navegar por los menús interactivos para realizar las acciones correspondientes a tu rol.

Autor
Jackelin Vásquez  1503725
Jorge Ernesto Tay 1532625
Jorge Rivera      1511425 
Pablo Quijivix    1578125


