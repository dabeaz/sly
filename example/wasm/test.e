# Experimental Wasm function examples.
# To run:
#
#    1. First run python3 expr.py test.e
#    2. Use python3 -m http.server
#
# Go to a browser and visit http://localhost:8000/test.html.
# From the browser, open the Javascript console.  Try executing
# the functions from there.
#   
# Some basic functions
add(x,y) = x+y;
sub(x,y) = x-y;
mul(x,y) = x*y;
div(x,y) = x/y;

# A function calling other functions
dsquare(x,y) = mul(x,x) + mul(y,y);

# A conditional
minval(a, b) = if a < b then a else b;

# Some recursive functions
fact(n) = if n <= 1 then 1 else n*fact(n-1);
fib(n) = if n < 2 then 1 else fib(n-1) + fib(n-2);
