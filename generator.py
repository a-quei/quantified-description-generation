#!/usr/local/bin/python3

"""
realiser.py: The main generator of the quantified description generation model.
			 More details can be found in the paper: Chen et al., *Generating Quantified Descriptions of Abstract Visual Scenes*
"""

__author__ = "Guanyi Chen"
__email__ = "g.chen@uu.nl"

from reasoner import Reasoner
from greedy_reasoner import GreedyReasoner
import random
from realiser import Realiser

class Generator():

	def _possible_situation(self, domain_size, target):
		situations = []
		for bs in range(domain_size + 1):
			for bc in range(domain_size - bs + 1):
				for rs in range (domain_size - bs - bc + 1):
					rc = domain_size - bs - bc - rs
					if [bs, bc, rs, rc] == target:
						continue
					situations.append([bs, bc, rs, rc, bs+bc, rs+rc, bs+rs, bc+rc])
					# bs, bc, rs, rc, b, r, s, c
		return situations

	def _all_possible_situation(self, domain_size):
		situations = []
		for bs in range(domain_size + 1):
			for bc in range(domain_size - bs + 1):
				for rs in range (domain_size - bs - bc + 1):
					rc = domain_size - bs - bc - rs
					situations.append([bs, bc, rs, rc, bs+bc, rs+rc, bs+rs, bc+rc])
					# bs, bc, rs, rc, b, r, s, c
		return situations

	def _preprocess(self, situation):
		N = 0
		for comb in situation:
			N += situation[comb]
		bs, bc, rs, rc = situation["BS"], situation["BC"], situation["RS"], situation["RC"]
		target = [bs, bc, rs, rc, bs+bc, rs+rc, bs+rs, bc+rc]
		return N, target, self._possible_situation(N, [bs, bc, rs, rc])


	def _get_po(self):
		PPO = [[[self.reasoner.All_comb]], [[self.reasoner.All, self.reasoner.Everything, self.reasoner.Only]], [[self.reasoner.Half, self.reasoner.Half_Rest], [self.reasoner.Equal]], \
				[[self.reasoner.Most, self.reasoner.Minority], [self.reasoner.More, self.reasoner.Fewer]], \
				[[self.reasoner.Some, self.reasoner.Some_1]], [[self.reasoner.Only_one]]]
		threshold_1, threshold_2 = 0.5, 0.8
		PO = []
		for qq_list in PPO:
			if len(qq_list) > 1:
				if random.random() > threshold_1:
					qq_list = [qq_list[1], qq_list[0]]
			for q_list in qq_list:
				if len(q_list) > 1 and random.random() > threshold_2 - 0.1 * len(q_list):
					PO.append(random.choice(q_list[1:]))
				PO.append(q_list[0])
		return PO


	def _get_input(self, scene):
		self.N, self.target, self.possible_situation = self._preprocess(scene)
		self.length = 5
		self.reasoner = Reasoner(self.N)
		self.PO = self._get_po()
	
	def ia_generate(self, scene):
		self._get_input(scene)
		Q = []
		for quantifier in self.PO:
			new_Q, self.possible_situation, self.length = quantifier(self.target, self.possible_situation, self.length)
			Q += new_Q
			if len(self.possible_situation) == 0 or self.length == 0:
				break
		return Q, len(self.possible_situation) == 0

	def _get_greedy_input(self, scene):
		self.N, self.target, self.possible_situation = self._preprocess(scene)
		self.length = 5
		self.reasoner = GreedyReasoner(self.N)

	def greedy_generate(self, scene):
		self._get_greedy_input(scene)
		Q = []
		q_list = [self.reasoner.All_comb, self.reasoner.All, self.reasoner.Everything, self.reasoner.Only, self.reasoner.Half, self.reasoner.Half_Rest, self.reasoner.Equal, \
				self.reasoner.Most, self.reasoner.Minority, self.reasoner.More, self.reasoner.Fewer, \
				self.reasoner.Some, self.reasoner.Some_1, self.reasoner.Only_one]
		
		while(self.length):
			max_case, max_single_out_size = [], 0
			for quantifier in q_list:
				new_Q, new_situation, new_single_out_size = quantifier(self.target, self.possible_situation)
				if new_single_out_size > max_single_out_size:
					max_single_out_size = new_single_out_size
					max_case = [(new_Q, new_situation)]
				elif new_single_out_size == max_single_out_size != 0:
					max_case.append((new_Q, new_situation))
			if max_single_out_size == 0:
				break
			selected_Q, selected_situation = random.choice(max_case)
			Q.append(selected_Q)
			self.possible_situation = selected_situation
			if len(self.possible_situation) == 0:
				break
		return Q, len(self.possible_situation) == 0

	def test_completeness(max_n):
		for N in range(2, max_n + 1):
			S = self._all_possible_situation(N)
			for s in S:
				D = S - s


		

if __name__ == '__main__':
	s = {"BS": 0, "BC": 1, "RS": 0, "RC":3}
	generator = Generator()
	realiser = Realiser()
	Q, is_complete = generator.ia_generate(s)
	print("IA: (" + str(is_complete) + ")", realiser.realise(Q))
	Q, is_complete = generator.greedy_generate(s)
	print("Greedy: (" + str(is_complete) + ")", realiser.realise(Q))