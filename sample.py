from docprompt import docprompt

DOC = """\

Hello World!
============

This is a configuration sample. You are welcome to do whatever you want.
I am going to ask you a few questions.

    :prompt: Do you have a disk:
    :name: has_repo
    :choices: ['y', 'n']
    :default: 'n'

Next, we will ask you another question.

    :prompt: Do you use hg or git (hg/git) [git]:
    :name: dvcs_type
    :choices: ['hg', 'git']
    :default: 'git'

Tell me about your user name. You can type but you won't see the input on the screen like when you are typing a password.

    :prompt: Your username:
    :name: username
    :secure: True

Finally, let me know your lucky number today. It's normal input again!

    :prompt: Lucky number is: 
    :name: lucky_number
    :secure: False

Thanks for using this system.
"""
d = docprompt(DOC)
print(d.display)
print('\n======\nNow prompt\n======\n')
d.prompt()

print('\n======\nNow print results\n======\n')
print("has_repo: %s" % d.has_repo)
print("dvcs_type: %s" % d.dvcs_type)
print("username: %s" % d.username)
print("lucky_number: %s" % d.lucky_number)

print("\nLast, let me show you you can access the question,\
 the choices and whether it has default.\n")
print("First question's choices are: %s" % d.has_repo_choices)
print("First question's has default? %s" % d.has_repo_has_default)
print("First question's question is: %s" % d.has_repo_question)

