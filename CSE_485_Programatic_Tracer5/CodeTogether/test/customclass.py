class Sprite:

    def __init__(self):
        self.x = 5
        self.y = 7
        self.width = 10
        self.height = 15

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_up(self):
        self.y += 1

    def move_down(self):
        self.y -= 1

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_width(self, new_width):
        self.width = new_width

    def set_height(self, new_height):
        self.height = new_height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


if __name__ == "__main__":
    testSprite = Sprite()
    testSprite.set_width(20)
    print(str(testSprite.get_width()))
