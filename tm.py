#! /usr/bin/env python3
from collections import defaultdict
from itertools import zip_longest, chain

def all_indexes(l, e):
	return [i for i,el in enumerate(l) if el==e]

class TM:
	def __init__(self):
		self.tape = defaultdict(lambda :0)
		self.state = 1
		self.pos = 0
		self.instructions = {}

	def eval(self, value, movement, state):
		self.tape[self.pos] = value
		self.pos += movement
		self.state = state
	
	def __iter__(self):
		return self

	def __next__(self):
		if self.state == 0:
			raise StopIteration
		else:
			inst = self.instructions[(self.state, self.tape[self.pos])]
			self.eval(*inst)
			return self
	
	def set_instructions(self, instructions_list):
		for inst in instructions_list:
			self.instructions[inst[0], inst[1]] = (inst[2], inst[3], inst[4])

	def _reset(self):
		self.tape.clear()
		self.state = 1
		self.pos = 0

	def set_input(self, value):
		self._reset()
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
		return tuple(sum(s)-1 for s in slices if any(s))
	
	def __str__(self):
		state = str(self.state)
		m = min(self.tape)
		cell_list = [str(v) for k,v in sorted(self.tape.items())]
		size = len(cell_list)
		return state + "v".rjust(self.pos+2-m) + "\n " + \
	("".join(cell_list)).rjust(size+len(state))


from unittest import TestCase, main
from random import randint
from itertools import accumulate

def prepare_list():
	return chain([0, 1], accumulate(randint(0,11) for i in range(20)))

def prepare_tuple_list():
	return chain([(0,0),(1,0),(0,1),(1,1)], ((randint(0,11),randint(0,11)) for i in range(20)))

def prepare_varlength_tuples():
	return chain([(0,0),(1,0),(0,1),(1,1)], ([randint(0, 11) for i in range(randint(2, 200))] for j in range(20)))

class AbstractTest:
	inputs = prepare_list()

	def setUp(self):
		self.tm = TM()
		self.tm.set_instructions(type(self).instructions)
		self.inputs = type(self).inputs
		

	def test_instructions(self):
		for inp in self.inputs:
			self.tm.set_input(inp)
			list(self.tm)
			self.check_output(inp)
		
	def check_output(self, inp):
		raise NotImplemented

class PlusOne(AbstractTest, TestCase):
	instructions = [
		(1,1,1,1,1),
		(1,0,1,0,0)
		]

	def check_output(self, inp):
		self.assertEqual(inp+1, *self.tm.get_output())

class CheckPair(AbstractTest, TestCase):
	instructions = [
		(1,1,1,0,0)
		]
	inputs = prepare_tuple_list()

	def check_output(self, inp):
		self.assertEqual(inp, self.tm.get_output())

class SumPair(AbstractTest, TestCase):
	instructions = [
		(1,1,1,1,1),
		(1,0,1,1,2),
		(2,1,1,1,2),
		(2,0,0,-1,3),
		(3,1,0,-1,4),
		(4,1,0,0,0)
		]
	inputs = prepare_tuple_list()

	def check_output(self, inp):
		self.assertEqual(sum(inp), *self.tm.get_output())

class Double(AbstractTest, TestCase):
	instructions = [
		(1,1,1,1,2),
		(2,0,0,0,0),
		(2,1,1,-1,3),
		(3,1,0,-1,3),
		(3,0,1,1,4),
		(4,0,1,1,4),
		(4,1,1,0,1)
		]

	def check_output(self, inp):
		self.assertEqual(2*inp, *self.tm.get_output())

class Sum(AbstractTest, TestCase):
	instructions = [
		(1,1,1,1,1),
		(1,0,1,1,5),
		(2,1,1,-1,2),
		(2,0,0,1,3),
		(3,1,0,1,4),
		(4,1,0,1,1),
		(5,1,1,0,2),
		(5,0,0,-1,6),
		(6,1,0,0,0),
		]
	inputs = prepare_varlength_tuples()

	def check_output(self, inp):
		self.assertEqual(sum(inp), *self.tm.get_output())

