from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import sympy as sp
import numpy as np
from scipy import signal
from sympy import symbols, laplace_transform, inverse_laplace_transform
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application)
from scipy.optimize import minimize_scalar

from lmfit import minimize, Parameters

import scipy.optimize as opt




def index(request):
    return render(request, 'index.html')

def derivadas_parciales_view(request):
    resultado = None

    if request.method == 'POST':
        derivada_input = request.POST.get('derivada_input')
        try:
            x, y = sp.symbols('x y')
            derivada = sp.sympify(derivada_input)
            derivada_x = sp.diff(derivada, x)
            derivada_y = sp.diff(derivada, y)
            resultado = {
                'derivada_x': str(derivada_x),
                'derivada_y': str(derivada_y),
            }
        except Exception as e:
            print(e)  # Imprimir el error para depurar
            resultado = {
                'error': 'Error: Ingresa una derivada válida.'
            }

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(resultado)
    else:
        return render(request, 'derivadas_parciales.html', {'resultado': resultado})


def transformada_laplace_view(request):
    resultado = None

    if request.method == 'POST':
        function_input = request.POST.get('function_input')
        try:
            t, s = symbols('t s')
            function = parse_expr(function_input, transformations=(standard_transformations + (implicit_multiplication_application,)))
            laplace_transform_result = laplace_transform(function, t, s, noconds=True)
            inverse_laplace_transform_result = inverse_laplace_transform(laplace_transform_result, s, t)
            
            # Construir el resultado como un diccionario
            resultado = {
                'laplace_transform': str(laplace_transform_result),
                'inverse_laplace_transform': str(inverse_laplace_transform_result),
            }
        except Exception as e:
            print(e)  # Imprimir el error para depurar
            resultado = {
                'error': 'Error: Ingresa una función válida.'
            }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(resultado)
    else:
        return render(request, 'transformada_laplace.html', {'resultado': resultado})

def optimizacion_funciones_view(request):
    if request.method == 'POST':
        print("Solicitud POST recibida")

        funcion_input = request.POST.get('function_input')
        print("Función ingresada:", funcion_input)

        try:
            # Define una función utilizando SymPy para cálculos
            x = sp.symbols('x')
            funcion_sym = sp.sympify(funcion_input)

            # Define la función que será optimizada
            def funcion_a_optimizar(params, x_value):
                return float(funcion_sym.subs(x, x_value))

            # Crear objeto Parameters y agregar parámetro
            params = Parameters()
            params.add('x_value', value=0)

            # Realizar la optimización
            result = minimize(funcion_a_optimizar, params, args=(0,), method='Levenberg-Marquardt')

            resultado = {
                'valor_minimo': result.params['x_value'].value,
                'argumento_minimo': result.params['x_value'].value,
                'valor_maximo': -result.params['x_value'].value,
                'argumento_maximo': -result.params['x_value'].value,
            }
        except Exception as e:
            print("Error:", str(e))
            resultado = {
                'error': 'Error: Ingresa una función válida.'
            }

        print("Resultado:", resultado)
        return JsonResponse(resultado)
    else:
        return render(request, 'optimizacion_funciones.html')