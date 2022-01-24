__author__ = 'Erick_Cardenas_Fernando_Rodriguez'

import redis
from pymongo import MongoClient
from geopy.geocoders import Nominatim
from geojson import Point
from math import sin, cos, sqrt, atan2, radians
from bson.objectid import ObjectId
import json
import uuid


#client = MongoClient('localhost')
#db = client.persona
def getCityGeoJSON(address):
	""" Devuelve las coordenadas de una direcciion a partir de un str de la direccion
	Cuidado, la API tiene un limite de peticiones.
	Argumentos:
		address (str) -- Direccion
	Return:
		(str) -- GeoJSON
	"""
	#from geopy.geocoders import Nominatim
	geolocator = Nominatim(user_agent="P1_GX_Erick_Cardenas_Fernando_Rodriguez.py")
	location = geolocator.geocode(address, timeout=20)
	location_point = Point((location.longitude, location.latitude))

	return location_point
	#TODO
	# Devolver GeoJSON de tipo punto con la latitud y longitud almacenadas
	# en las variables location.latitude y location.longitude

class ModelCursor:
	""" Cursor para iterar sobre los documentos del resultado de una
	consulta. Los documentos deben ser devueltos en forma de objetos
	modelo.
	"""

	def __init__(self, model_class, command_cursor):
		""" Inicializa ModelCursor
		Argumentos:
			model_class (class) -- Clase para crear los modelos del 
			documento que se itera.
			command_cursor (CommandCursor) -- Cursor de pymongo
		"""
		#TODO
		self.model_class = model_class
		self.command_cursor = command_cursor

	def next(self):
		""" Devuelve el siguiente documento en forma de modelo
		"""
		#TODO
		return self.model_class(**self.command_cursor.next())
	@property
	def alive(self):
		"""True si existen más modelos por devolver, False en caso contrario
		"""
		#TODO
		return self.command_cursor.alive
class Persona:
	#self.__dict__.update(kwargs)

	""" Prototipo de la clase modelo
		Copiar y pegar tantas veces como modelos se deseen crear (cambiando
		el nombre Model, por la entidad correspondiente), o bien crear tantas
		clases como modelos se deseen que hereden de esta clase. Este segundo 
		metodo puede resultar mas compleja
	"""
	required_vars = []
	admissible_vars = []
	db = None

	def __init__(self, **kwargs):
		#TODO Constructor
		self.__dict__.update(kwargs)
		for key in self.required_vars:
			if key not in kwargs:
				raise Exception("Error")

	def save(self):
		#TODO
		if hasattr(self, '_id'):
			for key in vars(self):
				if key in self.modified_atributes:
					self.db.update_one({'_id': self._id}, {'$set': {key: getattr(self, key)}})
		else:
			new_tuple = {}
			for key in vars(self):
				if key in self.modified_atributes:
					new_tuple.update({key: getattr(self, key)})

			self.db.insert_one(new_tuple)

		self.modified_atributes.clear
	def set(self, **kwargs):
		#TODO
		self.modified_atributes = []
		print(kwargs)
		for key, value in kwargs.items():
			if key == 'ciudad':
				value['coordenadas'] = getCityGeoJSON(value['nombre'])
			if key not in self.required_vars:
				if key not in self.admissible_vars:
					raise Exception("Error")
			self.modified_atributes.append(key)
			setattr(self, key, value)
	@classmethod
	def find(cls, filter):
		""" Devuelve un cursor de modelos        
		""" 
		#TODO
		# cls es el puntero a la clase
		model_cursor = ModelCursor(cls, cls.db.aggregate(filter))
		return model_cursor
	@classmethod
	def init_class(cls, db, vars_path="model_name.vars"):
		""" Inicializa las variables de clase en la inicializacion del sistema.
		Argumentos:
			db (MongoClient) -- Conexion a la base de datos.
			vars_path (str) -- ruta al archivo con la definicion de variables
			del modelo.
		"""
		cls.db = db
		with open(vars_path) as file:
			cls.required_vars = file.readline().split()
			cls.admissible_vars = file.readline().split()
		#TODO
		# cls es el puntero a la clase

	@classmethod
	def find_by_id(cls, id):
		data = redis_db.get(str(id))
		if data is None:
			data = db.Persona.find_one({"_id":ObjectId(id)})

			if data is None:
				print("No existe")
				return None

			else:
				redis_db.set(id, str(data))
		redis_db.expire(id, 86400)
		return data

