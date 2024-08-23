import fire

class Calculator:
    def add(self, x, y):
        return x + y

    def multiply(self, x, y):
        return x * y

    def power(self, x, y):
        return x ** y

def greet(name="World"):
    return f"Hello {name}!"

def temperature_converter():
    class TempConverter:
        def celsius_to_fahrenheit(self, celsius):
            return (celsius * 9/5) + 32

        def fahrenheit_to_celsius(self, fahrenheit):
            return (fahrenheit - 32) * 5/9

    return TempConverter()

if __name__ == '__main__':
    fire.Fire({
        'calc': Calculator,
        'greet': greet,
        'temp': temperature_converter
    })