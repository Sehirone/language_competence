

def grade_text(answer_text, answer_set):
    answer_text = answer_text.lower()
    answer_text = answer_text.replace('.', '')
    answer_text = answer_text.replace(',', '')
    answer_text_split = answer_text.split(' ')
    hit_count = 0
    miss_count = 0
    for q_answer in answer_set:
        hit_count = 0
        miss_count = 0
        q_answer = q_answer.answer_text.lower()
        q_answer_split = q_answer.split(' ')
        counter = 0
        for word in q_answer_split:
            word = word.replace('.', '')
            word = word.replace(',', '')
            if len(answer_text_split) <= counter:
                miss_count += 1
            elif answer_text_split[counter] == word:
                hit_count += 1
            elif word == '<tag>':
                hit_count += 1
            else:
                miss_count += 1
            counter += 1
        if hit_count > miss_count:
            return True
        else:
            return False
