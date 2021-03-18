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
    'en' : '''Alright! Here\'s the new #CLOCKWORK_EVENT\n<i>Make sure you have started me on private, else you won't receive the notification</i>\n\n''',
    'es' : '''¡Bien! Acá está el nuevo #CLOCKWORK_EVENT\n<i>Asegúrate de haberme iniciado en privado, de otra forma no recibirás notificaciones</i>\n\n''',
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

<b>/new_event <i>"event text"</i></b> - I'll start a new event, there's only allowed one event at time.
<b>/new_raffle <i>"texto del sorteo" "número de participantes"</i></b> - I\'ll start a raffle.

<b>NOTE</b>: if you want to cancel any of this you can use the <b><i>/cancel_event</i>/b> or <b><i>/cancel_raffle</i>/b>''',
#With the command /language you\'ll be able to change my language''',
  'es' : '''Acá un poco de ayuda

<b>/new_event <i>"texto del evento"</i></b> - Iniciaré un evento, solo se permite un evento por grupo a la vez.
<b>/new_raffle <i>"texto del sorteo" "número de participantes"</i></b> - Iniciaré un sorteo.

<b>NOTA</b>: si quieres cancelar alguno de estos puedes usar el comando <b><i>/cancel_event</i></b> o <b><i>/cancel_raffle</i></b>'''
#Con el comando /language podrás cambiar mi idioma'''
}

RAFFLE = {
    'en' : '''\n#CLOCKWORK_RAFFLE Press the button below to participate!''',
    'es' : '''\n#CLOCKWORK_RAFFLE ¡Presiona el botón de abajo para participar!'''
}

NOTIFICATION = {
    'en' : '''There is a <b>new</b> participant on the raffle, we have now: ''',
    'es' : '''Hay un <b>nuevo</b> participante en el sorteo, tenemos ahora: '''
}