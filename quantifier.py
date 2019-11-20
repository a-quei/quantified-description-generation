#!/usr/local/bin/python3

"""
realiser.py: Meaning of quantifiers used for generating quantified description.
			 More details can be found in the paper: Chen et al., *Generating Quantified Descriptions of Abstract Visual Scenes*
"""

__author__ = "Guanyi Chen"
__email__ = "g.chen@uu.nl"


import sys
from random import sample

class Quantifier():

	def __init__(self, N):
		self.N = N
		self.Union = ["BS", "BC", "RS", "RC"]
		self.Shape = ["C", "S"]
		self.Color = ["R", "B"]
		self.O = ["O"]
		self.p2i = {"BS": 0, "BC": 1, "RS": 2, "RC": 3, "B": 4, "R": 5, "S": 6, "C": 7}


	def shuffle_value(self):
		self.Union = sample(self.Union, len(self.Union))
		self.Shape = sample(self.Shape, len(self.Shape))
		self.Color = sample(self.Color, len(self.Color))

	def U(self, A, B):
		if A in self.Color and B in self.Shape:
			return A + B
		elif A in self.Shape and B in self.Color:
			return B + A
		else:
			print("Some wrong happens in UNION({0}, {1})".format(A, B))
			sys.exit(-1)


	def All(self, A, B, situation, plural=0):
		if A == "O":
			num_A = self.N
			num_B = situation[self.p2i[B]]
		elif A in self.Shape + self.Color:
			num_A = situation[self.p2i[A]]
			num_B = situation[self.p2i[self.U(A, B)]]
		else:
			print("Some wrong happens in All({0}, {1})".format(A, B))
			sys.exit(-1)
		return num_A == num_B, num_A == num_B and num_A > 1

	def Everything(self, A, situation):
		if self.N == 1:
			return False
		return situation[self.p2i[A]] == self.N

	def Only(self, A, situation):
		if self.N == 1:
			return False
		return situation[self.p2i[A]] == self.N

	def Half(self, A, B, situation, plural_a=0, plural_b=0):
		#if A != "O" and situation[self.p2i[A]] % 2 != 0:
		#	return False, False
		if A == "O":
			num_A = self.N
			num_B = situation[self.p2i[B]]
		elif A in self.Shape + self.Color:
			num_A = situation[self.p2i[A]]
			num_B = situation[self.p2i[self.U(A, B)]]
		else:
			print("Some wrong happens in Half({0}, {1})".format(A, B))
			sys.exit(-1)
		check_exact_one = True
		if plural_b == 0:
			if num_B != 1:
				check_exact_one = False
		return num_A == num_B * 2, num_A == num_B * 2 and num_A > plural_a and num_B > plural_b and check_exact_one


	def Some(self, A, B, situation):
		#if A != "O" and situation[self.p2i[A]] % 2 != 0:
		#	return False, False
		if A == "O":
			num_A = self.N
			num_B = situation[self.p2i[B]]
		elif A in self.Shape + self.Color:
			num_A = situation[self.p2i[A]]
			num_B = situation[self.p2i[self.U(A, B)]]
		else:
			print("Some wrong happens in Some({0}, {1})".format(A, B))
			sys.exit(-1)

		return num_B > 1, num_B > 1 and num_B < num_A

	def Some_1(self, A, situation):
		num_A = situation[self.p2i[A]]

		return num_A > 1, num_A > 1 and num_A < self.N

	def Only_one(self, A, situation):
		num_A = situation[self.p2i[A]]

		return num_A == 1

	def More(self, A, B, situation):
		num_A = situation[self.p2i[A]]
		num_B = situation[self.p2i[B]]

		return num_A > num_B, num_A > num_B and num_B > 1

	def Fewer(self, A, B, situation):
		num_A = situation[self.p2i[A]]
		num_B = situation[self.p2i[B]]

		return num_A < num_B, num_A < num_B and num_A > 1

	def Equal(self, A, B, situation):
		num_A = situation[self.p2i[A]]
		num_B = situation[self.p2i[B]]

		return num_A == num_B, num_A == num_B and num_A > 1


	def Most(self, A, B, situation, plural_a=0, plural_b=0):
		if A == "O":
			num_A = self.N
			num_B = situation[self.p2i[B]]
		elif A in self.Shape + self.Color:
			num_A = situation[self.p2i[A]]
			num_B = situation[self.p2i[self.U(A, B)]]
		else:
			print("Some wrong happens in Half({0}, {1})".format(A, B))
			sys.exit(-1)
		return num_A * 0.5 < num_B, (num_A * 0.5 < num_B and num_A > num_B) and num_A > plural_a and num_B > plural_b

	def Minority(self, A, B, situation, plural_a=0, plural_b=0):
		if A == "O":
			num_A = self.N
			num_B = situation[self.p2i[B]]
		elif A in self.Shape + self.Color:
			num_A = situation[self.p2i[A]]
			num_B = situation[self.p2i[self.U(A, B)]]
		else:
			print("Some wrong happens in Half({0}, {1})".format(A, B))
			sys.exit(-1)
		return num_A * 0.5 > num_B, num_A * 0.5 > num_B and num_A > plural_a and num_B > plural_b

	def All_comb(self, situation):
		return situation[0] > 0 and situation[1] > 0 and situation[2] > 0 and situation[3] > 0

	def Half_Rest(self, A, B, C, situation, plural_a=0, plural_b=0, plural_c=0):
		#if A != "O" and situation[self.p2i[A]] % 2 != 0:
		#	return False, False
		if A == "O":
			num_A = self.N
			num_B = situation[self.p2i[B]]
			num_C = situation[self.p2i[C]]
		elif A in self.Shape + self.Color:
			num_A = situation[self.p2i[A]]
			num_B = situation[self.p2i[self.U(A, B)]]
			num_C = situation[self.p2i[self.U(A, C)]]
		else:
			print("Some wrong happens in Half({0}, {1})".format(A, B))
			sys.exit(-1)

		check_exact_one = True
		if plural_b == 0:
			if B in self.Shape and num_B != 1:
				check_exact_one = False
		if plural_c == 0:
			if num_C != 1:
				check_exact_one = False
		return num_A == num_B * 2 == num_C * 2, num_A == num_B * 2 == num_C * 2 and num_A > plural_a and num_B > plural_b  and num_C > plural_c and check_exact_one



if __name__ == '__main__':
	s = [2, 2, 0, 0, 4, 0, 2, 2]
	quantifier = Quantifier(4)
	print(quantifier.Half("O", "S", s))
	print(quantifier.Half("B", "S", s, plural_a=1))