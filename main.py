# ============================================================
# 🌌 COSMIC STAR LAB
# CLASIFICADOR DE ESTRELLAS
# VERSIÓN 2.7 — COSMIC DEEP SPACE
#
# Autor: Jor Watanabe C.
# Python + Kivy
# ============================================================

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import (
    Color,
    Ellipse,
    Line
)
from kivy.uix.screenmanager import (
    ScreenManager,
    Screen,
    FadeTransition
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

from random import uniform
from math import sin, cos, pi


# ============================================================
# CONFIGURACIÓN
# ============================================================

AUTOR = "Jor Watanabe C."
VERSION = "v2.7"

Window.clearcolor = get_color_from_hex(
    "#02030A"
)


# ============================================================
# COLORES
# ============================================================

FONDO = "#02030A"
BLANCO = "#F4F7FF"
GRIS = "#8D9AB8"
CELESTE = "#6EE7FF"
AZUL = "#3CA9FF"
MORADO = "#A78BFA"
DORADO = "#FFD166"
VERDE = "#62E6A7"
ROJO = "#FF5C7A"


# ============================================================
# TEMPERATURAS DE REFERENCIA
# ============================================================

TEMPERATURAS = {

    "O2": 50000,
    "O3": 45900,
    "O4": 42900,
    "O5": 41400,
    "O6": 39800,
    "O7": 37900,
    "O8": 35100,
    "O9": 33300,

    "B0": 31400,
    "B1": 26000,
    "B2": 20600,
    "B3": 17000,
    "B4": 16400,
    "B5": 15700,
    "B6": 14500,
    "B7": 14000,
    "B8": 12300,
    "B9": 10700,

    "A0": 9700,
    "A1": 9300,
    "A2": 8840,
    "A3": 8600,
    "A4": 8250,
    "A5": 8100,
    "A6": 7910,
    "A7": 7760,
    "A8": 7590,
    "A9": 7400,

    "F0": 7220,
    "F1": 7020,
    "F2": 6820,
    "F3": 6750,
    "F4": 6670,
    "F5": 6550,
    "F6": 6350,
    "F7": 6280,
    "F8": 6180,
    "F9": 6050,

    "G0": 5930,
    "G1": 5860,
    "G2": 5770,
    "G3": 5720,
    "G4": 5680,
    "G5": 5660,
    "G6": 5600,
    "G7": 5550,
    "G8": 5480,
    "G9": 5380,

    "K0": 5290,
    "K1": 5170,
    "K2": 5100,
    "K3": 4870,
    "K4": 4600,
    "K5": 4440,
    "K6": 4300,
    "K7": 4090,
    "K8": 3990,
    "K9": 3930,

    "M0": 3850,
    "M1": 3660,
    "M2": 3560,
    "M3": 3430,
    "M4": 3210,
    "M5": 3060,
    "M6": 2810,
    "M7": 2680,
    "M8": 2570,
    "M9": 2380
}


# ============================================================
# INFORMACIÓN ESPECTRAL
# ============================================================

INFORMACION = {

    "O": {
        "nombre": "O — Azul intenso",
        "rgb": (0.25, 0.48, 1.00),
        "descripcion": (
            "Estrellas extremadamente calientes "
            "y luminosas."
        ),
        "ejemplo": "Estrellas masivas de tipo O"
    },

    "B": {
        "nombre": "B — Azul blanco",
        "rgb": (0.55, 0.76, 1.00),
        "descripcion": (
            "Estrellas muy calientes y luminosas."
        ),
        "ejemplo": "Spica"
    },

    "A": {
        "nombre": "A — Blanco",
        "rgb": (0.92, 0.96, 1.00),
        "descripcion": (
            "Estrellas blancas con fuertes "
            "líneas de hidrógeno."
        ),
        "ejemplo": "Sirio"
    },

    "F": {
        "nombre": "F — Blanco amarillento",
        "rgb": (1.00, 0.92, 0.62),
        "descripcion": (
            "Estrellas calientes de tonalidad "
            "blanco-amarilla."
        ),
        "ejemplo": "Procyon"
    },

    "G": {
        "nombre": "G — Amarillo",
        "rgb": (1.00, 0.74, 0.20),
        "descripcion": (
            "Estrellas amarillas similares al Sol."
        ),
        "ejemplo": "Sol — G2 V"
    },

    "K": {
        "nombre": "K — Naranja",
        "rgb": (1.00, 0.40, 0.09),
        "descripcion": (
            "Estrellas más frías que el Sol "
            "y de tonalidad naranja."
        ),
        "ejemplo": "Arcturus"
    },

    "M": {
        "nombre": "M — Rojo",
        "rgb": (1.00, 0.08, 0.025),
        "descripcion": (
            "Estrellas frías de tonalidad roja."
        ),
        "ejemplo": "Próxima Centauri"
    }
}


# ============================================================
# LUMINOSIDAD MK
# ============================================================

CLASES_LUMINOSIDAD = {

    "Ia": "Supergigante muy luminosa",
    "Ib": "Supergigante",
    "II": "Gigante luminosa",
    "III": "Gigante",
    "IV": "Subgigante",
    "V": "Secuencia principal"
}


FACTORES_LUMINOSIDAD = {

    "Ia": 1.40,
    "Ib": 1.30,
    "II": 1.20,
    "III": 1.12,
    "IV": 1.05,
    "V": 1.00
}


# ============================================================
# CLASIFICACIÓN
# ============================================================

def obtener_tipo_espectral(
    temperatura
):

    if temperatura >= 48000:
        return "O2"

    tipo_cercano = None
    diferencia_menor = None

    for tipo, valor in TEMPERATURAS.items():

        diferencia = abs(
            temperatura - valor
        )

        if (
            diferencia_menor is None
            or diferencia < diferencia_menor
        ):

            diferencia_menor = diferencia
            tipo_cercano = tipo

    return tipo_cercano


def obtener_letra(tipo):

    return tipo[0]


# ============================================================
# FONDO DE ESTRELLAS
# ============================================================

class FondoEstelar:

    def __init__(
        self,
        widget,
        cantidad=120
    ):

        self.widget = widget
        self.estrellas = []

        for _ in range(cantidad):

            self.estrellas.append({

                "x": uniform(0, 1),
                "y": uniform(0, 1),

                "radio": uniform(
                    0.5,
                    2.0
                ),

                "fase": uniform(
                    0,
                    pi * 2
                ),

                "velocidad": uniform(
                    0.5,
                    2.5
                )
            })

        Clock.schedule_interval(
            self.animar,
            1 / 30
        )

    def animar(self, dt):

        if not self.widget.parent:
            return

        self.widget.canvas.after.clear()

        with self.widget.canvas.after:

            for estrella in self.estrellas:

                brillo = (
                    sin(
                        Clock.get_time()
                        * estrella["velocidad"]
                        + estrella["fase"]
                    )
                    + 1
                ) / 2

                alpha = (
                    0.12
                    +
                    brillo * 0.75
                )

                Color(
                    1,
                    1,
                    1,
                    alpha
                )

                Ellipse(

                    pos=(
                        self.widget.x
                        + estrella["x"]
                        * self.widget.width,

                        self.widget.y
                        + estrella["y"]
                        * self.widget.height
                    ),

                    size=(
                        estrella["radio"],
                        estrella["radio"]
                    )
                )


# ============================================================
# BOTÓN CÓSMICO
# ============================================================

class BotonCosmico(Button):

    def __init__(
        self,
        color_texto=BLANCO,
        color_brillo=CELESTE,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.background_normal = ""
        self.background_down = ""

        # COMPLETAMENTE TRANSPARENTE
        self.background_color = (
            0,
            0,
            0,
            0
        )

        self.color = get_color_from_hex(
            color_texto
        )

        self.bold = True
        self.font_size = dp(14)

        self.color_brillo = get_color_from_hex(
            color_brillo
        )

        self.bind(
            size=self.dibujar,
            pos=self.dibujar
        )

        Clock.schedule_interval(
            self.animar_brillo,
            1 / 30
        )

    def dibujar(self, *args):

        self.canvas.before.clear()

        with self.canvas.before:

            # halo extremadamente sutil
            Color(
                self.color_brillo[0],
                self.color_brillo[1],
                self.color_brillo[2],
                0.035
            )

            Ellipse(

                pos=(
                    self.x + self.width * 0.04,
                    self.y + self.height * 0.12
                ),

                size=(
                    self.width * 0.92,
                    self.height * 0.76
                )
            )

    def animar_brillo(self, dt):

        if not self.parent:
            return

        brillo = (
            sin(
                Clock.get_time() * 1.7
            )
            + 1
        ) / 2

        self.canvas.before.clear()

        with self.canvas.before:

            Color(
                self.color_brillo[0],
                self.color_brillo[1],
                self.color_brillo[2],
                0.025 + brillo * 0.035
            )

            Ellipse(

                pos=(
                    self.x + self.width * 0.05,
                    self.y + self.height * 0.15
                ),

                size=(
                    self.width * 0.90,
                    self.height * 0.70
                )
            )


# ============================================================
# AGUJERO NEGRO
# ============================================================

class AgujeroNegro(Label):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.size_hint = (
            None,
            None
        )

        self.size = (
            dp(155),
            dp(155)
        )

        self.angulo = 0

        self.particulas = []

        for _ in range(35):

            self.particulas.append({

                "angulo": uniform(
                    0,
                    pi * 2
                ),

                "radio": uniform(
                    35,
                    72
                ),

                "velocidad": uniform(
                    0.4,
                    1.3
                ),

                "tamaño": uniform(
                    1,
                    3
                )
            })

        Clock.schedule_interval(
            self.animar,
            1 / 30
        )

    def animar(self, dt):

        self.angulo += 1.2

        self.canvas.clear()

        cx = self.center_x
        cy = self.center_y

        with self.canvas:

            # halo exterior
            Color(
                0.35,
                0.15,
                0.80,
                0.035
            )

            Ellipse(
                pos=(
                    cx - dp(73),
                    cy - dp(73)
                ),
                size=(
                    dp(146),
                    dp(146)
                )
            )

            # disco exterior
            Color(
                0.90,
                0.35,
                0.95,
                0.08
            )

            Line(
                ellipse=(
                    cx - dp(58),
                    cy - dp(20),
                    dp(116),
                    dp(40)
                ),
                width=dp(4)
            )

            Color(
                1,
                0.55,
                0.18,
                0.12
            )

            Line(
                ellipse=(
                    cx - dp(50),
                    cy - dp(14),
                    dp(100),
                    dp(28)
                ),
                width=dp(3)
            )

            # partículas
            for p in self.particulas:

                angulo = (
                    p["angulo"]
                    +
                    self.angulo
                    * p["velocidad"]
                    * 0.02
                )

                x = (
                    cx
                    +
                    cos(angulo)
                    * dp(p["radio"])
                )

                y = (
                    cy
                    +
                    sin(angulo)
                    * dp(p["radio"])
                    * 0.35
                )

                Color(
                    1,
                    0.55,
                    0.20,
                    0.25
                )

                Ellipse(
                    pos=(
                        x,
                        y
                    ),
                    size=(
                        dp(p["tamaño"]),
                        dp(p["tamaño"])
                    )
                )

            # disco interno
            Color(
                0.65,
                0.35,
                1,
                0.12
            )

            Ellipse(
                pos=(
                    cx - dp(48),
                    cy - dp(48)
                ),
                size=(
                    dp(96),
                    dp(96)
                )
            )

            # EVENT HORIZON
            Color(
                0.0,
                0.0,
                0.0,
                1
            )

            Ellipse(
                pos=(
                    cx - dp(35),
                    cy - dp(35)
                ),
                size=(
                    dp(70),
                    dp(70)
                )
            )

            # pequeño brillo alrededor
            Color(
                0.80,
                0.50,
                1,
                0.25
            )

            Line(
                circle=(
                    cx,
                    cy,
                    dp(36)
                ),
                width=dp(1.2)
            )


# ============================================================
# ESTRELLA 3D
# ============================================================

class VisorEstelar3D:

    def __init__(self):

        self.widget = None

        self.tipo = "G2"
        self.temperatura = 5770
        self.luminosidad = "V"

        self.rotacion = 0
        self.inclinacion = 0

        self.zoom = 1.0

        self.pausado = False

        self.puntos = []
        self.manchas = []

        self.crear_superficie()

    def crear_superficie(self):

        self.puntos.clear()

        for _ in range(1000):

            theta = uniform(
                0,
                pi * 2
            )

            phi = uniform(
                -pi / 2,
                pi / 2
            )

            x = cos(phi) * cos(theta)
            y = cos(phi) * sin(theta)
            z = sin(phi)

            variacion = uniform(
                0.94,
                1.04
            )

            self.puntos.append(
                (
                    x * variacion,
                    y * variacion,
                    z * variacion
                )
            )

    def crear_manchas(self):

        self.manchas.clear()

        letra = obtener_letra(
            self.tipo
        )

        if letra not in [
            "G",
            "K",
            "M"
        ]:

            return

        cantidad = {

            "G": 12,
            "K": 18,
            "M": 28

        }[letra]

        for _ in range(cantidad):

            theta = uniform(
                0,
                pi * 2
            )

            phi = uniform(
                -pi / 2,
                pi / 2
            )

            x = cos(phi) * cos(theta)
            y = cos(phi) * sin(theta)
            z = sin(phi)

            tamaño = uniform(
                0.015,
                0.06
            )

            self.manchas.append(
                (
                    x,
                    y,
                    z,
                    tamaño
                )
            )

    def conectar(
        self,
        widget
    ):

        self.widget = widget

        Clock.schedule_interval(
            self.actualizar,
            1 / 30
        )

    def cambiar_estrella(
        self,
        tipo,
        temperatura,
        luminosidad="V"
    ):

        self.tipo = tipo
        self.temperatura = temperatura
        self.luminosidad = luminosidad

        self.crear_superficie()
        self.crear_manchas()

        self.redibujar()

    def actualizar(
        self,
        dt
    ):

        if self.pausado:
            return

        self.rotacion += 0.65

        self.redibujar()

    def proyectar(
        self,
        x,
        y,
        z,
        centro_x,
        centro_y,
        radio
    ):

        angulo = (
            self.rotacion
            * pi
            / 180
        )

        x2 = (
            x * cos(angulo)
            -
            z * sin(angulo)
        )

        z2 = (
            x * sin(angulo)
            +
            z * cos(angulo)
        )

        inclinacion = (
            self.inclinacion
            * pi
            / 180
        )

        y2 = (
            y * cos(inclinacion)
            -
            z2 * sin(inclinacion)
        )

        z3 = (
            y * sin(inclinacion)
            +
            z2 * cos(inclinacion)
        )

        distancia = 3.2

        factor = distancia / (
            distancia - z3
        )

        px = (
            centro_x
            +
            x2
            * radio
            * factor
        )

        py = (
            centro_y
            +
            y2
            * radio
            * factor
        )

        return (
            px,
            py,
            z3
        )

    def redibujar(self):

        if not self.widget:
            return

        canvas = self.widget.canvas

        canvas.clear()

        ancho = self.widget.width
        alto = self.widget.height

        centro_x = ancho / 2
        centro_y = alto / 2

        letra = obtener_letra(
            self.tipo
        )

        datos = INFORMACION[
            letra
        ]

        rgb = datos["rgb"]

        factor_luz = FACTORES_LUMINOSIDAD.get(
            self.luminosidad,
            1.0
        )

        radio = (
            min(
                ancho,
                alto
            )
            * 0.25
            * self.zoom
            * factor_luz
        )

        # ----------------------------------------------------
        # HALO
        # ----------------------------------------------------

        with canvas:

            Color(
                rgb[0],
                rgb[1],
                rgb[2],
                0.035
            )

            Ellipse(
                pos=(
                    centro_x - radio * 1.9,
                    centro_y - radio * 1.9
                ),
                size=(
                    radio * 3.8,
                    radio * 3.8
                )
            )

            Color(
                rgb[0],
                rgb[1],
                rgb[2],
                0.06
            )

            Ellipse(
                pos=(
                    centro_x - radio * 1.5,
                    centro_y - radio * 1.5
                ),
                size=(
                    radio * 3.0,
                    radio * 3.0
                )
            )

        # ----------------------------------------------------
        # PUNTOS DE SUPERFICIE
        # ----------------------------------------------------

        puntos = []

        for x, y, z in self.puntos:

            px, py, profundidad = (
                self.proyectar(
                    x,
                    y,
                    z,
                    centro_x,
                    centro_y,
                    radio
                )
            )

            if profundidad > -0.30:

                brillo = (
                    0.43
                    +
                    (profundidad + 1)
                    * 0.30
                )

                tamaño = uniform(
                    2.3,
                    4.0
                )

                puntos.append(
                    (
                        profundidad,
                        px,
                        py,
                        brillo,
                        tamaño
                    )
                )

        puntos.sort(
            key=lambda p: p[0]
        )

        with canvas:

            for (
                profundidad,
                px,
                py,
                brillo,
                tamaño
            ) in puntos:

                Color(
                    min(
                        1,
                        rgb[0] * brillo
                    ),
                    min(
                        1,
                        rgb[1] * brillo
                    ),
                    min(
                        1,
                        rgb[2] * brillo
                    ),
                    0.95
                )

                Ellipse(
                    pos=(
                        px - tamaño / 2,
                        py - tamaño / 2
                    ),
                    size=(
                        tamaño,
                        tamaño
                    )
                )

        # ----------------------------------------------------
        # MANCHAS
        # ----------------------------------------------------

        if letra in [
            "G",
            "K",
            "M"
        ]:

            with canvas:

                for (
                    x,
                    y,
                    z,
                    tamaño
                ) in self.manchas:

                    px, py, profundidad = (
                        self.proyectar(
                            x,
                            y,
                            z,
                            centro_x,
                            centro_y,
                            radio
                        )
                    )

                    if profundidad > 0.18:

                        tam = (
                            radio
                            * tamaño
                        )

                        Color(
                            0.10,
                            0.02,
                            0.005,
                            0.75
                        )

                        Ellipse(
                            pos=(
                                px - tam,
                                py - tam
                            ),
                            size=(
                                tam * 2,
                                tam * 2
                            )
                        )

        # ----------------------------------------------------
        # BORDE
        # ----------------------------------------------------

        with canvas:

            Color(
                rgb[0],
                rgb[1],
                rgb[2],
                0.55
            )

            Line(
                circle=(
                    centro_x,
                    centro_y,
                    radio
                ),
                width=1.5
            )

    def aumentar_zoom(self):

        self.zoom = min(
            1.65,
            self.zoom + 0.10
        )

        self.redibujar()

    def disminuir_zoom(self):

        self.zoom = max(
            0.65,
            self.zoom - 0.10
        )

        self.redibujar()

    def alternar_pausa(self):

        self.pausado = not self.pausado

        return self.pausado


# ============================================================
# WIDGET ESTRELLA
# ============================================================

class WidgetEstrella3D(Label):

    def __init__(
        self,
        visor,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.visor = visor
        self.touch_inicial = None

        self.bind(
            size=self.actualizar,
            pos=self.actualizar
        )

    def actualizar(
        self,
        *args
    ):

        self.visor.redibujar()

    def on_touch_down(
        self,
        touch
    ):

        if self.collide_point(
            *touch.pos
        ):

            self.touch_inicial = (
                touch.pos
            )

            return True

        return super().on_touch_down(
            touch
        )

    def on_touch_move(
        self,
        touch
    ):

        if self.touch_inicial:

            dx = (
                touch.x
                -
                self.touch_inicial[0]
            )

            dy = (
                touch.y
                -
                self.touch_inicial[1]
            )

            self.visor.rotacion += (
                dx * 0.6
            )

            self.visor.inclinacion += (
                dy * 0.4
            )

            self.visor.inclinacion = max(
                -60,
                min(
                    60,
                    self.visor.inclinacion
                )
            )

            self.touch_inicial = (
                touch.pos
            )

            self.visor.redibujar()

            return True

        return super().on_touch_move(
            touch
        )

    def on_touch_up(
        self,
        touch
    ):

        self.touch_inicial = None

        return super().on_touch_up(
            touch
        )


# ============================================================
# INICIO
# ============================================================

class InicioScreen(Screen):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        FondoEstelar(
            self,
            145
        )

        principal = BoxLayout(

            orientation="vertical",

            padding=dp(22),

            spacing=dp(7)
        )

        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        principal.add_widget(

            Label(

                text="⭐ COSMIC STAR LAB",

                font_size=dp(30),

                bold=True,

                color=get_color_from_hex(
                    CELESTE
                ),

                size_hint_y=None,

                height=dp(48)
            )
        )

        principal.add_widget(

            Label(

                text=(
                    "CLASIFICADOR DE ESTRELLAS"
                ),

                font_size=dp(13),

                color=get_color_from_hex(
                    GRIS
                ),

                size_hint_y=None,

                height=dp(25)
            )
        )

        principal.add_widget(

            Label(

                text=(
                    f"By: {AUTOR}   •   {VERSION}"
                ),

                font_size=dp(11),

                color=get_color_from_hex(
                    GRIS
                ),

                size_hint_y=None,

                height=dp(25)
            )
        )

        # ----------------------------------------------------
        # AGUJERO NEGRO
        # ----------------------------------------------------

        zona_cosmica = BoxLayout(

            orientation="horizontal",

            size_hint_y=None,

            height=dp(170)
        )

        zona_cosmica.add_widget(
            Label(
                text=(
                    "Explora el universo.\n\n"
                    "Clasifica estrellas,\n"
                    "observa su color\n"
                    "y descubre su temperatura."
                ),
                font_size=dp(14),
                color=get_color_from_hex(
                    BLANCO
                ),
                halign="center"
            )
        )

        agujero = AgujeroNegro()

        zona_cosmica.add_widget(
            agujero
        )

        principal.add_widget(
            zona_cosmica
        )

        # ----------------------------------------------------
        # MENÚ
        # ----------------------------------------------------

        principal.add_widget(

            Label(

                text="✦  EXPLORACIÓN ESTELAR  ✦",

                font_size=dp(12),

                color=get_color_from_hex(
                    GRIS
                ),

                size_hint_y=None,

                height=dp(28)
            )
        )

        boton1 = BotonCosmico(
            text="⭐  CLASIFICAR UNA ESTRELLA",
            color_texto=BLANCO,
            color_brillo=CELESTE,
            size_hint_y=None,
            height=dp(48)
        )

        boton1.bind(
            on_release=lambda x:
            self.ir("clasificador")
        )

        principal.add_widget(
            boton1
        )

        boton2 = BotonCosmico(
            text="🌌  LABORATORIO ESTELAR 3D",
            color_texto=BLANCO,
            color_brillo=MORADO,
            size_hint_y=None,
            height=dp(48)
        )

        boton2.bind(
            on_release=lambda x:
            self.ir("laboratorio")
        )

        principal.add_widget(
            boton2
        )

        boton3 = BotonCosmico(
            text="🌡️  LABORATORIO DE TEMPERATURA",
            color_texto=BLANCO,
            color_brillo=DORADO,
            size_hint_y=None,
            height=dp(48)
        )

        boton3.bind(
            on_release=lambda x:
            self.ir("temperatura")
        )

        principal.add_widget(
            boton3
        )

        boton4 = BotonCosmico(
            text="📖  APRENDER O–B–A–F–G–K–M",
            color_texto=BLANCO,
            color_brillo=VERDE,
            size_hint_y=None,
            height=dp(48)
        )

        boton4.bind(
            on_release=lambda x:
            self.ir("aprender")
        )

        principal.add_widget(
            boton4
        )

        boton5 = BotonCosmico(
            text="📊  TABLA DE TEMPERATURAS",
            color_texto=BLANCO,
            color_brillo=AZUL,
            size_hint_y=None,
            height=dp(48)
        )

        boton5.bind(
            on_release=lambda x:
            self.ir("tabla")
        )

        principal.add_widget(
            boton5
        )

        boton6 = BotonCosmico(
            text="ℹ️  ACERCA DEL PROGRAMA",
            color_texto=GRIS,
            color_brillo=GRIS,
            size_hint_y=None,
            height=dp(45)
        )

        boton6.bind(
            on_release=lambda x:
            self.ir("acerca")
        )

        principal.add_widget(
            boton6
        )

        principal.add_widget(

            Label(

                text=(
                    "✦  Una pequeña ventana hacia "
                    "el universo  ✦"
                ),

                font_size=dp(10),

                color=get_color_from_hex(
                    GRIS
                )
            )
        )

        self.add_widget(
            principal
        )

    def ir(
        self,
        pantalla
    ):

        self.manager.current = pantalla


# ============================================================
# CLASIFICADOR
# ============================================================

class ClasificadorScreen(Screen):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        principal = BoxLayout(
            orientation="vertical"
        )

        principal.add_widget(

            Label(

                text="🔭 CLASIFICADOR ESTELAR",

                font_size=dp(24),

                bold=True,

                color=get_color_from_hex(
                    CELESTE
                ),

                size_hint_y=None,

                height=dp(55)
            )
        )

        scroll = ScrollView()

        contenido = BoxLayout(

            orientation="vertical",

            padding=dp(20),

            spacing=dp(12),

            size_hint_y=None
        )

        contenido.bind(
            minimum_height=
            contenido.setter(
                "height"
            )
        )

        contenido.add_widget(

            Label(

                text=(
                    "✦ SISTEMA ESPECTRAL DE HARVARD"
                ),

                font_size=dp(17),

                bold=True,

                color=get_color_from_hex(
                    DORADO
                ),

                size_hint_y=None,

                height=dp(35)
            )
        )

        self.entrada_temp = TextInput(

            hint_text="Temperatura en K",

            input_filter="float",

            multiline=False,

            font_size=dp(18),

            size_hint_y=None,

            height=dp(50)
        )

        contenido.add_widget(
            self.entrada_temp
        )

        boton = BotonCosmico(

            text="⭐  CLASIFICAR",

            color_texto=BLANCO,

            color_brillo=CELESTE,

            size_hint_y=None,

            height=dp(50)
        )

        boton.bind(
            on_release=lambda x:
            self.clasificar()
        )

        contenido.add_widget(
            boton
        )

        contenido.add_widget(

            Label(

                text=(
                    "✦ SISTEMA MORGAN–KEENAN (MK)"
                ),

                font_size=dp(17),

                bold=True,

                color=get_color_from_hex(
                    DORADO
                ),

                size_hint_y=None,

                height=dp(45)
            )
        )

        self.spinner = Spinner(

            text="Selecciona luminosidad",

            values=[
                "Ia",
                "Ib",
                "II",
                "III",
                "IV",
                "V"
            ],

            size_hint_y=None,

            height=dp(50)
        )

        contenido.add_widget(
            self.spinner
        )

        boton_mk = BotonCosmico(

            text="🌟  CLASIFICAR MK",

            color_texto=BLANCO,

            color_brillo=MORADO,

            size_hint_y=None,

            height=dp(50)
        )

        boton_mk.bind(
            on_release=lambda x:
            self.clasificar_mk()
        )

        contenido.add_widget(
            boton_mk
        )

        self.resultado = Label(

            text=(
                "\n✦ RESULTADO\n\n"
                "Introduce una temperatura."
            ),

            font_size=dp(16),

            color=get_color_from_hex(
                BLANCO
            ),

            halign="left",

            valign="top",

            size_hint_y=None,

            height=dp(300)
        )

        contenido.add_widget(
            self.resultado
        )

        boton3d = BotonCosmico(

            text="🌌  VER ESTRELLA EN 3D",

            color_texto=BLANCO,

            color_brillo=MORADO,

            size_hint_y=None,

            height=dp(50)
        )

        boton3d.bind(
            on_release=lambda x:
            self.ver_3d()
        )

        contenido.add_widget(
            boton3d
        )

        nuevo = BotonCosmico(

            text="↻  NUEVA CLASIFICACIÓN",

            color_texto=BLANCO,

            color_brillo=VERDE,

            size_hint_y=None,

            height=dp(50)
        )

        nuevo.bind(
            on_release=lambda x:
            self.nueva()
        )

        contenido.add_widget(
            nuevo
        )

        volver = BotonCosmico(

            text="←  VOLVER AL INICIO",

            color_texto=GRIS,

            color_brillo=GRIS,

            size_hint_y=None,

            height=dp(45)
        )

        volver.bind(
            on_release=lambda x:
            self.volver()
        )

        contenido.add_widget(
            volver
        )

        scroll.add_widget(
            contenido
        )

        principal.add_widget(
            scroll
        )

        self.add_widget(
            principal
        )

        self.tipo_actual = None
        self.temp_actual = None
        self.lum_actual = "V"

    def clasificar(self):

        try:

            temperatura = float(
                self.entrada_temp.text
            )

            if temperatura <= 0:
                raise ValueError

            tipo = obtener_tipo_espectral(
                temperatura
            )

            letra = obtener_letra(
                tipo
            )

            datos = INFORMACION[
                letra
            ]

            self.tipo_actual = tipo
            self.temp_actual = temperatura
            self.lum_actual = "V"

            self.resultado.text = (

                "⭐ RESULTADO\n\n"

                f"Tipo espectral: {tipo}\n"

                f"Temperatura: "
                f"{temperatura:,.0f} K\n\n"

                f"{datos['nombre']}\n\n"

                f"{datos['descripcion']}\n\n"

                f"Ejemplo: {datos['ejemplo']}\n\n"

                "Clase visualizada: V\n"
                "Secuencia principal."
            )

        except:

            self.mostrar_error(
                "Introduce una temperatura válida."
            )

    def clasificar_mk(self):

        try:

            temperatura = float(
                self.entrada_temp.text
            )

            if temperatura <= 0:
                raise ValueError

            if (
                self.spinner.text
                not in CLASES_LUMINOSIDAD
            ):

                self.mostrar_error(
                    "Selecciona una clase de luminosidad."
                )

                return

            tipo = obtener_tipo_espectral(
                temperatura
            )

            clase = self.spinner.text

            letra = obtener_letra(
                tipo
            )

            datos = INFORMACION[
                letra
            ]

            self.tipo_actual = tipo
            self.temp_actual = temperatura
            self.lum_actual = clase

            self.resultado.text = (

                "🌟 RESULTADO MK\n\n"

                f"Clasificación: "
                f"{tipo} {clase}\n\n"

                f"Temperatura: "
                f"{temperatura:,.0f} K\n\n"

                f"{datos['nombre']}\n\n"

                f"{datos['descripcion']}\n\n"

                "Clase de luminosidad:\n"

                f"{clase} — "
                f"{CLASES_LUMINOSIDAD[clase]}"
            )

        except:

            self.mostrar_error(
                "Introduce una temperatura válida."
            )

    def ver_3d(self):

        if not self.tipo_actual:

            self.mostrar_error(
                "Primero realiza una clasificación."
            )

            return

        laboratorio = (
            self.manager
            .get_screen(
                "laboratorio"
            )
        )

        laboratorio.mostrar_estrella(
            self.tipo_actual,
            self.temp_actual,
            self.lum_actual
        )

        self.manager.current = (
            "laboratorio"
        )

    def nueva(self):

        self.entrada_temp.text = ""

        self.spinner.text = (
            "Selecciona luminosidad"
        )

        self.resultado.text = (
            "\n✦ RESULTADO\n\n"
            "Introduce una temperatura."
        )

        self.tipo_actual = None
        self.temp_actual = None
        self.lum_actual = "V"

    def mostrar_error(
        self,
        mensaje
    ):

        caja = BoxLayout(

            orientation="vertical",

            padding=dp(20),

            spacing=dp(15)
        )

        caja.add_widget(

            Label(
                text=mensaje,
                font_size=dp(16)
            )
        )

        cerrar = BotonCosmico(

            text="ACEPTAR",

            color_texto=BLANCO,

            color_brillo=CELESTE,

            size_hint_y=None,

            height=dp(45)
        )

        caja.add_widget(
            cerrar
        )

        popup = Popup(

            title="⚠️ Atención",

            content=caja,

            size_hint=(
                0.85,
                0.35
            ),

            separator_color=(
                0,
                0,
                0,
                0
            )
        )

        cerrar.bind(
            on_release=popup.dismiss
        )

        popup.open()

    def volver(self):

        self.manager.current = "inicio"


# ============================================================
# LABORATORIO 3D
# ============================================================

class LaboratorioScreen(Screen):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        principal = BoxLayout(
            orientation="vertical"
        )

        principal.add_widget(

            Label(

                text="🌌 LABORATORIO ESTELAR 3D",

                font_size=dp(22),

                bold=True,

                color=get_color_from_hex(
                    CELESTE
                ),

                size_hint_y=None,

                height=dp(55)
            )
        )

        self.info = Label(

            text="Selecciona una estrella.",

            font_size=dp(15),

            color=get_color_from_hex(
                BLANCO
            ),

            size_hint_y=None,

            height=dp(65),

            halign="center"
        )

        principal.add_widget(
            self.info
        )

        self.visor = VisorEstelar3D()

        self.widget3d = WidgetEstrella3D(
            self.visor
        )

        principal.add_widget(
            self.widget3d
        )

        self.visor.conectar(
            self.widget3d
        )

        controles = GridLayout(

            cols=4,

            spacing=dp(5),

            padding=dp(7),

            size_hint_y=None,

            height=dp(55)
        )

        menos = BotonCosmico(
            text="−",
            color_brillo=CELESTE
        )

        menos.bind(
            on_release=lambda x:
            self.visor.disminuir_zoom()
        )

        controles.add_widget(
            menos
        )

        mas = BotonCosmico(
            text="+",
            color_brillo=CELESTE
        )

        mas.bind(
            on_release=lambda x:
            self.visor.aumentar_zoom()
        )

        controles.add_widget(
            mas
        )

        self.pausa = BotonCosmico(
            text="⏸",
            color_brillo=DORADO
        )

        self.pausa.bind(
            on_release=lambda x:
            self.pausar()
        )

        controles.add_widget(
            self.pausa
        )

        clasificar = BotonCosmico(
            text="⭐",
            color_brillo=VERDE
        )

        clasificar.bind(
            on_release=lambda x:
            self.ir_clasificador()
        )

        controles.add_widget(
            clasificar
        )

        principal.add_widget(
            controles
        )

        principal.add_widget(

            Label(

                text=(
                    "Arrastra la estrella para rotarla\n"
                    "Color = tipo espectral • "
                    "Tamaño = representación educativa "
                    "de luminosidad"
                ),

                font_size=dp(10),

                color=get_color_from_hex(
                    GRIS
                ),

                size_hint_y=None,

                height=dp(50),

                halign="center"
            )
        )

        volver = BotonCosmico(

            text="←  VOLVER AL INICIO",

            color_texto=GRIS,

            color_brillo=GRIS,

            size_hint_y=None,

            height=dp(45)
        )

        volver.bind(
            on_release=lambda x:
            self.volver()
        )

        principal.add_widget(
            volver
        )

        self.add_widget(
            principal
        )

    def mostrar_estrella(
        self,
        tipo,
        temperatura,
        luminosidad="V"
    ):

        self.visor.cambiar_estrella(
            tipo,
            temperatura,
            luminosidad
        )

        letra = obtener_letra(
            tipo
        )

        datos = INFORMACION[
            letra
        ]

        nombre_luminosidad = (
            CLASES_LUMINOSIDAD.get(
                luminosidad,
                ""
            )
        )

        self.info.text = (

            f"⭐ {tipo} {luminosidad}   |   "
            f"{temperatura:,.0f} K\n"
            f"{datos['nombre']}   •   "
            f"{nombre_luminosidad}"
        )

        self.pausa.text = "⏸"

    def pausar(self):

        estado = (
            self.visor
            .alternar_pausa()
        )

        if estado:

            self.pausa.text = "▶"

        else:

            self.pausa.text = "⏸"

    def volver(self):

        self.manager.current = "inicio"

    def ir_clasificador(self):

        self.manager.current = (
            "clasificador"
        )


# ============================================================
# LABORATORIO DE TEMPERATURA
# ============================================================

class TemperaturaScreen(Screen):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        FondoEstelar(
            self,
            100
        )

        principal = BoxLayout(

            orientation="vertical",

            padding=dp(15),

            spacing=dp(5)
        )

        principal.add_widget(

            Label(

                text="🌡️ LABORATORIO DE TEMPERATURA",

                font_size=dp(21),

                bold=True,

                color=get_color_from_hex(
                    CELESTE
                ),

                size_hint_y=None,

                height=dp(45)
            )
        )

        self.dato_tipo = Label(

            text="G2",

            font_size=dp(28),

            bold=True,

            color=get_color_from_hex(
                DORADO
            ),

            size_hint_y=None,

            height=dp(40)
        )

        principal.add_widget(
            self.dato_tipo
        )

        self.dato_temp = Label(

            text="5770 K",

            font_size=dp(18),

            color=get_color_from_hex(
                BLANCO
            ),

            size_hint_y=None,

            height=dp(30)
        )

        principal.add_widget(
            self.dato_temp
        )

        self.dato_color = Label(

            text="G — Amarillo",

            font_size=dp(15),

            color=get_color_from_hex(
                DORADO
            ),

            size_hint_y=None,

            height=dp(30)
        )

        principal.add_widget(
            self.dato_color
        )

        self.visor = VisorEstelar3D()

        self.widget3d = WidgetEstrella3D(
            self.visor
        )

        principal.add_widget(
            self.widget3d
        )

        self.visor.conectar(
            self.widget3d
        )

        principal.add_widget(

            Label(

                text="TEMPERATURA EFECTIVA",

                font_size=dp(12),

                color=get_color_from_hex(
                    GRIS
                ),

                size_hint_y=None,

                height=dp(22)
            )
        )

        self.slider = Slider(

            min=2380,

            max=50000,

            value=5770,

            step=10,

            size_hint_y=None,

            height=dp(45)
        )

        self.slider.bind(
            value=self.cambiar_temperatura
        )

        principal.add_widget(
            self.slider
        )

        controles = GridLayout(

            cols=3,

            spacing=dp(5),

            size_hint_y=None,

            height=dp(50)
        )

        menos = BotonCosmico(
            text="− 500 K",
            color_brillo=ROJO
        )

        menos.bind(
            on_release=lambda x:
            self.temperatura_menos()
        )

        controles.add_widget(
            menos
        )

        self.pausa = BotonCosmico(
            text="⏸",
            color_brillo=DORADO
        )

        self.pausa.bind(
            on_release=lambda x:
            self.pausar()
        )

        controles.add_widget(
            self.pausa
        )

        mas = BotonCosmico(
            text="+ 500 K",
            color_brillo=CELESTE
        )

        mas.bind(
            on_release=lambda x:
            self.temperatura_mas()
        )

        controles.add_widget(
            mas
        )

        principal.add_widget(
            controles
        )

        volver = BotonCosmico(

            text="←  VOLVER AL INICIO",

            color_texto=GRIS,

            color_brillo=GRIS,

            size_hint_y=None,

            height=dp(42)
        )

        volver.bind(
            on_release=lambda x:
            self.volver()
        )

        principal.add_widget(
            volver
        )

        self.add_widget(
            principal
        )

        self.actualizar_estudio(
            5770
        )

    def cambiar_temperatura(
        self,
        slider,
        valor
    ):

        self.actualizar_estudio(
            valor
        )

    def actualizar_estudio(
        self,
        temperatura
    ):

        temperatura = float(
            temperatura
        )

        tipo = obtener_tipo_espectral(
            temperatura
        )

        letra = obtener_letra(
            tipo
        )

        datos = INFORMACION[
            letra
        ]

        self.dato_tipo.text = tipo

        self.dato_temp.text = (
            f"{temperatura:,.0f} K"
        )

        self.dato_color.text = (
            datos["nombre"]
        )

        self.visor.cambiar_estrella(
            tipo,
            temperatura,
            "V"
        )

    def temperatura_menos(self):

        nueva = max(
            2380,
            self.slider.value - 500
        )

        self.slider.value = nueva

    def temperatura_mas(self):

        nueva = min(
            50000,
            self.slider.value + 500
        )

        self.slider.value = nueva

    def pausar(self):

        estado = (
            self.visor
            .alternar_pausa()
        )

        if estado:

            self.pausa.text = "▶"

        else:

            self.pausa.text = "⏸"

    def volver(self):

        self.manager.current = "inicio"


# ============================================================
# APRENDER
# ============================================================

class AprenderScreen(Screen):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        principal = BoxLayout(
            orientation="vertical"
        )

        principal.add_widget(

            Label(

                text="📖 APRENDER",

                font_size=dp(24),

                bold=True,

                color=get_color_from_hex(
                    CELESTE
                ),

                size_hint_y=None,

                height=dp(55)
            )
        )

        scroll = ScrollView()

        contenido = BoxLayout(

            orientation="vertical",

            padding=dp(20),

            spacing=dp(15),

            size_hint_y=None
        )

        contenido.bind(
            minimum_height=
            contenido.setter(
                "height"
            )
        )

        texto = (

            "🌌 CLASIFICACIÓN ESPECTRAL\n\n"

            "Las estrellas presentan espectros "
            "que permiten clasificarlas.\n\n"

            "SECUENCIA ESPECTRAL\n\n"

            "O → B → A → F → G → K → M\n\n"

            "🔵 O — azul intenso\n"
            "🔵 B — azul blanco\n"
            "⚪ A — blanco\n"
            "🟡 F — blanco amarillento\n"
            "☀️ G — amarillo\n"
            "🟠 K — naranja\n"
            "🔴 M — rojo\n\n"

            "Cada clase se subdivide "
            "normalmente en 0–9.\n\n"

            "Ejemplo:\n\n"

            "☀️ SOL ≈ G2 V\n\n"

            "G2 = tipo espectral\n"
            "V = luminosidad de secuencia principal\n\n"

            "La temperatura se utiliza en esta "
            "aplicación como aproximación educativa "
            "para determinar el tipo espectral."
        )

        contenido.add_widget(

            Label(

                text=texto,

                font_size=dp(16),

                color=get_color_from_hex(
                    BLANCO
                ),

                size_hint_y=None,

                height=dp(600),

                halign="left",

                valign="top"
            )
        )

        volver = BotonCosmico(

            text="←  VOLVER AL INICIO",

            color_texto=GRIS,

            color_brillo=GRIS,

            size_hint_y=None,

            height=dp(50)
        )

        volver.bind(
            on_release=lambda x:
            self.volver()
        )

        contenido.add_widget(
            volver
        )

        scroll.add_widget(
            contenido
        )

        principal.add_widget(
            scroll
        )

        self.add_widget(
            principal
        )

    def volver(self):

        self.manager.current = "inicio"


# ============================================================
# TABLA
# ============================================================

class TablaScreen(Screen):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        principal = BoxLayout(
            orientation="vertical"
        )

        principal.add_widget(

            Label(

                text="📊 TEMPERATURAS ESTELARES",

                font_size=dp(22),

                bold=True,

                color=get_color_from_hex(
                    CELESTE
                ),

                size_hint_y=None,

                height=dp(55)
            )
        )

        scroll = ScrollView()

        tabla = GridLayout(

            cols=3,

            spacing=dp(5),

            padding=dp(12),

            size_hint_y=None
        )

        tabla.bind(
            minimum_height=
            tabla.setter(
                "height"
            )
        )

        for encabezado in [
            "TIPO",
            "K",
            "COLOR"
        ]:

            tabla.add_widget(

                Label(

                    text=encabezado,

                    bold=True,

                    color=get_color_from_hex(
                        DORADO
                    ),

                    size_hint_y=None,

                    height=dp(35)
                )
            )

        tipos = [

            "O3",
            "B0",
            "A0",
            "F0",
            "G2",
            "K0",
            "M0"

        ]

        for tipo in tipos:

            letra = obtener_letra(
                tipo
            )

            tabla.add_widget(

                Label(

                    text=tipo,

                    color=get_color_from_hex(
                        BLANCO
                    ),

                    size_hint_y=None,

                    height=dp(32)
                )
            )

            tabla.add_widget(

                Label(

                    text=(
                        f"{TEMPERATURAS[tipo]:,}"
                    ),

                    color=get_color_from_hex(
                        BLANCO
                    ),

                    size_hint_y=None,

                    height=dp(32)
                )
            )

            tabla.add_widget(

                Label(

                    text=INFORMACION[
                        letra
                    ]["nombre"],

                    color=get_color_from_hex(
                        GRIS
                    ),

                    size_hint_y=None,

                    height=dp(32)
                )
            )

        scroll.add_widget(
            tabla
        )

        principal.add_widget(
            scroll
        )

        volver = BotonCosmico(

            text="←  VOLVER AL INICIO",

            color_texto=GRIS,

            color_brillo=GRIS,

            size_hint_y=None,

            height=dp(48)
        )

        volver.bind(
            on_release=lambda x:
            self.volver()
        )

        principal.add_widget(
            volver
        )

        self.add_widget(
            principal
        )

    def volver(self):

        self.manager.current = "inicio"


# ============================================================
# ACERCA
# ============================================================

class AcercaScreen(Screen):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        FondoEstelar(
            self,
            70
        )

        principal = BoxLayout(

            orientation="vertical",

            padding=dp(25),

            spacing=dp(12)
        )

        principal.add_widget(

            Label(

                text="✦ ACERCA DEL PROGRAMA ✦",

                font_size=dp(23),

                bold=True,

                color=get_color_from_hex(
                    CELESTE
                ),

                size_hint_y=None,

                height=dp(55)
            )
        )

        principal.add_widget(

            Label(

                text=(

                    "⭐ COSMIC STAR LAB\n\n"

                    f"Autor:\n{AUTOR}\n\n"

                    f"Versión: {VERSION}\n\n"

                    "Desarrollado con Python + Kivy.\n\n"

                    "CLASIFICACIÓN HARVARD\n"
                    "MORGAN–KEENAN\n"
                    "VISUALIZACIÓN ESTELAR 3D\n"
                    "LABORATORIO DE TEMPERATURA\n\n"

                    "🌌 Herramienta educativa "
                    "de astronomía"
                ),

                font_size=dp(16),

                color=get_color_from_hex(
                    BLANCO
                ),

                halign="center"
            )
        )

        volver = BotonCosmico(

            text="←  VOLVER AL INICIO",

            color_texto=GRIS,

            color_brillo=GRIS,

            size_hint_y=None,

            height=dp(50)
        )

        volver.bind(
            on_release=lambda x:
            self.volver()
        )

        principal.add_widget(
            volver
        )

        self.add_widget(
            principal
        )

    def volver(self):

        self.manager.current = "inicio"


# ============================================================
# APLICACIÓN
# ============================================================

class ClasificadorEstrellasApp(
    App
):

    def build(self):

        self.title = (
            "COSMIC STAR LAB "
            + VERSION
        )

        manager = ScreenManager(

            transition=FadeTransition(
                duration=0.25
            )
        )

        manager.add_widget(
            InicioScreen(
                name="inicio"
            )
        )

        manager.add_widget(
            ClasificadorScreen(
                name="clasificador"
            )
        )

        manager.add_widget(
            LaboratorioScreen(
                name="laboratorio"
            )
        )

        manager.add_widget(
            TemperaturaScreen(
                name="temperatura"
            )
        )

        manager.add_widget(
            AprenderScreen(
                name="aprender"
            )
        )

        manager.add_widget(
            TablaScreen(
                name="tabla"
            )
        )

        manager.add_widget(
            AcercaScreen(
                name="acerca"
            )
        )

        return manager


# ============================================================
# INICIO DEL PROGRAMA
# ============================================================

if __name__ == "__main__":

    ClasificadorEstrellasApp().run()
