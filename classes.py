
class Vial:
    def __init__(self, number, color_list):
        self.number = number
        self.color_list = color_list
        self.completed = False

    def update_full_list(self, n_color_list):
        self.color_list = n_color_list
    
    def pour(self, give_vial):
        self.color_list.append(give_vial.color_list.pop())
        # check if current guy is now completed
        self.completed = len(set(self.color_list)) == 1 and len(self.color_list) == 4
    
