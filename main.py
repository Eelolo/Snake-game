from tkinter import *
import random
from PIL import ImageTk, Image


class Snake(Frame):
    reversed_moves = {
        "left": 'right',
        "right": 'left',
        "up": 'down',
        "down": 'up'
    }

    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, self.parent)

        self.read_images()

        self.snake = []
        self.snake_img = self.head_img
        self.direction = 'right'
        self.last_direction = self.direction
        self.direction_changed = False
        self.moving = False

        self.create_widgets()
        self.new_apple()
        self.configure_widgets()
        self.draw_widgets()

    def read_images(self):
        self.bg_img = ImageTk.PhotoImage(Image.open('resources/background.jpg').resize((700, 700), 0))
        self.white_img = ImageTk.PhotoImage(Image.open('resources/white.png'))
        self.down_left_img = ImageTk.PhotoImage(Image.open('resources/down-left.png'))
        self.down_right_img = ImageTk.PhotoImage(Image.open('resources/down-right.png'))
        self.from_down_img = ImageTk.PhotoImage(Image.open('resources/from-down.png'))
        self.from_left_img = ImageTk.PhotoImage(Image.open('resources/from-left.png'))
        self.from_right_img = ImageTk.PhotoImage(Image.open('resources/from-right.png'))
        self.from_up_img = ImageTk.PhotoImage(Image.open('resources/from-up.png'))
        self.head_img = ImageTk.PhotoImage(Image.open('resources/head.png'))
        self.hor_img = ImageTk.PhotoImage(Image.open('resources/hor.png'))
        self.up_left_img = ImageTk.PhotoImage(Image.open('resources/up-left.png'))
        self.up_right_img = ImageTk.PhotoImage(Image.open('resources/up-right.png'))
        self.vert_img = ImageTk.PhotoImage(Image.open('resources/vert.png'))
        self.apple_img = ImageTk.PhotoImage(Image.open('resources/apple.png'))

    def calculate_field_coords(self):
        self.field_coords = []
        for x in range(0, 700, 100):
            for y in range(0, 700, 100):
                self.field_coords.append((x, y))

    def fill_field(self):
        self.white_rects = {}

        for x, y in self.field_coords:
            rect = self.canv.create_image(x, y, anchor='nw', image=self.white_img)
            self.white_rects[rect] = x, y

        self.canv.itemconfigure(self.get_white_rect_id(0, 0), state=HIDDEN)

    def disable_field(self):
        for item_id in self.white_rects.keys():
            self.canv.itemconfigure(item_id, state=HIDDEN)

    def create_widgets(self):
        self.canv = Canvas(self, width=700, height=700)
        self.canv.create_image(0, 0, anchor='nw', image=self.bg_img)
        self.calculate_field_coords()
        self.fill_field()
        self.head = self.canv.create_image(0, 0, anchor='nw', image=self.snake_img)
        self.snake.insert(0, self.head)

    def configure_widgets(self):
        self.canv.focus_set()

        self.canv.bind('<Left>', lambda event, direction='left': self.change_direction(event, direction))
        self.canv.bind('<Right>', lambda event, direction='right': self.change_direction(event, direction))
        self.canv.bind('<Up>', lambda event, direction='up': self.change_direction(event, direction))
        self.canv.bind('<Down>', lambda event, direction='down': self.change_direction(event, direction))

    def draw_widgets(self):
        self.canv.pack()

    def change_direction(self, event, direction):
        if self.reversed_moves[self.direction] != direction:
            self.last_direction = self.direction
            self.direction = direction

            if len(self.snake) > 1:
                self.define_angled_img()

        if not self.moving:
            self.moving = True
            self.move()

    def define_angled_img(self):
        lastdir = self.last_direction
        dir = self.direction

        if lastdir == dir:
            return

        if lastdir == 'left' and dir == 'down' or lastdir == 'up' and dir == 'right':
            self.snake_img = self.down_right_img
        elif lastdir == 'right' and dir == 'down' or lastdir == 'up' and dir == 'left':
            self.snake_img = self.down_left_img
        elif lastdir == 'left' and dir == 'up' or lastdir == 'down' and dir == 'right':
            self.snake_img = self.up_right_img
        else:
            self.snake_img = self.up_left_img

        self.direction_changed = True

    def get_left_coords(self):
        x, y = self.canv.coords(self.head)

        if x <= 0:
            x = 700

        x -= 100

        return x, y

    def get_right_coords(self):
        x, y = self.canv.coords(self.head)

        if x >= 600:
            x = -100

        x += 100

        return x, y

    def get_up_coords(self):
        x, y = self.canv.coords(self.head)

        if y <= 0:
            y = 700

        y -= 100

        return x, y

    def get_down_coords(self):
        x, y = self.canv.coords(self.head)

        if y >= 600:
            y = -100

        y += 100

        return x, y

    def get_move_coords(self):
        if self.direction == 'left':
            x, y = self.get_left_coords()
        elif self.direction == 'right':
            x, y = self.get_right_coords()
        elif self.direction == 'up':
            x, y = self.get_up_coords()
        else:
            x, y = self.get_down_coords()

        return x, y

    def delete_last(self):
        last = self.snake.pop(-1)
        x, y = self.canv.coords(last)
        self.canv.itemconfigure(self.get_white_rect_id(x, y), state=NORMAL)
        self.canv.delete(last)

    def get_white_rect_id(self, x, y):
        for k, v in self.white_rects.items():
            if v == (x, y):
                return k

    def create_first(self, x, y):
        if len(self.snake) == 0:
            self.head = self.canv.create_image(x, y, anchor='nw', image=self.head_img)
        elif len(self.snake) > 0:
            img = getattr(self, f'from_{self.reversed_moves[self.direction]}_img')
            self.head = self.canv.create_image(x, y, anchor='nw', image=img)

        self.canv.itemconfigure(self.get_white_rect_id(x, y), state=HIDDEN)
        self.snake.insert(0, self.head)

    def configure_img_direction(self):
        if len(self.snake) > 1:
            if self.direction in ('left', 'right'):
                if not self.direction_changed:
                    self.snake_img = self.hor_img
                else:
                    self.direction_changed = False

                self.canv.itemconfigure(self.snake[1], image=self.snake_img)
            else:
                if not self.direction_changed:
                    self.snake_img = self.vert_img
                else:
                    self.direction_changed = False

                self.canv.itemconfigure(self.snake[1], image=self.snake_img)

    def move(self):
        self.check_game_over()

        x, y = self.get_move_coords()
        self.delete_last()
        self.create_first(x, y)

        self.configure_img_direction()

        self.eat_apple()

        self.after(500, self.move)

    def eat_apple(self):
        if self.canv.coords(self.head) == self.canv.coords(self.apple):
            self.canv.delete(self.apple)
            del self.apple
            x, y = self.canv.coords(self.head)
            self.canv.itemconfigure(self.get_white_rect_id(x, y))
            self.increase_tail()
            self.new_apple()

    def get_snake_coords(self):
        snake_coords = []
        for item_id in self.snake:
            snake_coords.append(self.canv.coords(item_id))

        return snake_coords

    def new_apple(self):
        x, y = random.choice(self.field_coords)

        snake_coords = self.get_snake_coords()
        while [x, y] in snake_coords:
            x, y = random.choice(self.field_coords)

        self.canv.itemconfigure(self.get_white_rect_id(x, y), state=HIDDEN)
        self.apple = self.canv.create_image(x, y, anchor='nw', image=self.apple_img)

    def increase_tail(self):
        new_canv = self.canv.create_image(-100, -100, anchor='nw', image=self.head_img)
        setattr(self, f'tail{new_canv}', new_canv)
        self.snake.append(getattr(self, f'tail{new_canv}'))

    def check_game_over(self):
        snake_coords = self.get_snake_coords()
        if snake_coords[0] in snake_coords[1:]:
            self.quit()
            self.parent.quit()


if __name__ == '__main__':
    root = Tk()
    snake = Snake(root)
    snake.pack()
    while True:
        snake.destroy()
        snake = Snake(root)
        snake.pack()
        root.mainloop()
