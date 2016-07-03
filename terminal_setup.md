# Setting up the Terminal
While there are some interesting Terminal alternatives like [iTerm2](https://www.iterm2.com). I wanted to figure out how to set up my terminal to better suit my everyday activities.  A brief guide is below:

## Terminal Color Schemes
Changing the color in terminal can be very helpful for easily identifying folders or files and for separating commands from other CL text. To change the default views in Terminal I used the following articles
- [add ubuntu-like colors to terminal](http://apple.stackexchange.com/questions/9821/can-i-make-my-mac-os-x-terminal-color-items-according-to-syntax-like-the-ubuntu)
- [tweak the terminal colors and title](https://www.ibm.com/developerworks/linux/library/l-tip-prompt/)
- [a great unix article i only skimmed](http://unix.stackexchange.com/questions/148/colorizing-your-terminal-and-shell-environment)

From these articles I created a simple shell script to run from .bashrc **.ubuntu_colors.sh** It is helpful to note that the **tweak** article also describes all the terminal commands and how they align with color.

Add **ubuntu_colors.sh** to the home directory, then in **~./bashrc** add the following:

    source ubuntu_colors.sh
#### A minimal prompt
The following is also potentially useful instead of the Ubuntu setup for the CL prompt itself. If your short on screen space this is pretty sweet:

    export PS1="\[\e]2;\u@\H \w\a\e[32;1m\]>\[\e[0m\] "

## Terminal Themes
There are a handful of terminal themes available that seem fairly cool.

- [one-dark](https://github.com/anunez/one-dark-terminal)
- [ubuntu](http://media.tannern.com/tanner.terminal)

_There is another Atom Dark theme along with an Atom Light theme available_ [here](https://github.com/nathanbuchar/atom-one-dark-terminal).  _However it is hard to read._

## Vi Syntax Highlighting
[Referenced here](http://www.cyberciti.biz/faq/turn-on-or-off-color-syntax-highlighting-in-vi-or-vim/)... in **~/.vimrc** enter the following:

    syntax on
