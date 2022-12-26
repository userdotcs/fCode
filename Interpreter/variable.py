class Variable:
    def __init__(self, name, token):
        self.token = token
        self.name = name


class VariableList:
    def __init__(self, variables: list[Variable]):
        self.variable_list: list[Variable] = variables

    def add_variable(self, name, token):
        self.variable_list.append(Variable(name, token))

    def change_variable_value(self, name, token):
        ind = 0
        for var in self.variable_list:
            if var.name == name:
                self.variable_list[ind].token = token

            ind += 1

    def get_variable(self, name):
        ind = 0
        for var in self.variable_list:
            if var.name == name:
                return var.token
            ind += 1
        return None
