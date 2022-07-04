import openpyxl


class Tree:

    def __init__(self):
        self.excel_values = {}

    def get_data_from_excel(self, book_name='some_excel.xlsx'):
        book = openpyxl.open(book_name, read_only=True)
        sheet = book.active
        for column in range(0, sheet.max_column):
            data = []
            for row in range(2, sheet.max_row):
                data.append(sheet[row][column].value)
            self.excel_values[sheet[1][column].value] = data

    def get_children(self, *class_pairs):
        for lists in class_pairs:
            if len(lists) != 2:
                raise ValueError(f'Expected pair of classes, got {len(lists)} instead')
            else:
                print(lists)

    def grow_tree(self, *classificators):
        print(f'{"Root": ^55}')
        for clss in classificators:
            if clss in self.excel_values.keys():
                print('{}  {}  {}'.format(*self.excel_values[clss]).center(55))
            else:
                raise ValueError(f'No such classificator "{clss}" in excel file!')
        print('{}  {}  {}'.format(*self.excel_values['объект']).center(55))

        print(f'{"":~^55}')


if __name__ == '__main__':

    tree = Tree()
    # tree.get_children(['one', 'two', 'three', 'four'])  # Вызывает ошибку
    tree.get_children(['first', 'second'], ['third', 'fourth'], ['5th', '6th'])
    tree.get_data_from_excel()
    print(tree.excel_values)
    tree.grow_tree('классификатор1', 'классификатор2')
    tree.grow_tree('классификатор2', 'классификатор1')
    tree.grow_tree('классификатор1')

