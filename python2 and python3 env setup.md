## Setting up python 2.7 and 3.4 as seperate enviornments with anaconda
first we note that our enviornments are installed in this directory:

root *Library/anaconda/envs

we can find this using the following cmd:
>conda info -e

Then create the two enviornments **python2** and **python3** for 2.7 and 3.4 using:
>conda create -n python2 python=2.7 anaconda  
>conda create -n python3 python=3.4 anaconda

We can activate an enviornment, python 2.7 for instance, using the following cmd:
>source activate python2

we can deactivate the enviornment using
>source deactivate

The enviornments are now stored in these folders
>/Library/anaconda/envs/python2  
>/Library/anaconda/envs/python3

[Reference article on how to install 2 anaconda enviornments](http://stackoverflow.com/questions/24405561/how-to-install-2-anacondas-python-2-7-and-3-4-on-mac-os-10-9)

### Using spyder with python enviornments 2.7 and 3.4
Once the enviornments are setup as per the previous instructions, simply open an enviornment at the command line and tell open the program we want to work in i.e. **Spyder** or **iPython** or **iPython notebook** and it will launch with the appropriate version of python. Easy huh.




[Stackoverflow article  about where Spyder program lives in anaconda enviornments - note, this wasn't ultimately helpful](http://stackoverflow.com/questions/28318322/how-to-start-two-instances-of-spyder-with-python-2-7-python-3-4?lq=1)
