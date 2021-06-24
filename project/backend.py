import itertools
import string


# class passwords_creator():
#     def __init__(self, *args, **kwargs):


def removedoubles(li):
    l = []
    for word in li:
        if word not in l:
            l.append(word)
    return l


def wordscycle(l, min_len=0, max_len=32):
    """make all possible 'words' combinations by a given list of words"""
    full_perm = []
    for i in range(1, len(l) + 1):
        for sublist in itertools.combinations_with_replacement(l, i):
            for tup in (list(itertools.permutations(sublist))):
                s = "".join(tup)
                if max_len > len(s) > min_len:
                    if s not in full_perm:
                        full_perm.append(s)
    return full_perm


def wordscycle_with_special_chars(words_list):
    """ adds special chars given words in permutation: lovehate --> [love.hate, love hate, love!hate, love/hate, love,hate]"""
    spe_ch = [" ", ".", "!", "/", ",", "_", "-", "*", "^"]
    l = []
    for i in range(len(words_list) - 2, len(words_list) + 1):
        if i > 1:
            for tup in itertools.permutations(words_list, i):
                # print (tup)
                for ch in spe_ch:
                    s = ""
                    for word in tup:
                        if word == tup[-1]:
                            s += word
                        else:
                            s += word + ch
                    l.append(s)
    return l


def charswap(word, ch, n_ch):
    """ swap *all* identical chars by new char in a given string: hello --> h3llo """
    w = ""
    for i in range(len(word)):
        if word[i] == ch:
            w += n_ch
        else:
            w += word[i]
    return w


def all_swaps_available_combo(words_list):
    """ retrun a list with all char swap available: hello --> [h3llo, he11o, hell0, h311o, h3ll0, he110, h3110] """
    pass


def all_swaps_available(words_list):
    """ retrun a list with all char swap available: hello --> [h3llo, he11o, he77o, hell0, hellO] """
    d = {
        # numbers
        "l": ["1", "7"], "one": "1",
        "z": "2", "Z": "2", "to": "2", "two": "2", "too": "2",
        "e": "3", "E": "3", "three": "3",
        "a": ["4", "@"], "A": ["4", "@"], "for": "4", "four": "4",
        "s": ["$", "5"], "S": ["$", "5"], "five": "5",
        "G": "6", "six": "6",
        "L": "7", "T": "7", "R": "7", "r": "7", "seven": "7",
        "B": "8", "eight": "8",
        "g": ["9", "6"], "q": "9", "nine": "9",
        "o": ["O", "0"], "O": ["o", "0"], "zero": ["O", "0"], "Q": ["o", "0"],
        # special chars
        "@": ["a", "A", "o", "0"],
        "$": ["s", "S"],
        "0": ["o", "O", "Q"],
        # just chars
        "i": ["!", "1", "I"], "I": ["!", "i", "1"]

    }
    l = []
    for word in words_list:
        for char_key in d.keys():
            if char_key in word:
                if len(d[char_key]) > 1:
                    for each_ch in d[char_key]:
                        l.append(charswap(word, char_key, each_ch))
                else:
                    l.append(charswap(word, char_key, d[char_key]))
    return l


def capital_letters_run(words, all_base_combinations_list):
    """ run all the sub capital letters functions"""
    print("____________caps all chars:____________")
    l1 = capital_letters_all(all_base_combinations_list)
    save_to_db(l1)

    print("____________caps first char only:____________")
    l2 = capital_letters_first_word(all_base_combinations_list)
    save_to_db(l2)

    print("____________caps first char of each word:____________")
    l3 = capital_letters_leading_ch(words)
    save_to_db(l3)


def capital_letters_all(words):
    """ return list of all words combinations in capsLK"""
    return [word.upper() for word in words]


def capital_letters_first_word(words):
    """ return list of all words combinations in capsLK only for the first word in the string"""
    return [word.capitalize() for word in words]


def capital_letters_leading_ch(words):
    """ return list of all words combinations in capsLK only for the first char of the first word"""
    l = []
    for word in words:
        l.append(''.join(word[0].upper() + word[1:]))
    return wordscycle(l)


def create_numbers_list(start_num, end_num):
    """ 0, 999 - ['000', '001', '002', '003', '004', '005', '006', ... '999'] """
    length = len(str(end_num))
    numbers = []
    for num in range(start_num, end_num + 1):
        numbers.append(str(num).zfill(length))
    return numbers


def create_chars_list():  # len 36k
    " creates a list with aaa - zzz \ AAA-ZZZ: [a,b,..., aa, ab,..., aaa,...,zzz, A,..., Z,..., ZZZ"
    l_lower = []
    l_upper = []
    for i in range(1, 4):
        for combo in itertools.product(string.ascii_lowercase, repeat=i):
            l_lower.append(''.join(combo))
        for combo in itertools.product(string.ascii_uppercase, repeat=i):
            l_upper.append(''.join(combo))
    return l_lower + l_upper


def known_patterns_list():
    l = ["123456", "1234567", "12345678", "123456789", "1234567890",
         "654321", "7654321", "87654321", "987654321", "0987654321",
         "`", "`1", "`12", "`123", "`1234", "`12345", "`123456", "`1234567", "`12345678", "`123456789", "`1234567890",
         "~!", "~!@", "~!@#", "~!@#$", "~!@#$%", "~!@#$%^", "~!@#$%^&", "~!@#$%^&*", "~!@#$%^&*(", "~!@#$%^&*()",
         "~!@#$%^&*()_", "~!@#$%^&*()_+",
         "!@", "!@#", "!@#$", "!@#$%", "!@#$^%", "!@#$%^&", "!@#$%^&*", "!@#$%^&*(", "!@#$%^&*()",
         "@#", "@#$%", "#$", "#$%", "#$%^", "$%", "$%^", "$%^&", "%^", "%^&", "^&", "^&*",
         "#@!", "$#@", "%$#", "^%$", "&^%", "*&^", "@!", "#@", "$#", "%$", "^%", "&^", "*&", ")(",
         "abcd", "abcde", "qwer", "wert", "qaws", "wsed", "edrf", "QAWS", "WSED", "EDRF", "QSWD", "QWER", "asdf",
         "ASDF", "zxcv", "ZXCV"
         ]
    l_base = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "()", "-", "_", "+", "="]
    for i in range(1, 4):
        for ch in l_base:
            l.append(ch * i)
    # print (len(l))
    # print(l)
    return l


