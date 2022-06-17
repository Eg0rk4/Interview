from collections import defaultdict

example_string = 'привет пока как дела машина привет хорошо пока солнце привет хорошо пока заяй привет'


def count_words_with_default_dict(string, n=1):
    words_dict = defaultdict(int)
    string = string.split(' ')
    for word in string:
        words_dict[word] += 1
    return words_dict


result = count_words_with_default_dict(example_string)
for key, value in result.items():
    print(f'{key}: {value}')
print(f'{"Second variant":-^45}')

def count_words(string, n=1):
    words_dict = {}
    string = string.split(' ')
    for word in string:
        if word in words_dict:
            words_dict[word] += 1
        elif word not in words_dict:
            words_dict[word] = 1
        else:
            raise ValueError

    return words_dict


res = count_words(example_string)
for key, value in res.items():
    print(f'{key}: {value}')
