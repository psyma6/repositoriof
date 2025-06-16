# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user



#####                       FUNCIÓN A MODIFICAR  
# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    
    # debe ejecutar los siguientes pasos:
    
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    #Creamos la variable imagenes crudas, y para completarla llamamos a la funcion getAllImages() que existe en el modulo transport, esta funcion conecta con la API de pokemon
     imagenescrudas = transport.getAllImages()
     #Creamos una lista vacía llamada cards para almacenar la info obtenida
     cards = []
     
     
    # 2) convertir cada img. en una card.
    #Iniciaremos este bucle for y creamos la variable crudo para iterar sobre cada imagen en el listado y cada una de las imagenes se guarda temporalmente en esta variable.
     for crudo in imagenescrudas:
         
         #Creamos la variable card donde usaremos la funcion from requestintocard() card = translator.fromRequestIntoCard() del archivo translator para conventir crudo de Json a card
         card = translator.fromRequestIntoCard(crudo)
         
    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
         cards.append(card)
         #Con lo cual se agregan al listado cards
         




# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
       
        if name.lower() in card.name.lower(): #Para hacer que el nombre escrito en el buscador coincida con el nombre del pokemon los colocamos a ambos en minusculas (con lower)
                                              # Y verificamos  si name esta en card name
            filtered_cards.append(card)       
            #Si el nombre coincide, agrega esa card a la lista filtered cards.
    return filtered_cards




# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
        filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)