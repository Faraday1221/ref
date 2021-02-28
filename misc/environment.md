# Environments for new-coder projects
Although the guidelines for new-coder recommend using virtualenv I prefer conda as my VM and package manager. Setting up conda environments is very similar to virtualenv, except instead of **requirements.txt** we will create **environment.yml**

    touch environment.yml

A sample environment.yml file:

    name: env-name
    dependencies:
        - python=3.4
        - numpy

Once your environment.yml file is in place (in the appropriate directory)

    conda env create --name <env-name>

Then to activate the environment for that project simply type

    source activate <env-name>

#### Reference:
There is a lot more to conda environments than what is listed here, but this is plenty to get started.
- [Offical Conda Env Docs](https://github.com/conda/conda-env)
