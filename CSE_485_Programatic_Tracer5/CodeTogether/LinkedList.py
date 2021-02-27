# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Node:
    def __init__(self, frame_id, frame_vars):
        # frame id
        self.frame_id = frame_id
        # local vars
        self.frame_vars = frame_vars
        # enclosing 'parent' frame
        self.parent_frame = None
        # enclosed 'child' frame
        self.child_frame = None
        # next 'sibling' frame
        self.next_frame = None


class FrameList:
    def __init__(self):
        self.globals = None
        self.current_frame = None
        # list of frame ids
        self.frames = []

    def is_empty(self):
        if self.globals is None:
            return True

    # if event == call
    def insert_frame(self, frame_id, frame_vars):
        new_frame = Node(frame_id, frame_vars)
        self.frames.append(frame_id)
        if self.is_empty():
            self.globals = new_frame
            self.current_frame = new_frame
            return
        elif self.current_frame.child_frame is None:
            self.current_frame.child_frame = new_frame
        else:
            last_frame = self.current_frame.child_frame
            while last_frame.next_frame:
                last_frame = last_frame.next_frame
            last_frame.next_frame = new_frame
        new_frame.parent_frame = self.current_frame
        self.current_frame = new_frame
        return

    # if event == return
    def exit_frame(self):
        if self.is_empty():
            return
        elif self.current_frame == self.globals:
            self.current_frame = None
            return
        else:
            self.current_frame = self.current_frame.parent_frame

    # provide with frame id
    # returns
    def print_frame(self, frame_id):
        if frame_id not in self.frames:
            print('No Frame Called %s' % frame_id)
        else:
            if not self.is_empty():
                last_frame = self.globals
                while last_frame:
                    print(last_frame.frame_id)
                    if last_frame.frame_id == frame_id:
                        print('Current Frame: %s' % last_frame.frame_id)
                        print('Current Vars: ', last_frame.frame_vars)
                        if last_frame.parent_frame is not None:
                            print('Enclosing scope: %s' % last_frame.parent_frame.frame_id)
                        else:
                            print('Enclosing scope: None')
                        return
                    else:
                        if last_frame.child_frame is None:
                            last_frame = last_frame.parent_frame.next_frame
                        else:
                            last_frame = last_frame.child_frame

    def print_current_frame(self):
        if self.current_frame:
            print('Current Frame: %s' % self.current_frame.frame_id)
            print('Current Vars: ', self.current_frame.frame_vars)
            if self.current_frame.parent_frame is not None:
                print('Enclosing Frame: %s' % self.current_frame.parent_frame.frame_id)
            else:
                print('Enclosing Frame: None')
        else:
            print('Current Frame: None')

    def get_current_vars(self):
        if self.current_frame is not None:
            return self.current_frame.frame_vars
        else:
            print('Current Frame is Empty')
        return

    def mod_current_frame(self, var, val):
        if self.current_frame:
            if var in self.current_frame.frame_vars:
                self.current_frame.frame_vars[var] = val
            else:
                print('No Variable Called %s in Current Frame' % var)
        return

    def mod_outside_current_frame(self, var, val, frame_id):
        if frame_id not in self.frames:
            print('No Frame Called %s' % frame_id)
        else:
            if not self.is_empty():
                last_frame = self.globals
                while last_frame:
                    if last_frame.frame_id == frame_id:
                        if var in last_frame.frame_vars:
                            last_frame.frame_vars[var] = val
                            return
                        else:
                            print('No Variable Called %s in %s' % var, frame_id)
                            return
                    else:
                        if last_frame.child_frame is None:
                            last_frame = last_frame.parent_frame.next_frame
                        else:
                            last_frame = last_frame.child_frame

    def print_all_frames(self, level=0):
        frame = self.globals
        while frame:
            print('\t' * level + frame.frame_id + repr(frame.frame_vars))
            while frame.child_frame:
                level = level+1
                frame = frame.child_frame
                print('\t' * level + frame.frame_id + repr(frame.frame_vars))
            if frame.next_frame:
                frame = frame.next_frame
                continue
            level = level - 1
            frame = frame.parent_frame.next_frame


def main():

    # linked_list = FrameList()
    # linked_list.insert_frame('check', {'x': 2})
    # linked_list.insert_frame('check2', {'x': 2})
    # linked_list.insert_frame('check3', {'x': 2})
    # linked_list.exit_frame()
    # #linked_list.exit_frame()
    # linked_list.insert_frame('checkthing', {'t': 3})
    # linked_list.exit_frame()
    # #linked_list.exit_frame()
    # linked_list.print_all_frames()



    linked_list = FrameList()
    linked_list.insert_frame('module', {'x': 3})
    linked_list.insert_frame('check', {'x': 2})
    linked_list.print_current_frame()
    linked_list.insert_frame('for loop', {'x': 2})
    linked_list.print_current_frame()
    linked_list.insert_frame('secondfunction', {'s': 7})
    linked_list.exit_frame()
    linked_list.print_current_frame()
    #linked_list.exit_frame()
    linked_list.insert_frame('for loop', {'a': 3})
    linked_list.exit_frame()
    linked_list.exit_frame()
    linked_list.insert_frame('check', {'x': 4})
    linked_list.insert_frame('fun', {'x': 2})
    linked_list.print_current_frame()
    linked_list.insert_frame('thing',{'x':3})
    linked_list.print_current_frame()
    linked_list.insert_frame('checka',{'x':4})
    linked_list.print_current_frame()
    linked_list.exit_frame()
    linked_list.exit_frame()
    linked_list.exit_frame()
    linked_list.print_all_frames()



    # linked_list = FrameList()
    
    # linked_list.insert_frame('x', {'x': 1})
    # linked_list.print_current_frame()
    # print(linked_list.get_current_vars())
    # linked_list.insert_frame('y', {'y': 2})
    # linked_list.insert_frame('z', {'z': 3})
    # linked_list.insert_frame('a', {'a': 4})
    # linked_list.exit_frame()
    # linked_list.exit_frame()
    # linked_list.insert_frame('b', {'b': 5})
    # linked_list.print_current_frame()
    # linked_list.mod_current_frame('b', 100)
    # linked_list.print_current_frame()
    # linked_list.exit_frame()
    # linked_list.exit_frame()
    # linked_list.insert_frame('c', {'c': 6})
    # if 'c' in linked_list.current_frame.frame_vars:
    #     print('Found')
    #     print(linked_list.current_frame.frame_vars['c'])
    # linked_list.insert_frame('d', {'d': 7})
    # linked_list.exit_frame()
    # linked_list.exit_frame()
    # linked_list.print_current_frame()
    # linked_list.mod_current_frame('x', 100)
    # linked_list.print_current_frame()
    # linked_list.exit_frame()

    # linked_list.print_all_frames()
    # print('\n')
    # print(linked_list.frames)
    # print('\n')
    # linked_list.print_frame('d')
    # print('\n')
    # linked_list.mod_outside_current_frame('d', 25, 'd')
    # linked_list.print_all_frames()



    # structure of simulated program
    '''
    x{
        y{
            z{
                a{}
            }
            b{}
            c{
                d{}
            }
        }
    }
    '''

    #print(linked_list.frames)
    #print(linked_list.globals.next_frame)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
