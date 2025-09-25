#!/usr/bin/env python3
"""
🙏 Jotica Bible - Simulador Avanzado
Versión que funciona sin modelo entrenado, incluyendo apologética cristiana
con fundamentos históricos sólidos para responder a ateos y escépticos
"""

import re
import random
import json
from pathlib import Path

class JoticaApologetica:
    def __init__(self):
        """Inicializar Jotica con respuestas bíblicas y apologéticas"""
        
        # Cargar dataset apologético si existe
        self.respuestas_apologeticas = self.cargar_dataset_apologetico()
        
        self.respuestas_biblicas = {
            # Patrones apologéticos y de objeciones
            r'jesus no exist|jesus es mito|jesus nunca exist|mito de jesus': [
                "Comprendo tu inquietud, y es una pregunta legítima que merece una respuesta fundamentada. La evidencia histórica sobre la existencia de Jesús es abrumadora, incluso entre historiadores no cristianos.\n\nTenemos fuentes históricas no cristianas: Flavio Josefo menciona a Jesús dos veces, Tácito escribe sobre 'Cristo', Plinio el Joven describe las prácticas cristianas. Los manuscritos del Nuevo Testamento son los más numerosos de la antigüedad - más de 5,800 manuscritos griegos.\n\nIncluso historiadores ateos como Bart Ehrman afirma: 'Jesús existió, y los eruditos serios están de acuerdo en esto'. ¿Te gustaría profundizar en alguna evidencia específica?"
            ],
            
            r'biblia no es confiable|biblia escrita despues|manuscritos biblicos': [
                "La evidencia textual de la Biblia es extraordinaria. Los evangelios fueron escritos entre 50-90 d.C., apenas 20-60 años después de los eventos. Tenemos el fragmento P52 de Juan del 125 d.C., solo 25-30 años después de ser escrito.\n\nLos Rollos del Mar Muerto muestran que el texto de Isaías es 95% idéntico después de 1,000 años. Los eruditos como F.F. Bruce confirman que tenemos mejor evidencia manuscrita para el NT que para cualquier libro de la antigüedad.\n\n¿Qué aspecto específico de la confiabilidad histórica te interesa más?"
            ],
            
            r'no hay evidencia arqueologica|arqueologia biblia': [
                "La arqueología ha confirmado extraordinariamente la exactitud bíblica. La Estela de Merneptah menciona 'Israel' en 1230 a.C., la Inscripción de Pilato confirma su título exacto, los osarios de Caifás confirman al sumo sacerdote que juzgó a Jesús.\n\nLa piscina de Betesda fue descubierta exactamente como Juan la describe. William Albright declaró: 'La arqueología ha confirmado la sustancial historicidad de la tradición del Antiguo Testamento.' ¿Te interesa algún descubrimiento específico?"
            ],
            
            r'contradicciones biblia|errores biblia': [
                "Las aparentes contradicciones se resuelven con estudio del contexto y cultura antigua. Los evangelios son como cuatro testigos - cada uno ve desde su perspectiva. Las genealogías de Jesús siguen líneas diferentes: una legal (José), otra de sangre (María).\n\nGleason Archer, tras 60 años de estudio: 'No he encontrado una sola contradicción genuina que no pueda resolverse.' John Haley documentó más de 900 'contradicciones' aparentes con soluciones razonables. ¿Hay alguna contradicción específica que te inquieta?"
            ],
            
            r'cristianismo copia religion|mitra|horus|religion pagana': [
                "Esta objeción no resiste el escrutinio académico. Muchas supuestas 'fuentes' fueron escritas DESPUÉS del cristianismo. El mitraísmo alcanzó prominencia en el siglo II d.C., DESPUÉS del cristianismo.\n\nJonathan Z. Smith (Universidad de Chicago): 'Los paralelos han sido enormemente exagerados.' El cristianismo surgió del judaísmo con conceptos únicos como resurrección corporal y monoteísmo ético - ajenos a religiones mistéricas. ¿Te gustaría examinar alguna religión específica?"
            ],
            
            r'ciencia refuta dios|ciencia vs religion|evolucion': [
                "Muchos científicos prominentes son creyentes: Francis Collins (Genoma Humano), John Polkinghorne (físico cuántico). El ajuste fino del universo sugiere diseño - Paul Davies: 'La impresión de diseño es abrumadora.'\n\nEl Big Bang concuerda con 'En el principio creó Dios'. La ciencia describe el 'cómo', no necesariamente el 'por qué' último. Einstein: 'La ciencia sin religión es coja, la religión sin ciencia es ciega.' ¿Hay algún aspecto científico específico que te genera dudas?"
            ],
            
            r'problema del mal|sufrimiento|dios bueno pero sufrimient': [
                "Es la pregunta más profunda. Jesús mismo lloró ante el dolor (Juan 11:35). Consideraciones importantes: el libre albedrío requiere libertad para elegir el mal; un mundo con leyes consistentes permite ciencia pero también terremotos.\n\nEn Cristo, Dios entró en nuestro dolor. Corrie ten Boom: 'No hay abismo tan profundo que el amor de Dios no sea más profundo.' Apocalipsis 21:4 promete un día sin dolor. ¿Has experimentado sufrimiento que te hace cuestionar a Dios?"
            ],
            
            r'muchas religiones|solo cristianismo verdader': [
                "La existencia de billetes falsos no niega billetes auténticos. El cristianismo es único: históricamente verificable, salvación por gracia (no obras), Dios que desciende al humano (no humano que asciende a dios).\n\nTodas las culturas buscan lo trascendente, sugiriendo fuimos creados con 'vacío con forma de Dios' (Pascal). Cristo es único: 'el camino, la verdad y la vida' (Juan 14:6). ¿Has explorado otras religiones?"
            ],
            
            r'cristianos hipocrita|daño christian|cruzadas|inquisicion': [
                "Reconozco honestamente las fallas históricas: Cruzadas, Inquisición, abusos. Debemos distinguir entre Jesús (perfecto) y seguidores (imperfectos). Jesús denunció la hipocresía religiosa más duramente que nadie.\n\nPero cristianos también abolieron esclavitud, fundaron hospitales/universidades, lucharon por derechos civiles. La hipocresía confirma estándares morales. Gandhi: 'Me gusta tu Cristo, no me gustan tus cristianos.' ¿Has sido lastimado por cristianos hipócritas?"
            ],
            
            r'resurreccion imposible|muertos no resucitan': [
                "La pregunta no es si es 'normal', sino si ocurrió. Hechos aceptados por historiadores: Jesús murió crucificado, tumba vacía, discípulos afirmaron verlo resucitado, transformación radical de cobardes a valientes.\n\nTeoríás alternativas fallan: ¿discípulos cobardes vencieron guardias romanos? ¿Jesús medio muerto convenció que venció la muerte? N.T. Wright: 'La resurrección es la mejor explicación histórica disponible.' ¿Qué teoría alternativa te parece más plausible?"
            ],

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
            ]
        }
        
        self.respuestas_generales = [
            "Esa es una pregunta muy profunda que merece una respuesta bíblica fundamentada. Las Escrituras tienen mucha sabiduría sobre este tema, y la historia confirma su veracidad. ¿Te gustaría que exploremos juntos qué dice la Palabra de Dios al respecto?",
            
            "Me alegra que busques respuestas sólidas. Proverbios 3:5-6 nos anima a confiar en Jehová de todo corazón. La arqueología y la historia han confirmado la confiabilidad de las Escrituras una y otra vez. ¿Has llevado esta inquietud a Dios en oración?",
            
            "Es hermoso ver tu corazón buscador de la verdad. Jesús dijo en Juan 8:32: 'Conoceréis la verdad, y la verdad os hará libres.' Dios honra a quienes buscan Sus caminos con sinceridad y mente abierta."
        ]
        
        self.saludos = [
            "¡Hola! Soy Jotica, tu compañera en la búsqueda de la verdad. Me alegra poder conversar contigo sobre la fe cristiana con fundamentos históricos sólidos.",
            "¡Bendiciones! Es un gozo poder explorar contigo las evidencias históricas y arqueológicas que confirman la veracidad de las Escrituras.",
            "¡Paz y gracia! Estoy aquí para examinar juntos las evidencias que respaldan la fe cristiana con rigor intelectual."
        ]

    def cargar_dataset_apologetico(self):
        """Cargar dataset apologético desde archivo JSON si existe"""
        try:
            path = Path("data/processed/jotica_apologetica.json")
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"📚 Dataset apologético cargado: {len(data)} respuestas especializadas")
                    return data
        except Exception as e:
            print(f"⚠️ No se pudo cargar dataset apologético: {e}")
        return []

    def buscar_respuesta_especializada(self, mensaje: str) -> str:
        """Buscar respuesta especializada en el dataset apologético"""
        if not self.respuestas_apologeticas:
            return None
            
        mensaje_lower = mensaje.lower()
        
        # Palabras clave apologéticas
        keywords_map = {
            'existencia de jesus': ['jesus no exist', 'mito', 'nunca exist'],
            'confiabilidad biblia': ['biblia', 'manuscritos', 'confiable', 'escrita'],
            'arqueologia': ['arqueolog', 'evidencia', 'excavacion'],
            'contradicciones': ['contradicci', 'error', 'inconsisten'],
            'religiones paganas': ['copia', 'mitra', 'horus', 'pagana'],
            'ciencia': ['ciencia', 'evolucion', 'big bang', 'refuta'],
            'problema mal': ['sufrimiento', 'mal', 'dolor', 'bueno'],
            'muchas religiones': ['religiones', 'verdadero', 'solo cristian'],
            'cristianos hipocritas': ['hipocrita', 'daño', 'cruzadas', 'malo'],
            'resurreccion': ['resurreccion', 'muertos', 'imposible']
        }
        
        for item in self.respuestas_apologeticas:
            instruction_lower = item['instruction'].lower()
            for keyword_list in keywords_map.values():
                if any(keyword in mensaje_lower for keyword in keyword_list):
                    if any(keyword in instruction_lower for keyword in keyword_list):
                        return item['output']
        
        return None
        
    def detectar_patron(self, mensaje: str) -> str:
        """Detectar patrones en el mensaje del usuario con mayor precisión"""
        mensaje_lower = mensaje.lower()
        
        # Primero buscar respuesta especializada apologética
        respuesta_especializada = self.buscar_respuesta_especializada(mensaje)
        if respuesta_especializada:
            return respuesta_especializada
        
        # Limpiar signos de puntuación para mejor detección
        mensaje_clean = re.sub(r'[¿?¡!.,;:]', '', mensaje_lower)
        
        # Buscar patrones específicos (más específicos tienen prioridad)
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
        """Generar respuesta apropiada con fundamento apologético"""
        if self.es_saludo(mensaje):
            return random.choice(self.saludos)
        
        return self.detectar_patron(mensaje)
    
    def conversacion_interactiva(self):
        """Modo conversación interactiva con apologética"""
        print("🙏 ¡Bienvenido! Soy Jotica, tu asistente bíblico con fundamentos históricos.")
        print("💭 Puedo responder preguntas sobre fe, objeciones ateas, evidencias arqueológicas...")
        print("🔍 Tengo respuestas fundamentadas para escépticos y buscadores de la verdad.")
        print("✨ Escribe 'salir' para terminar.\n")
        
        while True:
            try:
                mensaje = input("👤 Tú: ").strip()
                
                if not mensaje:
                    continue
                    
                if mensaje.lower() in ['salir', 'exit', 'quit', 'adiós', 'adios']:
                    print("🙏 ¡Que Dios te bendiga grandemente! Espero que nuestra conversación te haya dado fundamentos sólidos para tu fe.")
                    break
                
                print("🤔 Jotica está analizando las evidencias...")
                respuesta = self.responder(mensaje)
                print(f"🙏 Jotica: {respuesta}\n")
                
            except KeyboardInterrupt:
                print("\n\n🙏 ¡Que tengas un día lleno de bendiciones y certeza en la verdad!")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                print("💡 Por favor, inténtalo de nuevo.")

