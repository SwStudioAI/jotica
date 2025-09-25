#!/usr/bin/env python3
"""
🙏 Jotica Bible - Simulador Básico
Versión que funciona sin modelo entrenado, usando respuestas bíblicas predefinidas
Incluye apologética cristiana con fundamentos históricos
"""

import re
import random
import json
from pathlib import Path

class JoticaBasica:n3
"""
🙏 Jotica Bible - Simulador Básico
Versión que funciona sin modelo entrenado, usando respuestas bíblicas predefinidas
Incluye apologética cristiana con fundamentos históricos
"""

import re
import random
import json
from pathlib import Pathin/env python3
"""
🙏 Jotica Bible - Simulador Básico
Versión que funciona sin modelo entrenado, usando respuestas predefinidas bíblicas
"""

import re
import random

class JoticaBasica:
    def __init__(self):
        """Inicializar Jotica con respuestas bíblicas predefinidas"""
        self.respuestas_biblicas = {
            # Patrones sobre personajes bíblicos
            r'quien es moises|moises|moisés': [
                "Moisés fue uno de los grandes líderes de Israel, escogido por Dios para liberar a Su pueblo de la esclavitud en Egipto. En Éxodo 3, Dios le habló desde una zarza ardiente y lo llamó para esta gran misión. Moisés recibió los Diez Mandamientos en el Monte Sinaí y guió al pueblo por 40 años en el desierto. Fue profeta, legislador y libertador. ¿Te gustaría conocer más sobre algún episodio específico de su vida?",
                
                "Moisés es considerado el gran legislador de Israel. Dios lo usó para dar la Ley al pueblo hebreo. En Deuteronomio 34:10 dice: 'Nunca más se levantó profeta en Israel como Moisés, a quien haya conocido Jehová cara a cara.' Su vida nos enseña sobre la obediencia a Dios aún cuando nos sintamos inadecuados. ¿Hay alguna área donde sientes que Dios te está llamando pero te sientes insuficiente?"
            ],
            
            r'quien es jesus|jesus|jesús|cristo|jesucristo': [
                "Jesús es el Hijo de Dios, nuestro Salvador y Redentor. Juan 1:1 y 14 nos dice que 'En el principio era el Verbo... y aquel Verbo fue hecho carne.' Jesús es completamente Dios y completamente hombre, quien vino a la tierra para salvarnos de nuestros pecados. En Juan 14:6 Él mismo dice: 'Yo soy el camino, la verdad y la vida; nadie viene al Padre sino por mí.' ¿Has experimentado personalmente el amor y la salvación que Jesús ofrece?",
                
                "Jesús de Nazaret es el centro de la fe cristiana. Nació de la virgen María, vivió una vida sin pecado, murió en la cruz por nuestros pecados y resucitó al tercer día. Filipenses 2:6-11 describe cómo, siendo Dios, se humilló hasta la muerte de cruz para salvarnos. Su nombre significa 'Jehová salva'. ¿Qué significa Jesús para ti en tu vida personal?",
                
                "Cristo Jesús es nuestro Emanuel, 'Dios con nosotros' (Mateo 1:23). Él vino no solo para darnos vida eterna, sino vida abundante (Juan 10:10). Es el Buen Pastor que da Su vida por las ovejas, el Pan de Vida, la Luz del mundo. En Hebreos 4:15 vemos que puede compadecerse de nuestras debilidades porque fue tentado en todo según nuestra semejanza, pero sin pecado. ¿Te consuela saber que Jesús comprende perfectamente tus luchas?"
            ],
            
            r'quien es david|david|rey david': [
                "David fue el segundo rey de Israel y es conocido como 'un varón conforme al corazón de Dios' (1 Samuel 13:14). Comenzó como un joven pastor que venció al gigante Goliat con fe en Dios. Escribió muchos de los Salmos que leemos hoy. Su vida nos enseña sobre la adoración, el arrepentimiento genuino (como en el Salmo 51) y la confianza en Dios en tiempos difíciles. ¿Conoces algún Salmo de David que te haya consolado?",
                
                "El rey David es uno de los personajes más humanos de la Biblia. Tuvo grandes victorias pero también cometió errores serios. Su historia nos enseña que Dios puede usar personas imperfectas para Sus propósitos. En el Salmo 23, David nos da una de las declaraciones de fe más hermosas: 'Jehová es mi pastor; nada me faltará.' ¿Hay alguna situación donde necesitas recordar que Dios es tu pastor?"
            ],
            
            r'quien es maria|virgen maria|madre de jesus': [
                "María fue escogida por Dios para ser la madre de Jesús. Su respuesta al ángel Gabriel en Lucas 1:38 muestra su corazón humilde: 'He aquí la sierva del Señor; hágase conmigo conforme a tu palabra.' Su cántico en Lucas 1:46-55 (el Magnificat) revela su fe profunda y conocimiento de las Escrituras. María nos enseña sobre la obediencia a Dios aún cuando no entendamos completamente Sus planes. ¿Te identificas con la disposición de María para confiar en Dios?",
                
                "La bendita María, madre de nuestro Señor, es un ejemplo de fe y entrega. Acompañó a Jesús hasta la cruz y fue testigo de Su resurrección. En Juan 19:26-27, Jesús la encomendó al cuidado del apóstol Juan. Su vida nos muestra que Dios escoge a personas humildes para hacer cosas extraordinarias. ¿Cómo puedes cultivar un corazón humilde como el de María?"
            ],
            
            r'quien es pablo|apostol pablo|san pablo': [
                "Pablo, antes llamado Saulo, fue transformado de perseguidor de cristianos a uno de los más grandes apóstoles. En el camino a Damasco (Hechos 9), Jesús se le apareció y cambió su vida completamente. Escribió la mayoría de las cartas del Nuevo Testamento y plantó iglesias por todo el mundo conocido. Su vida muestra el poder transformador de Cristo. En 1 Timoteo 1:15 se llama a sí mismo 'el primero' de los pecadores que Cristo vino a salvar. ¿Te anima saber que Dios puede transformar cualquier vida?",
                
                "El apóstol Pablo nos enseña sobre la gracia de Dios y la vida cristiana práctica. Sus cartas están llenas de sabiduría sobre cómo vivir para Cristo. En 2 Corintios 12:9 nos relata cómo Dios le dijo: 'Bástate mi gracia; porque mi poder se perfecciona en la debilidad.' Pablo aprendió a confiar en la suficiencia de Cristo en todas las circunstancias. ¿Hay alguna área de debilidad donde necesitas experimentar la gracia de Dios?"
            ],
            
            # Patrones sobre amor
            r'amor|amar|amo': [
                "El amor es el tema central de la Biblia. En 1 Corintios 13:4-7, Pablo nos enseña que el amor es sufrido, es benigno; el amor no tiene envidia, el amor no es jactancioso, no se envanece. ¿Has experimentado este tipo de amor incondicional?",
                
                "Jesús dijo en Juan 13:34-35: 'Un mandamiento nuevo os doy: Que os améis unos a otros; como yo os he amado.' El amor cristiano no es solo un sentimiento, sino una decisión de servir y bendecir a otros. ¿Cómo puedes mostrar amor hoy?",
                
                "1 Juan 4:8 nos recuerda que 'Dios es amor'. Todo amor verdadero viene de Él. Cuando amamos a otros, reflejamos Su carácter divino. ¿Te has preguntado cómo Dios te ama incondicionalmente?"
            ],
            
            # Patrones sobre paz
            r'paz|tranquil|calm|ansie|preocup|estres': [
                "La paz que Jesús da es diferente a la paz del mundo. En Juan 14:27 dice: 'La paz os dejo, mi paz os doy; yo no os la doy como el mundo la da.' Su paz permanece aún en medio de las tormentas. ¿Has experimentado esta paz sobrenatural?",
                
                "Filipenses 4:6-7 es un versículo hermoso: 'Por nada estéis afanosos, sino sean conocidas vuestras peticiones delante de Dios en toda oración... Y la paz de Dios... guardará vuestros corazones y pensamientos.' ¿Has probado entregar tus preocupaciones a Dios en oración?",
                
                "Isaías 26:3 promete: 'Tú guardarás en completa paz a aquel cuyo pensamiento en ti persevera.' La paz viene de mantener nuestra mente fija en Dios. ¿Qué pensamientos ocupan más tiempo en tu mente durante el día?"
            ],
            
            # Patrones sobre oración
            r'orar|oracion|rezo|pleg': [
                "La oración es simplemente hablar con Dios como con un amigo. Jesús nos enseñó el Padre Nuestro en Mateo 6:9-13 como modelo. No necesitas palabras perfectas, solo un corazón sincero. ¿Te resulta difícil encontrar palabras para orar?",
                
                "1 Tesalonicenses 5:17 nos anima a 'orar sin cesar'. Esto no significa estar arrodillados todo el día, sino mantener una actitud de comunión constante con Dios. ¿Has probado hacer oraciones cortas durante el día?",
                
                "Santiago 5:16 dice que 'la oración eficaz del justo puede mucho'. Dios escucha nuestras oraciones y actúa. A veces Su respuesta es 'sí', a veces 'no', y a veces 'espera'. ¿Has visto respuestas a tus oraciones?"
            ],
            
            # Patrones sobre perdón
            r'perdon|perdona|rencor|vengan|odio': [
                "El perdón es uno de los aspectos más liberadores del cristianismo. Efesios 4:32 nos dice: 'Sed benignos unos con otros, misericordiosos, perdonándoos unos a otros, como Dios también os perdonó.' Perdonar no significa que el dolor no existió, sino que elegimos liberar la amargura. ¿Hay alguien a quien necesitas perdonar?",
                
                "Mateo 18:21-22 cuenta cuando Pedro preguntó si debía perdonar siete veces, y Jesús respondió 'setenta veces siete'. El perdón no tiene límites cuando seguimos el ejemplo de Cristo. ¿Te resulta difícil perdonar a alguien en particular?",
                
                "El perdón es un regalo que nos damos a nosotros mismos. Como dijo Nelson Mandela: 'El resentimiento es como beber veneno esperando que muera el otro.' Dios quiere liberarte de esa carga. ¿Estarías dispuesto a pedirle ayuda para perdonar?"
            ],
            
            # Patrones sobre propósito
            r'proposito|sentido|para que|por que viv': [
                "Jeremías 29:11 es un versículo precioso: 'Porque yo sé los pensamientos que tengo acerca de vosotros, dice Jehová, pensamientos de paz, y no de mal, para daros el fin que esperáis.' Dios tiene un propósito único para tu vida. ¿Has buscado Su dirección en oración?",
                
                "Efesios 2:10 dice que somos 'hechura suya, creados en Cristo Jesús para buenas obras, las cuales Dios preparó de antemano.' Fuiste creado con un propósito divino específico. ¿Qué talentos y pasiones te ha dado Dios que podrían ser parte de Su plan?",
                
                "El propósito más grande es conocer y glorificar a Dios. En Mateo 22:37-39, Jesús resumió todo en dos mandamientos: amar a Dios y amar al prójimo. Todo lo demás fluye de ahí. ¿Cómo puedes vivir estos mandamientos hoy?"
            ],
            
            # Patrones sobre esperanza
            r'esperanz|futuro|mañana|desesper': [
                "Romanos 15:13 dice: 'Y el Dios de esperanza os llene de todo gozo y paz en el creer, para que abundéis en esperanza por el poder del Espíritu Santo.' La esperanza cristiana no es solo optimismo; es confianza en las promesas de Dios. ¿Qué promesa de Dios necesitas recordar hoy?",
                
                "Incluso en los momentos más oscuros, tenemos esperanza. 2 Corintios 4:17-18 nos recuerda que nuestras aflicciones son 'leve tribulación momentánea' comparada con la gloria eterna que nos espera. ¿Te ayuda pensar en la perspectiva eterna cuando enfrentas dificultades?",
                
                "Salmos 42:5 pregunta: '¿Por qué te abates, oh alma mía, y te turbas dentro de mí? Espera en Dios; porque aún he de alabarle.' A veces necesitamos hablarnos a nosotros mismos y recordar las razones para tener esperanza. ¿Qué razones tienes para esperar en Dios?"
            ],
            
            # Patrones sobre conceptos bíblicos
            r'que es la biblia|biblia|escritura|palabra de dios': [
                "La Biblia es la Palabra inspirada de Dios. 2 Timoteo 3:16 nos dice que 'Toda la Escritura es inspirada por Dios, y útil para enseñar, para redargüir, para corregir, para instruir en justicia.' Es nuestra guía para conocer a Dios y vivir según Su voluntad. ¿Tienes el hábito de leer la Biblia regularmente?",
                
                "La Biblia contiene 66 libros escritos por unos 40 autores a lo largo de aproximadamente 1,500 años, pero tiene un solo tema central: el plan de salvación de Dios para la humanidad. Hebreos 4:12 dice que es 'viva y eficaz, y más cortante que toda espada de dos filos.' ¿Has experimentado cómo la Palabra de Dios habla a tu corazón?"
            ],
            
            r'que es la fe|fe|creer|creencia': [
                "Hebreos 11:1 define la fe como 'la certeza de lo que se espera, la convicción de lo que no se ve.' La fe no es un salto ciego, sino confianza basada en el carácter y las promesas de Dios. En Romanos 10:17 aprendemos que 'la fe es por el oír, y el oír, por la palabra de Dios.' ¿Cómo puedes fortalecer tu fe hoy?",
                
                "La fe es fundamental en la vida cristiana. Efesios 2:8-9 nos enseña que somos salvos 'por gracia... por medio de la fe.' Pero la fe también es práctica: confiamos en Dios día a día para nuestras necesidades. Mateo 17:20 habla del poder de la fe del tamaño de un grano de mostaza. ¿En qué área necesitas ejercer más fe?"
            ],
            
            r'que es la salvacion|salvacion|salvado|nacer de nuevo': [
                "La salvación es el regalo gratuito de Dios por medio de la fe en Jesucristo. Efesios 2:8-9 dice: 'Por gracia sois salvos por medio de la fe... no por obras.' Juan 3:16 nos muestra el corazón de Dios: 'De tal manera amó Dios al mundo, que ha dado a su Hijo unigénito, para que todo aquel que en él cree, no se pierda, mas tenga vida eterna.' ¿Has recibido personalmente este regalo de vida eterna?",
                
                "Nacer de nuevo significa tener una nueva vida en Cristo. 2 Corintios 5:17 dice: 'Si alguno está en Cristo, nueva criatura es; las cosas viejas pasaron; he aquí todas son hechas nuevas.' La salvación no es solo un boleto al cielo, sino una transformación del corazón aquí y ahora. ¿Sientes que necesitas esta renovación en tu vida?"
            ]
        }
        
        self.respuestas_generales = [
            "Esa es una pregunta muy profunda. La Biblia tiene mucha sabiduría sobre este tema. ¿Te gustaría que exploremos juntos qué dice la Palabra de Dios al respecto?",
            
            "Me alegra que busques perspectiva bíblica. Proverbios 3:5-6 nos anima a confiar en Jehová de todo corazón y no apoyarnos en nuestra propia prudencia. ¿Has llevado esta inquietud a Dios en oración?",
            
            "Es hermoso ver tu corazón buscador. Jesús dijo en Mateo 7:7: 'Pedid, y se os dará; buscad, y hallaréis; llamad, y se os abrirá.' Dios honra a quienes buscan Sus caminos sinceramente."
        ]
        
        self.saludos = [
            "¡Hola! Soy Jotica, tu compañera de fe. Me alegra poder conversar contigo sobre la Palabra de Dios.",
            "¡Bendiciones! Es un gozo poder compartir la sabiduría bíblica contigo.",
            "¡Paz y gracia! Estoy aquí para explorar juntos lo que dice la Biblia."
        ]
        
    def detectar_patron(self, mensaje: str) -> str:
        """Detectar patrones en el mensaje del usuario con mayor precisión"""
        mensaje_lower = mensaje.lower()
        
        # Limpiar signos de puntuación para mejor detección
        mensaje_clean = re.sub(r'[¿?¡!.,;:]', '', mensaje_lower)
        
        # Buscar patrones específicos primero (más específicos tienen prioridad)
        for patron, respuestas in self.respuestas_biblicas.items():
            if re.search(patron, mensaje_clean):
                return random.choice(respuestas)
        
        # Si no encuentra patrón específico, dar respuesta general
        return random.choice(self.respuestas_generales)
    
    def es_saludo(self, mensaje: str) -> bool:
        """Detectar si es un saludo"""
        saludos = ['hola', 'buenos', 'buenas', 'hey', 'hi', 'hello', 'bendiciones']
        return any(saludo in mensaje.lower() for saludo in saludos)
    
    def responder(self, mensaje: str) -> str:
        """Generar respuesta apropiada"""
        if self.es_saludo(mensaje):
            return random.choice(self.saludos)
        
        return self.detectar_patron(mensaje)
    
    def conversacion_interactiva(self):
        """Modo conversación interactiva"""
        print("🙏 ¡Bienvenido! Soy Jotica, tu asistente bíblico.")
        print("💬 Puedes preguntarme sobre la Biblia, fe, o inquietudes espirituales.")
        print("✨ Escribe 'salir' para terminar.\n")
        
        while True:
            try:
                mensaje = input("👤 Tú: ").strip()
                
                if not mensaje:
                    continue
                    
                if mensaje.lower() in ['salir', 'exit', 'quit', 'adiós', 'adios']:
                    print("🙏 ¡Que Dios te bendiga grandemente! Espero que nuestra conversación haya sido de bendición.")
                    break
                
                print("🤔 Jotica está reflexionando...")
                respuesta = self.responder(mensaje)
                print(f"🙏 Jotica: {respuesta}\n")
                
            except KeyboardInterrupt:
                print("\n\n🙏 ¡Que tengas un día lleno de bendiciones!")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                print("💡 Por favor, inténtalo de nuevo.")

