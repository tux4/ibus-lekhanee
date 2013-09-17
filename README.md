##Input Method for Indic Languages for IBus.
Prasanna Suman

This is a quick proof of concept for better IM for Indic Languages based on IBus template.
I have been working with Nepali as an example although I plan to make it easily extendible for other Indic scripts.

To run, make sure your IBus daemon is running. 
>[Alt]+[F2]:ibus-daemon
Next, run 
> python ./engine/main.py
or, 
>run start.sh 
 The standard IBus shortcuts are used to activate and change the IM, so use [Ctrl]+[Space] to start, [Alt]+[/] to switch.

 GPL2
##News
 1) I am currently in the process of cleaning up the code. That begins with separating the transliterator as its own library because it can be used in many other cases and not just this. 

##Goals
 TODO
 1) Find all the dependencies so others can use it.
