class Node:

    def __init__(self, data=None):
        self.data = data
        self.next = None

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_next(self, new_next):
        self.next = new_next


class SinglyLinkedList:

    def __init__(self):
        self.head = None

    # only inserts at head
    def insert(self, data):
        newNode = Node(data)
        newNode.set_next(self.head)
        self.head = newNode

    def get_size(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.get_next()
        return count

    def search(self, goal):
        goalFound = False

        current = self.head
        while current and not goalFound:
            if current.data != goal:
                current = current.get_next()
            else:
                goalFound = True

        return goalFound

    def print_list(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next


if __name__ == "__main__":
    listA = SinglyLinkedList()
    listA.insert("Wednesday")
    listA.insert(5)
    listA.insert("7")

    if listA.search("Wednesday"):
        print("List contains Wednesday")
    listA.print_list()
