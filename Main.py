from tkinter import *
import time
import winsound

#TODO: Make highscore retain even when window is closed
#TODO: Make mothership go across screen  every x number of bullets
#TODO: End game when enemies hit the bottom
#TODO: Enemies fire back

winsound.PlaySound('arcade.wav', winsound.SND_LOOP + winsound.SND_ASYNC + winsound.SND_NOSTOP)

bullet = None
score = 0
high_score = 0
hero = None
heroes = []
enemies = []
main_button_text = "Start Game"

running = False


params = {"refresh_rate": 0.01, "num_enemies": 1, "x_spacing": 40, "y_spacing": 40,
          "start_x": 273, "start_y": 20, "x_vel": 1.5, "y_vel": 0, "win_text": None, "version": 1.0}


def set_variables():
    global hero
    global heroes
    for hero in heroes:
        hero.canvas.delete(hero.id)
    hero = Hero(canvas)
    heroes = []
    global enemies
    for enemy in enemies:
        enemy.canvas.delete(enemy.id)
    enemies = []
    heroes.append(hero)
    x = params["start_x"]
    y = params["start_y"]

    for i in range(params["num_enemies"]):

        enemy = Enemy(canvas, x=x, y=y, x_vel=params["x_vel"])

        enemies.append(enemy)
        x += params["x_spacing"]
        if i == (params["num_enemies"] / 2) - 1:
            x = params["start_x"]
            y += params["y_spacing"]


def start_game(evt):
    global win_text
    canvas.delete(start_text)

    global score
    global high_score
    if score >= high_score:
        high_score_label['text'] = "High Score: " + str(score)
        high_score = score
    score = 0
    score_label['text'] = "Score: " + str(score)

    winsound.PlaySound('win.wav', winsound.SND_ASYNC)

    set_variables()
    game_loop()


def game_loop():
    global running
    global main_button_text
    running = True
    play_button.config(text="Restart")
    while 1 and running:

        win()
        global bullet
        if hit_check():
            canvas.delete(bullet.id)
            bullet = None
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
        time.sleep(params["refresh_rate"])


def pause(evt):
    global running

    if not running:
        running = not running
        pause_button.config(text="Pause Game")
        game_loop()

    else:
        running = not running
        pause_button.config(text="Resume Game")


tk = Tk()
tk.title("Frase Invaders!")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
score_label = Label(text="Score: " + str(score), bg='lightblue', font=('System', 18))
score_label.grid(row=0, column=1, sticky='ew')
high_score_label = Label(text="High score: " + str(high_score), bg='pink', font=('System', 18))
high_score_label.grid(row=0, column=2, sticky='ew')
play_button = Button(tk, text=main_button_text, bg="pink", font=('System', 18))
play_button.bind("<Button-1>", start_game)
play_button.grid(row=1, column=0, sticky='nesw')
restart_button = Button(tk, text="Version {}".format(params['version']), bg="pale green", font=('System', 18))
restart_button.bind("<Button-1>")
restart_button.grid(row=2, column=0, sticky='nesw')
pause_button = Button(tk, text="Pause Game", bg="lightblue", font=('System', 18))
pause_button.bind("<Button-1>", pause)
pause_button.grid(row=3, column=0, sticky='nesw')
canvas = Canvas(tk, width=720, height=560, bd=0, highlightthickness=0)
canvas.config(bg="black")
canvas.grid(row=1, column=1, rowspan=3, columnspan=2)
start_text = canvas.create_text(360, 280, text="FRASE INVADERS", font=("System", 40), fill="white")
win_text = None
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

    def __init__(self, canvas, color="firebrick2", x=10, y=10, w=15, h=15, x_vel=1, y_vel=0):
        super(Enemy, self).__init__(canvas, color=color , x=x, y=y, w=w, h=h, x_vel=x_vel, y_vel=y_vel)


class Hero(Sprite):

    def __init__(self, canvas, color="deepskyblue2", x=340, y=500, w=40, h=40, x_vel=0, y_vel=0):

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

    def __init__(self, canvas, color="lightblue", x=360, y=400, w=6, h=10, x_vel=0, y_vel=-5, firing_object=None):
        positions = firing_object.canvas.coords(firing_object.id)
        super(Bullet, self).__init__(canvas, color=color, x=positions[0], y=positions[1], w=w, h=h, x_vel=x_vel, y_vel=y_vel)


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
        global hero
        bullet = Bullet(canvas, firing_object=hero)
        winsound.PlaySound('gunshot.wav', winsound.SND_ASYNC)


def hit_check():
    global bullet
    for enemy in enemies:
        if bullet is not None:
            if bullet.hit_other_object(enemy):
                enemies.remove(enemy)
                canvas.delete(enemy.id)
                global score
                score += 1
                score_label['text'] = "Score: " + str(score)
                winsound.PlaySound('hit.wav', winsound.SND_ASYNC)

                return True


def win():
    global score
    global high_score
    global win_text
    if score == params["num_enemies"]:
        win_text = canvas.create_text(360, 280, text="You Win!", font=("System", 40), fill="white")
    if score >= high_score:
        high_score_label['text'] = "High Score: " + str(score)
        high_score = score


canvas.bind_all('<KeyPress-Up>', up_key_press)

tk.mainloop()

