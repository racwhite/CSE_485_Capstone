
import ast
import os


def scan(path):
    result = []
    for root, dirs, files in os.walk(path, topdown=False):
        for file_name in files:
            rest = ''
            if file_name.endswith(".py"):
                file_name = str(root + '/' or root + '\\') + file_name
                file = open(file_name, 'r')
                for line in file.readlines():
                    rest += line
                expression = ast.parse(rest, filename=file_name, mode='exec')

                result += [ast.dump(expression)]
    return result


if __name__ == '__main__':

    # Please change this path to your local folder for now.
    path = os.getcwd() + "/target_code"
    print(path)
    #path = input("Please input path ")
    rest = scan(path)

    for i in rest:
        print(i)