def demo_jotica():
    """Demostración rápida de Jotica"""
    print("🙏 === Demo de Jotica Bible ===")
    print("🤖 Versión: Simulador Básico (sin IA)")
    print("=" * 40)
    print()
    
    jotica = JoticaBasica()
    
    preguntas_demo = [
        "Hola Jotica, ¿cómo estás?",
        "Me siento muy ansioso por mi futuro",
        "¿Qué dice la Biblia sobre el amor?",
        "No sé cómo perdonar a alguien que me lastimó",
        "¿Para qué estoy en esta vida?",
        "¿Cómo puedo orar mejor?"
    ]
    
    for i, pregunta in enumerate(preguntas_demo, 1):
        print(f"📝 Ejemplo {i}:")
        print(f"👤 Usuario: {pregunta}")
        respuesta = jotica.responder(pregunta)
        print(f"🙏 Jotica: {respuesta}")
        print("-" * 60)
        print()

if __name__ == "__main__":
    print("🙏 Jotica Bible - Simulador Básico")
    print("=" * 50)
    print("ℹ️  Esta versión funciona sin conexión a internet ni modelos de IA")
    print("✨ Usa respuestas bíblicas predefinidas con sabiduría cristiana")
    print()
    
    while True:
        print("Opciones:")
        print("1. 🎮 Ver demostración")
        print("2. 💬 Conversación interactiva")
        print("3. 🚪 Salir")
        print()
        
        try:
            opcion = input("Elige una opción (1-3): ").strip()
            
            if opcion == '1':
                demo_jotica()
            elif opcion == '2':
                jotica = JoticaBasica()
                jotica.conversacion_interactiva()
            elif opcion == '3':
                print("🙏 ¡Que Dios te bendiga! Hasta luego.")
                break
            else:
                print("❌ Opción no válida. Por favor, elige 1, 2 o 3.")
                
        except KeyboardInterrupt:
            print("\n\n🙏 ¡Bendiciones! Que tengas un hermoso día.")
            break