from language_evaluator.models import Test, Question


def calculate_result(test):
    result = 0
    divider = 0
    for q in test.questions_state_list():
        q_id = q[:-1]
        q_item = Question.objects.get(pk=q_id)
        status = q[-1:]
        if status == 'T':
            status = 1 * (q_item.competence_level + 1)
        else:
            status = 0
        result += status
        divider += (q_item.competence_level + 1)
    return round(result/divider, 2) * 100
