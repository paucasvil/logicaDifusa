import tkinter as tk
from PIL import Image, ImageTk
# Clase principal de la aplicación
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Calculadora de Propinas')
        self.geometry('500x500')
        self.frames = {}
        # Inicializamos todas las pantallas del sistema
        for F in (SplashScreen, ComidaScreen, ServicioScreen, ResultadoScreen):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')
        # Se muestra la pantalla inicial
        self.show_frame(SplashScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
#Pantalla de inicio, solo dura 2 segundos
class SplashScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg = 'white')
        bg_img = Image.open('fondo.jpg').resize((500, 500))
        self.bg_img = ImageTk.PhotoImage(bg_img)
        canvas = tk.Canvas(self, width = 500, height = 500)
        canvas.create_image(0, 0, image = self.bg_img, anchor = 'nw')
        canvas.pack(fill = 'both', expand = True)
        
        label = tk.Label(self, text = 'Calculadora de Propinas', font = ('Arial', 24))
        canvas.create_window(250, 150, window = label)
        # Después de 2 segundos cambia a la siguiente pantalla
        self.after(2000, lambda: parent.show_frame(ComidaScreen))

# Clase para mostrar estrellas y calificar
class StarRating(tk.Frame):
    def __init__(self, parent, label_text, callback, bg_image):
        super().__init__(parent)
        self.rating = 0  # Valor de calificación seleccionado
        self.callback = callback

        meanings = ['Pésimo', 'Mediocre', 'Regular', 'Bueno', 'Excelente']
        self.stars = [] # Almacena los IDs de cada estrella

        #imagen de fondo
        bg_img = Image.open(bg_image).resize((500, 500))
        self.bg_img = ImageTk.PhotoImage(bg_img)
        canvas = tk.Canvas(self, width = 500, height = 500)
        canvas.create_image(0, 0, image = self.bg_img, anchor = 'nw')
        canvas.pack(fill = 'both', expand = True)

        label = tk.Label(self, text = label_text, font = ('Arial', 18))
        canvas.create_window(250, 50, window = label)
        start_x = 250 - ((5 - 1) * 60) / 2   # Posicionamiento centrado de estrellas

        for i in range(5):
            x_pos = start_x + i * 60
            star = canvas.create_text(x_pos, 200, text='☆', font=('Arial', 40), fill='#f1c40f', tags=f'star{i}')
            canvas.tag_bind(f'star{i}', '<Button-1>', lambda e, idx=i: self.set_rating(idx + 1))
            self.stars.append(star) 

            canvas.create_text(x_pos, 250, text=meanings[i], font=('Arial', 10, 'bold'), fill='white')

        # Botón de aceptar (desactivado al inicio)
        self.next_btn = tk.Button(self, text = 'Aceptar', command = self.next_screen, state = 'disabled', 
                                  bg = '#e74c3c', fg = '#f7f7f7', font = ('Arial', 12, 'bold'), relief = 'raised', bd = 5, 
                                  padx = 10, pady = 5, borderwidth = 4, highlightbackground = '#ff4500')
        canvas.create_window(250, 350, window = self.next_btn)

        self.canvas = tk.Canvas(self, width = 500, height = 500)
        self.canvas.create_image(0, 0, image = self.bg_img, anchor = 'nw')
        self.canvas.pack(fill = 'both', expand = True)

    def set_rating(self, rating):
            self.rating = rating
            for i, star_id in enumerate(self.stars):
                new_text = '★' if i < rating else '☆'
                self.children['!canvas'].itemconfig(star_id, text=new_text)
            self.next_btn.config(state='normal')


    def next_screen(self):
        self.callback(self.rating)
# Pantalla para calificar la comida
class ComidaScreen(StarRating):
    def __init__(self, parent):
        super().__init__(parent, 'Evalúa la Comida', self.save_rating, 'fondo.jpg')

    def save_rating(self, rating):
        self.master.comida_rating = rating
        self.master.show_frame(ServicioScreen)
    def reset_rating(self):
        self.rating = 0
        for star_id in self.stars:
            self.canvas.itemconfig(star_id, text='☆')
        self.canvas.update_idletasks()
        self.next_btn.config(state='disabled')

# Pantalla para calificar el servicio
class ServicioScreen(StarRating):
    def __init__(self, parent):
        super().__init__(parent, 'Evalúa el Servicio', self.save_rating, 'mesero.jpg')

    def save_rating(self, rating):
        self.master.servicio_rating = rating
        self.master.show_frame(ResultadoScreen)
    def reset_rating(self):
        self.rating = 0
        for star_id in self.stars:
            self.canvas.itemconfig(star_id, text='☆')
        self.canvas.update_idletasks()
        self.next_btn.config(state='disabled')
