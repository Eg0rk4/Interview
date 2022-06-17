from collections import defaultdict

example_string = 'привет пока как дела машина привет хорошо пока солнце привет хорошо пока заяц привет yes yes yes'


print(f'{"Optimized variant":-^45}')


def count_words_with_default_dict(string, n=1):
    words_dict = defaultdict(int)
    string = string.split(' ')
    for word in string:
        words_dict[word] += 1

    words_dict = {k: v for k, v in sorted(words_dict.items(), key=lambda item: item[1])}
    for _ in range(n):
        key, value = words_dict.popitem()
        print(f'{key}: {value}')


count_words_with_default_dict(example_string, n=3)
print(f'{"Simple variant":-^45}')


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

    for _ in range(n):
        maximum = 0
        max_key = None
        for key, value in words_dict.items():
            if value >= maximum:
                maximum = value
                max_key = key

        print(f'{max_key}: {words_dict.pop(max_key)}')


count_words(example_string, n=3)
