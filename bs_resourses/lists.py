# Copyrighting (C) 2024 by AloneBown
#
# <-This code is free software; 
# you can redistribute it and/or modify it under the terms of the license
# This code is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.->
#  
# See GNU General Public License v3.0 for more information.
# You should receive a copy of it with code or visit https://www.gnu.org/licenses/gpl-3.0.html
# (do not remove this notice)

import random

class Admiral:
    def __init__(self, r, n, s, c):
        self.r = r
        self.n = n
        self.s = s
        self.c = c

class Lists:
    def __init__(self):
        self.country = ["USA", "UK", "Russia", "Netherlands", "Spain", "Fr*nce"]
        self.gender=["0", "1"]
        self.rank=["Admiral", "Vice Admiral", "Rear Admiral", "Commodore"]
        self.usa_m_names= ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Logan", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Paul", "Steven", "Andrew", "Joshua"]
        self.usa_f_names= ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Nancy", "Margaret", "Lisa", "Betty", "Dorothy", "Sandra", "Ashley", "Kimberly", "Emily", "Donna"]
        self.usa_sur=["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Sergeant", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"]
        self.uk_m_names=["James", "John", "William", "George", "Charles", "Thomas", "Henry", "Lando", "Robert", "David", "Richard", "Joseph", "Michael", "Daniel", "Matthew", "Christopher", "Benjamin", "Samuel", "Lewis", "Oliver"]
        self.uk_f_names=["Mary", "Elizabeth", "Sarah", "Anne", "Emily", "Charlotte", "Victoria", "Margaret", "Alice", "Lucy", "Dorothy", "Helen", "Rebecca", "Eleanor", "Grace", "Lily", "Florence", "Rose", "Catherine", "Irene", "Sophia"]
        self.uk_sur=["Russell", "Jones", "Taylor", "Brown", "Williams", "Wilson", "Johnson", "Davies", "Roberts", "Thomas", "Norris", "Wright", "Hamilton", "Harris", "Martin", "Jackson", "Clarke", "White", "Walker", "Green", "Hughes", "Hall", "King", "Scott", "Moore", "Allen", "Young", "Adams", "Mitchell", "Wood", "Lee", "Thomas", "Phillips", "Baker", "Carter", "Parker", "Cooper", "Morris", "Miller", "Graham", "Davies", "Riley"]
        self.ru_m_names=["Alexei", "Dmitry", "Ivan", "Sergei", "Andrei", "Vladimir", "Nikolai", "Mikhail", "Viktor", "Yuri", "Igor", "Roman", "Maxim", "Egor", "Pavel", "Artem", "Denis", "Konstantin", "Leonid", "Boris"]
        self.ru_f_names=["Maria", "Olga", "Anna", "Irina", "Tatiana", "Elena", "Natalia", "Ekaterina", "Svetlana", "Yulia", "Victoria", "Alina", "Daria", "Ksenia", "Larisa", "Vera", "Valentina", "Galina", "Nina", "Margarita"]
        self.ru_m_sur=["Rybakov", "Kuzmin", "Cherkasov", "Zverev", "Drozdov", "Plotnikov", "Golovin", "Vorobyov", "Shestakov", "Sorokin", "Prokhorov", "Abrosimov", "Lyubimov", "Suvorov", "Krylov", "Maltsev", "Kudryavtsev", "Bykov", "Kovalev", "Ryabov", "Tsvetkov", "Ushakov", "Gavrilov", "Kudrin", "Zhdanov", "Samoylov", "Yermakov", "Malinov", "Lazarev", "Polyakov", "Arkhipov", "Alekhin", "Seleznev", "Stepashin", "Trofimov", "Yefremov", "Matveev", "Panin", "Korotkov", "Savin", "Vlasov", "Zyuganov", "Borodin", "Fokin", "Nechaev", "Starikov", "Rodionov", "Zorin", "Laptev", "Mokhov"]
        self.ru_f_sur=["Rybakova", "Kuzmina", "Cherkasova", "Zvereva", "Drozdova", "Plotnikova", "Golovina", "Vorobyova", "Shestakova", "Sorokina", "Prokhorova", "Abrosimova", "Lyubimova", "Suvorova", "Krylova", "Maltseva", "Kudryavtseva", "Bykova", "Kovaleva", "Ryabova", "Tsvetkova", "Ushakova", "Gavrilova", "Kudrina", "Zhdanova", "Samoylova", "Yermakova", "Malinova", "Lazareva", "Polyakova", "Arkhipova", "Alekhina", "Selezneva", "Stepashina", "Trofimova", "Yefremova", "Matveeva", "Panina", "Korotkova", "Savina", "Vlasova", "Zyuganova", "Borodina", "Fokina", "Nechaeva", "Starikova", "Rodionova", "Zorina", "Lapteva", "Mokhova"]
        self.nl_m_names=["Jan", "Johan", "Willem", "Pieter", "Hendrik", "Cornelis", "Dirk", "Geert", "Kees", "Arjen", "Max", "Bart", "Lars", "Maarten", "Sander", "Thijs", "Koen", "Jasper", "Floris", "Ruben"]
        self.nl_f_names=["Anne", "Emma", "Sofie", "Maria", "Hendrika", "Cornelia", "Petronella", "Lotte", "Femke", "Elise", "Sanne", "Tessa", "Iris", "Esmee", "Marijke", "Roos", "Merel", "Eva", "Fleur", "Anouk"]
        self.nl_sur=["De Vries", "Van den Berg", "Jansen", "Visser", "Van Dijk", "Bakker", "Smit", "Meijer", "Mulder", "De Boer", "Kok", "Verstappen", "Schouten", "Hendriks", "Van Leeuwen", "Kramer", "Vos", "Van der Meer", "Kuiper", "Dekker","Hoekstra", "Brouwer", "Timmermans", "Van der Veen", "Scholten", "Van Dam", "Veldhuis", "Prins", "Verhoeven", "Blom", "Zijlstra", "Langenberg", "De Lange", "Van der Wal", "Postma", "Van Loon", "Heemskerk", "Vogel", "Ruijter", "De Koning", "Groen", "Van der Pol", "Wouters", "Zegers", "Van der Linden", "Boerma", "Sneijders", "Meijers", "Hooft", "De Ruiter"]
        self.es_m_names=["José", "Antonio", "Manuel", "Francisco", "Juan", "Javier", "Carlos", "David", "Pedro", "Jesús", "Álvaro", "Luis", "Sergio", "Fernando", "Pablo", "Raúl", "Jorge", "Rubén", "Adrián", "Alejandro"]
        self.es_f_names=["María", "Carmen", "Ana", "Laura", "Isabel", "Cristina", "Lucía", "Pilar", "Elena", "Rosa", "Silvia", "Teresa", "Paula", "Sara", "Clara", "Eva", "Inés", "Natalia", "Marta", "Victoria"]
        self.es_sur=["García", "Martínez", "López", "Sánchez", "Pérez", "Rodríguez", "Fernández", "Gómez", "Ruiz", "Hernández", "Díaz", "Álvarez", "Jiménez", "Moreno", "Muñoz", "Romero", "Vázquez", "Navarro", "Torres", "Domínguez", "Cano", "Ortega", "Castro", "Silva", "Vega", "Sainz", "Santiago", "Marín", "Iglesias", "Campos","Solís", "Roldán", "Pineda", "Valero", "Esteban", "Gallego", "Ferrer", "Blanco", "Calvo", "Carrasco", "Villanueva", "Quintana", "Salazar", "Bautista", "Suárez", "Delgado", "Luna", "Santana", "Cabezas", "Esparza"]
        self.fr_m_names=["Louis", "Gabriel", "Arthur", "Jules", "Léo", "Lucas", "Hugo", "Raphaël", "Nathan", "Théo", "Paul", "Maxime", "Antoine", "Thomas", "Clément", "Alexandre", "Charles", "Matéo", "Benjamin", "Émile"]
        self.fr_r_names=["Marie", "Camille", "Chloé", "Emma", "Léa", "Manon", "Julie", "Alice", "Élise", "Sophie", "Lucie", "Anna", "Claire", "Charlotte", "Jeanne", "Pauline", "Margaux", "Mathilde", "Aurore", "Émilie"]
        self.fr_m_sur=["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau","Simon", "Laurent", "Michel", "Garcia", "Roux", "David", "Bertrand", "Girard", "Garnier", "Lambert","Fontaine", "Chevalier", "Perrot", "François", "Marchand", "Aubert", "Blanc", "Dufour", "Mercier", "Moulin","Leclerc", "Robin", "Benoît", "Gaillard", "Renard", "Dumas", "Baron", "Gautier", "Noël", "Vidal","Chauvet", "Delacroix", "Dupuis", "Ferrand", "Pichon", "Sauvage", "Carpentier", "Monet", "Renaud", "Tristan"]
        self.fr_f_sur=["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petite", "Durande", "Leroye", "Moreaux","Simone", "Laurente", "Michele", "Garcie", "Rousse", "Davide", "Bertrande", "Girarde", "Garnie", "Lamberte","Fontaine", "Chevalière", "Perrote", "Françoise", "Marchande", "Auberte", "Blanche", "Dufoure", "Mercière", "Mouline","Leclercque", "Robine", "Benoîte", "Gaillarde", "Renarde", "Dumase", "Baronne", "Gautière", "Noëlle", "Vidale","Chauvette", "Delacroixe", "Dupuisse", "Ferrande", "Pichonne", "Sauvageonne", "Carpentière", "Monette", "Renaude", "Tristane"]
    
    def ai_admirals_randomiser(self):
        c = random.choice(self.country)
        g = random.choice(self.gender)
        r = random.choice(self.rank)
        if c == "USA":
            c="United States Navy"
            if g == "0":
                n = random.choice(self.usa_m_names); s = random.choice(self.usa_sur)
            else:    
                n = random.choice(self.usa_f_names); s = random.choice(self.usa_sur)
        elif c == "UK":
            c="Royal Navy"
            if g == "0":
                n = random.choice(self.uk_m_names); s = random.choice(self.uk_sur)
            else:    
                n = random.choice(self.uk_f_names); s = random.choice(self.uk_sur)
        elif c == "Russia":
            c="Rossiiskii Voenno-Morskoi Flot"
            if g == "0":
                n = random.choice(self.ru_m_names); s = random.choice(self.ru_m_sur)
            else:    
                n = random.choice(self.ru_f_names); s = random.choice(self.ru_f_sur)
        elif c == "Netherlands":
            c="Koninklijke Marine"
            if g == "0":
                n = random.choice(self.nl_m_names); s = random.choice(self.nl_sur)
            else:    
                n = random.choice(self.nl_f_names); s = random.choice(self.nl_sur)
        elif c == "Spain":
            c="Armada Española"
            if g == "0":
                n = random.choice(self.es_m_names); s = random.choice(self.es_sur)
            else:    
                n = random.choice(self.es_f_names); s = random.choice(self.es_sur)
        elif c == "Fr*nce":
            c="Marine Nationale"
            if g == "0":
                n = random.choice(self.fr_m_names); s = random.choice(self.fr_m_sur)
            else:    
                n = random.choice(self.fr_r_names); s = random.choice(self.fr_f_sur)
    
        return Admiral(r, n, s, c)