# Pantalla que muestra el resultado (propina)
class ResultadoScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        bg_img = Image.open('mesero.jpg').resize((500, 500))
        self.bg_img = ImageTk.PhotoImage(bg_img)
        canvas = tk.Canvas(self, width = 500, height = 500)
        canvas.create_image(0, 0, image = self.bg_img, anchor = 'nw')
        canvas.pack(fill = 'both', expand = True)
        
        self.result_label = tk.Label(self, font = ('Arial', 18), bg = 'white')
        canvas.create_window(250, 100, window = self.result_label)
        
        btn = tk.Button(self, text = 'Calcular Propina', command = self.calculate_tip, 
                        bg = '#27ae60', fg = '#f7f7f7', font = ('Arial', 12, 'bold'), relief = 'raised', bd = 5, 
                        padx = 10, pady = 5, borderwidth = 4, highlightbackground = '#008000')
        canvas.create_window(250, 300, window = btn)

        volver_btn = tk.Button(self, text='Volver a Calcular',
                       command=self.volver_a_calcular,
                       bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                       relief='raised', bd=5, padx=10, pady=5,
                       borderwidth=4, highlightbackground='#1e90ff')
        canvas.create_window(250, 370, window=volver_btn)
    # Reinicia el sistema para evaluar de nuevo
    def volver_a_calcular(self):
        self.master.comida_rating = 0
        self.master.servicio_rating = 0
        self.master.frames[ComidaScreen].reset_rating()
        self.master.frames[ServicioScreen].reset_rating()
        self.master.show_frame(ComidaScreen)
        self.result_label.config(text="")

    # Cálculo difuso de propina
    def calculate_tip(self):
        comida = self.master.comida_rating
        servicio = self.master.servicio_rating
        #Función triangular para los rangos
        def triangular(x, a, b, c):
            val = 0.0
            if a < x and x < b:
                val = (x - a) / (b - a)
            if b <= x and x < c:
                val = (c - x) / (c - b)
            if x == b:
                val = 1.0
            return max(0.0, min(1.0, val))

        # Fuzzificación: calcular grados de pertenencia
        comida_grados = {}
        servicio_grados = {}

        for nombre in ["pesimo", "mediocre", "regular", "bueno", "excelente"]:
            comida_grados[nombre] = 0.0
            servicio_grados[nombre] = 0.0

        # Funciones de la comida
        if True:
            if comida >= 1 and comida <= 2:
                comida_grados["pesimo"] = triangular(comida, 1, 1, 2)
            if comida >= 1 and comida <= 3:
                comida_grados["mediocre"] = triangular(comida, 1, 2, 3)
            if comida >= 2 and comida <= 4:
                comida_grados["regular"] = triangular(comida, 2, 3, 4)
            if comida >= 3 and comida <= 5:
                comida_grados["bueno"] = triangular(comida, 3, 4, 5)
            if comida >= 4 and comida <= 5:
                comida_grados["excelente"] = triangular(comida, 4, 5, 5)

        # Funciones del servicio
        if True:
            if servicio >= 1 and servicio <= 2:
                servicio_grados["pesimo"] = triangular(servicio, 1, 1, 2)
            if servicio >= 1 and servicio <= 3:
                servicio_grados["mediocre"] = triangular(servicio, 1, 2, 3)
            if servicio >= 2 and servicio <= 4:
                servicio_grados["regular"] = triangular(servicio, 2, 3, 4)
            if servicio >= 3 and servicio <= 5:
                servicio_grados["bueno"] = triangular(servicio, 3, 4, 5)
            if servicio >= 4 and servicio <= 5:
                servicio_grados["excelente"] = triangular(servicio, 4, 5, 5)

        # Base para las reglas 
        salida_agregada = {
            "ausente": 0.0,
            "regular": 0.0,
            "adecuada": 0.0,
            "generosa": 0.0
        }
        # Reglas 
        for s_key in servicio_grados:
            for c_key in comida_grados:
                grado = min(servicio_grados[s_key], comida_grados[c_key])
                if s_key == "excelente" and c_key == "excelente":
                    if salida_agregada["generosa"] < grado:
                        salida_agregada["generosa"] = grado
                if s_key == "excelente" and c_key == "bueno":
                    if salida_agregada["generosa"] < grado:
                        salida_agregada["generosa"] = grado
                if s_key == "excelente" and c_key == "regular":
                    if salida_agregada["adecuada"] < grado:
                        salida_agregada["adecuada"] = grado
                if s_key == "excelente" and c_key == "mediocre":
                    if salida_agregada["regular"] < grado:
                        salida_agregada["regular"] = grado
                if s_key == "excelente" and c_key == "pesimo":
                    if salida_agregada["ausente"] < grado:
                        salida_agregada["ausente"] = grado
                if s_key == "bueno" and c_key == "excelente":
                    if salida_agregada["generosa"] < grado:
                        salida_agregada["generosa"] = grado
                if s_key == "bueno" and c_key == "bueno":
                    if salida_agregada["generosa"] < grado:
                        salida_agregada["generosa"] = grado
                if s_key == "bueno" and c_key == "regular":
                    if salida_agregada["adecuada"] < grado:
                        salida_agregada["adecuada"] = grado
                if s_key == "bueno" and c_key == "mediocre":
                    if salida_agregada["regular"] < grado:
                        salida_agregada["regular"] = grado
                if s_key == "bueno" and c_key == "pesimo":
                    if salida_agregada["ausente"] < grado:
                        salida_agregada["ausente"] = grado
                if s_key == "regular" and c_key == "excelente":
                    if salida_agregada["generosa"] < grado:
                        salida_agregada["generosa"] = grado
                if s_key == "regular" and c_key == "bueno":
                    if salida_agregada["adecuada"] < grado:
                        salida_agregada["adecuada"] = grado
                if s_key == "regular" and c_key == "regular":
                    if salida_agregada["regular"] < grado:
                        salida_agregada["regular"] = grado
                if s_key == "regular" and c_key == "mediocre":
                    if salida_agregada["regular"] < grado:
                        salida_agregada["regular"] = grado
                if s_key == "regular" and c_key == "pesimo":
                    if salida_agregada["ausente"] < grado:
                        salida_agregada["ausente"] = grado
                if s_key == "mediocre" and c_key == "excelente":
                    if salida_agregada["adecuada"] < grado:
                        salida_agregada["adecuada"] = grado
                if s_key == "mediocre" and c_key == "bueno":
                    if salida_agregada["adecuada"] < grado:
                        salida_agregada["adecuada"] = grado
                if s_key == "mediocre" and c_key == "regular":
                    if salida_agregada["regular"] < grado:
                        salida_agregada["regular"] = grado
                if s_key == "mediocre" and c_key == "mediocre":
                    if salida_agregada["regular"] < grado:
                        salida_agregada["regular"] = grado
                if s_key == "mediocre" and c_key == "pesimo":
                    if salida_agregada["ausente"] < grado:
                        salida_agregada["ausente"] = grado
                if s_key == "pesimo" and c_key == "excelente":
                    if salida_agregada["adecuada"] < grado:
                        salida_agregada["adecuada"] = grado
                if s_key == "pesimo" and c_key == "bueno":
                    if salida_agregada["regular"] < grado:
                        salida_agregada["regular"] = grado
                if s_key == "pesimo" and c_key == "regular":
                    if salida_agregada["regular"] < grado:
                        salida_agregada["regular"] = grado
                if s_key == "pesimo" and c_key == "mediocre":
                    if salida_agregada["ausente"] < grado:
                        salida_agregada["ausente"] = grado
                if s_key == "pesimo" and c_key == "pesimo":
                    if salida_agregada["ausente"] < grado:
                        salida_agregada["ausente"] = grado

        # Defuzzificación método de centroide
        resultado = 0.0
        suma = 0.0
        for x in range(0, 16):
            μ = 0.0
            val = triangular(x, 0, 0, 5)
            if μ < min(salida_agregada["ausente"], val):
                μ = min(salida_agregada["ausente"], val)
            val = triangular(x, 0, 5, 10)
            if μ < min(salida_agregada["regular"], val):
                μ = min(salida_agregada["regular"], val)
            val = triangular(x, 5, 10, 15)
            if μ < min(salida_agregada["adecuada"], val):
                μ = min(salida_agregada["adecuada"], val)
            val = triangular(x, 14, 15, 15)
            if μ < min(salida_agregada["generosa"], val):
                μ = min(salida_agregada["generosa"], val)

            resultado += x * μ
            suma += μ

        if suma > 0:
            resultado = resultado / suma

        self.result_label.config(text=f"Propina sugerida: {resultado:.2f}%") #se muestra el resultado

if __name__ == "__main__":
    app = App()
    app.mainloop()