import random

import pygame

pygame.init()
icon = pygame.image.load("icon.png")

screen = pygame.display.set_mode((1280, 660))
pygame.display.set_caption("Respiration!")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Times New Roman", 18)
mouse_holding = False
mouse_holding_2 = False


class Button:
    def __init__(self, position, color, name, toggle = False, pressed = False):
        self.color = color
        self.font = pygame.font.SysFont("Times New Roman", 18)
        self.name = self.font.render(name, False, (0, 0, 0))
        self.sname = name
        self.height = self.name.get_height() + 2
        self.position = position
        self.tex_pos = (self.position[0], self.position[1])
        self.rectpos = (self.position[0], self.position[1])
        self.toggle = toggle
        self.pressed = pressed

    def draw(self):
        color = self.color
        if self.pressed == True:
            color = (self.color[0] - 65, self.color[1] - 65, self.color[2] - 65)
        elif self.pressed == False:
            color = self.color
        pygame.draw.circle(screen, color, (self.position[0], self.position[1] + self.height / 2), self.height / 2)
        pygame.draw.circle(screen, color, (self.position[0] + self.name.get_width(), self.position[1] + self.height / 2), self.height / 2)
        pygame.draw.rect(screen, color, [self.rectpos[0] - 1, self.rectpos[1] - 1, self.name.get_width() + 2, self.height])
        screen.blit(self.name, self.tex_pos)

    def click(self):
        if self.pressed == True and self.toggle == False:
            self.pressed = False
        if self.position[0] < pygame.mouse.get_pos()[0] < self.position[0] + self.name.get_width() and self.position[1] < pygame.mouse.get_pos()[1] < self.position[1] + self.name.get_height():
            if mouse_click_2:
                if self.toggle == True:
                    self.pressed = not self.pressed
                elif self.toggle == False and self.pressed == False:
                    self.pressed = True


class Mitochondria:
    def __init__(self, name, image, position, show = True, containing_chemicals = None):
        self.name = font.render(name, False, (255, 255, 255))
        image = pygame.image.load(image)
        self.image = pygame.transform.rotate(image, random.randint(-10, 10))
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / 4, self.image.get_height() / 4))
        self.position = position
        self.show = show
        desc = 'Mitochondria: An organelle inside eukaryotic organisms that conducts Aerobic metabolism and produces Adenosine Triphosphate.'
        self.desctext = font.render(desc, False, (0, 0, 0), (255, 255, 255))
        if containing_chemicals == None:
            self.containing_chemicals = []
        else:
            self.containing_chemicals = containing_chemicals


    def randmidpos(self, brand, rand):
        return (self.position[0] + (self.image.get_width() / 2) + random.randint(brand, rand), self.position[1] + (self.image.get_height() / 2) + random.randint(brand, rand))

    def update(self):
        global mouse_holding, oxygenated_mitochondria, mitochondria_desc
        if self.show:
            screen.blit(self.image, self.position)
            if self.position[0] < pygame.mouse.get_pos()[0] < self.position[0] + self.image.get_width() and self.position[1] < pygame.mouse.get_pos()[1] < self.position[1] + self.image.get_height():
                screen.blit(self.desctext, (20, 600))
                mitochondria_desc = True
            going_through_chems = 0
            chem_names = []
            chems = []
            while going_through_chems < len(chemical_list):
                chem = chemical_list[going_through_chems]
                chempos = (chem.position[0] + chem.image.get_width() / 2, chem.position[1] + chem.image.get_height() / 2)
                if chem.going_to_mouse == False:
                    if self.position[0] < chempos[0] < self.position[0] + self.image.get_width() and self.position[1] < chempos[1] < self.position[1] + self.image.get_height() and chem.show:
                        if chem.on_mitochondria == 0:
                            chem.on_mitochondria = 1
                            chem.on_cytoplasm = 0
                            chem.on_chloroplast = 0
                        if chem.on_mitochondria == 1:
                            self.containing_chemicals.append(chemical_list[going_through_chems])
                            chem_names.append(chem.str_name)
                            chems.append(chem)
                    elif chem.show:
                        if self.containing_chemicals.count(chem) > 0:
                            self.containing_chemicals.remove(chem)
                        chem_names.append(" ")
                        chems.append(" ")
                going_through_chems += 1
            if chem_names.count("Molecular Oxygen") >= 6:
                if oxygenated_mitochondria == 1:
                    oxygenated_mitochondria = 2
                elif oxygenated_mitochondria == 0:
                    oxygenated_mitochondria = 1
                if chem_names.count("Glucose") >= 1:
                    remo = 0
                    chems[chem_names.index("Glucose")].disappear()
                    chems[chem_names.index("Glucose")].on_mitochondria = 0
                    self.containing_chemicals.remove(chems[chem_names.index("Glucose")])
                    chems.remove(chems[chem_names.index("Glucose")])
                    chem_names.remove("Glucose")
                    while remo < 6:
                        chems[chem_names.index("Molecular Oxygen")].disappear()
                        chems[chem_names.index("Molecular Oxygen")].on_mitochondria = 0
                        self.containing_chemicals.remove(chems[chem_names.index("Molecular Oxygen")])
                        chems.remove(chems[chem_names.index("Molecular Oxygen")])
                        chem_names.remove("Molecular Oxygen")
                        remo += 1
                    atp_count = 0
                    while atp_count < 36:
                        make_atp(self.randmidpos(-50, 50), random.randint(-2, 2), random.randint(-2, 2))
                        atp_count += 1
                    c_c = 0
                    while c_c < 6:
                        make_water(self.randmidpos(-30, 30), 0, random.randint(-12, -4))
                        make_carbon_dioxide(self.randmidpos(-30, 30), 0, random.randint(-12, -4))
                        c_c += 1
            elif chem_names.count("Molecular Oxygen") < 5:
                if oxygenated_mitochondria == 1:
                    oxygenated_mitochondria = 0
                elif oxygenated_mitochondria == 2:
                    oxygenated_mitochondria = 1

