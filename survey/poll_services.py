""" Survey Process Steps"""

from .services.analytics import Analytics
from .services.trie import Trie
from .models import Question, Answer, Poll

def completing_survey_process(user_id: int,
                              last_question: int,
                              last_answer: int,
                              polid: int,
                              queid: int) -> [bool, dict]:
    """ Service for issuing a card 
    with the results of passing the previous question:
    the next card or summary report on completed questions """

    # to verify honesty
    if Trie().is_cheating(user_id=user_id,
                          questionnaire_id=polid,
                          question_id=last_question,
                          for_answer_id=last_answer):
        return [False, {}]

    # data on the current page
    question = Question.objects.get(id=queid)
    answers = Answer.objects.filter(question_id=queid)

    voted = _verify_answers_to_the_question(
        user_id, polid, queid, answer_ids=answers.values_list('id', flat=True))

    _add_record_to_poll(user_id, last_question, last_answer, polid)

    # analytics_by_questions, analytics_by_answers
    # to generate an analytical report
    analytics_by_questions = []
    analytics_by_answers = []
    total_count_of_users = 0
    if question.conclusion:
        if last_question and last_question > 0:
            analytic = Analytics(questionnaire_id=polid)
            analytics_by_questions = analytic.rating_of_questions(
                question_id=last_question)
            analytics_by_answers = analytic.rating_of_answers(
                question_id=last_question)
            total_count_of_users = analytic.count_of_vouted_users()

    return [True, {
                    "is_final": question.conclusion,
                    "question": question,
                    "questionnaire": question.questionnaire,
                    "answers": answers,
                    "analytics_by_questions": analytics_by_questions,
                    "analytics_by_answers": analytics_by_answers,
                    "count_of_vouted_users": total_count_of_users,
                    "voted": voted,
                  }]

def _add_record_to_poll(user_id: int,
                        last_question: int,
                        last_answer: int,
                        polid: int) -> None:
    """ Add an answer to the survey results """
    if last_question and last_question > 0:
        Poll.objects.get_or_create(
            user_id=user_id,
            questionnaire_id=polid,
            question_id=last_question,
            answer_id=last_answer
        )

def _verify_answers_to_the_question(user_id: int,
                                    polid: int,
                                    queid: int,
                                    answer_ids: list
                                    ) -> bool:
    """ Verify the status Voted – to block answers on the curent page """
    return bool(
        Poll.objects.filter(user_id=user_id,
                            questionnaire_id=polid,
                            question_id=queid,
                            answer_id__in=answer_ids)
    )
