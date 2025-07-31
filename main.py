"""
author : Léo Imbert
@created : 31/07/2025 10:18
@updated : 31/07/2025 18:54
"""

import random
import pyxel
import math
import sys
import os

PALETTE = [0x000000, 0xEEEEEE, 0x202840, 0X273E82, 0x0032C4, 0xA9C1FF, 0xA3A3A3, 0x19959C, 0x70C6A9, 0xE9C35B, 0xD38441, 0xD4186C, 0x7E2072, 0x8B4852, 0xFF9798, 0xEDC7B0]

class PyxelManager:

    def __init__(self, width:int, height:int, scenes:list, default_scene_id:int=0, fps:int=60, fullscreen:bool=False, mouse:bool=False, quit_key:int=pyxel.KEY_ESCAPE, camera_x:int=0, camera_y:int=0):
        
        self.__fps = fps
        self.__scenes_dict = {scene.id:scene for scene in scenes}
        self.__current_scene = self.__scenes_dict.get(default_scene_id, 0)
        self.__transition = {}

        self.__cam_x = self.__cam_tx = camera_x
        self.__cam_y = self.__cam_ty = camera_y
        self.__shake_amount = 0
        self.__sub_shake_amount = 0

        pyxel.init(width, height, fps=self.__fps, quit_key=quit_key)
        pyxel.fullscreen(fullscreen)
        pyxel.mouse(mouse)

        if self.__current_scene.pyxres_path:
            pyxel.load(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), self.__current_scene.pyxres_path))
        pyxel.title(self.__current_scene.title)
        pyxel.screen_mode(self.__current_scene.screen_mode)
        pyxel.colors.from_list(self.__current_scene.palette)

    @property
    def camera_x(self)-> int:
        return self.__cam_x
    
    @property
    def camera_y(self)-> int:
        return self.__cam_y

    @property
    def mouse_x(self)-> int:
        return self.__cam_x + pyxel.mouse_x
    
    @property
    def mouse_y(self)-> int:
        return self.__cam_y + pyxel.mouse_y
    
    @property
    def fps(self)-> int:
        return self.__fps
    
    def set_camera(self, new_camera_x:int, new_camera_y:int):
        self.__cam_x = self.__cam_tx = new_camera_x
        self.__cam_y = self.__cam_ty = new_camera_y

    def move_camera(self, new_camera_x:int, new_camera_y:int):
        self.__cam_tx = new_camera_x
        self.__cam_ty = new_camera_y

    def shake_camera(self, amount:int, sub_amount:float):
        self.__shake_amount = amount
        self.__sub_shake_amount = sub_amount

    def change_scene(self, new_scene_id:int, new_camera_x:int=0, new_camera_y:int=0):
        self.set_camera(new_camera_x, new_camera_y)

        if self.__current_scene.on_exit:
            self.__current_scene.on_exit()
        self.__current_scene = self.__scenes_dict.get(new_scene_id, 0)
        if self.__current_scene.on_enter:
            self.__current_scene.on_enter()

        if self.__current_scene.pyxres_path:
            pyxel.load(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), self.__current_scene.pyxres_path))
        pyxel.title(self.__current_scene.title)
        pyxel.screen_mode(self.__current_scene.screen_mode)
        pyxel.colors.from_list(self.__current_scene.palette)

    def change_scene_dither(self, new_scene_id:int, speed:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"dither",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "dither":0
        }

    def change_scene_circle(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"circle",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "radius":0,
            "max_radius":((pyxel.width ** 2 + pyxel.height ** 2) ** 0.5) / 2
        }

    def change_scene_closing_doors(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"closing_doors",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "w":0,
            "x":self.__cam_x + pyxel.width
        }

    def change_scene_rectangle_right_left(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"rectangle_right_left",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "x":self.__cam_x + pyxel.width,
            "w":0
        }

    def change_scene_rectangle_left_right(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"rectangle_left_right",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "x":self.__cam_x,
            "w":0
        }

    def change_scene_outer_circle(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"outer_circle",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "start_end":int(((pyxel.width ** 2 + pyxel.height ** 2) ** 0.5) / 2) + 1,
            "end":int(((pyxel.width ** 2 + pyxel.height ** 2) ** 0.5) / 2) + 1
        }

    def change_scene_triangle(self, new_scene_id:int, speed:int, transition_color:int, rotation_speed:int, new_camera_x:int=0, new_camera_y:int=0):
        self.__transition = {
            "type":"triangle",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "rotation_speed":rotation_speed,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "size":0,
            "angle":270
        }

    def apply_palette_effect(self, effect_function, **kwargs):
        pyxel.colors.from_list(effect_function(self.__current_scene.palette, kwargs))

    def reset_palette(self):
        pyxel.colors.from_list(self.__current_scene.palette)

    def handle_transitions(self):

        if self.__transition.get("type") == "dither":
            self.__transition["dither"] += self.__transition["speed"] * self.__transition["direction"]

            if self.__transition["dither"] > 1 and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["dither"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.dither(self.__transition["dither"])
            pyxel.rect(self.__cam_x, self.__cam_y, pyxel.width, pyxel.height, self.__transition["transition_color"])
            pyxel.dither(1)

        elif self.__transition.get("type") == "circle":
            self.__transition["radius"] += self.__transition["speed"] * self.__transition["direction"]

            if self.__transition["radius"] > self.__transition["max_radius"] and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["radius"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.circ(self.__cam_x + pyxel.width / 2, self.__cam_y + pyxel.height / 2, self.__transition["radius"], self.__transition["transition_color"])

        elif self.__transition.get("type") == "closing_doors":
            self.__transition["w"] += self.__transition["speed"] * self.__transition["direction"]
            self.__transition["x"] -= self.__transition["speed"] * self.__transition["direction"]

            if self.__transition["w"] > pyxel.width // 2 and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["w"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.rect(self.__cam_x, self.__cam_y, self.__transition["w"], pyxel.height, self.__transition["transition_color"])
            pyxel.rect(self.__transition["x"], self.__cam_y, self.__transition["w"], pyxel.height, self.__transition["transition_color"])

        elif self.__transition.get("type") == "rectangle_right_left":
            self.__transition["w"] += self.__transition["speed"] * self.__transition["direction"]
            if self.__transition["direction"] == 1:
                self.__transition["x"] -= self.__transition["speed"]

            if self.__transition["w"] > pyxel.width and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["w"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.rect(self.__transition["x"], self.__cam_y, self.__transition["w"], pyxel.height, self.__transition["transition_color"])

        elif self.__transition.get("type") == "rectangle_left_right":
            self.__transition["w"] += self.__transition["speed"] * self.__transition["direction"]
            if self.__transition["direction"] == -1:
                self.__transition["x"] += self.__transition["speed"]

            if self.__transition["w"] > pyxel.width and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["w"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.rect(self.__transition["x"], self.__cam_y, self.__transition["w"], pyxel.height, self.__transition["transition_color"])

        elif self.__transition.get("type") == "outer_circle":
            self.__transition["end"] -= self.__transition["speed"] * self.__transition["direction"]

            if self.__transition["end"] < 0 and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["end"] > self.__transition["start_end"] and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            
            for radius in range(self.__transition["start_end"], self.__transition["end"], -1):
                pyxel.ellib(self.__cam_x + pyxel.width / 2 - radius, self.__cam_y + pyxel.height / 2 - radius, radius * 2, radius * 2, self.__transition["transition_color"])
                pyxel.ellib(self.__cam_x + pyxel.width / 2 - radius + 1, self.__cam_y + pyxel.height / 2 - radius, radius * 2, radius * 2, self.__transition["transition_color"])

        elif self.__transition.get("type") == "triangle":
            self.__transition["size"] += self.__transition["speed"] * self.__transition["direction"]
            self.__transition["angle"] += self.__transition["rotation_speed"] * self.__transition["direction"]

            if self.__transition["size"] / 2.5 > max(pyxel.width, pyxel.height) and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"])
            if self.__transition["size"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            d = math.sqrt(3) / 3 * self.__transition["size"]
            x1, y1 = self.__cam_x + pyxel.width / 2 + d * math.cos(math.radians(0 + self.__transition["angle"])), self.__cam_y + pyxel.height / 2 + d * math.sin(math.radians(0 + self.__transition["angle"]))
            x2, y2 = self.__cam_x + pyxel.width / 2 + d * math.cos(math.radians(120 + self.__transition["angle"])), self.__cam_y + pyxel.height / 2 + d * math.sin(math.radians(120 + self.__transition["angle"]))
            x3, y3 = self.__cam_x + pyxel.width / 2 + d * math.cos(math.radians(240 + self.__transition["angle"])), self.__cam_y + pyxel.height / 2 + d * math.sin(math.radians(240 + self.__transition["angle"]))
            pyxel.tri(x1, y1, x2, y2, x3, y3, self.__transition["transition_color"])

    def update(self):
        self.__cam_x += (self.__cam_tx - self.__cam_x) * 0.1
        self.__cam_y += (self.__cam_ty - self.__cam_y) * 0.1

        if self.__shake_amount > 0:
            amount = int(self.__shake_amount)
            pyxel.camera(self.__cam_x + random.randint(-amount, amount), self.__cam_y + random.randint(-amount, amount))
            self.__shake_amount -= self.__sub_shake_amount
        else:
            pyxel.camera(self.__cam_x, self.__cam_y)

        if not self.__transition.get("type"):
            self.__current_scene.update()

    def draw(self):
        self.__current_scene.draw()
        if self.__transition:
            self.handle_transitions()

    def run(self):
        pyxel.run(self.update, self.draw)

class Scene:

    def __init__(self, id:int, title:str, update, draw, pyxres_path:str=None, palette:list=PALETTE, screen_mode:int=0, on_exit=None, on_enter=None):
        self.id = id
        self.title = title
        self.update = update
        self.draw = draw
        self.pyxres_path = pyxres_path
        self.palette = palette
        self.screen_mode = screen_mode
        self.on_exit = on_exit
        self.on_enter = on_enter

class Sprite:

    def __init__(self, img:int, u:int, v:int, w:int, h:int, colkey:int=None):
        self.img = img
        self.u, self.v = u, v
        self.w, self.h = w, h
        self.colkey = 0 if colkey == 0 else colkey
        self.flip_horizontal = False
        self.flip_vertical = False

class Animation:

    def __init__(self, sprite:Sprite, total_frames:int=1, frame_duration:int=20, loop:bool=True):
        self.sprite = sprite
        self.__total_frames = total_frames
        self.frame_duration = frame_duration
        self.__loop = loop
        self.__start_frame = pyxel.frame_count
        self.current_frame = 0
        self.__is_finished = False

    def is_finished(self)-> bool:
        return self.__is_finished and not self.__loop
    
    def is_looped(self)-> bool:
        return self.__loop
    
    def reset(self):
        self.__start_frame = pyxel.frame_count
        self.current_frame = 0
        self.__is_finished = False

    def update(self):
        if self.is_finished():
            return
        
        if pyxel.frame_count - self.__start_frame >= self.frame_duration:
            self.__start_frame = pyxel.frame_count
            self.current_frame += 1
            if self.current_frame >= self.__total_frames:
                if self.__loop:
                    self.current_frame = 0
                else:
                    self.__is_finished = True
                    self.current_frame = self.__total_frames - 1

    def draw(self, x:int, y:int):
        w = -self.sprite.w if self.sprite.flip_horizontal else self.sprite.w
        h = -self.sprite.h if self.sprite.flip_vertical else self.sprite.h
        pyxel.blt(x, y, self.sprite.img, self.sprite.u + self.current_frame * abs(self.sprite.w), self.sprite.v, w, h, self.sprite.colkey)

class Bullet:

    def __init__(self, x:int, y:int, tx:int, ty:int):
        self.x, self.y = x, y
        self.w, self.h = 6, 6
        self.speed = 1
        self.lifetime = 500
        self.dither = 1

        mag = ((tx - x) ** 2 + (ty - y) ** 2) ** 0.5
        self.vx = (tx - x) / mag * self.speed
        self.vy = (ty - y) / mag * self.speed

        self.animation = Animation(Sprite(0, 32, 48, self.w, self.h, 14), 3, 15, False)

    def update(self):
        self.lifetime -= 1

        self.x += self.vx
        self.y += self.vy

        if self.x > pyxel.width:
            self.x = -self.w
        elif self.x + self.w < 0:
            self.x = pyxel.width

        if self.y > pyxel.height:
            self.y = -self.h
        elif self.y + self.h < 0:
            self.y = pyxel.height

        self.animation.update()

        if self.lifetime <= 10:
            self.dither = self.lifetime / 10

    def draw(self):
        pyxel.dither(self.dither)
        self.animation.draw(self.x, self.y)
        pyxel.dither(1)

class Player:
    
    def __init__(self, x:int, y:int):
        self.x, self.y = x, y
        self.w, self.h = 16, 16

        self.vx, self.vy = 0, 0
        self.max_vx, self.max_vy = 1.5, 1.5
        self.speed = 0.8
        self.friction = 0.85

        self.bullets = []

        self.idle = Animation(Sprite(0, 0, 16, 16, 16, 14), 2, 20, True)
        self.walk = Animation(Sprite(0, 0, 32, 16, 16, 14), 2, 10, True)
        self.current_animation = self.idle

        self.facing_right = True

    def update_velocity_x(self):
        if self.vx != 0:
            step_x = 1 if self.vx > 0 else -1
            for _ in range(int(abs(self.vx))):
                if True:
                    self.x += step_x
                else:
                    self.vx = 0
                    break

    def update_velocity_y(self):
        if self.vy != 0:
            step_y = 1 if self.vy > 0 else -1
            for _ in range(int(abs(self.vy))):
                if True:
                    self.y += step_y
                else:
                    self.vy = 0
                    break

    def update(self):
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [bullet for bullet in self.bullets if bullet.lifetime > 0]

        self.vx *= self.friction
        self.vy *= self.friction

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_A):
            self.vx = max(self.vx - self.speed, -self.max_vx)
            self.facing_right = False
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.vx = min(self.vx + self.speed, self.max_vx)
            self.facing_right = True
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_W):
            self.vy = max(self.vy - self.speed, -self.max_vy)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.vy = min(self.vy + self.speed, self.max_vy)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.bullets.append(Bullet(self.x + 5, self.y + 5, pyxel.mouse_x, pyxel.mouse_y))
            self.facing_right = not pyxel.mouse_x < self.x + 8

        if abs(self.vx) > 0.1 or abs(self.vy) > 0.1:
            self.current_animation = self.walk
        else:
            self.current_animation = self.idle

        self.update_velocity_x()
        self.update_velocity_y()

        if self.x > pyxel.width:
            self.x = -self.w
        elif self.x + self.w < 0:
            self.x = pyxel.width

        if self.y > pyxel.height:
            self.y = -self.h
        elif self.y + self.h < 0:
            self.y = pyxel.height

        self.current_animation.update()

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()

        self.current_animation.sprite.flip_horizontal = not self.facing_right
        self.current_animation.draw(self.x, self.y)

class Spider:

    def __init__(self, x:int, y:int):
        self.x, self.y = x, y
        self.w, self.h = 16, 16
        self.speed = 0.5

        self.idle = Animation(Sprite(0, 80, 16, self.w, self.h, 14), 2, 20)
        self.walk = Animation(Sprite(0, 80, 32, self.w, self.h, 14), 4, 10)
        self.current_animation = self.idle

    def update(self, player_x:int, player_y:int):
        dx = player_x - self.x
        dy = player_y - self.y
        mag = (dx ** 2 + dy ** 2) ** 0.5

        if mag < 80:
            self.current_animation = self.walk
            self.current_animation.sprite.flip_horizontal = dx < 0
            self.x += dx / mag * self.speed
            self.y += dy / mag * self.speed
        else:
            self.current_animation = self.idle

        self.current_animation.update()

    def draw(self):
        self.current_animation.draw(self.x, self.y)

class Scarab:

    def __init__(self, x:int, y:int):
        self.x, self.y = x, y
        self.w, self.h = 16, 16
        self.speed = 0.5

        self.idle = Animation(Sprite(0, 0, 112, self.w, self.h, 14), 2, 20)
        self.walk = Animation(Sprite(0, 0, 128, self.w, self.h, 14), 4, 10)
        self.current_animation = self.idle

    def update(self, player_x:int, player_y:int):
        dx = player_x - self.x
        dy = player_y - self.y

        if abs(dx) > pyxel.width / 2:
            dx -= pyxel.width * (1 if dx > 0 else -1)
        if abs(dy) > pyxel.height / 2:
            dy -= pyxel.height * (1 if dy > 0 else -1)

        mag = (dx ** 2 + dy ** 2) ** 0.5

        if mag < 80:
            self.current_animation = self.walk
            self.current_animation.sprite.flip_horizontal = dx < 0
            self.x += dx / mag * self.speed
            self.y += dy / mag * self.speed
        else:
            self.current_animation = self.idle


        if self.x > pyxel.width:
            self.x = -self.w
        elif self.x + self.w < 0:
            self.x = pyxel.width

        if self.y > pyxel.height:
            self.y = -self.h
        elif self.y + self.h < 0:
            self.y = pyxel.height

        self.current_animation.update()

    def draw(self):
        self.current_animation.draw(self.x, self.y)

class Hornet:

    def __init__(self, x:int, y:int):
        self.x, self.y = x, y
        self.w, self.h = 24, 24
        self.speed = 0.4

        self.idle = Animation(Sprite(0, 0, 176, self.w, self.h, 14), 8, 10)
        self.attack = Animation(Sprite(0, 0, 200, self.w, self.h, 14), 8, 10)
        self.current_animation = self.idle

        self.shoot_timer = 0
        self.wander_timer = 0

    def update(self, player_x:int, player_y:int, player_bullets:list):
        mag = ((player_x - self.x) ** 2 + (player_y - self.y) ** 2) ** 0.5

        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            if mag < 80:
                player_bullets.append(Bullet(self.x + 9, self.y + 9, player_x, player_y))
            self.shoot_timer = random.randint(100, 240)

        if mag < 80:
            self.current_animation = self.attack
        else:
            self.current_animation = self.idle

        self.wander_timer -= 1
        if self.wander_timer <= 0:

            mag_tp = 0
            while mag_tp < 50:
                self.tx, self.ty = random.randint(0, 228), random.randint(0, 128)
                mag_tp = ((self.tx - player_x) ** 2 + (self.ty - player_y) ** 2) ** 0.5

            self.wander_timer = 120

        dx = self.tx - self.x
        dy = self.ty - self.y

        if abs(dx) > pyxel.width / 2:
            dx -= pyxel.width * (1 if dx > 0 else -1)
        if abs(dy) > pyxel.height / 2:
            dy -= pyxel.height * (1 if dy > 0 else -1)

        mag = (dx ** 2 + dy ** 2) ** 0.5

        self.x += dx / mag * self.speed
        self.y += dy / mag * self.speed

        if self.x > pyxel.width:
            self.x = -self.w
        elif self.x + self.w < 0:
            self.x = pyxel.width

        if self.y > pyxel.height:
            self.y = -self.h
        elif self.y + self.h < 0:
            self.y = pyxel.height

        self.current_animation.update()
        self.current_animation.sprite.flip_horizontal = player_x - self.x < 0

    def draw(self):
        self.current_animation.draw(self.x, self.y)

class Game:

    def __init__(self):
        #? Scenes
        main_menu_scene = Scene(0, "Loop Shot - Main Menu", self.update_main_menu, self.draw_main_menu, "assets.pyxres")
        credits_scene = Scene(1, "Loop Shot - Credits", self.update_credits, self.draw_credits, "assets.pyxres")
        game_scene = Scene(2, "Loop Shot - Game", self.update_game, self.draw_game, "assets.pyxres")
        scenes = [main_menu_scene, credits_scene, game_scene]

        #? Pyxel Init
        self.pyxel_manager = PyxelManager(228, 128, scenes, 2, 60, True)

        #? Game Variables
        self.player = Player(10, 10)
        self.spider = Hornet(200, 100)

        #? Run
        self.pyxel_manager.run()

    def update_main_menu(self):
        pass

    def draw_main_menu(self):
        pyxel.cls(0)

    def update_credits(self):
        pass

    def draw_credits(self):
        pyxel.cls(0)

    def update_game(self):
        self.player.update()
        self.spider.update(self.player.x, self.player.y, self.player.bullets)

    def draw_game(self):
        pyxel.cls(6)
        pyxel.bltm(0, 0, 0, 0, 0, 230, 128, 0)

        self.player.draw()
        self.spider.draw()

        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, 0, 0, 8, 8, 14)

if __name__ == "__main__":
    Game()