mitochondria_desc = False


class Chloroplast:
    def __init__(self, name, image, position, show = True, containing_chemicals = None):
        self.name = font.render(name, False, (255, 255, 255))
        image = pygame.image.load(image)
        self.image = pygame.transform.rotate(image, random.randint(-10, 10))
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / 3, self.image.get_height() / 3))
        self.position = position
        self.show = show
        desc = 'Chloroplast: An organelle inside some cells of the organisms in the kingdom Plantae. This is the place of photosynthesis.'
        self.desctext = font.render(desc, False, (0, 0, 0), (255, 255, 255))
        if containing_chemicals == None:
            self.containing_chemicals = []
        else:
            self.containing_chemicals = containing_chemicals

    def randmidpos(self, brand, rand):
        return (self.position[0] + (self.image.get_width() / 2) + random.randint(brand, rand), self.position[1] + (self.image.get_height() / 2) + random.randint(brand, rand))

    def update(self):
        global mouse_holding
        if self.show:
            screen.blit(self.image, self.position)
            if self.position[0] < pygame.mouse.get_pos()[0] < self.position[0] + self.image.get_width() and self.position[1] < pygame.mouse.get_pos()[1] < self.position[1] + self.image.get_height() and not chem_desc:
                screen.blit(self.desctext, (20, 600))
            going_through_chems = 0
            chem_names = []
            chems = []
            while going_through_chems < len(chemical_list):
                chem = chemical_list[going_through_chems]
                chempos = (chem.position[0] + chem.image.get_width() / 2, chem.position[1] + chem.image.get_height() / 2)
                if chem.going_to_mouse == False:
                    if self.position[0] < chempos[0] < self.position[0] + self.image.get_width() and self.position[1] < chempos[1] < self.position[1] + self.image.get_height() and chem.show:
                        if chem.on_chloroplast == 0:
                            self.containing_chemicals.append(chemical_list[going_through_chems])
                            chem.on_chloroplast = 1
                            chem.on_cytoplasm = 0
                            chem.on_mitochondria = 0
                        if chem.on_chloroplast == 1:
                            self.containing_chemicals.append(chemical_list[going_through_chems])
                            chem_names.append(chem.str_name)
                            chems.append(chem)
                    elif chem.on_chloroplast == 0:
                        if self.containing_chemicals.count(chem) > 0:
                            self.containing_chemicals.remove(chem)
                        chem.on_chloroplast = 0
                        chem_names.append(" ")
                        chems.append(" ")
                going_through_chems += 1
            if sunlight:
                if chem_names.count("Carbon Dioxide") >= 6:
                    if chem_names.count("Water") >= 6:
                        remo = 0
                        while remo < 6:
                            chems[chem_names.index("Carbon Dioxide")].disappear()
                            chems[chem_names.index("Carbon Dioxide")].on_cytoplasm = 0
                            self.containing_chemicals.remove(chems[chem_names.index("Carbon Dioxide")])
                            chems.remove(chems[chem_names.index("Carbon Dioxide")])
                            chem_names.remove("Carbon Dioxide")
                            chems[chem_names.index("Water")].disappear()
                            chems[chem_names.index("Water")].on_cytoplasm = 0
                            self.containing_chemicals.remove(chems[chem_names.index("Water")])
                            chems.remove(chems[chem_names.index("Water")])
                            chem_names.remove("Water")
                            remo += 1
                        make_glucose(self.randmidpos(-30, 30), 0, random.randint(3, 8))
                        c_c = 0
                        while c_c < 6:
                            make_mol_oxygen(self.randmidpos(-30, 30), 0, random.randint(4, 12))
                            c_c += 1
            elif not sunlight:
                if chem_names.count("Glucose") >= 1:
                    if chem_names.count("Molecular Oxygen") >= 6:
                        chems[chem_names.index("Glucose")].disappear()
                        chems[chem_names.index("Glucose")].on_mitochondria = 0
                        self.containing_chemicals.remove(chems[chem_names.index("Glucose")])
                        chems.remove(chems[chem_names.index("Glucose")])
                        chem_names.remove("Glucose")
                        remo = 0
                        while remo < 6:
                            chems[chem_names.index("Molecular Oxygen")].disappear()
                            chems[chem_names.index("Molecular Oxygen")].on_mitochondria = 0
                            self.containing_chemicals.remove(chems[chem_names.index("Molecular Oxygen")])
                            chems.remove(chems[chem_names.index("Molecular Oxygen")])
                            chem_names.remove("Molecular Oxygen")
                            remo += 1
                        atp_count = 0
                        while atp_count < 32:
                            make_atp(self.randmidpos(-30, 30), random.randint(-2, 2), random.randint(-2, 2))
                            atp_count += 1
                        c_c = 0
                        while c_c < 6:
                            make_water(self.randmidpos(-30, 30), 0, random.randint(-8, -4))
                            make_carbon_dioxide(self.randmidpos(-30, 30), 0, random.randint(-8, -4))
                            c_c += 1
            if chem_names.count("Adenosine Triphosphate") >= random.randint(1, 60):
                remo = 0
                while remo < 1:
                    chems[chem_names.index("Adenosine Triphosphate")].disappear()
                    chems[chem_names.index("Adenosine Triphosphate")].on_cytoplasm = 0
                    self.containing_chemicals.remove(chems[chem_names.index("Adenosine Triphosphate")])
                    chems.remove(chems[chem_names.index("Adenosine Triphosphate")])
                    chem_names.remove("Adenosine Triphosphate")
                    remo += 1


