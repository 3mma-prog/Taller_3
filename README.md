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
| Método | Ruta | Descripción | Scope Requerido | Roles Autorizados |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/auth/token` | Login y obtención de JWT. | N/A | Todos los registrados |

### Usuarios
| Método | Ruta | Descripción | Scope Requerido | Roles Autorizados |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/usuarios/` | Crear nuevo usuario. | `usuarios:gestionar` | Admin |
| `GET` | `/usuarios/` | Listar todos los usuarios. | N/A (Solo lectura) | Admin, Auxiliar |
| `GET` | `/usuarios/{id}` | Obtener detalle de usuario. | N/A | Todos |

### Laboratorios y Servicios
| Método | Ruta | Descripción | Scope Requerido | Roles Autorizados |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/laboratorios/` | Crear un laboratorio. | `usuarios:gestionar` | Admin |
| `GET` | `/laboratorios/` | Listar laboratorios. | N/A | Todos |
| `POST` | `/servicios/` | Crear un servicio. | `usuarios:gestionar` | Admin |
| `GET` | `/servicios/` | Listar servicios. | N/A | Todos |

### Gestión de Tickets
| Método | Ruta | Descripción | Scope Requerido | Roles Autorizados |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/tickets/` | Crear un nuevo ticket. | `tickets:crear` | Solicitante, Admin |
| `GET` | `/tickets/` | Ver lista de tickets. | `tickets:ver_todos` o `ver_propios` | Todos (según filtro) |
| `GET` | `/tickets/{id}` | Detalle de un ticket. | `tickets:ver_propios` | Todos |
| `PATCH`| `/tickets/{id}/estado` | Actualizar estado del ticket. | Ver nota debajo* | Auxiliar, Responsable, Técnico |

#### Detalle de Scopes para Actualización de Estado:
*   **Recibir:** `tickets:recibir` (Responsable Técnico, Admin).
*   **Asignar:** `tickets:asignar` (Responsable Técnico, Admin).
*   **Atender:** `tickets:atender` (Auxiliar, Técnico Especializado, Admin).
*   **Finalizar:** `tickets:finalizar` (Responsable Técnico, Admin).

---

## 📸 6. Evidencias de Funcionamiento

