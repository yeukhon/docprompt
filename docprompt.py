import re
import ast
import types

def syntax(ident, groupname, rep):
    """
    Return a regex for a single syntax.

    Parameters
    ----------
    ident : str
        Identifier of the syntax.
    groupname : str
        The name of the regex group.
    rep : str
        A valid regex repetition symbol
        such as * or +. If not used,
        specified it as '' empty string.
  
    Returns
    -------
    regex : str

    """

    if rep:
        return r'(({id})\s+(?P<{gn}>[^.+^\r\n]+)){rep}'.format(id=ident,\
                                                        gn=groupname,\
                                                        rep=rep)
    else:
        return r'({id})\s+(?P<{gn}>[^.+^\r\n]+)'.format(id=ident, gn=groupname) 

def chain_syntax(syntax_group):
    """
    Construct a docprompt chain regex syntax.

    Parameters
    ----------
    syntax_group : list
        A list of tuples of (ident, groupname, rep). 
        e.g. [ (':prompt:', 'question'), ('name', 'vname'), \
               ( ':default:', 'default', '*') ]

    Returns
    -------
    pattern : string
        A docprompt chain regex.

    See Also
    --------
    repo : see ``syntax`` for usage.
    syntax : Function returns regex for a single syntax group.
    
    """
    return r'([\r\n][\s]+)*'.join( [syntax(id, gn, deli) for (id, gn, deli)  in syntax_group] )

def keys_iter(pattern, text):
    """
    Return a list of dictionary of syntax keys.

    Paramters
    ---------
    pattern : regex
        Compiled Python regex pattern.
    text : str

    Returns
    -------
    output : list
        A list of dictionaries containing all the 
        values matched to its named regex group.
        Keys in the dictionary are groupname.

    See Also
    --------
    chain_syntax : Function produces the regex pattern \
    for a chain of syntax groups.
    syntax : Function produces the regex for a single \
    syntax group.

    """

    return [m.groupdict() for m in pattern.finditer(text)]


class docprompt(object):
    keys = [ (':prompt:', 'question', ''),\
             (':name:', 'vname', ''),\
             (':choices:', 'choices', '?'),\
             (':default:', 'default', '?')
           ]
    parse_rule = chain_syntax(keys)
    replace_rule = '[\s\t]*' + parse_rule
    pattern = re.compile(parse_rule)

    def __init__(self, source):
        self.source = source
        self.values = keys_iter(self.pattern, self.source)
        self.display_text = ''

        # next we have to make attributes out of all the dictionaries
        # so we can access, e.g. Object.foo if foo is one of the 'vname'
        for item in self.values:
            vname = item['vname']
            question_name = vname + '_question'
            choices_name = vname + '_choices'
            has_default_name = vname + '_has_default'
            if isinstance(item['choices'], types.NoneType):
                choices = None
            else:
                try:
                    choices = ast.literal_eval(item['choices'])
                except ValueError:
                    print("You supplied choices {c}. Make sure it's properly written.".format(c=item['choices']))
                    return
            if isinstance(item['default'], types.NoneType):
                default = None
            else:                
                try:
                    default = ast.literal_eval(item['default'])
                except ValueError:
                    print("You supplied default {d}. Make sure it's properly written.".format(d=item['default']))
                    return
            # now we can finally set attributes
            setattr(self, question_name, item['question']) # Object.foo_question 'Do you ...'
            setattr(self, vname, default) # Object.foo = default value
            setattr(self, choices_name, choices) # Object.foo_choices = [ .... ]
            setattr(self, has_default_name, True if default else False) # Object.foo_has_default

    def __iter__(self):
        """ Parse source with pattern and return iterator. """
        return (group for group in self.values)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, slice):
        return self.values[slice]

    def __replace(self, group):
        question = '> ' + group['question']
        return re.sub(self.replace_rule, '\n'+question, src_copy, count=1)
        
    @property
    def display(self):
        """ Display the full parsed configurator text. """
        if self.display_text:
            return self.display_text

        src_copy = self.source
        for each in self:
            question = '> '+each['question']
            src_copy = re.sub(self.replace_rule, '\n'+question, src_copy, count=1)
        self.display_text = src_copy
        return self.display_text

    def prompt(self):
        """ Iterate over a prompt for each question. """
        if not self.display_text:
            self.display
        
        memor_start_pos = 0  # cache the last starting text to display to user
        for each in self:
            question = '> ' + each['question']
            len_q = len(question)
            vname = each['vname']
            vname_choices = getattr(self, vname + '_choices')
            vname_has_default = getattr(self, vname + '_has_default')
            # the amount of text outputs to terminal is exactly
            # from memor_start_pos to the 
            # index of str.find('<question>') + (len(<question>) -1)
            end = self.display_text.find(question) + (len_q-1)
            while True:
                # Four cases to handle:
                # 1. when user presses ENTER but no default provided
                # 2. when user presses ENTER but default is provided
                # 3. when user enters her own value but not among the choices
                # 4. finally, when user value is one of the choices, EXIT
                user_ans = raw_input(self.display_text[memor_start_pos:end])
                if not user_ans and not vname_has_default:
                    print("[!] You must provide an answer.\n")
                elif not user_ans:
                    break
                elif user_ans and not user_ans in vname_choices:
                    print("[!] Your input is not accpetable. Only {c} are allowed.".format(c=vname_choices))
                elif user_ans in vname_choices:
                    setattr(self, vname, user_ans)
                    break
                
            memor_start_pos = end+1
        if memor_start_pos < len(self.display_text):
            print(self.display_text[memor_start_pos:])
     
