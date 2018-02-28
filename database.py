# -*- coding: utf-8 -*-
import logging

from logging import getLogger
from pprint import pprint
from pymongo import MongoClient


logger = logging.getLogger(__name__)


class AmandaDB():
    """
    Clase base con la conexión a Mongosync
    """

    def __init__(self, collection: str):
        self.client = MongoClient(
            "mongodb://amanda:4m4nd4@clusteramanda-shard-00-00-ja603.mongodb.net:27017,clusteramanda-shard-00-01-ja603.mongodb.net:27017,clusteramanda-shard-00-02-ja603.mongodb.net:27017/test?ssl=true&replicaSet=ClusterAmanda-shard-0&authSource=admin")
        self.collection = self.client.test[str(collection)]

    def remove_all(self):
        """
        Limpia todas las conversaciones activas en la BD
        """
        self.collection.update(
            {},
            {'$set': {'context': None, 'workspace': None}})
        return

    def list(self, phone=None):
        """
        Lista todas las conversaciones
        """
        for conv in self.collection.find({}):
            pprint(conv)
        return

    def update(self, query: dict, changes: dict):
        """
        Actualiza información en la BD
        """
        self.collection.update(query, changes)
        # TODO: detectar cuando no es posible realizar el update
        return True


class AmandaConversation(AmandaDB):
    """
    BD de conversaciones activas
    """

    def __init__(self):
        AmandaDB.__init__(self, 'conversations2')

    def get(self, phone: str):
        """
        Obtiene una conversación de acuerdo a un número

        Salida: dict
        ----------
        doc: es la conversación
        new: indica si se creó la conversación o ya habia una anterior
        """
        logger.info('hola estoy en get de la database.py')

        create = False
        doc = self.collection.find_one({'phone': str(phone)})
        if doc is None:
            create = True
            self.collection.insert_one({
                'phone': str(phone),
                'workspace': None,
                'context': None
            })
            doc = self.collection.find_one({'phone': str(phone)})

        return {'doc': doc, 'new': create}

    def set(self, phone: str, changes: dict):
        """
        Actualiza la información de una conversación

        phone: número de la conversación
        changes: cambios para actualizar
        """
        return self.update(
            {'phone': str(phone)},
            {'$set': changes})

    def push(self, phone: str, add: object):
        """
        Agrega un valor a un array en un documento

        phone: número de la conversación
        add: elemento para agregar a la lista
        """
        return self.update(
            {'phone': str(phone)},
            {'$push': add})

    def start(self, phone: str, workspace: str, usuario: str,
              fecha_compra: str, fecha_entrega: str, productos: list, miniticket: bool):
        """
        Inicia una conversación
        """
        context = self.get(phone)['doc']['context']
        if context is not None:
            # si hay un contexto, guardarlo en el historial
            history = AmandaConversationHistory()
            history.push(phone, {'context': context})

        changes = {
            'workspace': str(workspace),
            'context': {
                'username': usuario,
                'fecha_compra': fecha_compra,
                'fecha_entrega': fecha_entrega,
                'productos': productos,
                'miniticket': miniticket
            },
            'contactar': 0
        }
        return self.set(phone, changes)

    def finish(self, phone: str):
        """
        Termina una conversación, vuelve a los valores por defecto
        """
        context = self.get(phone)['doc']['context']
        if context is not None:
            # si hay un contexto, guardarlo en el historial
            history = AmandaConversationHistory()
            history.push(phone, {'context': context})

        changes = {
            'workspace': None,
            'context': None,
            'contactar': 0
        }
        return self.set(phone, changes)

    def pause(self, phone: str, seconds: int):
        """
        Cambia el tiempo en que una conversación está en pausa
        """
        # TODO: esto se puede cambiar por una tarea programada u similar, para no tener hilos activos con sleep
        changes = {
            'contactar': seconds
        }
        return self.set(phone, changes)


class AmandaConversationHistory(AmandaDB):
    """
    BD de conversaciones pasadas
    """

    def __init__(self):
        AmandaDB.__init__(self, 'history')

    def get(self, phone: str):
        """
        Obtiene las conversaciones históricas de un número

        phone: número de contacto
        """
        doc = self.collection.find_one({'phone': str(phone)})
        if doc is None:
            self.collection.insert_one({
                'phone': str(phone),
                'context': []
            })
            doc = self.collection.find_one({'phone': str(phone)})

        return doc

    def set(self, phone: str, changes: dict):
        """
        Actualiza la información de una conversación

        phone: número de la conversación
        changes: cambios para actualizar
        """
        return self.update(
            {'phone': str(phone)},
            {'$set': changes})

    def push(self, phone: str, add: object):
        """
        Agrega un valor a un array en un documento

        phone: número de la conversación
        add: elemento para agregar a la lista
        """
        # obtener el historial, porque si no existe lo va a crear
        self.get(phone)
        return self.update(
            {'phone': str(phone)},
            {'$push': add})


class AmandaMessages(AmandaDB):
    """
    BD de mensajes
    """

    def __init__(self):
        AmandaDB.__init__(self, 'messages')

    def get(self, phone: str):
        """
        Obtiene una lista de mensajes de acuerdo a un número
        """
        messages = self.collection.find_one({'phone': str(phone)})

        return messages

    def push(self, phone: str, add: object):
        """
        Agrega un mensaje

        phone: número de la conversación
        add: elemento para agregar a la lista
        """
        doc = self.collection.find_one({'phone': str(phone)})
        if doc is None:
            self.collection.insert_one({
                'phone': str(phone),
                'messages': []
            })
        return self.update(
            {'phone': str(phone)},
            {'$push': add})

    def list(self, phone: str = None):
        """
        Lista todas las conversaciones
        """
        for messsage in self.collection.find({'phone': str(phone)}):
            pprint(messsage)
        return
