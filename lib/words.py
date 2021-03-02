# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:30:32 2021
"""

GREETING = {
    'en' : '''Hi! Im Clockwork Fox
I\'m here to greet every new member of your groups, also I can help you with some events you may want to do with friends.
    
If you want to know how to do some you can use some /help
''',
    'es' : '''¡Hola! Soy Clockwork Fox
Estoy acá para dar la bienvenida a los nuevos miembros de tus grupos, también puedo ayudarte con algunos eventos que quieras hacer con amigos.
    
Si quieres saber como hacer algunas cosas puedes usar /help
'''
    }

EVENT = {
    'en' : '''Alright! Here\'s the new #CLOCKWORK_EVENT\n\n''',
    'es' : '''¡Bien! Acá está el nuevo #CLOCKWORK_EVENT\n\n''',
    'en_btn' : "I\'m in!",
    'es_btn' : "¡Cuenta conmigo!",
    'en_error' : "Sorry, there\'s an event running",
    'es_error' : "Lo siento, ya hay un evento en marcha"
    }

LANG = {
    'en' : "Alright, how sould I speak?",
    'es' : "Bien, ¿cómo debería hablar?"
}

HELP = {
  'en' : '''Here\'s some help
By using the command /new_event followed by the text of the event we start a new event, there\'s only allowed an event once at the time.''',
#With the command /language you\'ll be able to change my language''',
  'es' : '''Acá un poco de ayuda
El comando **/new_event** seguido del texto del evento comezamos un nuevo evento, solo se permite un evento a la vez.
Con <b>/raffle</b> seguido de un texto comenzará un evento de sorteo, define un número de lugares para ganar un premio poniendo un número al final, en caso de omitirlo asumiré que habrán 3 lugares ganadores, por ejemplo:
<b>/raffle Nuevo sorteo 3</b>'''
#Con el comando /language podrás cambiar mi idioma'''
}