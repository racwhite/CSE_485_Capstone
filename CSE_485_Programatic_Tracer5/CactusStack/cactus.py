class Node:
	# list of scopes
	scopes = []
	
	def __init__(self, id, vars):
		# frame name
		self.id = id
		# local vars
		self.vars = vars
		# global scope is root, other scopes have parents updated in push()
		self.parent = None
		# tracking children allows for backtracking to 'popped' frames
		self.children = []
		# add scope to list
		Node.scopes.append(id)
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
		if not self.is_empty():
			# begin by looking at local vars, and work up to global
			while(temp is not None):
				if(var in temp.vars):
					# print scope name and var value
					print('Variable found in: ', temp.id)
					return temp
				temp = temp.parent
			print('Not found')
		else:
			print('Stack is empty')

	# check if frame stack is empty
	def is_empty(self):
		if(self.current_frame is None):
			return True
		else:
			return False

	# new program, empty scope list
	def reset_scopes(self):
		Node.scopes = []

	# return children of current_frame
	def get_children(self):
		return self.current_frame.children

	# only modify variable in current scope, essentially redundant with mod_outside_scope
	def mod_current_scope(self, var, val):
		if not self.is_empty():
			# check if var exists in current scope
			if var in self.current_frame.vars:
				# if it does, modify it
				self.current_frame.vars[var] = val
			else:
				print('Var not found')
		else:
			print('Stack is empty')

	# modify variables in any scope that exists in the tree
	def mod_outside_scope(self, var, val, name):
		# make sure scope exists
		if name not in Node.scopes:
			print('No scope called %s' % name)
		else:
			# check if current scope is the desired one
			if self.id == name:
				# if so, make sure variable exists in scope
				if var in self.vars:
					# if so, modify it
					self.vars[var] = val
				else:
					print('No variable called %s in %s' % (var, name))
			else:
				# since scope exists in tree, recursively search for it
				for child in self.children:
					child.mod_outside_scope(var, val, name)

	# print scopes that exist in tree
	def print_all_scopes(self):
		if not self.is_empty():
			print(repr(self.scopes) + '\n')
		else:
			print('Stack is empty')

	# print tree structure
	def print_tree(self, level = 0):
		# print scope name and vars
		# indents represent child vs parent
		ret = '\t'*level+self.id+repr(self.vars)+'\n'
		# recursively traverse tree
		for child in self.children:
			# increase indent to represent children
			ret += child.print_tree(level+1)
		return ret


if __name__ == '__main__':
	Cactus = Node('__module__', {'func1':'func1', 'func2':'func2', 'fucn3':'func3', 'a':1, 'b':2, 'c':3, 'd':4, 'z':8})
	Cactus.push(Node('func1', {'a':10, 'b':20, 'c':30}))
	Cactus.push(Node('func2', {'a':100, 'b':200, 'c':300}))
	Cactus.pop()
	Cactus.pop()
	Cactus.push(Node('func3', {'a':1000, 'b':2000, 'c':3000}))

	print(Cactus.print_tree())

	Cactus.print_all_scopes()

	Cactus.mod_current_scope('a', 700000)
	Cactus.mod_outside_scope('z', 50000, '__module__')
	Cactus.mod_outside_scope('b', 0, 'func2')

	print(Cactus.print_tree())
