=========
docprompt
=========

Inspired by docopt (https://docopt.org), docprompt allows developers
to write configuration prompts in RST or docstring format.

Why? Because I need this shit for my research project l-o-l.


Example
-------

Suppose you want to write an interactive configurator for a blog
system, you can express the entire configuration in RST or docstring.

In either a RST file or as a docstring in a Python file::
    
    Database Configurations
    =======================

    XXX Blog Engine works with major SQL servers. You must provide
    proper credentials to connect the engine with the database.

    
        :prompt: Choose database (mysql,postgres,oracle) [mysql]:
        :name: db_type
        :choices: ['mysql', 'postgres', 'oracle']
        :default: 'mysql

        :prompt: Database host [localhost]:
        :name: db_host
        :default: 'localhost'

        :prompt: Database user:
        :name: db_user

    Site Configurations
    ===================

    Almost done! Just a few questions to configure your site! 

        :prompt: Choose an admin account [admin]:
        :name: admin_acc_name
        :default: 'admin'
        
        :prompt: Allows search engines (y/n) [y]:
        :name: allow_search
        :choices: ['y', 'n']
        :default: 'n'    


Usage
=====

There are two parts:

1. construct prompts in rst/docstring

2. access the results from users

Construct prompts
-----------------

`docprompt` provides two required arguments `prompt` and
`name`, as well as two optional arguments called 
`default` and `choices`.

A `prompt` is an interactive ask/answer input. All inputs will
be treated as raw strings. We don't implement casting because
a configurator will either write to a config file or pass
the information to some functions such as connecting to database.
Thus, in nearly every single real usecase, casting a string
to another type (e.g. int) should be handled by the developers.

`name` is the variable name used to reference the answer from
the user. It has to be a legal python variable name. 
We encourage to adapt standard variable naming convention.
An example of a variable name is `db_host` instead of
`db-host` which is illegal as a variable name.

For a simple question without need for choices or default::

    :prompt: <Start typing your question here>
    :name: <legal-python-variable-name>

In addition, if prompts requires a default value, add `default``::

    :default: 'a string'


Finally, if a list of choices are required, add `choices`::
    
    :choices: ['item1-in-string', 'item2-in-string', 'and-so-on']


Order doesn't matter, but for consistency we encourage to
use the format shown in the examples above.


Access results from users
-------------------------

All the `name` of all `prompts` are collected
and made into member attributes of the object
`docprompt`. 

For example, if we assume the text in the example above
is a global docstring (the ver first one, actually),
we can construct the example above::

    import docprompt
    
    if __name__ == '__main__':
        quick_start = docprompt(source=__doc__)
        assert quick_start.db_host in ['mysql', 'postgres', 'oracle']

You are welcome to write up multiple doc strings using
multiple `docprompt` objects. This is common for an
application provides a command-line interface. 


Bonus: Build command-line interface with docopt
-----------------------------------------------

I actually find `docopt` very handy for building
a command-line client. My project `docprompt`
can migiate the need to write a bunch of
`raw_input`. 

Suppose you want to build a command-line interface,
first construct the commands using `docopt`, 
and then use `docprompt` to construct the prompts
and access the user inputs in a novel way!

Cheer.