class Sun:
    def __init__(self, position, pressed=False):
        self.position = position
        self.name = "Sun"
        self.toggle = True
        self.pressed = pressed
        self.image1 = pygame.image.load("sun.png")
        self.image2 = pygame.image.load("moon.png")
        desc = 'Sun: Producer of the light essential for photosynthesis.'
        desc2 = 'Moon: Overwatcher of the night; when the moon is out and there is no sun, photosynthesis cannot be naturally conducted'
        self.desctext = font.render(desc, False, (0, 0, 0), (255, 255, 255))
        self.desctext2 = font.render(desc2, False, (0, 0, 0), (255, 255, 255))

    def draw(self):
        if self.pressed == True:
            screen.blit(self.image1, self.position)
        elif self.pressed == False:
            screen.blit(self.image2, self.position)

    def click(self):
        if self.position[0] < pygame.mouse.get_pos()[0] < self.position[0] + self.image1.get_width() and self.position[1] < pygame.mouse.get_pos()[1] < self.position[1] + self.image1.get_height():
            if self.pressed:
                screen.blit(self.desctext, (20, 600))
            if not self.pressed:
                screen.blit(self.desctext2, (20, 600))
            if mouse_click_2:
                self.pressed = not self.pressed


class Cytoplasm:
    def __init__(self, name, image, position, show = True, containing_chemicals = None):
        self.name = font.render(name, False, (255, 255, 255))
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / 3, self.image.get_height() / 3))
        self.position = position
        self.show = show
        desc = 'Cytoplasm: The place where anaerobic metabolism occurs.'
        self.desctext = font.render(desc, False, (0, 0, 0), (255, 255, 255))
        if containing_chemicals == None:
            self.containing_chemicals = []
        else:
            self.containing_chemicals = containing_chemicals

    def randmidpos(self, brand, rand):
        return (self.position[0] + (self.image.get_width() / 2) + random.randint(brand, rand), self.position[1] + (self.image.get_height() / 2) + random.randint(brand, rand))


    def update(self):
        global mouse_holding, mitochondria_1
        if self.show:
            screen.blit(self.image, self.position)
            if self.position[0] < pygame.mouse.get_pos()[0] < self.position[0] + self.image.get_width() and self.position[1] < pygame.mouse.get_pos()[1] < self.position[1] + self.image.get_height() and not mitochondria_desc and not chem_desc:
                screen.blit(self.desctext, (20, 600))
            going_through_chems = 0
            chem_names = []
            chems = []
            while going_through_chems < len(chemical_list):
                chem = chemical_list[going_through_chems]
                chempos = (chem.position[0] + chem.image.get_width() / 2, chem.position[1] + chem.image.get_height() / 2)
                if chemical_list[going_through_chems].going_to_mouse == False:
                    if self.position[0] < chempos[0] < self.position[0] + self.image.get_width() and self.position[1] < chempos[1] < self.position[1] + self.image.get_height() and chem.on_cytoplasm == 0:
                        self.containing_chemicals.append(chemical_list[going_through_chems])
                        chem.on_cytoplasm = 1
                        chem.on_chloroplast = 0
                    if chem.str_name == "Glucose" or chem.str_name == "Molecular Oxygen":
                        if chem.on_cytoplasm and not chem.on_mitochondria:
                            if chem.position[0] < self.position[0] + (self.image.get_width() / 2):
                                chem.xvel -= (chem.position[0] - mitochondria_2.position[0] - (mitochondria_2.image.get_width() / 2)) / 2800
                                chem.yvel -= (chem.position[1] - mitochondria_2.position[1] - (mitochondria_2.image.get_height() / 2)) / 2800
                            if chem.position[0] > self.position[0] + (self.image.get_width() / 2):
                                chem.xvel -= (chem.position[0] - mitochondria_1.position[0] - (mitochondria_1.image.get_width() / 2)) / 2800
                                chem.yvel -= (chem.position[1] - mitochondria_1.position[1] - (mitochondria_1.image.get_height() / 2)) / 2800
                elif not self.position[0] < chempos[0] < self.position[0] + self.image.get_width() and not self.position[1] < chempos[1] < self.position[1] + self.image.get_height():
                    if self.containing_chemicals.count(chem) > 0:
                        self.containing_chemicals.remove(chem)
                    chem.on_cytoplasm = 0
                if chem.on_cytoplasm == 1 and chem.show:
                    chem_names.append(chem.str_name)
                    chems.append(chem)
                else:
                    chem_names.append(" ")
                    chems.append(" ")
                going_through_chems += 1
            if chem_names.count("Adenosine Triphosphate") >= random.randint(1, 40):
                remo = 0
                while remo < 1:
                    chems[chem_names.index("Adenosine Triphosphate")].disappear()
                    chems[chem_names.index("Adenosine Triphosphate")].on_cytoplasm = 0
                    self.containing_chemicals.remove(chems[chem_names.index("Adenosine Triphosphate")])
                    del chems[chem_names.index("Adenosine Triphosphate")]
                    chems.remove(chems[chem_names.index("Adenosine Triphosphate")])
                    chem_names.remove("Adenosine Triphosphate")
                    remo += 1
            if chem_names.count("Molecular Oxygen") >= 2 and oxygenated_mitochondria == 0:
                if chem_names.count("Glucose") >= 1:
                    try:
                        remo = 0
                        chems[chem_names.index("Glucose")].disappear()
                        chems[chem_names.index("Glucose")].on_cytoplasm = 0
                        self.containing_chemicals.remove(chems[chem_names.index("Glucose")])
                        chems.remove(chems[chem_names.index("Glucose")])
                        chem_names.remove("Glucose")
                        while remo < 2:
                            chems[chem_names.index("Molecular Oxygen")].disappear()
                            chems[chem_names.index("Molecular Oxygen")].on_cytoplasm = 0
                            self.containing_chemicals.remove(chems[chem_names.index("Molecular Oxygen")])
                            chems.remove(chems[chem_names.index("Molecular Oxygen")])
                            chem_names.remove("Molecular Oxygen")
                            remo += 1
                        atp_count = 0
                        while atp_count < 2:
                            make_atp(self.randmidpos(-50, 50), random.randint(-2, 2), random.randint(-2, 2))
                            atp_count += 1
                        c_c = 0
                        while c_c < 2:
                            make_lactic_acid(self.randmidpos(-30, 30), random.randint(-3, 3), random.randint(-3, 3))
                            c_c += 1
                    except:
                        pass


