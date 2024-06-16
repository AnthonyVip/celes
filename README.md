
# Prueba Celes

"Prueba Celes" es un proyecto desarrollado como parte de una prueba técnica para la empresa Celes. El objetivo del proyecto es desarrollar un microservicio en Python que interactue con un Datamart y proporcione una interfaz para realizar consultas y operaciones especificas. Ademas, el microservicio integra la autenticacion con Firebase y se enfoca en pruebas unitarias y CI/CD.




## Requisitos

Los requisitos estan definidos en el archivo pyproject.toml
## Installation

Clonar el repositorio

Dentro del repositorio crear una carpeta llamada "data" y colocar dentro de ella los archivos .parquet que vienen en el zip

crear dentro de la carpeta raiz del proyecto el archivo .env con el siguiente formato:

```bash
ENVIRONMENT="local"
SECRET_KEY=you_secret_key_for_jwt_token
DEBUG=True
OPENAPI_PREFIX=""
ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_TOKEN_PREFIX="Bearer"
ALGORITHM="HS256"
JWT_SUBJECT="access"
DATA_PATH="data/data_chunk*.snappy.parquet"
FIRE_BASE_API_KEY=your_fire_base_api_key
EMAIL_TEST=valid_email_create_in_firebase
PASS_TEST=password_for_email_create_in_firebase
FIREBASE_SERVICE_ACCOUNT=private_key_in_json_format_for_account_service_fire_base_in_base64_format
```

para generar el base64 a partir del archivo json de firebase se podria ejecutar el siguiente comando en Linux:
```bash
cat nombre_del_archivo.json | base64
```

Instalar poetry y las dependencias del proyecto ejecutando los comando:
```bash
python -m pip install --upgrade pip
pip install poetry
poetry install
```

Una vez creado el entorno con poetry ejecutar el siguiente comando para iniciar el servidor:
```bash
poetry run uvicorn main:app
```


## Docker

Desplegar proyecto en docker:

Crear la red en docker:
```bash
docker network create "celes-net"
```

Ejecutar el siguiente comando:
```bash
docker compose -f docker-compose.yml up --build -d
```

para verificar el correcto despliegue del servicio ingresar al swagger en el siguiente link:
```bash
http://127.0.0.1:8000/docs
```

## CI/CD
Ir a los settings del repositorio clonado y crear los siguientes secrets con sus correspondientes values:

```bash
EMAIL_TEST
FIREBASE_SERVICE_ACCOUNT
FIRE_BASE_API_KEY
PASS_TEST
SECRET_KEY
```

el flujo ejecuta las pruebas unitarias automaticamente cuando se hace push a la rama main.

## Documentation

Endpoint para crear usuario:
```bash
http://127.0.0.1:8000/users/create

request:
{
  "email": "email@email.com",
  "password": "test123"
}

response:
{
	"jwt_token": "token"
}
```

Endpoint para login:
```bash
http://127.0.0.1:8000/users/login

request:
{
  "email": "email@email.com",
  "password": "test123"
}

response:
{
	"jwt_token": "token"
}
```

Endpoint Sales Period By Employee
```bash
http://127.0.0.1:8000/datamart/sales_period_by_employee

request:
{
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "key_employee": "key_employee"
}

response:
{
	"cantidad": 0,
	"total": 0.0
}
```

Endpoint Sales Period By Product
```bash
http://127.0.0.1:8000/datamart/sales_period_by_product

request:
{
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "key_product": "key_product"
}

response:
{
	"cantidad": 0,
	"total": 0.0
}
```

Endpoint Sales Period By Store
```bash
http://127.0.0.1:8000/datamart/sales_period_by_store

request:
{
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "key_store": "key_store"
}

response:
{
	"cantidad": 0,
	"total": 0.0
}
```

Endpoint Average Sales By Employee
```bash
http://127.0.0.1:8000/datamart/avg_sales_by_employee

request:
{
  "key_employee": "key_employee"
}

{
	"average_sales": 0.0,
	"total_sales": 0
}
```

Endpoint Average Sales By Product
```bash
http://127.0.0.1:8000/datamart/avg_sales_by_product

request:
{
  "key_product": "key_product"
}

{
	"average_sales": 0.0,
	"total_sales": 0
}
```

Endpoint Average Sales By Store
```bash
http://127.0.0.1:8000/datamart/avg_sales_by_store

request:
{
  "key_store": "key_store"
}

{
	"average_sales": 0.0,
	"total_sales": 0
}
```