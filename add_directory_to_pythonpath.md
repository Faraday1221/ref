# Temporarily adding a Directory to PYTHONPATH

These are my notes when first learning about Unix and PATH.
These are my notes when trying to add the Library directory to the PATH.
At the time I didn't understand the _.profile_ file and that the following is a
temporary solution. None the less here are my notes:


## Python commands to update the PATH

    import sys   #loads the system module
    sys.path    #shows the path for Python

    #adds a specified directory to the 0th list position
    sys.path.insert(0, '~Documents/Python/Library')

    #in future path updates we should probably use:
    #sys.path.insert(1, ‘path’)

### Refrences
- [dive into python, section 1.4](http://www.diveintopython3.net/your-first-python-program.html)
- [sys documentation](https://docs.python.org/2/library/sys.html)
- [PYTHONPATH documentation](https://docs.python.org/2/using/cmdline.html#envvar-PYTHONPATH)
- [modules documentation](https://docs.python.org/2/tutorial/modules.html)

# Permanently Adding a Directory to PYTHONPATH
http://stackoverflow.com/questions/3402168/permanently-add-a-directory-to-pythonpath

A particularly helpful comment from the link above:
> This worked perfectly for me, but make sure the directory you point to has
at the topmost init.py file in your directory structure. This wasn't perfectly
clear for me at first. For example, I tried export
PYTHONPATH=$PYTHONPATH:/Users/joey/repos but it did not work because my repos
directory did not have _init_.py. Going down one directory further:
/Users/joey/repos/specificRepo did the trick. Now python can traverse any
downward directory connected to the specificRepo directory that contains a
init.py !

[A nice explaination of the \__init__.py file](http://mikegrouchy.com/blog/2012/05/be-pythonic-__init__py.html)
