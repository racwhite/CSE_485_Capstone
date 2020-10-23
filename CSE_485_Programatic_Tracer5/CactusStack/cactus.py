class Node:
	def __init__(self, id, vars):
		# frame name
		self.id = id
		# local vars
		self.vars = vars
		# global scope is root, other scopes have parents updated in push()
		self.parent = None
		# tracking children allows for backtracking to 'popped' frames
		self.children = []
		# new node represents current frame
		self.current_frame = self
		# global scope has no enclosed scope, other scopes have enclosed scopes updated in push()
		self.enclosed_frame = None

	# scope enter, add child node
	def push(self, child):
		# parent of new node is the enclosing scope(presently the current frame)
		child.parent = self.current_frame
		# add child to parents list of children
		self.current_frame.children.append(child)
		# update current and enclosing frame
		self.current_frame = child
		self.enclosed_frame = child.parent

	# scope exit, update current and enclosing frames
	def pop(self):
		# if current frame stack is not empty, update current frame
		if(not self.is_empty()):
			self.current_frame = self.current_frame.parent
		else:
			print('Stack is empty')
		# if enclosing frame is not empty, update enclosing frame
		if(self.enclosed_frame is not None):
			self.enclosed_frame = self.enclosed_frame.parent
		# otherwise simply 'pop' current frame
		else:
			self.current_frame = None

	# print current and enclosing frame info
	def print_frame(self):
		# if current frame is not null, print name and local vars
		if(self.current_frame is not None):
			print('Current scope: ', self.current_frame.id)
			print('Local vars: ', self.current_frame.vars)
		else:
			print('Current scope: None')
		# if enclosing frame is not null, print name
		if(self.enclosed_frame is not None):
			print('Enclosed scope: ', self.enclosed_frame.id)
		else:
			print('Enclosed scope: None')
		print('\n')

	# print calling structure of frame stack
	def print_frame_stack(self):
		# temp variable to traverse tree
		temp = self.current_frame
		# traverse all the way to the root, but no further
		while(temp is not None):
			if(temp.parent is not None):
				# non root 
				print(temp.id, ' called by:')
			else:
				# root
				print(temp.id + '\n')
			temp = temp.parent

	# find var in current frame stack
	def find_var(self, var):
		temp = self.current_frame
		# begin by looking at local vars, and work up to global
		while(temp is not None):
			if(var in temp.vars):
				# print scope name and var value
				print('Variable found in: ', temp.id)
				return temp.vars.get(var)
			temp = temp.parent
		return 'Not found'

	# check if frame stack is empty
	def is_empty(self):
		if(self.current_frame is None):
			return True
		else:
			return False

	# return children of current_frame
	def get_children(self):
		return self.current_frame.children



if __name__ == '__main__':
	Cactus = Node('__module__', {'func1':'func1', 'func2':'func2', 'fucn3':'func3', 'a':1, 'b':2, 'c':3, 'd':4})
	Cactus.push(Node('func1', {'a':10, 'b':20, 'c':30}))
	Cactus.push(Node('func2', {'a':100, 'b':200, 'c':300}))
	Cactus.print_frame_stack()

	print(Cactus.find_var('c'))
	print('\n')

	Cactus.pop()
	print(Cactus.get_children()[0].id)
	print(Cactus.get_children()[0].vars)
	print('\n')

	Cactus.print_frame_stack()
	print('Children of current frame %s: ' % Cactus.current_frame.id)
	for child in Cactus.get_children():
		print(child.id)
	print('\n')

	Cactus.pop()
	Cactus.print_frame_stack()

	Cactus.push(Node('func3', {'a':1000, 'b':2000, 'c':3000}))
	Cactus.print_frame()

	Cactus.pop()
	Cactus.print_frame()

	print(Cactus.find_var('e'))
	print('\n')

	if(Cactus.is_empty()):
		print('Stack is empty')
	else:
		print('Stack is not empty')
	print('Children of current frame %s: ' % Cactus.current_frame.id)
	for child in Cactus.get_children():
		print(child.id)
	print('\n')

	Cactus.pop()
	if(Cactus.is_empty()):
		print('Stack is empty')
	else:
		print('Stack is not empty')

	Cactus.pop()
	Cactus.print_frame()
