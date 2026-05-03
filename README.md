# 🛠️ Mesa de Servicios - Gestión de Laboratorios ITM

## 👥 1. Información General
*   **Nombre del Proyecto:** Sistema de Gestión de Tickets
*   **Integrantes del Equipo:** Emmanuel Urrego Gomez
*   **Asignatura:** Aplicaciones y Servicios Web
*   **Institución:** Instituto Tecnológico Metropolitano (ITM)
*   **Fecha:** mayo 2026

---

## 📝 2. Descripción del Sistema

### General
Este sistema es un API REST desarrollado con **FastAPI** diseñado para gestionar de manera eficiente las solicitudes de servicio técnico en los laboratorios de la institución. Aqui se permite el seguimiento completo de un ticket, como desde su creación hasta su cierre. Un usuario reporta un problema en un laboratorio específico y el sistema se encarga de asignar responsables y actualizar el estado de la solicitud.

### Entidades Implementadas
El sistema se basa en cuatro entidades fundamentales modelados con SQLAlchemy y validados mediante Pydantic:
*   **Usuarios:** Gestión de cuentas con roles (Admin, Solicitante, Técnico, Responsable) y seguridad mediante hashing de contraseñas.
*   **Laboratorios:** Registro de espacios donde se prestan los servicios.
*   **Servicios:** Listado de tipos de soportes disponibles (Mantenimiento, Redes, Software, etc.).
*   **Tickets:** Entidad central que vincula a usuarios, laboratorios y servicios, manejando estados de flujo y fechas de control.

### Arquitectura
Se ha implementado una arquitectura de **Capas** para separar las responsabilidades del código y asi grantizar la escalabilidad y el mantenimiento:
1.  **Capa de Modelos (`models.py`):** Define la estructura de las tablas en PostgreSQL.
2.  **Capa de Esquemas (`schemas.py`):** El corazon de la validacion de datos en FASTAPI.
3.  **Capa CRUD (`crud.py`):** Lógica de persistencia y acceso a la base de datos.
4.  **Capa de Seguridad (`security.py`):** Manejo de autenticación JWT y autorización basada en *Scopes*.
5.  **Capa de Rutas (`main.py`):** Orquestación de los endpoints y control de acceso.

---

## ⚙️ 3. Configuración del Entorno

### Requisitos Previos
*   Python 3.10 o superior
*   PostgreSQL instalado y configurado

### 1. Creación y activación del entorno virtual
Los entornos virtuales sirven para que las librerías de este proyecto no se mezclen con otras que se tengan en el equipo.
Para aislar las dependencias del proyecto, ejecuta:

### Crear el entorno virtual
python -m venv venv

### Activar en Windows
source venv/Scripts/activate

### 2. Instalación de Dependencias y Uso de ***requirements.txt***
Una vez activado el entorno, se instala todas las herramientas necesarias que están listadas en el archivo requirements.txt:

### Lista de Dependencias
* fastapi
* uvicorn
* sqlalchemy
* psycopg2-binary
* python-jose[cryptography] — generación y verificación de tokens JWT
* passlib[bcrypt] — hashing seguro de contraseñas
* python-multipart — requerido por el formulario de login de FastAPI
* python-dotenv — manejo de variables de entorno desde archivo .env

### Instalar Dependencias
pip install -r requirements.txt

### 3. Configuración de Variables de Entorno (.env)
Para que el sistema funcione correctamente, se debe de crear un archivo llamado .env en la carpeta principal del proyecto. Este archivo contiene "secretos" de configuración que no deben compartirse públicamente.

Se definen las siguientes variables:

DATABASE_URL: La dirección de conexión a tu base de datos PostgreSQL.

SECRET_KEY: Una clave secreta única para firmar los tokens de seguridad de los usuarios.

ALGORITHM: El método de cifrado para la seguridad (ej. HS256).

ACCESS_TOKEN_EXPIRE_MINUTES: Tiempo de duración de la sesión del usuario antes de pedirle ingresar de nuevo.

---

## 🗄️ 4. Configuración de la Base de Datos

El sistema utiliza **PostgreSQL** como motor de base de datos relacional. La interacción se realiza a través de **SQLAlchemy ORM**.

*   **Motor de BD:** PostgreSQL.
*   **Esquema (Schema):** `jwt_grupo_15`.
*   **Gestión de Conexión:** 
    *   Se utiliza una `SessionLocal` para manejar las transacciones.
    *   La conexión se define mediante la variable de entorno `DATABASE_URL` en el archivo `.env`.
    *   Las tablas se crean automáticamente al iniciar la aplicación mediante `Base.metadata.create_all`.

---

## 🚀 5. Endpoints Implementados

A continuación se detallan los endpoints disponibles, los permisos necesarios para acceder a ellos y qué roles los poseen.

