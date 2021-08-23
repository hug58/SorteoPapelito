# Sorteo




## Instalacion

Compila primero todo los servicios 

```bash
  docker-compose up -d --build
```


```bash
  docker-compose up
```

## Config
en el example.env cambia las auth del servidor de correo

```bash
  EMAIL_HOST_USER = "name@gmail.com"
  EMAIL_HOST_PASSWORD = "123456"
```



### Registrar un usuario
Ejemplo:

```bash

curl -X POST "http://localhost:8000/api/auth/register/" -H  "accept: application/json" -H  "Content-Type: application/json" -H  "X-CSRFToken: MUbXf9Zg4IjHO4qcc1Pp7021pSsGdb2zqTTv98O0Ll13G2eBMxMHfZZhlEvruPe9" -d "{  \"email\": \"mohu88vdet@gmail.com\",  \"username\": \"mohu88\",  \"address\": \"mi_casa\",  \"phone\": \"04127682166\",  \"sex\": 0}"

```

En el correo deberia llegarte un mensaje con un link asi:

```bash

http://localhost:8000/api/auth/password-reset/NQ/artilm-4be653e8cbb2f600c9157e6944e53ebc/

```
La peticion bash seria asi:

```bash
curl -X PATCH "http://localhost:8000/api/auth/password-reset/NQ/artilm-4be653e8cbb2f600c9157e6944e53ebc/" -H  "accept: application/json" -H  "Content-Type: application/json" -H  "X-CSRFToken: MUbXf9Zg4IjHO4qcc1Pp7021pSsGdb2zqTTv98O0Ll13G2eBMxMHfZZhlEvruPe9" -d "{  \"password\": \"sombra\"}"

```

### Login

Para activar el sorteo se necesita a un usuario logueado usando jwt

```bash
curl -X POST "http://localhost:8000/api/auth/login/" -H  "accept: application/json" -H  "Content-Type: application/json" -H  "X-CSRFToken: MUbXf9Zg4IjHO4qcc1Pp7021pSsGdb2zqTTv98O0Ll13G2eBMxMHfZZhlEvruPe9" -d "{  \"email\": \"mohu88vdet@gmail.com\",  \"password\": \"sombra\"}"

```

con esto obtendiamos..

``` json
{
  "email": "mohu88vdet@gmail.com",
  "username": "mohu88",
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyOTc4MjU0OSwianRpIjoiOTA4ZTRkMjQwMWRlNDM1ZDk3NzU3NzAxZDIxNGJlZjUiLCJ1c2VyX2lkIjo1fQ.UwSTJC1Y_Rtvp_s6HwgpqMIZHE2F2s06xAv4xG5galY",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI5Njk3OTQ5LCJqdGkiOiI5NTZkNGUyNmVjZjI0ZGQ5ODdjODg0ZjY3ZmY2MTk4MCIsInVzZXJfaWQiOjV9.0eA-QNnY7zMKEyPtrsXeLtCwRHaFqVeP_ukgc8UKUck"
  }
}

```

### Sorteos

y ahora lo usamos en la peticion de los sorteos


```bash

curl -X GET "http://localhost:8000/api/winner" -H  "accept: application/json" -H  "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI5Njk3OTQ5LCJqdGkiOiI5NTZkNGUyNmVjZjI0ZGQ5ODdjODg0ZjY3ZmY2MTk4MCIsInVzZXJfaWQiOjV9.0eA-QNnY7zMKEyPtrsXeLtCwRHaFqVeP_ukgc8UKUck" -H  "X-CSRFToken: MUbXf9Zg4IjHO4qcc1Pp7021pSsGdb2zqTTv98O0Ll13G2eBMxMHfZZhlEvruPe9"

```
El response(como solo hay un concursante, pues obviamente el ganador es mohu) :

```json 

{
  "message": "winner is mohu88",
  "info-user": {
    "email": "mohu88vdet@gmail.com",
    "username": "mohu88",
    "address": "mi_casa",
    "phone": "04127682166",
    "sex": 0
  }
}

```


### Swagger

En raiz (http://localhost:8000/) esta instalado el doc, mucho mas facil de seguir. Ten en cuenta que se usa Bearer para
la autenticacion


## Para desmontar la imagen usa el comando

```bash
  docker-compose down -v
```

