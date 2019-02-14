import tkinter as tk

class Game(tk.Frame):
	def __init__(self, master):
		super(Game, self).__init__(master)
		self.lives = 3
		self.width = 900
		self.height = 600
		self.paddle_collisions = 0
		self.canvas = tk.Canvas(self, bg='#ffffff', width=self.width, height=self.height)
		self.canvas.pack()
		self.pack()
		
		self.items = {}
		self.ball = None
		self.bola = None
		self.paddle = Paddle(self.canvas, self.width/2, 420)
		self.items[self.paddle.item] = self.paddle
		
		self.hud = None
		self.setup_game()
		self.canvas.focus_set()
		self.canvas.bind('<Left>', lambda _: self.paddle.move(-20))
		self.canvas.bind('<Right>', lambda _: self.paddle.move(20))
		
	def setup_game(self):
		self.add_ball()
		self.update_lives_text()
		self.biodata()
		self.text = self.draw_text(450, 200, 'Press space to start')
		self.canvas.bind('<space>', lambda _: self.start_game())
		
	def add_ball(self):
		if self.ball and self.bola is not None:
			self.ball.delete()
			self.bola.delete()
		paddle_coords = self.paddle.get_position()
		x = (paddle_coords[0] + paddle_coords[2]) * 0.5
		self.ball = Ball(self.canvas, x + 15, 405)
		self.bola = Bola(self.canvas, x - 15, 405)
		self.paddle.set_ball(self.ball)
		self.paddle.set_bola(self.bola)
		
	def draw_text(self, x, y, text, size='40'):
		font = ('Arial', size)
		return self.canvas.create_text(x, y, text=text, font=font)
		
	def update_lives_text(self):
		text = 'Lives: %s' % self.lives
		if self.hud is None:
			self.hud = self.draw_text(850, 20, text, 15)
		else:
			self.canvas.itemconfig(self.hud, text=text)
			
	def biodata(self):
		font = ('Arial')
		text = self.draw_text(101, 20, 'Nama	=   Faturachman Yusup', 10)
		text = self.draw_text(75, 35, 'NIM	=   311810214', 10)
		text = self.draw_text(67, 50, 'Kelas      =   TI.18.D2', 10)
		
			
	def start_game(self):
		self.canvas.unbind('<space>')
		self.canvas.delete(self.text)
		self.paddle.ball = None
		self.paddle.bola = None
		self.game_loop()
		
	def game_loop(self):
		self.check_collisions()
		self.check_collisionsb()
		if self.ball.get_position()[1] >= self.height and self.bola.get_position()[1] >= self.height:
			self.bola.speed = None
			self.ball.speed = None
			self.lives -= 1
			if self.lives < 0:
				self.draw_text(300, 200, 'Game Over')
			else:
				self.paddle_collisions = 0
				self.after(1000, self.setup_game)
		else:
			self.ball.update()
			self.bola.update()
			self.after(50, self.game_loop)
			
	def check_collisions(self):
		bola_coords = self.bola.get_position()
		items = self.canvas.find_overlapping(*bola_coords)
		if len(items) > 1:
			if self.paddle_collisions > 0:
				self.bola.direction[1] *= -1
				x = self.bola.direction[0] * self.bola.speed
				y = self.bola.direction[1] * self.bola.speed
				self.bola.move(x, y)
			self.paddle_collisions += 1
			
	def check_collisionsb(self):
		ball_coords = self.ball.get_position()
		itemss = self.canvas.find_overlapping(*ball_coords)
		if len(itemss) > 1:
			if self.paddle_collisions > 0:
				self.ball.direction[1] *= -1
				x = self.ball.direction[0] * self.ball.speed
				y = self.ball.direction[1] * self.ball.speed
				self.ball.move(x, y)
			self.paddle_collisions += 1	

class GameObject(object):
	def __init__(self, canvas, item):
		self.canvas = canvas
		self.item = item
		
	def get_position(self):
		return self.canvas.coords(self.item)
		
	def move(self, x, y):
		self.canvas.move(self.item, x, y)
		
	def delete(self):
		self.canvas.delete(self.item)
		
class Ball(GameObject):
	def __init__(self, canvas, x, y):
		self.radius = 10
		self.direction = [1, 1]
		self.speed = 5
		item = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, fill='#008')
		super(Ball, self).__init__(canvas, item)
		
	def update(self):
		coords = self.get_position()
		width = self.canvas.winfo_width()
		if coords[0] <= 0 or coords[2] >= width:
			self.direction[0] *= -1
		if coords[1] <= 0:
			self.direction[1] *= -1
		x = self.direction[0] * self.speed
		y = self.direction[1] * self.speed
		self.move(x, y)
		
class Bola(GameObject):
	def __init__(self, canvas, x, y):
		self.radius = 10
		self.direction = [-1, -1]
		self.speed = 7
		item = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, fill='#800')
		super(Bola, self).__init__(canvas, item)
		
	def update(self):
		coords = self.get_position()
		width = self.canvas.winfo_width()
		if coords[0] <= 0 or coords[2] >= width:
			self.direction[0] *= -1
		if coords[1] <= 0:
			self.direction[1] *= -1
		x = self.direction[0] * self.speed
		y = self.direction[1] * self.speed
		self.move(x, y)
		
class Paddle(GameObject):
	def __init__(self, canvas, x, y):
		self.width = 80
		self.height = 10
		self.ball = None
		self.bola = None
		item = canvas.create_rectangle(x - self.width / 2, y - self.height / 2, x + self.width / 2, y + self.height / 2, fill='#000000')
		super(Paddle, self).__init__(canvas, item)
		
	def set_ball(self, ball):
		self.ball = ball
		
	def set_bola(self, bola):
		self.bola = bola
		
	def move(self, offset):
			coords = self.get_position()
			width = self.canvas.winfo_width()
			if coords[0] + offset >= 0 and coords[2] + offset <= width:
				super(Paddle, self).move(offset, 0)
				if self.ball and self.bola is not None:
					self.ball.move(offset, 0)
					self.bola.move(offset, 0)
					
if __name__ == '__main__':
	root = tk.Tk()
	root.title('GameBall')
	game = Game(root)
	game.mainloop()