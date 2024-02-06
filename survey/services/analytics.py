from .db_query import DBQuery
from .trie import Trie

class Analytics:
    filter = None
    questionnaire = None

    def __init__(self, questionnaire_id: int):     
        self.questionnaire = questionnaire_id


    def count_of_vouted_users(self) -> int:
        sql = """
            select COUNT(DISTINCT user_id) from polls where questionnaire_id = %s;
            """
        t = DBQuery(sql=sql.strip(), attributes=[self.questionnaire]).easy_execute()
        if len(t) == 0: 
            return 0

        return t[0][0]

    def rating_of_questions(self, question_id: int) -> list:
        sql = """
            with question_list as (
              select
                question_id,
                q.body as q_body,
                count(*) as users_count,
                round(count(*) * 100 / survey_users.total) as users_pct
              from polls
              cross join (
                select count(distinct user_id) as total 
                  from polls 
                  where questionnaire_id = %s
                ) as survey_users
              join ( select id, body from questions) as q on q.id = polls.question_id
              where questionnaire_id = %s
              group by question_id, survey_users.total, q.body
              order by question_id desc
            ),
            user_counter as (
              select distinct users_count
              from question_list
              order by users_count desc
            ),
            user_numbered as (
              select 
                row_number() over(),
                users_count
              from user_counter
            )
            select 
              question_list.*,
              user_numbered.row_number as rating
            from question_list
            join user_numbered on user_numbered.users_count = question_list.users_count;
            """
        l = DBQuery(sql=sql.strip(), attributes=[self.questionnaire, self.questionnaire]).execute()
        if len(l) == 0: 
            return []

        return self._select_by_filter(from_query=l, question_id=question_id)


    def rating_of_answers(self, question_id: int) -> list:
        sql = """
            with answer_list as (
              select
                a.id as a_id,
                a.body as a_body,
                question_id,
                count(*) as users_count,
                round(count(*) * 100 / survey_users.total) as users_pct
              from polls
              cross join (
                select count(distinct user_id) as total 
                  from polls 
                  where questionnaire_id = %s
                ) as survey_users
              join ( select id, body from answers) as a on a.id = polls.answer_id
              where questionnaire_id = %s
              group by question_id, survey_users.total, a.id, a.body
              order by a.id desc
            ),
            user_counter as (
              select distinct users_count
              from answer_list
              order by users_count desc
            ),
            user_numbered as (
              select 
                row_number() over(),
                users_count
              from user_counter
            )
            select 
              answer_list.*,
              user_numbered.row_number as rating
            from answer_list
            join user_numbered on user_numbered.users_count = answer_list.users_count;
            """
        l = DBQuery(sql=sql.strip(), attributes=[self.questionnaire, self.questionnaire]).execute()
        if len(l) == 0: 
            return []

        return self._select_by_filter(from_query=l, question_id=question_id)

    def _select_by_filter(self, from_query: list, question_id: int) -> list:
        if self.filter is None:
            self.filter = Trie().take_from(questionnaire_id=self.questionnaire, question_id=question_id) 

        return [x for x in from_query if x['question_id'] in self.filter ]