class Producer:

    def __init__(self, position, product, name, color, producing = False):
        self.name = font.render(name, False, (0, 0, 0))
        self.str_name = name
        self.position = position
        self.going_to_mouse = False
        self.color = color
        self.producing = producing
        self.product = product
        self.cyc = 0
        self.interval = 100
        self.pressed = False
        self.toggle = True

    def update(self):
        global mouse_holding
        self.cyc += 1

        if self.cyc >= self.interval:
            self.cyc = 0
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.name.get_width(), self.name.get_height()))
        if not self.pressed:
            pygame.draw.circle(screen, (30, 30, 30), (self.position[0] - self.name.get_height() / 2, self.position[1] + (self.name.get_height() / 2)), self.name.get_height() / 2)
        elif self.pressed:
            pygame.draw.circle(screen, self.color, (self.position[0] - self.name.get_height() / 2, self.position[1] + (self.name.get_height() / 2)), self.name.get_height() / 2)
        pygame.draw.line(screen, self.color, (self.position[0] + self.name.get_width(), (self.position[1] + (self.name.get_height() / 2))), (self.position[0] + self.name.get_width() + 15, (self.position[1] + (self.name.get_height() / 2))), 3)
        screen.blit(self.name, self.position)

        if self.pressed == True and self.toggle == False:
            self.pressed = False
        if self.position[0] - self.name.get_height() < pygame.mouse.get_pos()[0] < self.position[0] and self.position[1] < pygame.mouse.get_pos()[1] < self.position[1] + self.name.get_height():
            if mouse_click_2:
                if self.toggle == True:
                    self.pressed = not self.pressed
                elif self.toggle == False and self.pressed == False:
                    self.pressed = True

        if self.position[0] < pygame.mouse.get_pos()[0] < self.position[0] + self.name.get_width() and self.position[1] < pygame.mouse.get_pos()[1] < self.position[1] + self.name.get_height():
            if mouse_click_2 and not mouse_holding and not mouse_holding_2:
                self.going_to_mouse = True
                mouse_holding = True
            elif mouse_click_2 and mouse_holding:
                self.going_to_mouse = False
                mouse_holding = False
        if self.going_to_mouse:
            self.position = (pygame.mouse.get_pos()[0] - self.name.get_width() / 2, pygame.mouse.get_pos()[1] - self.name.get_height() / 2)
        if self.pressed:
            self.producing = True
        else:
            self.producing = False
        if self.cyc == 0 and self.producing:
            if self.product == "Water":
                make_water((self.position[0] + self.name.get_width() + 15, (self.position[1] + (self.name.get_height() / 2))), 0, random.randint(4, 16), False)
            if self.product == "Carbon Dioxide":
                make_carbon_dioxide((self.position[0] + self.name.get_width() + 15, (self.position[1] + (self.name.get_height() / 2))), 0, random.randint(1, 16), False)
            if self.product == "Glucose":
                make_glucose((self.position[0] + self.name.get_width() + 15, (self.position[1] + (self.name.get_height() / 2))), 0, random.randint(4, 16), False)
            if self.product == "Molecular Oxygen":
                make_mol_oxygen((self.position[0] + self.name.get_width() + 15, (self.position[1] + (self.name.get_height() / 2))), 0, random.randint(4, 16), False)
            if self.product == "Adenosine Triphosphate":
                make_atp((self.position[0] + self.name.get_width() + 15, (self.position[1] + (self.name.get_height() / 2))), random.randint(-4, 4), random.randint(-4, 4), False)


