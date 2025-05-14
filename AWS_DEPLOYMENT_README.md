# Despliegue en AWS

## Crear una instancia EC2 en AWS:
##### 1.- AWS - EC2 - Lanzar instancia.
##### 2.- Eligir Ubuntu Server
##### 3.- Seleccionar tipo t2.micro

## Configura grupo de seguridad:
##### 1.- Puerto 8000 (para acceder a la api django)

## Instalar docker y docker compose:
##### 1.- sudo apt update && sudo apt install -y docker.io docker-compose
##### 2.- sudo usermod -aG docker $USER
##### 3.- newgrp docker

## Clonar repositorio github:
##### 1.- https://github.com/lmunoz8612/tm-consulting.git

## Levantamiento de aplicación (en terminal):
##### 1.- cd tm-consulting
##### 2.- sudo docker-compose up -d --build
##### 3.- Verificar si esta funcionando la aplicación:
    - sudo systemctl status docker (En caso contrario: sudo systemctl start docker)

##### 4.- http://XX.XXX.XXX.XXX:8000/. Deberia de aparecer:

```bash 
Using the URLconf defined in api.urls, Django tried these URL patterns, in this order:

  admin/
  api/products/
  api/inventory/
  api/stores/
  docs.<format>/ [name='schema-json']
  docs/ [name='schema-swagger-ui']
  redocs/ [name='schema-redoc']
  The empty path didn't match any of these.
```

## Errores conocidos

### No se reconoce docker:
##### 1.- Asegurarse que docker este instalado.
##### 2.- Si no esta instalado:
    - sudo apt update
    - sudo apt install -y docker.io
    - sudo systemctl start docker
    - sudo systemctl enable docker
###### Verificar:
    - docker --version
##### 3.- Asegurarse que docker-compose este instalado. En caso contrario:
    - sudo apt install docker-compose
###### Verificar:
    - sudo docker-compose --version
    - docker ps

### No esta instalado Python:
    - sudo apt update && sudo apt upgrade -y
    - sudo apt install software-properties-common -y
    - sudo apt install python3.12 python3.12-venv python3.12-dev -y
    - python3.12 --version

### Puerto 8000 en EC2 no esta activo o firewall lo bloquea.
##### 1.- Ejecutar:
    - sudo ufw allow 8000
    - sudo ufw reload