class User:
    username = None
    password = None
    privilegios = None

    def init_class(cls, name, passwd, priv):
        cls.username = name
        cls.password = passwd
        cls.privilegios = priv
        return cls

def login(r, log):
    while(True):
        user = input("Cual es tu nombre de usuario:")
        contrasena = input("Cual es tu contrasena:")
        if r.hget("users", user) != None:

            if r.hget("users", user) == contrasena:
                print("Datos correctos, privilegios:" + r.hget("privilegios", user))
                log.init_class(user, contrasena,r.hget("privilegios", user))
                tok = str(uuid.uuid4())
                r.set(tok, user, ex=2629800000)
                print(tok)
                break
            else:
                print("Datos incorrectos1")
        else:
            print("Datos incorrectos2")

def loginByToken(r,token, log):
    if r.get(token) != None:
        user = r.get(token)
        log.init_class(user, r.hget("users", user),r.hget("privilegios", user))
        print("Datos correctos")
        print(log.username)
    else:
        print("Ese token no pertenece a nadie")

def peticionAyuda(id, prioridad):
	redis_db.zadd('colaAyuda',{id:prioridad})

def gestionAyuda():
	print(redis_db.bzpopmax('colaAyuda',0))

if __name__ == '__main__':
	jsonPath = "redES.json"
	client = MongoClient()
	db = client.test2
	with open(jsonPath,'r') as info:
		model_data = json.loads(info.read())

	Persona.init_class(db['Persona'],"personaVariables.txt")

	#print(db.Persona.find({"nombre.nombre":"Fernando"}))

	redis_db = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
	redis_db.config_set("maxmemory", "150mb")				#Limitar la memoria maxima a 150 mb
	redis_db.config_set("maxmemory-policy", "volatile-ttl")	#gestion del exceso de memoria

	log = User()
	# login(redis_db, log)
	loginByToken(redis_db, "21f2c706-0eba-4ab8-bd90-300062ab143b", log)

	# peticionAyuda(log.username, 3)

	# gestionAyuda()

	# Q1: Listado de todas las personas de Huelva.
	# Q1 = db.Persona.find({"ciudad.nombre":"Huelva, Spain"})
	# Q1 = [{"ciudad.nombre":"Huelva, Spain"}]

# Q2: Listado de todas personas que han estudiado en la UPM o UAM
#Q2 = db.Persona.find({$or:[{"estudios.universidad":"UAM"},{"estudios.universidad":"UPM"}]})

# Q3: Listado de las diferentes ciudades en las que se encuentran las personas
#Q3 = db.Persona.aggregate([{$group:{_id:"$by_user",ciudad:{$addToSet:"$ciudad"}}}])

# Q4: Listado de las 10 personas más cercanas a unas coordenadas determinadas.
#Q4 = db.Persona.aggregate([{$geoNear: {near:{type:"Point",coordinates:[ -3.703582, 40.416705 ]}, distanceField:"ciudad.coordenadas", spherical:true}},{$limit:10}])

# Q5: Guarda en una tabla nueva el listado de las personas que ha terminado alguno de sus
# estudios en el 2017 o después
# Q5 = db.Persona.aggregate([{$match: { "estudios.final" : { $gte: ISODate("2017-01-01") } } } ])

# Q6: Calcular el número medio de estudios realizados por las personas que han trabajado o
# trabajan en la UPM.
#Q6 = db.Persona.aggregate({$match:{"trabajo.empresa":"UPM"}},{$group:{_id:"Average", studies:{$avg: {$size:"$estudios"}}}})

# Q7: Listado de las tres universidades que más veces aparece como centro de estudios de las
# personas registradas. Mostrar universidad y el número de veces que aparece
#Q7 = db.Personas.aggregate([{$unwind:"$estudios"}, {$group : {_id:"$estudios.universidad",count : {$sum : 1}}}, {$limit:3}])
