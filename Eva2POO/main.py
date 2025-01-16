from clases.empleado import Empleado
from clases.departamento import Departamento
from clases.proyecto import Proyecto
from clases.registro_tiempo import RegistroTiempo
from clases.usuario import Usuario
from datetime import datetime
import re

def validar_entrada(texto, tipo):
    if tipo == "nombre":
        return bool(re.match(r"^[A-Za-zÁ-Úá-úñÑ\s]{2,100}$", texto))
    elif tipo == "email":
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", texto))
    elif tipo == "telefono":
        return bool(re.match(r"^\+?[0-9]{8,15}$", texto))
    elif tipo == "fecha":
        try:
            datetime.strptime(texto, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    return True

def input_validado(mensaje, tipo):
    while True:
        valor = input(mensaje)
        if validar_entrada(valor, tipo):
            return valor
        print(f"Entrada inválida. Por favor, ingrese un {tipo} válido.")

def menu_inicio():
    print("\n=== Sistema de Gestión de Empleados ===")
    print("1. Iniciar Sesión")
    print("2. Registrarse")
    print("3. Salir")
    return input("Seleccione una opción: ")

def registrar_usuario():
    print("\n=== Registro de Usuario ===")
    username = input_validado("Username: ", "username")
    password = input("Contraseña (mínimo 6 caracteres): ")
    if len(password) < 6:
        print("La contraseña debe tener al menos 6 caracteres")
        return False

    print("\nRoles disponibles:")
    print("1. Empleado")
    print("2. RRHH")
    rol_opcion = input("Seleccione el rol (1-2): ")
    
    if rol_opcion == "1":
        rol = "empleado"
    elif rol_opcion == "2":
        rol = "rrhh"
    else:
        print("Opción no válida")
        return False

    usuario = Usuario(username, password, rol)
    if usuario.guardar():
        print("Usuario creado exitosamente")
        
        # Si es empleado, crear registro en tabla empleados
        if rol == "empleado":
            print("\nPor favor, complete los datos del empleado:")
            nombre = input_validado("Nombre completo: ", "nombre")
            direccion = input("Dirección: ")
            telefono = input_validado("Teléfono: ", "telefono")
            fecha_inicio = input_validado("Fecha de inicio (YYYY-MM-DD): ", "fecha")
            while True:
                try:
                    salario = float(input("Salario: "))
                    if salario > 0:
                        break
                    print("El salario debe ser mayor que 0")
                except ValueError:
                    print("Por favor ingrese un número válido")
            
            empleado = Empleado(nombre, direccion, telefono, username, fecha_inicio, salario)
            if empleado.guardar():
                print("Empleado registrado exitosamente")
                return True
            else:
                print("Error al registrar empleado")
                return False
        return True
    else:
        print("Error al crear usuario")
        return False

def login():
    print("\n=== Login ===")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    
    usuario = Usuario(username, password, "")
    rol = usuario.verificar_credenciales()
    
    if rol:
        print(f"Bienvenido, {username} ({rol})")
        return rol, username
    else:
        print("Credenciales inválidas")
        return None, None

def mostrar_menu(rol):
    print("\n=== Menú Principal ===")
    if rol in ['admin', 'rrhh']:
        print("1. Registrar Empleado")
        print("2. Gestionar Departamentos")
        print("3. Asignar Empleado a Departamento")
        print("4. Registrar Tiempo")
        print("5. Gestionar Proyectos")
        print("6. Salir")
    else:  # empleado
        print("1. Registrar Tiempo")
        print("2. Ver Mis Registros")
        print("3. Salir")
    return input("Seleccione una opción: ")

def registrar_empleado():
    print("\n=== Registro de Empleado ===")
    nombre = input_validado("Nombre: ", "nombre")
    direccion = input("Dirección: ")
    telefono = input_validado("Teléfono: ", "telefono")
    email = input_validado("Email: ", "email")
    fecha_inicio = input_validado("Fecha de inicio (YYYY-MM-DD): ", "fecha")
    while True:
        try:
            salario = float(input("Salario: "))
            if salario > 0:
                break
            print("El salario debe ser mayor que 0")
        except ValueError:
            print("Por favor ingrese un número válido")

    empleado = Empleado(nombre, direccion, telefono, email, fecha_inicio, salario)
    if empleado.guardar():
        print("Empleado registrado exitosamente")
    else:
        print("Error al registrar empleado")

def gestionar_departamentos():
    while True:
        print("\n=== Gestión de Departamentos ===")
        print("1. Crear Departamento")
        print("2. Listar Departamentos")
        print("3. Actualizar Departamento")
        print("4. Eliminar Departamento")
        print("5. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input_validado("Nombre del departamento: ", "nombre")
            departamento = Departamento(nombre, None)
            if departamento.guardar():
                print("Departamento creado exitosamente")
            else:
                print("Error al crear departamento")
        
        elif opcion == "2":
            print("\n=== Listado de Departamentos ===")
            departamento = Departamento("", None)
            departamento.db.conectar()
            
            # Consulta para obtener departamentos con información del gerente
            query = """
                SELECT d.id, d.nombre, 
                       COALESCE(e.nombre, 'Sin gerente') as gerente,
                       COUNT(emp.id) as num_empleados
                FROM departamentos d
                LEFT JOIN empleados e ON d.gerente_id = e.id
                LEFT JOIN empleados emp ON emp.departamento_id = d.id
                GROUP BY d.id, d.nombre, e.nombre
                ORDER BY d.id
            """
            
            departamentos = departamento.db.ejecutar_query(query)
            departamento.db.desconectar()
            
            if not departamentos:
                print("No hay departamentos registrados")
                continue
            
            print("\nID | Nombre                  | Gerente                | N° Empleados")
            print("-" * 75)
            
            for dep in departamentos:
                id_dep, nombre, gerente, num_empleados = dep
                print(f"{id_dep:2} | {nombre:22} | {gerente:20} | {num_empleados:11}")
        
        elif opcion == "3":
            try:
                id_departamento = int(input("ID del departamento a actualizar: "))
                nombre = input_validado("Nuevo nombre del departamento: ", "nombre")
                departamento = Departamento(nombre, None)
                if departamento.actualizar(id_departamento):
                    print("Departamento actualizado exitosamente")
                else:
                    print("Error al actualizar departamento")
            except ValueError:
                print("ID inválido")
        
        elif opcion == "4":
            try:
                id_departamento = int(input("ID del departamento a eliminar: "))
                departamento = Departamento("", None)
                if departamento.eliminar(id_departamento):
                    print("Departamento eliminado exitosamente")
                else:
                    print("Error al eliminar departamento")
            except ValueError:
                print("ID inválido")
        
        elif opcion == "5":
            break
        else:
            print("Opción no válida")

def asignar_empleado_departamento():
    print("\n=== Asignar Empleado a Departamento ===")
    try:
        # Mostrar empleados disponibles
        print("\nEmpleados disponibles:")
        print("ID | Nombre | Email")
        print("-" * 50)
        empleado = Empleado("", "", "", "", "", 0)
        empleado.db.conectar()
        query = "SELECT id, nombre, email FROM empleados"
        empleados = empleado.db.ejecutar_query(query)
        empleado.db.desconectar()

        if not empleados:
            print("No hay empleados registrados")
            return

        for emp in empleados:
            print(f"{emp[0]} | {emp[1]} | {emp[2]}")

        # Mostrar departamentos disponibles
        print("\nDepartamentos disponibles:")
        print("ID | Nombre | Gerente")
        print("-" * 50)
        departamento = Departamento("", None)
        departamento.db.conectar()
        query = """
            SELECT d.id, d.nombre, COALESCE(e.nombre, 'Sin gerente') 
            FROM departamentos d 
            LEFT JOIN empleados e ON d.gerente_id = e.id
        """
        departamentos = departamento.db.ejecutar_query(query)
        departamento.db.desconectar()

        if not departamentos:
            print("No hay departamentos registrados")
            return

        for dep in departamentos:
            print(f"{dep[0]} | {dep[1]} | {dep[2]}")

        # Pedir IDs
        empleado_id = int(input("\nID del empleado: "))
        departamento_id = int(input("ID del departamento: "))

        # Asignar empleado al departamento
        empleado = Empleado("", "", "", "", "", 0)
        if empleado.asignar_departamento(departamento_id, empleado_id):
            print("Empleado asignado exitosamente al departamento")
        else:
            print("Error al asignar empleado al departamento")
    except ValueError:
        print("ID inválido")

def registrar_tiempo(empleado_id=None):
    print("\n=== Registro de Tiempo ===")
    try:
        # Solo pedir ID si es admin/rrhh (cuando empleado_id es None)
        if empleado_id is None:
            empleado_id = int(input("ID del empleado: "))
        else:
            print(f"Registrando tiempo para empleado ID: {empleado_id}")
        
        # Mostrar lista de proyectos disponibles
        print("\nProyectos disponibles:")
        print("ID | Nombre | Descripción")
        print("-" * 50)
        proyecto = Proyecto("", "", "")
        proyectos = proyecto.listar_todos()
        if proyectos:
            for p in proyectos:
                print(f"{p[0]} | {p[1]} | {p[2]}")
        else:
            print("No hay proyectos disponibles")
            return
        
        proyecto_id = int(input("\nID del proyecto: "))
        fecha = input_validado("Fecha (YYYY-MM-DD): ", "fecha")
        while True:
            try:
                horas = float(input("Horas trabajadas: "))
                if 0 < horas <= 24:
                    break
                print("Las horas deben estar entre 0 y 24")
            except ValueError:
                print("Por favor ingrese un número válido")
        descripcion = input("Descripción de las tareas: ")

        registro = RegistroTiempo(empleado_id, proyecto_id, fecha, horas, descripcion)
        if registro.guardar():
            print("Tiempo registrado exitosamente")
        else:
            print("Error al registrar tiempo")
    except ValueError:
        print("ID inválido")

def gestionar_proyectos():
    print("\n=== Gestión de Proyectos ===")
    print("1. Crear Proyecto")
    print("2. Actualizar Proyecto")
    print("3. Eliminar Proyecto")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nombre = input_validado("Nombre del proyecto: ", "nombre")
        descripcion = input("Descripción: ")
        fecha_inicio = input_validado("Fecha de inicio (YYYY-MM-DD): ", "fecha")
        proyecto = Proyecto(nombre, descripcion, fecha_inicio)
        if proyecto.guardar():
            print("Proyecto creado exitosamente")
        else:
            print("Error al crear proyecto")
    elif opcion == "2":
        try:
            id_proyecto = int(input("ID del proyecto a actualizar: "))
            nombre = input_validado("Nuevo nombre del proyecto: ", "nombre")
            descripcion = input("Nueva descripción: ")
            fecha_inicio = input_validado("Nueva fecha de inicio (YYYY-MM-DD): ", "fecha")
            proyecto = Proyecto(nombre, descripcion, fecha_inicio)
            if proyecto.actualizar(id_proyecto):
                print("Proyecto actualizado exitosamente")
            else:
                print("Error al actualizar proyecto")
        except ValueError:
            print("ID inválido")
    elif opcion == "3":
        try:
            id_proyecto = int(input("ID del proyecto a eliminar: "))
            proyecto = Proyecto("", "", "")
            if proyecto.eliminar(id_proyecto):
                print("Proyecto eliminado exitosamente")
            else:
                print("Error al eliminar proyecto")
        except ValueError:
            print("ID inválido")

def ver_registros_tiempo(empleado_id):
    print("\n=== Mis Registros de Tiempo ===")
    registro = RegistroTiempo(empleado_id, None, None, None, None)
    registros = registro.obtener_registros_empleado(empleado_id)
    
    if not registros:
        print("No hay registros de tiempo disponibles.")
        return
    
    print("\nFecha       | Horas | Proyecto        | Descripción")
    print("-" * 70)
    
    for reg in registros:
        fecha, horas, descripcion, nombre_proyecto = reg
        # Si el nombre del proyecto es None, mostrar "Desconocido"
        nombre_proyecto = nombre_proyecto if nombre_proyecto else "Desconocido"
        # Formatear la fecha como string si no lo está
        if isinstance(fecha, str):
            fecha_str = fecha
        else:
            fecha_str = fecha.strftime("%Y-%m-%d")
        
        print(f"{fecha_str} | {horas:5.1f} | {nombre_proyecto:13} | {descripcion}")

def main():
    while True:
        opcion = menu_inicio()
        
        if opcion == "1":
            rol, username = login()
            if rol:
                empleado_id = None
                if rol == "empleado":
                    # Obtener el ID del empleado basado en su usuario
                    empleado = Empleado("", "", "", "", "", 0)
                    empleado.db.conectar()
                    query = "SELECT id FROM empleados WHERE email = %s"
                    resultado = empleado.db.ejecutar_query(query, (username,))
                    empleado.db.desconectar()
                    if resultado:
                        empleado_id = resultado[0][0]
                        print(f"Bienvenido empleado ID: {empleado_id}")
                    else:
                        print("Error: No se encontró el registro de empleado")
                        continue
                
                while True:
                    try:
                        opcion = mostrar_menu(rol)
                        if rol in ['admin', 'rrhh']:
                            if opcion == "1":
                                registrar_empleado()
                            elif opcion == "2":
                                gestionar_departamentos()
                            elif opcion == "3":
                                asignar_empleado_departamento()
                            elif opcion == "4":
                                registrar_tiempo()  # Sin empleado_id para admin/rrhh
                            elif opcion == "5":
                                gestionar_proyectos()
                            elif opcion == "6":
                                print("¡Hasta luego!")
                                break
                        else:  # rol empleado
                            if opcion == "1":
                                registrar_tiempo(empleado_id)  # Pasar empleado_id
                            elif opcion == "2":
                                ver_registros_tiempo(empleado_id)
                            elif opcion == "3":
                                print("¡Hasta luego!")
                                break
                        
                    except Exception as e:
                        print(f"Error: {str(e)}")
                        
        elif opcion == "2":
            registrar_usuario()
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()
