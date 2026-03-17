"""
Beam Search
===============

"""
import numpy as np

from textattack.goal_function_results import GoalFunctionResultStatus
from textattack.search_methods import SearchMethod
from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree
import re
import string


class BeamSearch(SearchMethod):
    """An attack that maintains a beam of the `beam_width` highest scoring
    AttackedTexts, greedily updating the beam with the highest scoring
    transformations from the current beam.

    Args:
        goal_function: A function for determining how well a perturbation is doing at achieving the attack's goal.
        transformation: The type of transformation.
        beam_width (int): the number of candidates to retain at each step
    """

    def __init__(self, beam_width=2):
        self.beam_width = beam_width
        


    def function(self,line,con_list,a):

        length=len(con_list)
        list1=[]
            
        list1[:]=line[:]
        string_list=' '.join(con_list)
        for j in con_list:
            if j==',':
                return line
        for j in range(len(line)):
            if string_list in line[j]:
                return line    
        notion=0
        
        for i in range(len(line)-length+1):
            
            note=1
            for j in range(length):
                if line[i+j]!=con_list[j]:
                    note=0
            if note==1:
                notion=1
                if con_list==['it','s']:
                    if 'it \'s' in a:
                        list1[i]=' '.join(['it' ,'\'s'])
                    if 'it\'s' in a:
                        list1[i]=''.join(['it' ,'\'s'])

                else:
                    list1[i]=' '.join(con_list)
                list1[i+1:i-length+1]=line[i+length:]
                break
        if notion==1:
            return list1[:len(line)-length+1]
        else:
            return line
    def conlist(self,a,line):

        nlp = StanfordCoreNLP('/root/stanford-corenlp-4.5.1')
        annotations=nlp.parse(a)

        ptree = ParentedTree.fromstring(annotations)
        phrase_level = [
                    'ASJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX',
                    'PP', 'PRN', 'PRT', 'QP', 'RRC',
                    'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP', 'WHPP', 'X', 'S', 'SBAR'
                ]
        
        line=self.function(line,['it', 's'],a)
        for node in ptree.subtrees(filter=lambda t: t.label() in phrase_level):
            if node.label() == 'NP':
                con_list=[]
                if (node.right_sibling() != None and node.right_sibling().label() == 'VP') or (len(node.leaves())==2):
                    con_list=node.leaves()
                    if len(con_list)>1:
                        line=self.function(line,con_list,a)
                
            if node.label() == 'PP':
                con_list=node.leaves()
                if len(con_list)>1:
                        line=self.function(line,con_list,a)
        return line


    def perform_search(self, initial_result):
        beam = [initial_result.attacked_text]

        best_result = initial_result
        if '[math]' in beam[0].text:
            return best_result,0

        beam_list=[beam[0].words[:]]

        print(beam[0])

        print(beam[0].text)
        print('beam_list0')
        print(beam_list)

        beam_list=[self.conlist(beam[0].text,beam_list[0])]
        print('beam_list2')
        print(beam_list)
        iii=0
        t=2#2*(len(beam_list[0]))


        while not best_result.goal_status == GoalFunctionResultStatus.SUCCEEDED and iii<t:
            print('yikaishi===========')

            iii+=1
            #print(beam_list)

            potential_next_beam = []
            potential_next_beam_list = []
            for i,(text,text_list) in enumerate(zip(beam,beam_list)):
                transformations,lists = self.get_transformations(
                    text, text_list,original_text=initial_result.attacked_text
                )
                potential_next_beam += transformations
                potential_next_beam_list += lists
            #print('beam_search================transformations==list')
            #print(transformations)
            #print(lists)

            if len(potential_next_beam) == 0:
                # If we did not find any possible perturbations, give up.
                return best_result,iii
            results, search_over = self.get_goal_results(potential_next_beam)
            scores = np.array([r.score for r in results])
            best_result = results[scores.argmax()]
            if search_over:
                return best_result,iii

            # Refill the beam. This works by sorting the scores
            # in descending order and filling the beam from there.
            best_indices = (-scores).argsort()[: self.beam_width]
            beam = [potential_next_beam[i] for i in best_indices]
            beam_list = [potential_next_beam_list[i].tolist() for i in best_indices]
        return best_result,iii

    @property
    def is_black_box(self):
        return True

    def extra_repr_keys(self):
        return ["beam_width"]
