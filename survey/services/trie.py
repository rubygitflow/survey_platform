""" User behavior in the survey tree """
# pylint: disable=missing-class-docstring

from .db_query import DBQuery
from survey.models import Poll

class Trie:
    def take_from(self, questionnaire_id: int, question_id: int) -> list:
        """ Get nodes from user path in survey tree """
        sql = """
            select a.next_question_id as key, ARRAY[ a.question_id, a.next_question_id] as value
            from answers  a
            join questions q on q.id = a.question_id
            join questions next_q on next_q.id = a.next_question_id
            where q.questionnaire_id = %s and next_q.conclusion = false
            order by a.next_question_id ;
            """
        h = DBQuery(sql=sql.strip(), attributes=[questionnaire_id]).key_value()
        if question_id not in h.keys(): 
            return []

        k = question_id
        children = [k]
        while k in h.keys():
            k = h[k][0]
            children.append(k)
        return children

    def is_honesty(
            self,
            user_id: int,
            questionnaire_id: int,
            question_id: int,
            for_answer_id: int) -> bool:
        """ is there another answer to question_id or not - No"""
        answers = Poll.objects.filter(
            user_id=user_id,
            questionnaire_id=questionnaire_id,
            question_id=question_id
        ).values_list('answer_id', flat=True)

        if len(answers) == 0:
            return True

        if len(answers) > 1:
            return False

        if answers[0] == for_answer_id:
            return True

        return False

    def is_cheating(
            self,
            user_id: int,
            questionnaire_id: int,
            question_id: int,
            for_answer_id: int) -> bool:
        """ is there another answer to question_id or not - Yes"""
        return not self.is_honesty(
            user_id=user_id,
            questionnaire_id=questionnaire_id,
            question_id=question_id,
            for_answer_id=for_answer_id
        )
