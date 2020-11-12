import random

characters = {"clear": {"clear": "empty"},
              "wizard":
                  {"happy": ":-)",
                   "neutral": ":-|",
                   "sad": ":-(",
                   "angry": ">:-("},
              "shopkeeper":
                  {"neutral": ":-|"},
              }

backgrounds = {"city": "^^^^^",
               "castle": "|_|_|_|",
               "static": "######",
               "ocean": "~~~~~~~"}


def dict_to_list(dict):
    dict_list = []
    for i, v in dict.items():
        dict_list.append(v)

    return dict_list


def shuffle_list(li):
    random.shuffle(li)


if __name__ == "__main__":

    # print loop to confirm contents of nested dictionary, can also be used to test traces of i, j, and v
    for i in characters.keys():
        print(i)
        for j, v in characters[i].items():
            print("{} : {}".format(j, v))