def listrunneradder(word, obj_list, end=1, min_len=0, max_len=32):
    """ gets 2 lists - words_list and a objects list ([1,2,3,4,5] or [a,b,c,d,e] or [!,@,#,$,%]) and adds it to each word
        to the end of the word (end=1) and to the begining (end=0)"""
    l = []
    if end:
        for obj in obj_list:
            s = word + obj
            if max_len > len(s) > min_len:
                l.append(word + obj)
    else:
        for obj in obj_list:
            s = word + obj
            if max_len > len(s) > min_len:
                l.append(obj + word)
    return l


def add_chars(words_list, end=1):
    """add to each word/combo word at the begining and at the end: ~73.2k append to each XD"""
    l = create_chars_list()
    l += known_patterns_list()
    print (l)
    print (len(l))
    # add each word


def add_numbers(words_list, end=1, min_len=0, max_len=32):
    """ add to each word/combo word 1-4 ALL digits number - 11.1k (22.2k with end)"""
    l = []
    l_num09 = create_numbers_list(0, 9)
    l_num0099 = create_numbers_list(00, 99)
    l_num000999 = create_numbers_list(000, 999)
    l_num00009999 = create_numbers_list(0000, 9999)

    for word in words_list:
        l += listrunneradder(word, l_num09, end, min_len, max_len)  # add 0-9
        l += listrunneradder(word, l_num0099, end, min_len, max_len)  # add 00-99
        l += listrunneradder(word, l_num000999, end, min_len, max_len)  # add 000-999
        l += listrunneradder(word, l_num00009999, end, min_len, max_len)  # add 0000-9999
    return l


def add_numbers5059(words_list, end=1, min_len=0, max_len=32):
    """ because of computing power - seperated to a new process - 100k (200k with end)"""
    l = []
    l_num0000099999 = create_numbers_list(00000, 99999)
    # add 00000-99999
    for word in words_list:
        l += listrunneradder(word, l_num0000099999, end, min_len, max_len)
    return l


def save_to_db(words_list):
    """ add the supplied list to local memory"""
    # to check chunk sizes - each word at a time, 5 words, 20, 100, all
    # print to load_frame text
    print(words_list)
    print(len(words_list))


def save_to_file(db_handler, file_name):
    pass


def run_minimalist(base_words):
    all_base_combinations_list = wordscycle(base_words)
    print("____________all base combo:____________")  # 340
    print(all_base_combinations_list)
    print(len(all_base_combinations_list))

    print("____________special list -.- :____________")
    spec_ch_list = wordscycle_with_special_chars(base_words)
    print(spec_ch_list)
    print(len(spec_ch_list))

    capital_letters_run(base_words,all_base_combinations_list)

def run_small(base_words):
    pass

def run_big(base_words):
    pass

def run_huge(base_words):
    pass



def start(selected_words, selected_checkboxes, filesize_option, threads_num):
    base_words = removedoubles(selected_words)
    size = ""
    if filesize_option == 0:
        size = "minimalist"
        run_minimalist(base_words)
    elif filesize_option == 1:
        run_small(base_words)
        size = "small"
    elif filesize_option == 2:
        run_big(base_words)
        size = "big"
    else:
        run_huge(base_words)
        size = "huge"

    filename = ""
    l = []
    for word in base_words:
        l.append(''.join(word[0].upper() + word[1:]))
    for w in l:
        filename += w
    filename = filename + "_" + size +'.txt'
    print (filename)



    #add_chars(all_base_combinations_list, end=1)

    # print("____________all base combo + numbers:____________")
    # print(add_numbers(all_base_combinations_list))
    # print(len(add_numbers(all_base_combinations_list)))
    # print("____________all base combo + numbers reverse:____________")
    # print(add_numbers(all_base_combinations_list, end=0))
    # print(len(add_numbers(all_base_combinations_list)))
    # print(len(all_base_combinations_list))
    # print ("____________special list -.- :____________")                # 540
    # spec_ch_list = wordscycle_with_special_chars(base_words)
    # print(spec_ch_list)
    # print(len(spec_ch_list))
    #
    # capital_letters_run(base_words, all_base_combinations_list)      # 1000
    #
    # print("____________caps first char in special list -.- :____________ ") # 540
    # spec_ch_with_caps_list = capital_letters_first_word(spec_ch_list)
    # print (spec_ch_with_caps_list)
    # print(len(spec_ch_with_caps_list))
    #
    # print("____________char swap :____________ ")                           # 3100
    # swap_list = all_swaps_available(all_base_combinations_list)
    # print (swap_list)
    # print(len(swap_list))
    # swap_list_extend = all_swaps_available(spec_ch_list)    # 5500
    # print (swap_list_extend)
    # print(len(swap_list_extend))


start(["jon", "elk", "bon"], [], 0, 1)

# add year 1900 - 2100
# Capital letters – all words, first word only, first char of each
# Appending number of chars
# adding 1000 most used pass


# yo = passwords_creator("x", "y", "z")
# print(yo.all_swaps_available("loveass"))

# print (all_swaps_available("hello"))
# print(charswap("heello", "e", "3"))
