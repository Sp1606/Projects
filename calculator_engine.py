import re
import math

def clean_input(expression):
    expression = expression.lower()
    expression = expression.replace('x', '*')
    expression = expression.replace('^', '**')
    expression = expression.replace('sqrt', 'math.sqrt')
    return expression

def calculate(expression):
    try:
        expression = clean_input(expression)
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {e}"