# 🛒 TechGear API: Catálogo de productos y gestión de pedidos

Este proyecto proporciona una API REST para la gestión de un catálogo de productos y la creación de pedidos, desarrollada utilizando **Python, FastAPI y MongoDB**.

La aplicación permite crear, consultar, actualizar y eliminar productos, además de generar pedidos asociados a los productos disponibles y controlar automáticamente el stock.

## 📄 Description

**TechGear API** is a RESTful web API designed to manage products and orders for a technology catalog.

The application is built with **Python, FastAPI, MongoDB and Pydantic**, providing a simple and efficient backend for managing product information and processing orders.

The API allows users to:

* Create new products.
* List all available products.
* Update existing products.
* Delete products.
* Create orders associated with products.
* Validate product existence.
* Validate available stock before creating an order.
* Calculate the total value of each order.
* Automatically decrease the product stock after a successful order.

The API uses **MongoDB** as its database and **Motor** as the asynchronous MongoDB driver.

## 🛠️ Technologies

* **Python**
* **FastAPI**
* **MongoDB**
* **Motor**
* **Pydantic**
* **Uvicorn**
* **python-dotenv**

Las dependencias del proyecto se encuentran definidas en `requirements.txt`.

## 📁 Project Structure

```text
taller2_pydeploy/
│
├── main.py
├── database.py
├── models.py
├── requirements.txt
└── .gitignore
```

### `main.py`

Contiene la aplicación FastAPI y los endpoints para la gestión de productos y pedidos.

### `models.py`

Define los modelos de datos utilizando Pydantic para validar la información de productos y pedidos.

### `database.py`

Gestiona la conexión con MongoDB y define las colecciones `productos` y `pedidos`. La conexión utiliza la variable de entorno `MONGODB_URL`.

## 🚀 Installation

Clona el repositorio:

```bash
git clone https://github.com/carloscastrox/taller2_pydeploy.git
```

Ingresa al proyecto:

```bash
cd taller2_pydeploy
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables

Crea un archivo `.env` en la raíz del proyecto:

```env
MONGODB_URL=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/
```

La aplicación utiliza esta variable para conectarse al clúster de MongoDB. Si no se encuentra definida, el proyecto utiliza por defecto `mongodb://localhost:27017`.

## ▶️ Run the API

Ejecuta la aplicación con Uvicorn:

```bash
uvicorn main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

## 📚 API Documentation

FastAPI genera automáticamente documentación interactiva para probar los endpoints.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

## 🔗 Endpoints

### Productos

| Método   | Endpoint                   | Descripción            |
| -------- | -------------------------- | ---------------------- |
| `POST`   | `/productos/`              | Crear un producto      |
| `GET`    | `/productos/`              | Listar productos       |
| `PUT`    | `/productos/{producto_id}` | Actualizar un producto |
| `DELETE` | `/productos/{producto_id}` | Eliminar un producto   |

### Pedidos

| Método | Endpoint    | Descripción     |
| ------ | ----------- | --------------- |
| `POST` | `/pedidos/` | Crear un pedido |

Los endpoints de productos y pedidos están implementados directamente en `main.py`.

## 📦 Product Example

Ejemplo de información para crear un producto:

```json
{
  "nombre": "Laptop Gamer",
  "descripcion": "Laptop para gaming y trabajo",
  "precio": 3500000,
  "stock": 10
}
```

## 🛍️ Order Example

Para crear un pedido se debe proporcionar el ID del producto y la cantidad:

```json
{
  "producto_id": "ID_DEL_PRODUCTO",
  "cantidad": 2
}
```

La API verifica que el producto exista y que haya stock suficiente. Posteriormente calcula el valor total y descuenta automáticamente las unidades solicitadas del inventario.

## ☁️ API Desplegada

API desplegada en Render con URL pública:

**[API Onrender](https://taller2-pydeploy.onrender.com)**

## 📖 Documentación en Swagger

**[Swagger UI](https://taller2-pydeploy.onrender.com/docs)**

## 👨‍💻 Author

**Carlos Castro**

GitHub: **[carloscastrox](https://github.com/carloscastrox)**