class Chemical:
    def __init__(self, name, s_image, chemical_formula, position, show = True, on_cytoplasm = 0, on_mitochondria = 0, on_chloroplast = 0, xvel = 0, yvel = 0, gotomouse = False):
        self.name = font.render(name, False, (255, 255, 255))
        self.str_name = name
        image = pygame.image.load(s_image)
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / 10, self.image.get_height() / 10))
        alt = s_image[0:-4] + "_2" + s_image[-4:]
        self.altimage = pygame.image.load(alt)
        self.altimage = pygame.transform.scale(self.altimage, (self.altimage.get_width() / 4, self.altimage.get_height() / 4))
        self.chem_formula = chemical_formula
        self.position = position
        self.show = show
        self.going_to_mouse = gotomouse
        self.on_cytoplasm = 0
        self.on_mitochondria = 0
        self.on_chloroplast = 0
        self.xvel = xvel
        self.yvel = yvel
        desc = ''
        if self.str_name == "Molecular Oxygen":
            desc = 'Two oxygen atoms paired together. A byproduct of photosynthesis and an important reactant in aerobic cellular respiration.'
        elif self.str_name == "Carbon Dioxide":
            desc = 'A carbon atom with two attached oxygen atoms. This molecule is a byproduct of cellular respiration. A reactant in the equation for photosynthesis.'
        elif self.str_name == "Glucose":
            desc = 'A molecule that is a product of photosynthesis and can be metabolised in cellular respiration.'
        elif self.str_name == "Water":
            desc = "A molecule containing two hydrogen atom and a single oxygen atom. It's both a product of aerobic metabolism and a reactant in the equation for photosynthesis."
        elif self.str_name == "Lactic Acid":
            desc = 'A product of anaerobic metabolism, this molecule contains three hydrogen, six carbon, and three oxygen atoms.'
        elif self.str_name == "Adenosine Triphosphate":
            desc = 'This molecule is a form of dense and easy to access chemical energy, and is the product of metabolism. The goal of metabolism is to create this molecule.'
        self.desc_text = font.render(desc, False, (0, 0, 0), (255, 255, 255))


    def disappear(self):
        self.show = False
        self.position = (1390, 1300)

    def show_name(self):
        global chem_desc
        screen.blit(self.name, pygame.mouse.get_pos())
        if not chem_desc:
            screen.blit(self.desc_text, (20, 550))
            chem_desc = True

    def update(self):
        if self.position[0] > 1280 or self.position[0] < -10 or self.position[1] > 680 or self.position[1] < -10:
            self.show = False
        if not self.show:
            chemical_list.remove(self)
            del self
        else:
            global mouse_holding, chem_desc
            if self.on_mitochondria == 1:
                if self.str_name == "Glucose" or self.str_name == "Molecular Oxygen":
                    self.xvel = self.xvel / (1.075 * (clock.get_time() / 19))
                    self.yvel = self.yvel / (1.075 * (clock.get_time() / 19))
            elif self.on_chloroplast == 1:
                if self.str_name == "Water" or self.str_name == "Carbon Dioxide":
                    self.xvel = self.xvel / (1.015 * (clock.get_time() / 19))
                    self.yvel = self.yvel / (1.015 * (clock.get_time() / 19))
                elif not sunlight:
                    if self.str_name == "Glucose" or self.str_name == "Molecular Oxygen":
                        self.xvel = self.xvel / (1.015 * (clock.get_time() / 19))
                        self.yvel = self.yvel / (1.015 * (clock.get_time() / 19))
            elif self.on_cytoplasm == 1 or self.on_chloroplast == 1:
                if self.str_name == "Adenosine Triphosphate":
                    self.xvel = self.xvel / (1.02 * (clock.get_time() / 19))
                    self.yvel = self.yvel / (1.02 * (clock.get_time() / 19))
            self.position = (self.position[0] + (self.xvel * clock.get_time() / 15), self.position[1] + (self.yvel * clock.get_time() / 15))
            if graphic == False:
                screen.blit(self.image, self.position)
                if self.position[0] < pygame.mouse.get_pos()[0] < self.position[0] + self.image.get_width() and self.position[1] < pygame.mouse.get_pos()[1] < self.position[1] + self.image.get_height():
                    self.show_name()
                    if mouse_click_2 and not mouse_holding and not mouse_holding_2:
                        self.going_to_mouse = True
                        mouse_holding = True
                    elif mouse_click_2 and mouse_holding:
                        self.going_to_mouse = False
                        mouse_holding = False
            elif graphic == True:
                screen.blit(self.altimage, self.position)
                if self.position[0] < pygame.mouse.get_pos()[0] < self.position[0] + self.altimage.get_width() and self.position[1] < pygame.mouse.get_pos()[1] < self.position[1] + self.altimage.get_height():
                    self.show_name()
                    if mouse_click_2 and not mouse_holding and not mouse_holding_2:
                        self.going_to_mouse = True
                        mouse_holding = True
                    elif mouse_click_2 and mouse_holding:
                        self.going_to_mouse = False
                        mouse_holding = False
            if self.going_to_mouse:
                self.show_name()
                if graphic == False:
                    self.position = (pygame.mouse.get_pos()[0] - self.image.get_width() / 2, pygame.mouse.get_pos()[1] - self.image.get_height() / 2)
                elif graphic == True:
                    self.position = (pygame.mouse.get_pos()[0] - self.altimage.get_width() / 2, pygame.mouse.get_pos()[1] - self.altimage.get_height() / 2)
            self.on_chloroplast = 0
            self.on_mitochondria = 0


