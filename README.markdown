
[Define Unity Lens](http://home.iitb.ac.in/~saifhhasan/)
=================

Define Unity Lens provides user with mathamatical results and dictionary look from unity dash interface only. Suppose you are reading pdf and want to get meaning of some word just press <super>+c and enter the word you want to lookup for

It's created and maintained by [Saif Hasan](http://www.cse.iitb.ac.in/~saifhhasan) at IIT Bombay.



Hack Night Competition - 2012, IIT Bombay
-----------
This application was developed in Hack Night Competition organized by [Web and Coding Club](http://stab-iitb.org/wncc). To know about other application developed in Hack Night visit [Web and Coding Club at GitHub](https://github.com/wncc)

You can visit Web and Coding Club on [WnCC Wiki](http://stab-iitb.org/wiki/Web_n_Coding_club)

If you are IIT Bombay student then you can join [WnCC Google Group](https://groups.google.com/group/wncc_iitb)




Dependency
-----------

It depends on python-gobject, python-sympy and singlet module which is included along with the source code only.

To install dependecies run the following commands in terminal:

* sudo apt-get install python-gobject
* sudo apt-get install python-sympy




Installation
----------

Clone the repository or download the zip file from [Github Repository](https://github.com/saifhhasan/Define-Unity-Lens).

Install all the dependecies as mentioned above

To install :

* sudo ./install.sh

To uninstall :

* sudo ./uninstall.sh



Features and Getting Started With
-----------

You might have to logout and login back inorder to start using lens. After login press `<super> + c` to open the Dash. In this you can directly enter whatever you want to Evaluate or Lookup

The features of application are:

* Evaluates mathematical expression and shows up results
* Might suggest you the speeling if you enter wrong spell
* Displays you the various dictionary meanings along with sample example usage. e.g. Noun, Adjective, Verb etc
* Shows the possible Web Definitions of your query  (Try IIT Bombay)




Insights of Define Lens
-------

This lens uses sympy library to evaluate the mathematical expressions.

Lens uses bing spell suggestion api to fetch the correct spelling of a query, and uses Google Dictionary API to fetch the Meanings and Web Definitions.




Authors
-------

**Saif Hasan**

+ http://github.com/saifhhasan
+ http://www.cse.iitb.ac.in/~saifhhasan
+ http://facebook.com/saifhhasan



Copyright and license
---------------------

Copyright 2012 Saif Hasan

This is opensource. Anybobdy can copy, use or distribute this software.

