#! /usr/bin/env python3
from collections import defaultdict
from itertools import zip_longest

class InvalidState(Exception): pass

class _State: pass

class State:
	instances = {n:_State() for n in range(2)}
	def __new__(cls, n):
		inst = cls.instances.get(n, None)
		if not inst:
			raise InvalidState("%s is not a valid state" % n)
		return inst

def all_indexes(l, e):
	return [i for i,el in enumerate(l) if el==e]

class TM:
	def __init__(self):
		self.tape = defaultdict(lambda :0)
		self.state = State(1)
		self.pos = 0
		self.instructions = {}

	def eval(self, value, movement, state):
		self.tape[self.pos] = value
		self.pos += movement
		self.state = state
	
	def __iter__(self):
		return self

	def __next__(self):
		if self.state == State(0):
			raise StopIteration
		else:
			inst = self.instructions[(self.state, self.tape[self.pos])]
			self.eval(*inst)
			return None
	
	def set_instructions(self, instructions_list):
		for inst in instructions_list:
			self.instructions[State(inst[0]), inst[1]] = (inst[2], inst[3], State(inst[4]))

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
