#!/usr/local/bin/python3

"""
realiser.py: The reasoner of the incremental algorithm for generating quantified description.
			 More details can be found in the paper: Chen et al., *Generating Quantified Descriptions of Abstract Visual Scenes*
"""

__author__ = "Guanyi Chen"
__email__ = "g.chen@uu.nl"

import sys
from quantifier import Quantifier


class Reasoner():

	def __init__(self, N):
		self.quantifier = Quantifier(N)

	def _combination(self, list_1, list_2):
		result = []
		for item_1 in list_1:
			for item_2 in list_2:
				result.append((item_1, item_2))
		return result

	def _combination_3(self, list_1, list_2):
		result = []
		for item_1 in list_1:
			for item_2 in list_2:
				for item_3 in list_2:
					if item_3 != item_2:
						result.append((item_1, item_2, item_3))
		return result

	def _self_combination(self, l):
		result = []
		for item_1 in l:
			for item_2 in l:
				if item_1 != item_2:
					result.append((item_1, item_2))
		return result

	def _is_plural(self, property, situation):
		return situation[self.quantifier.p2i[property]] > 0

	def All(self, target, situations, length):
		Q = []
		self.quantifier.shuffle_value() # increaase the diversity
		possible_comb = self._combination(self.quantifier.O, self.quantifier.Union + self.quantifier.Shape + self.quantifier.Color) + \
						self._combination(self.quantifier.Shape, self.quantifier.Color) + \
						self._combination(self.quantifier.Color, self.quantifier.Shape)
		for A, B in possible_comb:
			# pluralty of the A:
			pluarl_a = 1 if A == "O" or self._is_plural(A, target) else 0
			# pluralty of the B:
			plural_b = 1 if self._is_plural(B, target) else 0
			# if P(V) is true for the target
			if self.quantifier.All(A, B, target, pluarl_a)[1]:
				# how many possible situations left
				left_reason, left = [], []
				for distractor in situations:
					is_left_reason, is_left = self.quantifier.All(A, B, distractor, pluarl_a)
					if is_left_reason:
						left_reason.append(distractor)
					if is_left:
						left.append(distractor)
				if len(situations) - len(left_reason) > 0:
					Q.append({"quantifier": "all", "params": [(A, pluarl_a), (B, plural_b)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length

	def Everything(self, target, situations, length):
		Q = []
		possible_comb = self.quantifier.Union + self.quantifier.Shape + self.quantifier.Color
		for A in possible_comb:
			# if P(V) is true for the target
			if self.quantifier.Everything(A, target):
				# how many possible situations left
				left = []
				for distractor in situations:
					if self.quantifier.Everything(A, distractor):
						left.append(distractor)
				if len(situations) - len(left) > 0:
					Q.append({"quantifier": "everything", "params": [(A, 1)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length

	def Only(self, target, situations, length):
		Q = []
		possible_comb = self.quantifier.Union + self.quantifier.Shape + self.quantifier.Color
		for A in possible_comb:
			# if P(V) is true for the target
			if self.quantifier.Only(A, target):
				# how many possible situations left
				left = []
				for distractor in situations:
					if self.quantifier.Only(A, distractor):
						left.append(distractor)
				if len(situations) - len(left) > 0:
					Q.append({"quantifier": "only", "params": [(A, 1)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length

	def Only_one(self, target, situations, length):
		Q = []
		possible_comb = self.quantifier.Union
		for A in possible_comb:
			# if P(V) is true for the target
			if self.quantifier.Only_one(A, target):
				# how many possible situations left
				left = []
				for distractor in situations:
					if self.quantifier.Only_one(A, distractor):
						left.append(distractor)
				if len(situations) - len(left) > 0:
					Q.append({"quantifier": "only-one", "params": [(A, 0)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length


	def Half(self, target, situations, length):
		Q = []
		self.quantifier.shuffle_value()
		possible_comb = self._combination(self.quantifier.O, self.quantifier.Union + self.quantifier.Shape + self.quantifier.Color) + \
						self._combination(self.quantifier.Shape, self.quantifier.Color) + \
						self._combination(self.quantifier.Color, self.quantifier.Shape)
		for A, B in possible_comb:
			# pluralty of the A:
			pluarl_a = 1 if A == "O" or self._is_plural(A, target) else 0
			# pluralty of the B:
			plural_b = 1 if self._is_plural(B, target) else 0
			# if P(V) is true for the target
			if self.quantifier.Half(A, B, target, pluarl_a, plural_b)[1]:
				# how many possible situations left
				left_reason, left = [], []
				for distractor in situations:
					is_left_reason, is_left = self.quantifier.Half(A, B, distractor, pluarl_a, plural_b)
					if is_left_reason:
						left_reason.append(distractor)
					if is_left:
						left.append(distractor)
				if len(situations) - len(left_reason) > 0:
					Q.append({"quantifier": "half", "params": [(A, pluarl_a), (B, plural_b)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length


	def Some(self, target, situations, length):
		Q = []
		self.quantifier.shuffle_value()
		possible_comb = self._combination(self.quantifier.O, self.quantifier.Union + self.quantifier.Shape + self.quantifier.Color) + \
						self._combination(self.quantifier.Shape, self.quantifier.Color) + \
						self._combination(self.quantifier.Color, self.quantifier.Shape)
		for A, B in possible_comb:
			plural = 0 if B in self.quantifier.Color else 1
			if self.quantifier.Some(A, B, target)[1]:
				# how many possible situations left
				left_reason, left = [], []
				for distractor in situations:
					is_left_reason, is_left = self.quantifier.Some(A, B, distractor)
					if is_left_reason:
						left_reason.append(distractor)
					if is_left:
						left.append(distractor)
				if len(situations) - len(left_reason) > 0:
					Q.append({"quantifier": "some", "params": [(A, 1), (B, plural)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length

	def Some_1(self, target, situations, length):
		Q = []
		possible_comb = self.quantifier.Union + self.quantifier.Shape + self.quantifier.Color
		for A in possible_comb:
			# if P(V) is true for the target
			if self.quantifier.Some_1(A, target):
				# how many possible situations left
				left = []
				for distractor in situations:
					if self.quantifier.Some_1(A, distractor):
						left.append(distractor)
				if len(situations) - len(left) > 0:
					Q.append({"quantifier": "some-1", "params": [(A, 1)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length


	def Half_Rest(self, target, situations, length):
		Q = []
		self.quantifier.shuffle_value()
		possible_comb = self._combination_3(self.quantifier.O, self.quantifier.Union) + \
						self._combination_3(self.quantifier.O, self.quantifier.Color) + \
						self._combination_3(self.quantifier.O, self.quantifier.Shape) + \
						self._combination_3(self.quantifier.Shape, self.quantifier.Color) + \
						self._combination_3(self.quantifier.Color, self.quantifier.Shape)
		for A, B, C in possible_comb:
			# pluralty of the A:
			pluarl_a = 1 if A == "O" or self._is_plural(A, target) else 0
			# pluralty of the B:
			plural_b = 1 if self._is_plural(B, target) else 0
			plural_c = 1 if self._is_plural(C, target) else 0
			# if P(V) is true for the target
			if self.quantifier.Half_Rest(A, B, C, target, pluarl_a, plural_b, plural_c)[1]:
				# how many possible situations left
				left_reason, left = [], []
				for distractor in situations:
					is_left_reason, is_left = self.quantifier.Half_Rest(A, B, C, distractor, pluarl_a, plural_b, plural_c)
					if is_left_reason:
						left_reason.append(distractor)
					if is_left:
						left.append(distractor)
				if len(situations) - len(left_reason) > 0:
					Q.append({"quantifier": "half-rest", "params": [(A, pluarl_a), (B, plural_b), (C, plural_c)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length

	def Most(self, target, situations, length):
		Q = []
		self.quantifier.shuffle_value()
		possible_comb = self._combination(self.quantifier.O, self.quantifier.Union + self.quantifier.Shape + self.quantifier.Color) + \
						self._combination(self.quantifier.Shape, self.quantifier.Color) + \
						self._combination(self.quantifier.Color, self.quantifier.Shape)
		for A, B in possible_comb:
			# pluralty of the A:
			pluarl_a = 1 if A == "O" or self._is_plural(A, target) else 0
			# pluralty of the B:
			plural_b = 1 if self._is_plural(B, target) else 0
			# if P(V) is true for the target
			if self.quantifier.Most(A, B, target, pluarl_a, plural_b)[1]:
				# how many possible situations left
				left_reason, left = [], []
				for distractor in situations:
					is_left_reason, is_left = self.quantifier.Most(A, B, distractor, pluarl_a)
					if is_left_reason:
						left_reason.append(distractor)
					if is_left:
						left.append(distractor)
				if len(situations) - len(left_reason) > 0:
					Q.append({"quantifier": "most", "params": [(A, pluarl_a), (B, plural_b)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length

	def Minority(self, target, situations, length):
		Q = []
		self.quantifier.shuffle_value()
		possible_comb = self._combination(self.quantifier.O, self.quantifier.Union + self.quantifier.Shape + self.quantifier.Color) + \
						self._combination(self.quantifier.Shape, self.quantifier.Color) + \
						self._combination(self.quantifier.Color, self.quantifier.Shape)
		for A, B in possible_comb:
			# pluralty of the A:
			pluarl_a = 1 if A == "O" or self._is_plural(A, target) else 0
			# pluralty of the B:
			plural_b = 1 if self._is_plural(B, target) else 0
			# if P(V) is true for the target
			if self.quantifier.Minority(A, B, target, pluarl_a, plural_b)[1]:
				# how many possible situations left
				left_reason, left = [], []
				for distractor in situations:
					is_left_reason, is_left = self.quantifier.Minority(A, B, distractor, pluarl_a)
					if is_left_reason:
						left_reason.append(distractor)
					if is_left:
						left.append(distractor)
				if len(situations) - len(left_reason) > 0:
					Q.append({"quantifier": "minority", "params": [(A, pluarl_a), (B, plural_b)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length

	def More(self, target, situations, length):
		Q = []
		self.quantifier.shuffle_value()
		possible_comb = self._self_combination(self.quantifier.Union) + \
						self._self_combination(self.quantifier.Shape) + \
						self._self_combination(self.quantifier.Color)
		for A, B in possible_comb:
			# if P(V) is true for the target
			if self.quantifier.More(A, B, target)[1]:
				# how many possible situations left
				left_reason, left = [], []
				for distractor in situations:
					is_left_reason, is_left = self.quantifier.More(A, B, distractor)
					if is_left_reason:
						left_reason.append(distractor)
					if is_left:
						left.append(distractor)
				if len(situations) - len(left_reason) > 0:
					Q.append({"quantifier": "more", "params": [(A, 1), (B, 1)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length

	def Fewer(self, target, situations, length):
		Q = []
		self.quantifier.shuffle_value()
		possible_comb = self._self_combination(self.quantifier.Union) + \
						self._self_combination(self.quantifier.Shape) + \
						self._self_combination(self.quantifier.Color)
		for A, B in possible_comb:
			# if P(V) is true for the target
			if self.quantifier.Fewer(A, B, target)[1]:
				# how many possible situations left
				left_reason, left = [], []
				for distractor in situations:
					is_left_reason, is_left = self.quantifier.Fewer(A, B, distractor)
					if is_left_reason:
						left_reason.append(distractor)
					if is_left:
						left.append(distractor)
				if len(situations) - len(left_reason) > 0:
					Q.append({"quantifier": "fewer", "params": [(A, 1), (B, 1)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length

	def Equal(self, target, situations, length):
		Q = []
		self.quantifier.shuffle_value()
		possible_comb = self._self_combination(self.quantifier.Union) + \
						self._self_combination(self.quantifier.Shape) + \
						self._self_combination(self.quantifier.Color)
		for A, B in possible_comb:
			# if P(V) is true for the target
			if self.quantifier.Equal(A, B, target)[1]:
				# how many possible situations left
				left_reason, left = [], []
				for distractor in situations:
					is_left_reason, is_left = self.quantifier.Equal(A, B, distractor)
					if is_left_reason:
						left_reason.append(distractor)
					if is_left:
						left.append(distractor)
				if len(situations) - len(left_reason) > 0:
					Q.append({"quantifier": "equal", "params": [(A, 1), (B, 1)]})
					length -= 1
					situations = left
			
			if len(situations) == 0 or length == 0:
				break
		return Q, situations, length

	def All_comb(self, target, situations, length):
		Q = []
		if self.quantifier.All_comb(target):
			left = []
			for distractor in situations:
				is_left = self.quantifier.All_comb(distractor)
				if is_left:
					left.append(distractor)
			if len(situations) - len(left) > 0:
				Q.append({"quantifier": "all_comb", "params": []})
				length -= 1
				situations = left
		return Q, situations, length		
		