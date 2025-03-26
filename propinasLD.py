import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Propinas")
        self.geometry("800x600")
        self.frames = {}

        for F in (SplashScreen, ComidaScreen, ServicioScreen, ResultadoScreen):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SplashScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class SplashScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg='white')
        tk.Label(self, text="Calculadora de Propinas", font=("Arial", 32), bg='white').pack(expand=True)
        self.after(2000, lambda: parent.show_frame(ComidaScreen))

class StarRating(tk.Frame):
    def __init__(self, parent, label_text, callback):
        super().__init__(parent)
        self.rating = 0
        self.callback = callback

        meanings = ["Pesimo", "Mediocre", "Regular", "Bueno", "Excelente"]
        self.stars = []

        bg_img = Image.open("comida.png").resize((800, 600))
        self.bg_img = ImageTk.PhotoImage(bg_img)
        canvas = tk.Canvas(self, width=800, height=600)
        canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        canvas.pack(fill="both", expand=True)

        label = tk.Label(self, text=label_text, font=("Arial", 24), bg='#ffffff')
        canvas.create_window(400, 50, window=label)

        for i in range(5):
            star_label = tk.Label(self, text="☆", font=("Arial", 50), bg='#ffffff')
            star_label.bind("<Button-1>", lambda e, idx=i: self.set_rating(idx + 1))
            canvas.create_window(150 + i * 100, 200, window=star_label)
            self.stars.append(star_label)

            meaning = tk.Label(self, text=meanings[i], font=("Arial", 12), bg='#ffffff')
            canvas.create_window(150 + i * 100, 280, window=meaning)

        self.next_btn = tk.Button(self, text="Siguiente", command=self.next_screen, state="disabled")
        canvas.create_window(400, 350, window=self.next_btn)

    def set_rating(self, rating):
        self.rating = rating
        for i, star_label in enumerate(self.stars):
            star_label.config(text="★" if i < rating else "☆", fg="gold", bg="transparent")
        self.next_btn.config(state="normal")

    def next_screen(self):
        self.callback(self.rating)

class ComidaScreen(StarRating):
    def __init__(self, parent):
        super().__init__(parent, "Evalúa la Comida", self.save_rating)

    def save_rating(self, rating):
        self.master.comida_rating = rating
        self.master.show_frame(ServicioScreen)

class ServicioScreen(StarRating):
    def __init__(self, parent):
        super().__init__(parent, "Evalúa el Servicio", self.save_rating)

    def save_rating(self, rating):
        self.master.servicio_rating = rating
        self.master.show_frame(ResultadoScreen)

class ResultadoScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.result_label = tk.Label(self, text="", font=("Arial", 24))
        self.result_label.pack(pady=50)
        tk.Button(self, text="Calcular Propina", command=self.calculate_tip).pack()

    def calculate_tip(self):
        comida = self.master.comida_rating
        servicio = self.master.servicio_rating

        # Lógica difusa
        servicio_var = ctrl.Antecedent(np.arange(1, 5, 1), 'servicio')
        comida_var = ctrl.Antecedent(np.arange(1, 5, 1), 'comida')
        propina = ctrl.Consequent(np.arange(0, 15, 1), 'propina')

        servicio_var.automf(3)
        comida_var.automf(3)

        #Rangos de propinas
        propina['Ausente'] = fuzz.trimf(propina.universe, [0, 0, 5])
        propina['Regular'] = fuzz.trimf(propina.universe, [0, 5, 10])
        propina['Adecuada'] = fuzz.trimf(propina.universe, [5, 10, 15])
        propina['Generosa'] = fuzz.trimf(propina.universe, [10, 15, 20])

        #Reglas
        regla1 = ctrl.Rule(servicio_var['poor'] & comida_var['poor'], propina['Generosa'])
        regla2 = ctrl.Rule(servicio_var['average'] & comida_var['average'], propina['Generosa'])
        regla3 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Adecuada'])
        regla4 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Regular'])
        regla5 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Ausente'])

        regla6 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Generosa'])
        regla7 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Generosa'])
        regla8 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Adecuada'])
        regla9 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Regular'])
        regla10 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Ausente'])

        regla11 = ctrl.Rule(servicio_var['poor'] & comida_var['poor'], propina['Generosa'])
        regla12 = ctrl.Rule(servicio_var['average'] & comida_var['average'], propina['Adecuada'])
        regla13 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Regular'])
        regla14 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Regular'])
        regla15 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Ausente'])

        regla16 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Adecuada'])
        regla17 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Adecuada'])
        regla18 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Regular'])
        regla19 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Regular'])
        regla20 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Ausente'])

        regla21 = ctrl.Rule(servicio_var['poor'] & comida_var['poor'], propina['Adecuada'])
        regla22 = ctrl.Rule(servicio_var['average'] & comida_var['average'], propina['Regular'])
        regla23 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Regular'])
        regla24 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Ausente'])
        regla25 = ctrl.Rule(servicio_var['good'] & comida_var['good'], propina['Ausente'])

        sistema = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8, regla9, regla10, regla11,
                                      regla12, regla13, regla14, regla15, regla16, regla17, regla18, regla19, regla20, 
                                       regla21, regla22, regla23, regla24, regla25 ])
        sim = ctrl.ControlSystemSimulation(sistema)

        sim.input['servicio'] = servicio
        sim.input['comida'] = comida
        sim.compute()

        self.result_label.config(text=f"Propina sugerida: {sim.output['propina']:.4f}%")

if __name__ == "__main__":
    app = App()
    app.mainloop()
