class Tree:

    def __init__(self):
        pass

    def get_children(self, *class_pairs):
        for lists in class_pairs:
            print(lists)
            if len(lists) != 2:
                raise ValueError




tree = Tree()
# tree.get_children(['one', 'two', 'three'])
tree.get_children(['first', 'second'], ['third', 'fourth'], ['5th', '6th'])

