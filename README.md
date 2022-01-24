# Ampliación de base de datos - Mongodb y Redis
## Mongo
Creación de una base de datos de personas, empresas y centros educativos. Diseño de una aplicación que pueda gestionar la entrada de nuevas entidades y realizar búsquedas.

Aparte realizar las siguientes búsquedas:
1. Listado de todas las personas de Huelva.
2. Listado de todas personas que han estudiado en la UPM o UAM.
3. Listado de las diferentes ciudades en las que se encuentran las personas
4. Listado de las 10 personas más cercanas a unas coordenadas determinadas.
5. Guarda en una tabla nueva el listado de las personas que ha terminado alguno de sus
estudios en el 2017 o después.
6. Calcular el número medio de estudios realizados por las personas que han trabajado o
trabajan en la UPM.
7. Listado de las tres universidades que más veces aparece como centro de estudios de las
personas registradas. Mostrar universidad y el número de veces que aparece.

## Redis
El ejercicio consiste en utilizar la base de datos de mongodb e implementar un sistema de caché, sesiones y una help desk.

##### Caché
Se trata de implementar un sistema de cache que guarda las búsquedas que se hacen en la base de datos de mongodb, para que si son buscados una segunda vez algo y se vuelve a pedir en las próximas 24 horas se mantenga en la base de redis y la búsqueda sea mucho mas rapida.

##### Sesiones
Implementación de un sistema de sesiones y una base de datos que guarde la información.

##### HelpDesk
Diseño e implementación de las funciones necesarias para la gestión de peticiones de ayuda de los usuarios.
