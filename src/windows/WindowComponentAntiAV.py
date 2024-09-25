import dearpygui.dearpygui as dpg
from random import randint

from windows.Window import Window

bullets = []
entities = []

class Bullet:
    def __init__(self, pos:tuple|list, size: int, color: tuple|list, speed: int, **kwargs):
        self.pos = pos
        self.last_pos = None
        self.size = size
        self.color = color
        self.fill = color
        self.speed = speed
        self.hitbox = ((self.pos[0],self.pos[1]), (self.pos[0]+self.size+2, self.pos[1]+self.size+2))
        #               Levý horní roh          , pravý dolní roh

    def update(self):
        # Zamaskuje starou pozici
        dpg.draw_rectangle(parent="anti_av.drawlist", pmin=self.hitbox[0], pmax=self.hitbox[1], color=(0,0,0), fill=(0,0,0))
        self.last_pos = self.pos
        self.pos = (self.pos[0], self.pos[1]+self.speed)
        self.hitbox = ((self.pos[0],self.pos[1]), (self.pos[0]+self.size+2, self.pos[1]+self.size+2))
        dpg.draw_rectangle(parent="anti_av.drawlist", pmin=self.hitbox[0], pmax=self.hitbox[1], color=self.color, fill=self.fill)

class Entity:
    def __init__(self, pos: tuple|list, size: int, color: tuple|list, fill: tuple|list, **kwargs):
        self.pos = pos  # Levý horní roh
        self.last_pos = None
        self.move_speed = kwargs["move_speed"] if "move_speed" in kwargs else 10
        self.size = size
        self.color = color
        self.fill = fill
        self.sprite = kwargs["sprite"] if kwargs["sprite"] else lambda: (dpg.draw_rectangle(parent="anti_av.drawlist", pmin=self.hitbox[0], pmax=self.hitbox[1], color=self.color, fill=self.fill))
        self.hitbox = ((self.pos[0],self.pos[1]), (self.pos[0]+self.size+2, self.pos[1]+self.size+2))
        #               Levý horní roh          , pravý dolní roh
        self.show_hitbox = kwargs["show_hitbox"] if "show_hitbox" in kwargs else False


    def move(self, x=0, y=0):
        # Zamaskuje starou pozici
        dpg.draw_rectangle(parent="anti_av.drawlist", pmin=self.hitbox[0], pmax=self.hitbox[1], color=(0,0,0), fill=(0,0,0))
        self.last_pos = self.pos
        newpos = (self.pos[0]+x, self.pos[1]+y)

        # Screen edge check
        if newpos[0] <= 0 or newpos[0] >= 550 or newpos[1] <= 0 or newpos[1] >= 520:
            pass
        else:
            self.pos = newpos
            self.hitbox = ((self.pos[0],self.pos[1]), (self.pos[0]+self.size+2, self.pos[1]+self.size+2))

        if self.show_hitbox:
            dpg.draw_rectangle(parent="anti_av.drawlist", pmin=self.hitbox[0], pmax=self.hitbox[1], color=(0,0,0), fill=(255,0,255))
        self.sprite()

    def shoot(self):
        global bullets
        bullets.append(Bullet((self.pos[0]+(self.size/2)-10, self.pos[1]-10), 5, self.color, 10))

    def shoot_up(self):
        global bullets
        bullets.append(Bullet((self.pos[0]+(self.size/2), self.pos[1]-10), 5, self.color, -10))

    def isHit(self, bullet: Bullet):
        return (self.hitbox[0][0] <= bullet.pos[0] <= self.hitbox[1][0] and self.hitbox[0][1] <= bullet.pos[1] <= self.hitbox[1][1]) or (self.hitbox[0][0] <= bullet.pos[0]+bullet.size <= self.hitbox[1][0] and self.hitbox[0][1] <= bullet.pos[1]+bullet.size <= self.hitbox[1][1])

    def kill(self):
        global entities
        dpg.draw_rectangle(parent="anti_av.drawlist", pmin=self.hitbox[0], pmax=self.hitbox[1], color=(0,0,0), fill=(0,0,0))
        try:
            entities.remove(self)
        except Exception:
            pass
        del self

