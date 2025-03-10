from .models import Income,FixedExpense,VariableExpense 



def total_fixed_expenses():
        sum = 0
        for obj in FixedExpense:
                sum += obj.amount
        return sum
    
def current_total_variable_expenses():
        sum = 0
        for obj in VariableExpense:
                sum += obj.amount_left
        return sum


def total_income():
        sum = 0
        for obj in Income:
                sum += obj.amount
        return sum

print(total_income)