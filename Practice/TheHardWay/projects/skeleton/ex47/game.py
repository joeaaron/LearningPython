class Room(object):
	"""docstring for Room"""
	def __init__(self, name, description):
		self.name = name
		self.description = description
		self.paths = {}

	def go(self, direction):
		return self.paths.get(direction, None)

	def add_paths(self, paths):
		self.paths.update(paths)

		