class WindowComponentAntiAV(Window):
    def __init__(self, theme = None):
        super().__init__("anti_av", 600, 600, ["center", 0, 0], False, True, theme=theme, label="Anti-Antivir", no_collapse=True)

        # Variables
        self.player = Entity((270, 410), 30, (255,0,0), (255,0,0), sprite=lambda: (dpg.draw_polygon(parent="anti_av.drawlist", points=[[self.player.pos[0],self.player.pos[1]+self.player.size],[self.player.pos[0]+(self.player.size/2),self.player.pos[1]+(3*self.player.size/4)], [self.player.pos[0]+self.player.size,self.player.pos[1]+self.player.size], [self.player.pos[0]+(self.player.size/2),self.player.pos[1]]],color=(255,0,0), fill=(255,0,0))))

        self.score = 0
        self.finished = False
        self.last_update_time = dpg.get_total_time()

        # Setup okna
        dpg.add_drawlist(tag="anti_av.drawlist", parent="anti_av", width=self.width, height=self.height-50, pos=(0,0))
        dpg.draw_rectangle(parent="anti_av.drawlist", pmin=(0,0), pmax=(self.width, self.height), color=(0,0,0), fill=(0,0,0))
        dpg.add_text(f"Skóre: {self.score}/15", tag="anti_av.score", parent="anti_av", pos=(10, 20), color=(255,255,255))

        with dpg.handler_registry():
            dpg.add_key_press_handler(callback=self.move_player, key=dpg.mvKey_Up, user_data="up")
            dpg.add_key_press_handler(callback=self.move_player, key=dpg.mvKey_Left, user_data="left")
            dpg.add_key_press_handler(callback=self.move_player, key=dpg.mvKey_Down, user_data="down")
            dpg.add_key_press_handler(callback=self.move_player, key=dpg.mvKey_Right, user_data="right")
            dpg.add_key_press_handler(callback=self.shoot, key=dpg.mvKey_Spacebar)

        # Show player
        self.player.move()

    def add_bullet(self, bullet):
        bullets.append(bullet)

    def move_player(self, sender, app_data, user_data):
        if self.finished:
            return

        match user_data:
            case "up":
                self.player.move(y=-10)
            case "left":
                self.player.move(x=-10)
            case "down":
                self.player.move(y=+10)
            case "right":
                self.player.move(x=+10)


    def shoot(self):
        self.player.shoot_up()

    def add_enemy(self):
        global entities
        new_entity = Entity(
            pos=(randint(30, 550), randint(30, 100)),
            size=30,
            color=(0,255,0),
            fill=(0,255,0),
            move_speed=1.5,
            sprite=lambda: (dpg.draw_rectangle(
                                            pmin=(new_entity.pos[0], new_entity.pos[1]),
                                            pmax=(new_entity.pos[0]+new_entity.size, new_entity.pos[1]+new_entity.size),
                                            parent="anti_av.drawlist",
                                            color=(0,255,0),
                                            fill=(0,255,0)
                                            )))
        entities.append(new_entity)


    def frame_update(self):
        global bullets, entities
        # Spouštění funkční pouze když je okno viditelné nebo dokud není skóre 15
        if dpg.is_item_shown("anti_av") and not self.finished:
            delta_time = dpg.get_total_time() - self.last_update_time

            # Spuštění po 1/30 sekundy
            if delta_time > 1/30:
                self.last_update_time = dpg.get_total_time()
                dpg.draw_rectangle(parent="anti_av.drawlist", pmin=(0,0), pmax=(self.width, self.height), color=(0,0,0), fill=(0,0,0))

                # Score check
                if self.score >= 15:
                    self.finished = True
                    dpg.draw_rectangle(parent="anti_av.drawlist", pmin=(0,0), pmax=(self.width, self.height), color=(0,0,0), fill=(0,0,0))
                    dpg.add_text("Implementace komponentu Anti-Antivirus úspěšná!", parent=self.tag, pos=((self.width/2)-175, (self.height/2)-10), color=(0, 255, 0))
                    self.set_progress(5, 1, "component")
                    return

                # Spawn enemeies
                if len(entities) < 5:
                    self.add_enemy()

                # Posun entit
                for entity in entities:
                    entity.move(y=entity.move_speed)

                # hitcheck dolni hranice
                for entity in entities:
                    if entity.pos[1]+entity.size >= 510:
                        self.score -= 3
                        if self.score < 0:
                            self.score = 0
                        entity.kill()
                        dpg.set_value("anti_av.score", f"Skóre: {self.score}/15")

                # Hitcheck bulletu jestli nejdou offscreen
                for bullet in bullets:
                    bullet.update()
                    if bullet.pos[1] < 0 or bullet.pos[1] > self.height:
                        bullets.remove(bullet)

                # Hitbox checky
                for entity in entities:
                    for bullet in bullets:
                        if entity.isHit(bullet):
                            entity.kill()
                            bullets.remove(bullet)
                            self.score += 1
                            dpg.set_value("anti_av.score", f"Skóre: {self.score}/15")

                dpg.draw_line(parent="anti_av.drawlist", p1=(0, 508), p2=(self.width, 508), color=(255,255,255))
                self.player.sprite()