oxygenated_mitochondria = False
C = "carbon"
H = "hydrogen"
P = "phosphorous"
N = "nitrogen"
Ox = "oxygen"
reset_button = Button((50, 50), (255, 255, 255), "reset")
sources_button = Button((50, 80), (255, 255, 255), "sources")
glucose_button = Button((50, 110), (255, 255, 255), "glucose")
o2_button = Button((50, 140), (255, 255, 255), "oxygen")
co2_button = Button((50, 170), (255, 255, 255), "carbon dioxide")
water_button = Button((50, 200), (255, 255, 255), "water")
difdis_button = Button((1100, 50), (255, 255, 255), "graphics toggle")
sun = Sun((200, 50))

buttonlist = [reset_button, sources_button, glucose_button, o2_button, co2_button, water_button, difdis_button, sun]

chemical_list = []


def make_atp(position, xvel = 0, yvel = 0, gotomouse = False):
    chemical_list.append(Chemical("Adenosine Triphosphate", "atp.png", {C: 10, H: 16, N: 5, Ox: 13, P: 3}, position, True, 0, 0, 0, xvel / 10, yvel / 10, gotomouse))


def make_lactic_acid(position, xvel = 0, yvel = 0, gotomouse = False):
    chemical_list.append(Chemical("Lactic Acid", "lactic_acid.png", {C: 3, H: 6, Ox: 3}, position, True, 0, 0, 0, xvel / 10, yvel / 10, gotomouse))


