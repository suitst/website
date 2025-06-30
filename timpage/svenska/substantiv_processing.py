from svenska.models import Substantiv


def check_answers(dic, question, answer_dict):
    """Checks submitted answers against stored answers. \
        Returns """
    
    question_fields = ['På Engelska',
              'Obestämt Singular',
              'Bestämt Singular',
              'Obestämt Plural',
              'Bestämt Plural',
              ]
    
    attribute_fields = [question.engelska,
                        question.obestämt_singular,
                        question.bestämt_singular, 
                        question.obestämt_plural,
                        question.bestämt_plural,
                        ]

    
    for question_field, attribute_field in zip(question_fields, attribute_fields):
        if dic[question_field] == attribute_field:
            answer_dict[question_field] = 'Correct!'
        else:
            answer_dict[question_field] = f'Incorrect! {attribute_field}'
    


