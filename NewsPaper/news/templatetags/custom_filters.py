from django import template



register = template.Library()
list_=['хуй','музыка', 'чмо', 'долбаеб','котики','гитара','кошки','свет','история','события','автомобили']


@register.filter()
def censor(value , a =list_):
    if isinstance(value,str):
        words_list = value.split()

        for i, x in enumerate(words_list):
            y = x[0]
            x = x.lower()
            if x in list_:
                for j in range(len(x)-1):
                    y = y + '*'
                words_list[i] = y
        return ' '.join(words_list)
    else:
        raise TypeError('этот фильтр применим только к строке')



