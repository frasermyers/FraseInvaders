from tkinter import *
import time

tk = Tk()
tk.title("Frase Invaders!")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=720, height=560, bd=0, highlightthickness=0)
canvas.config(bg="black")
canvas.create_line(0, 30, 720, 30, fill="pink")
canvas.pack()
tk.update()


class Sprite:

    def __init__(self, canvas, color="white", x=10, y=10, w=15, h=15, x_vel=0, y_vel=0):
        self.canvas = canvas
        self.id = canvas.create_oval(x, y, x+w, y+h, fill=color)
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.pos = self.canvas.coords(self.id)

    def draw(self):
        self.canvas.move(self.id, self.x_vel, self.y_vel)

    def hit_wall(self):
        pos = self.canvas.coords(self.id)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        if pos[2] >= self.canvas_width:
            return True
        if pos[0] <= 0:
            return True
        return False

    def hit_roof(self):
        pos = self.canvas.coords(self.id)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        if pos[3] <= 35:
            canvas.delete(self.id)
            return True
        return False

    def hit_other_object(self, other_object):
        current_object_pos = self.canvas.coords(self.id)
        other_object_pos = self.canvas.coords(other_object.id)

        if other_object_pos[0] <= current_object_pos[2] <= other_object_pos[2]:
            if other_object_pos[3] >= current_object_pos[3] >= other_object_pos[1]:
                return True

        if other_object_pos[0] <= current_object_pos[0] <= other_object_pos[2]:
            if other_object_pos[3] >= current_object_pos[3] >= other_object_pos[1]:
                return True

        if other_object_pos[0] <= current_object_pos[2] <= other_object_pos[2]:
            if other_object_pos[3] >= current_object_pos[1] >= other_object_pos[1]:
                return True

        if other_object_pos[0] <= current_object_pos[0] <= other_object_pos[2]:
            if other_object_pos[3] >= current_object_pos[1] >= other_object_pos[1]:
                return True

        return False


class Enemy(Sprite):

    def __init__(self, canvas, color="Red", x=10, y=10, w=15, h=15, x_vel=1, y_vel=0):
        super(Enemy, self).__init__(canvas, color=color , x=x, y=y, w=w, h=h, x_vel=x_vel, y_vel=y_vel)


class Hero(Sprite):

    def __init__(self, canvas, color="SeaGreen1", x=360, y=500, w=40, h=40, x_vel=0, y_vel=0):

        super(Hero, self).__init__(canvas, color=color, x=x, y=y, w=w, h=h, x_vel=x_vel, y_vel=y_vel)
        self.canvas.bind_all('<KeyPress-Left>', self.left_key_pressed)
        self.canvas.bind_all('<KeyRelease-Left>', self.left_key_released)
        self.canvas.bind_all('<KeyPress-Right>', self.right_key_pressed)
        self.canvas.bind_all('<KeyRelease-Right>', self.right_key_released)

    def left_key_pressed(self, evt):
        self.x_vel = -2

    def left_key_released(self, evt):
        self.x_vel = 0

    def right_key_pressed(self, evt):
        self.x_vel = 2

    def right_key_released(self, evt):
        self.x_vel = 0


class Bullet(Sprite):

    def __init__(self, canvas, color="Pink", x=360, y=400, w=6, h=10, x_vel=0, y_vel=-5, firing_object=None):
        positions = firing_object.canvas.coords(firing_object.id)
        super(Bullet, self).__init__(canvas, color=color, x=positions[0], y=positions[1], w=w, h=h, x_vel=x_vel, y_vel=y_vel)


refresh_rate = 0.01
num_enemies = 10
x_spacing = 40
y_spacing = 40
enemies = []
heroes = []
start_x = 10
start_y = 40
x = start_x
y = start_y
x_vel = 1.5
y_vel = 0

for i in range(num_enemies):

    enemy = Enemy(canvas, x=x, y=y, x_vel=x_vel)
    enemies.append(enemy)
    x += x_spacing
    if i == (num_enemies/2)-1:
        x = start_x
        y += y_spacing


hero = Hero(canvas)
heroes.append(hero)

score = 0


def draw_all_enemies():
    for enemy in enemies:
        enemy.draw()


def wall_hit_check():
    wall_hit = False
    for enemy in enemies:
        if enemy.hit_wall():
            wall_hit = True
    return wall_hit


def shift_enemies():
    for enemy in enemies:
        enemy.x_vel = enemy.x_vel * -1
        enemy.canvas.move(enemy.id, 0, 10)


def draw_all_heroes():
    for hero in heroes:
        hero.draw()


def up_key_press(evt):
    global bullet
    if bullet is None:
        bullet = Bullet(canvas, firing_object=hero)


score_text_1 = score_text = canvas.create_text(630, 15, text="Score: ", font=("Arial", 16), fill="white")
score_text = canvas.create_text(680, 15, text=score, font=("Arial", 16), fill="white")


def hit_check(bullet):
    for enemy in enemies:
        if bullet is not None:
            if bullet.hit_other_object(enemy):
                enemies.remove(enemy)
                canvas.delete(enemy.id)
                global score
                global score_text
                score += 1
                canvas.delete(score_text)
                score_text = canvas.create_text(680, 15, text=score, font=("Arial", 16), fill="white")
                return True


win_text = None


def win():
    if score == num_enemies:
        global win_text
        win_text = canvas.create_text(360, 280, text="You Win!", font=("Arial", 40), fill="white")


canvas.bind_all('<KeyPress-Up>', up_key_press)

bullet = None


while 1:
    win()
    hit_check(bullet)
    draw_all_enemies()
    draw_all_heroes()
    if bullet is not None:
        bullet.draw()
        if bullet.hit_roof():
            bullet = None
    enemy_hit_wall = wall_hit_check()
    if enemy_hit_wall:
        shift_enemies()

    tk.update_idletasks()
    tk.update()
    time.sleep(refresh_rate)


tk.mainloop()

