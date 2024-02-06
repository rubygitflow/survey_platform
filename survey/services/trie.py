from .db_query import DBQuery

class Trie:

    def take_from(self, questionnaire_id: int, question_id: int) -> list:
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