def demo_jotica_apologetica():
    """Demostración de Jotica con capacidades apologéticas"""
    print("🙏 === Demo de Jotica Bible Apologética ===")
    print("🤖 Versión: Simulador con Fundamentos Históricos")
    print("🔍 Especializada en responder objeciones ateas")
    print("=" * 50)
    print()
    
    jotica = JoticaApologetica()
    
    preguntas_demo = [
        "Hola Jotica, soy escéptico sobre el cristianismo",
        "Un amigo ateo dice que Jesús nunca existió",
        "¿Hay evidencia arqueológica que respalde la Biblia?",
        "Me dicen que hay muchas contradicciones en la Biblia",
        "¿No es el cristianismo solo una copia de religiones paganas?",
        "Si Dios es bueno, ¿por qué permite tanto sufrimiento?",
        "¿Cómo puedo saber que la resurrección realmente ocurrió?"
    ]
    
    for i, pregunta in enumerate(preguntas_demo, 1):
        print(f"📝 Ejemplo {i}:")
        print(f"👤 Escéptico: {pregunta}")
        respuesta = jotica.responder(pregunta)
        # Mostrar solo los primeros 300 caracteres para el demo
        respuesta_corta = respuesta[:300] + "..." if len(respuesta) > 300 else respuesta
        print(f"🙏 Jotica: {respuesta_corta}")
        print("-" * 70)
        print()

if __name__ == "__main__":
    print("🙏 Jotica Bible - Simulador Apologético")
    print("=" * 50)
    print("ℹ️  Versión especializada en apologética cristiana")
    print("🔍 Respuestas fundamentadas para escépticos y ateos")
    print("📚 Incluye evidencias históricas y arqueológicas")
    print()
    
    while True:
        print("Opciones:")
        print("1. 🎮 Ver demostración apologética")
        print("2. 💬 Conversación interactiva")
        print("3. 🚪 Salir")
        print()
        
        try:
            opcion = input("Elige una opción (1-3): ").strip()
            
            if opcion == '1':
                demo_jotica_apologetica()
            elif opcion == '2':
                jotica = JoticaApologetica()
                jotica.conversacion_interactiva()
            elif opcion == '3':
                print("🙏 ¡Que Dios te bendiga! La verdad siempre prevalece.")
                break
            else:
                print("❌ Opción no válida. Por favor, elige 1, 2 o 3.")
                
        except KeyboardInterrupt:
            print("\n\n🙏 ¡Bendiciones! Que la verdad de Cristo sea tu fundamento.")
            break