from django.test import TestCase

# Create your tests here.
import misaka as m
st="""some other text hello
        hw are u
        1) good"""
print(m.html(st))