import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Calculadora de Propinas')
        self.geometry('500x500')
        ## self.eval('tk::PlaceWindow . center')
        self.frames = {}

        for F in (SplashScreen, ComidaScreen, ServicioScreen, ResultadoScreen):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')

        self.show_frame(SplashScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

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
        self.after(2000, lambda: parent.show_frame(ComidaScreen))

class StarRating(tk.Frame):
    def __init__(self, parent, label_text, callback, bg_image):
        super().__init__(parent)
        self.rating = 0
        self.callback = callback

        meanings = ['Pésimo', 'Mediocre', 'Regular', 'Bueno', 'Excelente']
        self.stars = []

        bg_img = Image.open(bg_image).resize((500, 500))
        self.bg_img = ImageTk.PhotoImage(bg_img)
        canvas = tk.Canvas(self, width = 500, height = 500)
        canvas.create_image(0, 0, image = self.bg_img, anchor = 'nw')
        canvas.pack(fill = 'both', expand = True)

        label = tk.Label(self, text = label_text, font = ('Arial', 18))
        canvas.create_window(250, 50, window = label)

        for i in range(5):
            star_label = tk.Label(self, text = '☆', font = ('Arial', 40))
            star_label.bind('<Button-1>', lambda e, idx = i: self.set_rating(idx + 1))
            canvas.create_window(100 + i * 60, 200, window = star_label)
            self.stars.append(star_label)

            meaning = tk.Label(self, text = meanings[i], font = ('Arial', 10))
            canvas.create_window(100 + i * 60, 250, window = meaning)

        self.next_btn = tk.Button(self, text = 'Aceptar', command = self.next_screen, state = 'disabled', 
                                  bg = '#e74c3c', fg = '#f7f7f7', font = ('Arial', 12, 'bold'), relief = 'raised', bd = 5, 
                                  padx = 10, pady = 5, borderwidth = 4, highlightbackground = '#ff4500')
        canvas.create_window(250, 350, window = self.next_btn)

    def set_rating(self, rating):
        self.rating = rating
        for i, star_label in enumerate(self.stars):
            star_label.config(text = '★' if i < rating else '☆', fg = '#f1c40f')
        self.next_btn.config(state = 'normal')

    def next_screen(self):
        self.callback(self.rating)

class ComidaScreen(StarRating):
    def __init__(self, parent):
        super().__init__(parent, 'Evalúa la Comida', self.save_rating, 'fondo.jpg')

    def save_rating(self, rating):
        self.master.comida_rating = rating
        self.master.show_frame(ServicioScreen)

class ServicioScreen(StarRating):
    def __init__(self, parent):
        super().__init__(parent, 'Evalúa el Servicio', self.save_rating, 'mesero.jpg')

    def save_rating(self, rating):
        self.master.servicio_rating = rating
        self.master.show_frame(ResultadoScreen)

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

    def calculate_tip(self):
        comida = self.master.comida_rating
        servicio = self.master.servicio_rating

        # Lógica difusa
        servicio_var = ctrl.Antecedent(np.arange(1, 6, 1), 'servicio') 
        comida_var = ctrl.Antecedent(np.arange(1, 6, 1), 'comida')     
        propina = ctrl.Consequent(np.arange(0, 16, 1), 'propina')

        servicio_var['pesimo'] = fuzz.trimf(servicio_var.universe, [1, 1, 2])
        servicio_var['mediocre'] = fuzz.trimf(servicio_var.universe, [1, 2, 3])
        servicio_var['regular'] = fuzz.trimf(servicio_var.universe, [2, 3, 4])
        servicio_var['bueno'] = fuzz.trimf(servicio_var.universe, [3, 4, 5])
        servicio_var['excelente'] = fuzz.trimf(servicio_var.universe, [4, 5, 5]) 

        comida_var['pesimo'] = fuzz.trimf(comida_var.universe, [1, 1, 2])
        comida_var['mediocre'] = fuzz.trimf(comida_var.universe, [1, 2, 3])
        comida_var['regular'] = fuzz.trimf(comida_var.universe, [2, 3, 4])
        comida_var['bueno'] = fuzz.trimf(comida_var.universe, [3, 4, 5])
        comida_var['excelente'] = fuzz.trimf(comida_var.universe, [4, 5, 5])  

        propina['Ausente'] = fuzz.trimf(propina.universe, [0, 0, 5])
        propina['Regular'] = fuzz.trimf(propina.universe, [0, 5, 10])
        propina['Adecuada'] = fuzz.trimf(propina.universe, [5, 10, 15])  
        propina['Generosa'] = fuzz.trapmf(propina.universe, [14, 15, 15, 15])  

        reglas = [
            ctrl.Rule(servicio_var['excelente'] & comida_var['excelente'], propina['Generosa']),
            ctrl.Rule(servicio_var['excelente'] & comida_var['bueno'], propina['Generosa']),
            ctrl.Rule(servicio_var['excelente'] & comida_var['regular'], propina['Adecuada']),
            ctrl.Rule(servicio_var['excelente'] & comida_var['mediocre'], propina['Regular']),
            ctrl.Rule(servicio_var['excelente'] & comida_var['pesimo'], propina['Ausente']),
            
            ctrl.Rule(servicio_var['bueno'] & comida_var['excelente'], propina['Generosa']),
            ctrl.Rule(servicio_var['bueno'] & comida_var['bueno'], propina['Generosa']),
            ctrl.Rule(servicio_var['bueno'] & comida_var['regular'], propina['Adecuada']),
            ctrl.Rule(servicio_var['bueno'] & comida_var['mediocre'], propina['Regular']),
            ctrl.Rule(servicio_var['bueno'] & comida_var['pesimo'], propina['Ausente']),
            
            ctrl.Rule(servicio_var['regular'] & comida_var['excelente'], propina['Generosa']),
            ctrl.Rule(servicio_var['regular'] & comida_var['bueno'], propina['Adecuada']),
            ctrl.Rule(servicio_var['regular'] & comida_var['regular'], propina['Regular']),
            ctrl.Rule(servicio_var['regular'] & comida_var['mediocre'], propina['Regular']),
            ctrl.Rule(servicio_var['regular'] & comida_var['pesimo'], propina['Ausente']),
            
            ctrl.Rule(servicio_var['mediocre'] & comida_var['excelente'], propina['Adecuada']),
            ctrl.Rule(servicio_var['mediocre'] & comida_var['bueno'], propina['Adecuada']),
            ctrl.Rule(servicio_var['mediocre'] & comida_var['regular'], propina['Regular']),
            ctrl.Rule(servicio_var['mediocre'] & comida_var['mediocre'], propina['Regular']),
            ctrl.Rule(servicio_var['mediocre'] & comida_var['pesimo'], propina['Ausente']),
            
            ctrl.Rule(servicio_var['pesimo'] & comida_var['excelente'], propina['Adecuada']),
            ctrl.Rule(servicio_var['pesimo'] & comida_var['bueno'], propina['Regular']),
            ctrl.Rule(servicio_var['pesimo'] & comida_var['regular'], propina['Regular']),
            ctrl.Rule(servicio_var['pesimo'] & comida_var['mediocre'], propina['Ausente']),
            ctrl.Rule(servicio_var['pesimo'] & comida_var['pesimo'], propina['Ausente']),
        ]

        sistema = ctrl.ControlSystem(reglas)
        sim = ctrl.ControlSystemSimulation(sistema)

        sim.input['servicio'] = servicio
        sim.input['comida'] = comida
        sim.compute()

        self.result_label.config(text = f"Propina sugerida: {sim.output['propina']:.2f}%")

if __name__ == "__main__":
    app = App()
    app.mainloop()