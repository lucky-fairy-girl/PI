"""
WordInsertion Class
-------------------------------
Word Insertion transformations act by inserting a new word at a specific word index.
For example, if we insert "new" in position 3 in the text "I like the movie", we get "I like the new movie".
Subclasses can implement the abstract ``WordInsertion`` class by overriding ``self._get_new_words``.
"""
from textattack.transformations import Transformation



new_words=[]
insert_word_path = '/root/miniconda3/envs/text/lib/python3.7/site-packages/textattack/transformations/word_insertions/word_final.txt' 
with open(insert_word_path,encoding='gbk') as f:
    lines = f.readlines()
for line in lines:
    insert_word = line.rstrip()
    new_words.append(insert_word)

new_words_tail=[]
insert_word_path = '/root/miniconda3/envs/text/lib/python3.7/site-packages/textattack/transformations/word_insertions/word_tail.txt' 
with open(insert_word_path,encoding='gbk') as f:
    lines = f.readlines()
for line in lines:
    insert_word = line.rstrip()
    new_words_tail.append(insert_word)



class WordInsertion(Transformation):
    """A base class for word insertions."""

    def _get_new_words(self, current_text, index):
        """Returns a set of new words we can insert at position `index` of `current_text`
        Args:
            current_text (AttackedText): Current text to modify.
            index (int): Position in which to insert a new word
        Returns:
            list[str]: List of new words to insert.
        """
        raise NotImplementedError()

    def _get_transformations(self, current_text, current_text_list,indices_to_modify):
        """
        Return a set of transformed texts obtained by insertion a new word in `indices_to_modify`
        Args:
            current_text (AttackedText): Current text to modify.
            indices_to_modify (list[int]): List of positions in which to insert a new word.

        Returns:
            list[AttackedText]: List of transformed texts
        """
        transformed_texts = []
        transformed_texts_list = []
        #print('current_text=========')
        #print(current_text)
        #print(current_text_list)

        for i in range(len(indices_to_modify)+1):
            new_transformted_texts = []
            new_transformted_texts_list = []
            if i==len(indices_to_modify):
                print('=====indices_to_modify====')
                print(new_words_tail)

                for w in new_words_tail:
                    neww=current_text_list[i-1]+','+' '+w
                    current_text_list1[i-1]=neww
                    current_text_list2[i-1]=neww
            else:
                print('=====else====')
                print(new_words)

                for w in new_words:

                    current_text_list1=current_text_list[:]
                    current_text_list2=current_text_list[:]

                    if i==0:
                        #print('current_text_list=======---00')
                        #print(current_text_list)

                        neww=w+' '+','+' '+current_text_list1[i]

                        current_text_list1[i]=neww
                        current_text_list2[i]=neww

                    else:

                        neww=','+' '+w+' '+','+' '+current_text_list[i]
                        neww=neww.replace(', ,',',')
                        current_text_list1[i]=neww
                        ne=w+' '+','+' '+current_text_list[i]
                        current_text_list2[i]=ne

                new_transformted_texts.append(
                    current_text.generate_new_attacked_text1(current_text_list,current_text_list1)
                )
                new_transformted_texts_list.append(
                    current_text_list2
                )
            transformed_texts.extend(new_transformted_texts)
            transformed_texts_list.extend(new_transformted_texts_list)
            #print('transformed_texts================')

            #print(transformed_texts)



        return transformed_texts,transformed_texts_list
