#! /usr/bin/env python3
from collections import defaultdict
from itertools import zip_longest

class InvalidState(Exception): pass

class State: pass

def all_indexes(l, e):
	return [i for i,el in enumerate(l) if el==e]

class TM:
	def __init__(self, num_states=2):
		[setattr(self, str(n), type(str(n), (State,), {})) for n in range(num_states)]
		self.state = getattr(self,"1")
		self.tape = defaultdict(lambda :0)
		self.pos = 0
		self.instructions = {}

	def eval(self, value, movement, state):
		self.tape[self.pos] = value
		self.pos += movement
		self.state = state
	
	def __iter__(self):
		return self

	def __next__(self):
		if self.state == getattr(self,"0"):
			raise StopIteration
		else:
			inst = self.instructions[(self.state, self.tape[self.pos])]
			self.eval(*inst)
			return None
	
	def set_instructions(self, instructions_list):
		for inst in instructions_list:
			self.instructions[getattr(self,str(inst[0])), inst[1]] = (inst[2], inst[3], getattr(self,str(inst[4])))

	def set_input(self, value):
		value_list = []
		try:
			for e in value:
				value_list.extend([1]*(int(e)+1) + [0])
		except TypeError:
			value_list = [1]*(int(value)+1)
		self.tape.update(enumerate(value_list))
			
	def get_output(self):
		cell_list = [v for k,v in sorted(self.tape.items())]
		zeros = [None] + all_indexes(cell_list, 0)
		slices = (cell_list[slice(*s)] for s in zip_longest(zeros, zeros[1:]))
		return tuple(sum(s)-1 for s in slices)

if __name__ == "__main__":
	instructions = [
		(1,1,1,1,1),
		(1,0,1,0,0)
		]
	tm = TM()
	tm.set_instructions(instructions)
	tm.set_input(4)
	list(tm)
	print(tm.get_output())
