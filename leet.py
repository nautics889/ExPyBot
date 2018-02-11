word_list = {'а': '@', 'б': '6', 'в': '|3', 'г': 'r', 'д': 'D', 'е': '€', 'ё': '€', 'ж': '}|{', 'з': '3', 'и': 'u', 'й': 'ú', 'к': '|{', 'л': 'J|', 'м': '|\/|', 'н': '|-|', 'о': '0', 'п': '/7', 'р': 'ρ', 'с': 'ς', 'т': '₸', 'у': 'Y', 'ф': 'o|o', 'х': '}{', 'ц': 'u.', 'ч': '4', 'ш': 'III', 'щ': 'III.', 'ъ': '*b', 'ы': 'bI', 'ь': 'b', 'э': 'ǝ', 'ю': '|-0', 'я': '9|', ' ': '   '}

def transformToLeet(input_string):
    input_string.lower()
    output_list = []

    for i in range(len(input_string)):
        try:
            output_list.append(word_list[input_string[i]])
        except:
            output_list.append(input_string[i])

    output_string = ''.join(output_list)
    return output_string