def make_glucose(position, xvel = 0, yvel = 0, gotomouse = False):
    chemical_list.append(Chemical("Glucose", "glucose.png", {C: 6, H: 12, Ox: 6}, position, True, 0, 0, 0, xvel / 10, yvel / 10, gotomouse))


def make_mol_oxygen(position, xvel = 0, yvel = 0, gotomouse = False):
    chemical_list.append(Chemical("Molecular Oxygen", "oxygen.png", {Ox: 2}, position, True, 0, 0, 0, xvel / 10, yvel / 10, gotomouse))


def make_carbon_dioxide(position, xvel = 0, yvel = 0, gotomouse = False):
    chemical_list.append(Chemical("Carbon Dioxide", "carbon_dioxide.png", {C: 1, Ox: 2}, position, True, 0, 0, 0, xvel / 10, yvel / 10, gotomouse))


def make_water(position, xvel = 0, yvel = 0, gotomouse = False):
    chemical_list.append(Chemical("Water", "water.png", {C: 1, Ox: 2}, position, True, 0, 0, 0, xvel / 10, yvel / 10, gotomouse))


mitochondria_1 = Mitochondria("Mitochondria", "mitochondria.png", (970, 550))
mitochondria_2 = Mitochondria("Mitochondria", "mitochondria.png", (780, 560))
chloroplast_1 = Chloroplast("Chloroplast", "chloroplast.png", (770, 200))
chloroplast_2 = Chloroplast("Chloroplast", "chloroplast.png", (980, 160))


