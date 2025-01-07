import pygame

class Mouse():
	def __init__(self):
		self.button = {}
		self.button["Left"] = False
		self.button["Middle"] = False
		self.button["Right"] = False
		self.pos = (0,0)

		self.scroll_dir = 0

		self.triggered = {}
		self.triggered["Left"] = False
		self.triggered["Middle"] = False
		self.triggered["Right"] = False

		self.flags = {}
		self.flags["Left"] = False
		self.flags["Middle"] = False
		self.flags["Right"] = False
		
	
	def update(self):
		##This will be run in the main loop at all times
		L_click, M_click, R_click = pygame.mouse.get_pressed(num_buttons=3)
		self.button["Left"] = L_click
		self.button["Middle"] = M_click
		self.button["Right"] = R_click
		self.pos = pygame.mouse.get_pos()
		self.scroll_dir = 0

		if L_click and not self.flags["Left"]:
			self.triggered["Left"] = True
			self.flags["Left"] = True
		elif L_click:
			self.triggered["Left"] = False
		else:
			self.flags["Left"] = False
			self.triggered["Left"] = False

		if M_click and not self.flags["Middle"]:
			self.triggered["Middle"] = True
			self.flags["Middle"] = True
		elif M_click:
			self.triggered["Middle"] = False
		else:
			self.flags["Middle"] = False
			self.triggered["Middle"] = False

		if R_click and not self.flags["Right"]:
			self.triggered["Right"] = True
			self.flags["Right"] = True
		elif R_click:
			self.triggered["Right"] = False
		else:
			self.flags["Right"] = False
			self.triggered["Right"] = False

	def peek_button(self, button:str) -> bool:
		##button: (str) "Left", "Middle", "Right"
		return self.button[button]
	
	def peek_pos(self) -> tuple[int,int]:
		##Returns (x,y) of mouse
		return self.pos
	
	def press_triggered(self, button:str) -> bool:
		##button: (str) "Left", "Middle", "Right"
		##Check if button was just now pressed
		return self.triggered[button]



class Input_events():
	def __init__(self):
		self.keys = {}
		self.keys["Return"] = False
		self.keys["Alt"] = False

		self.keys["Enter"] = False

		self.keys["F1"] = False
		self.keys["F2"] = False
		self.keys["F3"] = False

		self.mouse_wheel = 0
		# ^ = -1 (up)
		# ^ = 1 (down)
	
	def update(self, event):
		##This will be run in the main loop at all time
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				self.keys["Return"] = True
			elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
				self.keys["Alt"] = True

			elif event.key == pygame.K_RETURN:
				self.keys["Enter"] = True
			
			elif event.key == pygame.K_F1:
				self.keys["F1"] = True
			elif event.key == pygame.K_F2:
				self.keys["F2"] = True
			elif event.key == pygame.K_F3:
				self.keys["F3"] = True
		
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RETURN:
				self.keys["Return"] = False
			elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
				self.keys["Alt"] = False
			
			elif event.key == pygame.K_RETURN:
				self.keys["Enter"] = False
	
			elif event.key == pygame.K_F1:
				self.keys["F1"] = False
			elif event.key == pygame.K_F2:
				self.keys["F2"] = False
			elif event.key == pygame.K_F3:
				self.keys["F3"] = False

		elif event.type == pygame.MOUSEWHEEL:
			self.mouse_wheel = event.y
	
	def reset_events(self):
		#runs in main loop to reset some events like scroll wheel
		self.mouse_wheel = 0

	def peek_key(self, key:str):
		#keys: (str) what keys do you wnat to know the state of
		return self.keys[key]
	
	def peek_wheel_dir(self):
		return self.mouse_wheel