### Autenticación
| Método | Ruta | Descripción | Scope Requerido | Rol(es) Autorizados |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/auth/token` | Login para obtener el Token de acceso | Ninguno | Público |

### Usuarios 🔒
| Método | Ruta | Descripción | Scope Requerido | Rol(es) Autorizados |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/usuarios/` | Listar todos los usuarios | `usuarios:gestionar` | Admin |
| `POST` | `/usuarios/` | Crear un nuevo usuario | `usuarios:gestionar` | Admin |
| `GET` | `/usuarios/{id_usuario}` | Consultar detalle de un usuario | `usuarios:gestionar` | Admin |

### Laboratorios 🔒
| Método | Ruta | Descripción | Scope Requerido | Rol(es) Autorizados |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/laboratorios/` | Listar laboratorios operativos | Autenticado | Todos los roles |
| `POST` | `/laboratorios/` | Registrar nuevo laboratorio | Autenticado | Admin |
| `GET` | `/laboratorios/{id_laboratorio}` | Consultar un laboratorio específico | Autenticado | Todos los roles |

### Servicios 🔒
| Método | Ruta | Descripción | Scope Requerido | Rol(es) Autorizados |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/servicios/` | Listar servicios disponibles | Autenticado | Todos los roles |
| `POST` | `/servicios/` | Crear nuevo tipo de servicio | Autenticado | Admin |
| `GET` | `/servicios/{id_servicio}` | Consultar detalle de un servicio | Autenticado | Todos los roles |

### Tickets 🔒
| Método | Ruta | Descripción | Scope Requerido | Rol(es) Autorizados |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/tickets/` | Ver lista de tickets | `tickets:ver_propios` / `ver_todos` | Todos (según visibilidad) |
| `POST` | `/tickets/` | Crear una nueva solicitud | `tickets:crear` | Solicitante, Admin |
| `GET` | `/tickets/{id_ticket}` | Consultar detalle de un ticket | `tickets:ver_propios` / `ver_todos` | Todos (según visibilidad) |
| `PATCH`| `/tickets/{id_ticket}/estado` | Actualizar estado del ticket | Dinámico (ver flujo) | Según transición |

---

### Detalles de Autorización en el Flujo de Estados

Para el endpoint de actualización de estado (`PATCH`), se aplican reglas de negocio adicionales para garantizar la integridad del proceso:

*   **Recibir Ticket (`solicitado` → `recibido`):** Requiere scope `tickets:recibir`. Autorizado para **Responsable Técnico** y **Admin**.
*   **Asignar Ticket (`recibido` → `asignado`):** Requiere scope `tickets:asignar`. Autorizado para **Responsable Técnico** y **Admin**.
*   **Atender Ticket (`asignado` → `en_proceso` / `en_revision`):** Requiere scope `tickets:atender`. Solo permitido al **Auxiliar/Técnico asignado** al ticket o **Admin**.
*   **Finalizar Ticket (`en_revision` → `terminado`):** Requiere scope `tickets:finalizar`. Autorizado para **Responsable Técnico** y **Admin**.

> **Nota:** Todos los endpoints protegidos requieren el encabezado `Authorization: Bearer <token_jwt>`. La falta de token resultará en un error `401 Unauthorized`, mientras que la falta de permisos adecuados resultará en un `403 Forbidden`.
---

## 📸 6. Evidencias de Funcionamiento

# 6. Evidencias de Funcionamiento

A continuación, se presentan las pruebas realizadas a través de la interfaz de Swagger UI para validar los requerimientos de autenticación, autorización y lógica de negocio.

---

### 🔐 Autenticación con JWT

### 6.1. Login exitoso y generación de Token

### 6.2. Uso del botón Authorize en Swagger

### 6.3. Consulta de endpoint protegido con Token válido

### 6.4. Intento de acceso sin Token

---

## 🛡️ Autorización con Scopes

### 6.5. Usuario con Scope (Acción Permitida)

### 6.6. Usuario sin Scope (Acción Denegada)

---

## ⚙️ Reglas de Negocio del Ticket (Ciclo de Vida)

### 6.7. Creación de Ticket


### 6.8. Recepción (Solicitado → Recibido)

### 6.9. Asignación (Recibido → Asignado)

### 6.10. Ejecución (Asignado → En Proceso)

### 6.11. Revisión (En Proceso → En Revisión)

### 6.12. Finalización (En Revisión → Terminado)

---

## 🚫 Evidencia de Restricciones y Errores

### 6.13. Restricción de Rol

### 6.14. Restricción de Propietario (Técnico no asignado)

### 6.15. Salto de Estado No Permitido


## 7. Control de Versiones
### Enlace al repositorio
https://github.com/3mma-prog/Taller_3.git