def reset():
    global chemical_list, cytoplasm, mitochondria_1, mitochondria_2, chloroplast_1, chloroplast_2, waterprod, prodlist, co2prod

    chemical_list = []
    cytoplasm = Cytoplasm("Cytoplasm", "cytoplasm1.png", (700, 430))
    mitochondria_1 = Mitochondria("Mitochondria", "mitochondria.png", (970, 550))
    mitochondria_2 = Mitochondria("Mitochondria", "mitochondria.png", (780, 560))
    chloroplast_1 = Chloroplast("Chloroplast", "chloroplast.png", (770, 200))
    chloroplast_2 = Chloroplast("Chloroplast", "chloroplast.png", (980, 160))
    waterprod = Producer((50, 400), "Water", "Water Producer", (255, 255, 255))
    co2prod = Producer((50, 450), "Carbon Dioxide", "Carbon Dioxide Producer", (255, 255, 255))
    glucoseprod = Producer((50, 350), "Glucose", "Glucose Producer", (255, 255, 255))
    o2prod = Producer((50, 500), "Molecular Oxygen", "Oxygen Producer", (255, 255, 255))
    prodlist = [waterprod, co2prod, glucoseprod, o2prod]


def display_sources():
    dfont = pygame.font.SysFont("Times New Roman", 22)
    text = dfont.render("www.bbc.co.uk/bitesize/guides/zcjy97h/revision/5", False, (0, 70, 0))
    text2 = dfont.render("micro.magnet.fsu.edu/cells/chloroplasts/chloroplasts.html", False, (0, 70, 0))
    screen.blit(text, (180, 260)), screen.blit(text2, (180, 290))

displaying_source = False
reset()
play = True
p_pres = False
sunlight = False
graphic = False
opti_cyc = 0
while play:
    clock.tick(50)
    chem_desc = False
    mitochondria_desc = False
    if sunlight:
        screen.fill((200, 200, 200))
    else:
        screen.fill((50, 50, 50))
    if reset_button.pressed == True:
        reset()
    if sources_button.pressed == True:
        displaying_source = not displaying_source
    if displaying_source:
        display_sources()
    if difdis_button.pressed == True:
        graphic = not graphic
    updatein = 0
    while updatein < len(prodlist):
        prodlist[updatein].update()
        updatein += 1
    mitochondria_1.update()
    mitochondria_2.update()
    chloroplast_1.update()
    chloroplast_2.update()
    cytoplasm.update()
    keys = pygame.key.get_pressed()
    updatein = 0
    while updatein < len(chemical_list):
        if chemical_list[updatein].show == False:
            chemical_list.remove(chemical_list[updatein])
        else:
            chemical_list[updatein].update()
            updatein += 1
    if mouse_holding == False:
        mouse_holding_2 = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
            hold_var = False
        else:
            mouse_click = False
            hold_var = False
            mouse_click_2 = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not p_pres:
                    p_pres = True
                elif p_pres:
                    p_pres = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                p_pres = False
    if mouse_click and not hold_var:
        mouse_click_2 = True
    else:
        mouse_click_2 = False
    if mouse_click:
        hold_var = True
    updatein = 0
    while updatein < len(buttonlist):
        currbut = buttonlist[updatein]
        currbut.draw()
        currbut.click()
        if currbut.pressed and not mouse_holding and currbut.name != "Sun":
            if currbut.sname == "water":
                make_water(pygame.mouse.get_pos(), 0, 0, True)
            if currbut.sname == "carbon dioxide":
                make_carbon_dioxide(pygame.mouse.get_pos(), 0, 0, True)
            if currbut.sname == "glucose":
                make_glucose(pygame.mouse.get_pos(), 0, 0, True)
            if currbut.sname == "oxygen":
                make_mol_oxygen(pygame.mouse.get_pos(), 0, 0, True)
        elif currbut.name == "Sun":
            if currbut.pressed == True:
                sunlight = True
            else:
                sunlight = False
        updatein += 1
    opti_cyc += 1
    if opti_cyc > 1000:
        newchemlist = []
        opti_cyc = 0
        chemcyc = 0
        while chemcyc < len(chemical_list):
            currchem = chemical_list[chemcyc]
            if currchem.show == True:
                newchemlist.append(currchem)
            else:
                chemical_list.remove(currchem)
                del currchem
            chemcyc += 1
        chemical_list.clear()
        chemical_list = newchemlist
    pygame.display.flip()
