#!/usr/local/bin/python3

"""
realiser.py: The realiser of the quantified description generation model.
			 More details can be found in the paper: Chen et al., *Generating Quantified Descriptions of Abstract Visual Scenes*
"""

__author__ = "Guanyi Chen"
__email__ = "g.chen@uu.nl"

import random


class Realiser():

	def __init__(self):
		self.Color = ["R", "B"]
		self.r2s = {"O": "object", "C": "circle", "S": "square", "R": "red", "B": "blue", "BS": "blue square", "BC": "blue circle", "RS": "red square", "RC": "red circle"}
		self.q_surface = {
			"all": ["All of the", "Every"],
			"everything": ["Everything"],
			"half": ["Half of the"],
			"half-rest": ["the other half", "the rest"],
			"most": ["Most of the", "A majority of the", "More than half of the"],
			"minority": ["A minority of the", "Less then half of the"],
			"equal": ["equally many"],
			"more": ["more"],
			"fewer": ["fewer"],
			"some": ["Some"]
		}

	def _color(self, cell, is_later_place):
		head, is_plural = cell
		if is_later_place:
			return self.r2s[head]
		elif is_plural:
			return self.r2s[head] + " " + "objects"
		else:
			return "a " + self.r2s[head] + " " + "object"

	def _s_o_u(self, cell):
		head, is_plural = cell
		if is_plural:
			return self.r2s[head] + "s"
		else:
			return "a " + self.r2s[head]

	def _quantifier(self, normalised_quantifier):
		candidates = self.q_surface[normalised_quantifier]
		return random.choice(candidates)

	def _realise_cell(self, cell, is_later_place=False):
		if cell[0] in self.Color:
			cell = self._color(cell, is_later_place)
		else:
			cell = self._s_o_u(cell)
		return cell

	def _realise_qe(self, qe):
		if qe["quantifier"] == "all_comb":
			realised_qe = "All possible objects are shown."
		elif qe["quantifier"] in ["all", "most", "some"]:
			Q = self._quantifier(qe["quantifier"])
			A, B = qe["params"]
			plural = A[1]
			if plural == 1:
				realised_qe = "{0} {1} are {2}.".format(Q, self._realise_cell(A), self._realise_cell(B, is_later_place=True))
				if "Every" in realised_qe and "are" in realised_qe:
					realised_qe = realised_qe.replace(" are ", " is ").replace("s.", ".").replace("squares", "square").replace("circles", "circle").replace("objects", "object")
			else:
				print("Something wrong happens in", qe)
		elif qe["quantifier"] in ["half", "minority"]:
			Q = self._quantifier(qe["quantifier"])
			A, B = qe["params"]
			plural = B[1]
			if plural == 1:
				realised_qe = "{0} {1} are {2}.".format(Q, self._realise_cell(A), self._realise_cell(B, is_later_place=True))
			else:
				realised_qe = "{0} {1} is {2}.".format(Q, self._realise_cell(A), self._realise_cell(B, is_later_place=True))
		elif qe["quantifier"] in ["half-rest"]:
			Q = self._quantifier(qe["quantifier"])
			A, B, C = qe["params"]
			plural = B[1]
			if plural == 1:
				realised_qe = "Half of the {0} are {1}, {2} are {3}.".format(self._realise_cell(A), self._realise_cell(B, is_later_place=True), Q, self._realise_cell(C, is_later_place=True))
			else:
				realised_qe = "Half of the {0} is {1}, {2} is {3}.".format(self._realise_cell(A), self._realise_cell(B, is_later_place=True), Q, self._realise_cell(C, is_later_place=True))
		elif qe["quantifier"] == "everything":
			Q = self._quantifier(qe["quantifier"])
			A = qe["params"][0]
			realised_qe = "{0} is {1}.".format(Q, self._realise_cell(A, is_later_place=True)).replace("s.", ".")
		elif qe["quantifier"] == "only":
			A = qe["params"][0]
			realised_qe = "There are only {0}.".format(self._realise_cell(A))
		elif qe["quantifier"] == "equal":
			Q = self._quantifier(qe["quantifier"])
			A, B = qe["params"]
			realised_qe = "There are {0} {1} and {2}.".format(Q, self._realise_cell(A), self._realise_cell(B))
		elif qe["quantifier"] in ["more", "fewer"]:
			Q = self._quantifier(qe["quantifier"])
			A, B = qe["params"]
			realised_qe = "There are {0} {1} than {2}.".format(Q, self._realise_cell(A), self._realise_cell(B))
		elif qe["quantifier"] == "some-1":
			A = qe["params"][0]
			realised_qe = "There are some {0}.".format(self._realise_cell(A))
		elif qe["quantifier"] == "only-one":
			A = qe["params"][0]
			plural = qe["params"][0][1]
			if plural == 0:
				realised_qe = "There is only {0}.".format(self._realise_cell(A))
				realised_qe = realised_qe.replace(" a ", " one ")
			else:
				print("Some thing wrong happens in", qe)

		return realised_qe

	def realise(self, description):
		realised_description = []
		for qe in description:
			realised_qe = self._realise_qe(qe)
			realised_description.append(realised_qe)
		return " ".join(realised_description)