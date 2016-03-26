# Profiling Code with IPython
_A quick overview of Basic Profiling using %prun for macro profiling and %lprun for micro profiling in IPython_

## Basic Profiling: %prun
cProfile is the main Python profiling module and can be accessed via IPython through two magic commands that will allow us to call cProfile within IPython.

There is some documentation around cProfile that is somewhat difficult to unpack. Here is a simple use case for running cProfile using built in magic commands in IPython.

    def some_fcn(x,y):
        result = x+y
        print(result)
The simplest example of this command is as follows:

    %prun some_fcn(10,11)
    21
             3 function calls in 0.000 seconds

       Ordered by: internal time

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 test2.py:6(main)
            1    0.000    0.000    0.000    0.000 <string>:1(<module>)
            1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}_

A slightly more complicated, but more useful profile call is with some supporting flags to limit and sort the output

    %prun -l 1 -s time some_fcn(10,11)
    21
             3 function calls in 0.000 seconds

       Ordered by: internal time
       List reduced from 3 to 1 due to restriction <1>

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 test2.py:6(main)

Now lets unpack this a bit **-l** stands for list and **limits the output to only those number of lines**, **-s** is sort and will sort by either **time** *(internal time)* as above or **cumulative** time. We can also sort by **calls**.

Here are some examples:

    %prun -s calls some_fcn(10,11)

    %prun -s cumulative some_fcn(10,11)

    %prun -s time some_fcn(10,11)

While the example provided here is trivial it should hopefully shed light on the general concept. It is helpful to note that this may be most useful when evaluating the timing of a program, we look at the **line_profiler** to investigate code blocks or functions where the output of cProfile may be difficult to interpert.

### A quick note about %run -p
The **%run -p** command is the same as the **%prun** command in IPython, except that here the **-p** flag is calling the profiler function.

## Profiling a Function Line-by-Line
_In some cases the information you obtain from %prun may not tell the whole story about a function's execution time, or it may be so complex that the results, aggregated by function name, are hard to interpert_ **-Python for Data Analysis** _(p.66)_

In this case we can use the line_profiler library, first we have to install line_profiler. The file can be [downloaded here](https://anaconda.org/anaconda/line_profiler). line_profiler [docs can be found here](https://github.com/rkern/line_profiler). The command to install is

    conda install -c https://conda.anaconda.org/anaconda line_profiler



This is only half the battle, to use this within IPython instead of via the command line we need to update our IPython config file. The config file is located by default as:

    ~/.ipython/profile_default/ipython_config.py

if there is no default profile setup, we can easily add the default profile by running:

    $ ipython profile create

we then edit _ipython_config.py_ with the following code to add line_profiler as an ipython extension _(which enables us to use the magic command %lprun within IPython)_.

    # A list of dotted module names of IPython extensions to load.
    c.TerminalIPythonApp.extensions = ['line_profiler']

Once we restart IPython we should have access to the **%lprun** command. The general syntax is:

    %lprun -f func1 -f func2 <statement_to_profile>
Using the previous example of **some_fcn()** we see:

    %lprun -f some_fcn some_fcn(10,11)
    21
    Timer unit: 1e-06 s

    Total time: 0.003215 s
    File: test2.py
    Function: main at line 6

    Line #      Hits         Time  Per Hit   % Time  Line Contents
    ==============================================================
         6                                           def main(x,y):
         7         1         2729   2729.0     84.9      result = x+y
         8         1          486    486.0     15.1      print(result)

## Reference
- most of this was taken directly from **Data Analysis with Python**
- [line_profiler docs](https://github.com/rkern/line_profiler)
- [IPython config docs](http://ipython.readthedocs.org/en/stable/config/intro.html#profiles)
- [An excellent resource for general profiling and performance analysis](https://www.huyng.com/posts/python-performance-analysis)
