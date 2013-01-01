import sys
import re
import unittest
from docprompt import *

class TestChainDirective(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prompt = (':prompt:', 'question', '')
        cls.name = (':name:', 'vname', '')
        cls.choices = (':choices:', 'choices', '?')
        cls.default = (':default:', 'default', '?')

    def test_prompt_name_chain_equal(self):
        chain = [self.prompt, self.name]
        expected = r'(:prompt:)\s+(?P<question>[^.+^\r\n]+)([\r\n][\s]+)*(:name:)\s+(?P<vname>[^.+^\r\n]+)'
        result = chain_syntax(chain)
        self.assertEqual(expected, result)

    def test_prompt_name_choice_equal(self):
        chain = [self.prompt, self.name, self.choices]
        expected = r'(:prompt:)\s+(?P<question>[^.+^\r\n]+)([\r\n][\s]+)*(:name:)\s+(?P<vname>[^.+^\r\n]+)([\r\n][\s]+)*((:choices:)\s+(?P<choices>[^.+^\r\n]+))?'
        result = chain_syntax(chain)
        self.assertEqual(expected, result)

    def test_prompt_name_defaultequal(self):
        chain = [self.prompt, self.name, self.default]
        expected = r'(:prompt:)\s+(?P<question>[^.+^\r\n]+)([\r\n][\s]+)*(:name:)\s+(?P<vname>[^.+^\r\n]+)([\r\n][\s]+)*((:default:)\s+(?P<default>[^.+^\r\n]+))?'
        result = chain_syntax(chain)
        self.assertEqual(expected, result)

    def test_prompt_name_choice_default_equal(self):
        chain = [self.prompt, self.name, self.choices, self.default]
        expected = r'(:prompt:)\s+(?P<question>[^.+^\r\n]+)([\r\n][\s]+)*(:name:)\s+(?P<vname>[^.+^\r\n]+)([\r\n][\s]+)*((:choices:)\s+(?P<choices>[^.+^\r\n]+))?([\r\n][\s]+)*((:default:)\s+(?P<default>[^.+^\r\n]+))?'
        result = chain_syntax(chain)
        self.assertEqual(expected, result)
        
        
class TestChianPatternMatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text1 = """\
                This is a simple configurator.
                ==============================

                Please answer questions.

                :prompt: first question :
                :name: first_question
        """
        cls.text2 = cls.text1 + """\
                \n
                Another question.

                :prompt: second question [y/n] [n]:
                :name: second_question
                :choices: ['y', 'n']
                :default: 'n'
        """
        cls.text3 = cls.text2 + """\
                \n
                Without default values.

                :prompt: third question [y/n]:
                :name: third_question
                :choices: ['y', 'n']
        """
        cls.text4 = cls.text3 + """\
                \n
                Finally, default only.

                :prompt: last question [yeukhon]:
                :name: last_question
                :default: 'yeukhon'
        """
        cls.prompt = (':prompt:', 'question', '')
        cls.name = (':name:', 'vname', '')
        cls.choices = (':choices:', 'choices', '?')
        cls.default = (':default:', 'default', '?')

    def test_prompt_name_text1_matched(self):
        chain = [self.prompt, self.name]
        pattern = re.compile(chain_syntax(chain))
        keys_list = keys_iter(pattern, self.text1)
        expected = [{'question': 'first question :',\
                     'vname': 'first_question'
                   }]
        self.assertEqual(expected, keys_list)

    def test_prompt_name_choices_default_text2_matched(self):
        chain = [self.prompt, self.name, self.choices, self.default]
        pattern = re.compile(chain_syntax(chain))
        keys_list = keys_iter(pattern, self.text2)
        expected = [{'question': 'first question :',\
                     'vname': 'first_question',\
                     'choices': None,\
                     'default': None
                    },\
                    {'question': 'second question [y/n] [n]:',\
                     'vname': 'second_question',\
                     'choices': "['y', 'n']",\
                     'default': "'n'"
                    }]
        self.assertEqual(expected, keys_list)
        
    def test_text3_matched(self):
        chain = [self.prompt, self.name, self.choices, self.default]
        pattern = re.compile(chain_syntax(chain))
        keys_list = keys_iter(pattern, self.text3)
        expected = [{'question': 'first question :',\
                     'vname': 'first_question',\
                     'choices': None,\
                     'default': None
                    },\
                    {'question': 'second question [y/n] [n]:',\
                     'vname': 'second_question',\
                     'choices': "['y', 'n']",\
                     'default': "'n'"
                    },\
                     {'question': 'third question [y/n]:',\
                      'vname': 'third_question',\
                      'choices': "['y', 'n']",\
                      'default': None
                    }]
        self.assertEqual(expected, keys_list)

    def test_text4_matched(self):
        chain = [self.prompt, self.name, self.choices, self.default]
        pattern = re.compile(chain_syntax(chain))
        keys_list = keys_iter(pattern, self.text4)
        expected = [{'question': 'first question :',\
                     'vname': 'first_question',\
                     'choices': None,\
                     'default': None
                    },\
                    {'question': 'second question [y/n] [n]:',\
                     'vname': 'second_question',\
                     'choices': "['y', 'n']",\
                     'default': "'n'"
                    },\
                     {'question': 'third question [y/n]:',\
                      'vname': 'third_question',\
                      'choices': "['y', 'n']",\
                      'default': None
                    },\
                     {'question': 'last question [yeukhon]:',\
                      'vname': 'last_question',\
                      'choices': None,\
                      'default': "'yeukhon'"
                    }]
        self.assertEqual(expected, keys_list)

class TestDocPromptAttribute(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text1 = """\
                This is a simple configurator.
                ==============================

                Please answer questions.

                :prompt: first question :
                :name: first_question
        """
        cls.text2 = cls.text1 + """\
                \n
                Another question.

                :prompt: second question [y/n] [n]:
                :name: second_question
                :choices: ['y', 'n']
                :default: 'n'
        """
        cls.text3 = cls.text2 + """\
                \n
                Without default values.

                :prompt: third question [y/n]:
                :name: third_question
                :choices: ['y', 'n']
        """
        cls.text4 = cls.text3 + """\
                \n
                Finally, default only.

                :prompt: last question [yeukhon]:
                :name: last_question
                :default: 'yeukhon'
        """                
    def test_text1_attribute_set_correctly(self):
        doc = docprompt(self.text1)
        self.assertEqual(doc.first_question, None)
        self.assertEqual(doc.first_question_choices, None)
        self.assertEqual(doc.first_question_question, 'first question :')   
        self.assertEqual(doc.first_question_has_default, False)

    def test_text2_attribute_set_correctly(self):
        doc = docprompt(self.text2)
        self.assertEqual(doc.first_question, None)
        self.assertEqual(doc.first_question_choices, None)
        self.assertEqual(doc.first_question_question, 'first question :')   
        self.assertEqual(doc.first_question_has_default, False)
        self.assertEqual(doc.second_question, 'n')
        self.assertEqual(doc.second_question_choices, ['y', 'n'])
        self.assertEqual(doc.second_question_question, 'second question [y/n] [n]:')
        self.assertEqual(doc.second_question_has_default, True)

    def test_text3_attribute_set_correctly(self):
        doc = docprompt(self.text3)
        self.assertEqual(doc.first_question, None)
        self.assertEqual(doc.first_question_choices, None)
        self.assertEqual(doc.first_question_question, 'first question :')   
        self.assertEqual(doc.first_question_has_default, False)
        self.assertEqual(doc.second_question, 'n')
        self.assertEqual(doc.second_question_choices, ['y', 'n'])
        self.assertEqual(doc.second_question_question, 'second question [y/n] [n]:')
        self.assertEqual(doc.second_question_has_default, True)
        self.assertEqual(doc.third_question, None)
        self.assertEqual(doc.third_question_choices, ['y', 'n'])
        self.assertEqual(doc.third_question_question, 'third question [y/n]:')
        self.assertEqual(doc.third_question_has_default, False)

    def test_text4_attribute_set_correctly(self):
        doc = docprompt(self.text4)
        self.assertEqual(doc.first_question, None)
        self.assertEqual(doc.first_question_choices, None)
        self.assertEqual(doc.first_question_question, 'first question :')   
        self.assertEqual(doc.first_question_has_default, False)
        self.assertEqual(doc.second_question, 'n')
        self.assertEqual(doc.second_question_choices, ['y', 'n'])
        self.assertEqual(doc.second_question_question, 'second question [y/n] [n]:')
        self.assertEqual(doc.second_question_has_default, True)
        self.assertEqual(doc.third_question, None)
        self.assertEqual(doc.third_question_choices, ['y', 'n'])
        self.assertEqual(doc.third_question_question, 'third question [y/n]:')
        self.assertEqual(doc.third_question_has_default, False)
        self.assertEqual(doc.last_question, 'yeukhon')
        self.assertEqual(doc.last_question_choices, None)
        self.assertEqual(doc.last_question_question, 'last question [yeukhon]:')
        self.assertEqual(doc.last_question_has_default, True)

if __name__ == '__main__':
    unittest.main()
