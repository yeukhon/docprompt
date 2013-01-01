#import docprompt
t = """\
    :prompt: Do you like this?
    :name: like_this

    :prompt: I am good
    :name: hello
    :choices: [1, 2 3]
    :default: 1

"""
"""
for each in docprompt.docprompt(t):
    print each
docprompt.docprompt(t).parse()
"""

keys = [ (':prompt:', 'question', ''),\
         (':name:', 'vname', ''),\
         (':choices:', 'choices', '?'),\
         (':default:', 'default', '?')
       ]
import re
from docprompt import *
c = chain_syntax(keys)
p = re.compile(chain_syntax(keys))
t2 = t
t3 = ''
count = 1
for match in p.finditer(t):
    t3 = ''
    m2 = match.groupdict()
    #t2 = re.sub('[\s\t]*:prompt:\s+(?P<question>[^.+^\r\n]+)', '\n'+m2['question'], t2, count=1)
    if count == 1:
        t2 = re.sub('[\s\t]*'+c, '\n'+m2['question'], t2, count=1)

        #t3 = t2[match.span()[0]:match.span()[0]+len('\n'+m2['question'])]
        #print t3
    else:
        t3 = t2
        t2 = re.sub('[\s\t]*'+c, '\n\n'+m2['question'], t2, count=1)
        start, end = match.span()
        #print t3[start:end]
    count += 1

t4 = """\

Hello World!
============

This is a configuration sample. You are welcome to do whatever you want.
I am going to ask you a few questions.
    :prompt: Do you have the repo on disk (y/n) [n]:
    :name: has_repo
    :choices: ['y', 'n']
    :default: 'n'


Next, we will ask you another question.
    :prompt: Do you use hg or git (hg/git) [git]:
    :name: dvcs_type
    :choices: ['hg', 'git']
    :default: 'git'

Thanks for using this system.
"""
d = docprompt(t4)
d.prompt()
#assert d.has_repo == 'n'
#assert d.dvcs_type == 'git'
print d.has_repo
print d.dvcs_type