class Fc1(AbstractTest, TestCase):
	# instructions = [
	# 	(1,1,1,1,2),
	# 	(2,0,1,1,0),
	# 	(2,1,0,1,3),
	# 	(3,0,0,1,0),
	# 	(3,1,1,-1,4),
	# 	(4,0,1,1,5),
	# 	(5,1,0,1,5),
	# 	(5,0,0,1,0),
	# 	]
	instructions = [
		(1,1,1,1,2),
		(2,0,1,1,0),
		(2,1,1,1,3),
		(3,0,0,-1,4),
		(3,1,0,1,4),
		(4,1,0,1,4),
		(4,0,0,0,0),
		]
	inputs = range(20)
	
	def check_output(self, inp):
		if inp == 1:
			self.assertEqual(0, *self.tm.get_output())
		else:
			self.assertEqual(1, *self.tm.get_output())

# class SwapMul2(AbstractTest, TestCase):
# 	instructions = [
# 		(1,1,0,1,9),
# 		(9,0,0,1,10),
# 		(9,1,1,1,2),
# 		(2,1,1,1,2),
# 		(2,0,0,1,3),
# 		(3,1,1,1,3),
# 		(3,0,0,1,4),
# 		(4,0,1,1,5),
# 		(4,1,1,1,4),
# 		(5,0,1,-1,6),
# 		(6,1,1,-1,6),
# 		(6,0,0,-1,7),
# 		(7,1,1,-1,7),
# 		(7,0,0,-1,8),
# 		(8,1,1,-1,8),
# 		(8,0,0,1,1),
# 		(10,1,1,1,10),
# 		(10,0,0,1,11),
# 		(11,0,1,1,12),
# 		(11,1,1,1,11),
# 		(12,0,1,-1,0),
# 		]
# 	inputs = prepare_tuple_list()
	
# 	def check_output(self, inp):
# 		self.assertEqual((inp[1], 2*inp[0]), self.tm.get_output())

class testF(AbstractTest, TestCase):
	instructions = [
		(1,1,0,1,2),
		(2,1,0,1,3),
		(3,1,0,1,4),
		(4,1,0,1,5),
		(5,0,0,1,8),
		(3,0,1,0,0),
		(4,0,0,1,6),
		(6,1,1,1,6),
		(6,0,0,1,7),
		(7,1,0,1,7),
		(7,0,0,0,0),
		(8,1,0,1,8),
		(8,0,0,0,0),
		]
	# instructions = [
	# 	(1,1,0,1,2),
	# 	(2,1,0,1,3),
	# 	(3,0,1,0,0),
	# 	(3,1,0,1,4),
	# 	(4,0,0,1,5),
	# 	(5,1,1,1,5),
	# 	(5,0,0,1,6),
	# 	(6,1,0,1,6),
	# 	(6,0,0,0,0),
	# 	(4,1,0,1,7),
	# 	(7,0,0,1,8),
	# 	(8,1,0,1,8),
	# 	(8,0,0,0,0),
	# 	]
	inputs = [(1,0), (1,1)]+[(1,randint(0,22)) for i in range(10)] + \
		[(2,0,0), (2,0,1), (2,1,0), (2,1,1)]+[(2,randint(0,22), randint(0,22)) for i in range(10)] + \
		[(3,0,0,0), (3,0,1,1), (3,1,0,0), (3,1,1,1)]+[(3,randint(0,22), randint(0,22), randint(0,22)) for i in range(10)]
	
	def check_output(self, inp):
		self.assertEqual(self.f(inp), self.tm.get_output())

	def f(self, inp):
		x, y = inp[0], inp[1:]
		if x==1:
			if len(y)!=1: raise Exception()
			return (y[0]+1,)
		elif x==2:
			return (y[0],)
		elif x==3:
			return (y[1], y[2])

if __name__ == "__main__":
	main()
