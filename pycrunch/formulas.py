from collections import defaultdict

from expressions import parse_expr


# if pdl.age and pdl.gender and pdl.race and pdl.e14_presvote12 and pdl.educ:
my_formula = """

 if pdl.race == 3 and pdl.e14_presvote12 == 1 and pdl.age >= 18 and pdl.age <= 34: polistrata_hisp = 1
 if pdl.race == 3 and pdl.e14_presvote12 == 1  and pdl.age >=35: polistrata_hisp = 2
 if pdl.race == 3 and  pdl.e14_presvote12 in [3,4] and pdl.age >= 18 and pdl.age <= 34: polistrata_hisp = 3
 if pdl.race == 3 and pdl.e14_presvote12 in [3,4] and pdl.age >=35: polistrata_hisp = 4
 if pdl.race == 3 and pdl.e14_presvote12 == 2 and pdl.age >= 18 and pdl.age <= 34: polistrata_hisp = 5
 if pdl.race == 3 and pdl.e14_presvote12 == 2 and pdl.age >=35: polistrata_hisp = 6
 elif pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [1,2,3,4]: polistrata_hisp =  7
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [5,6]: polistrata_hisp =  8
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [1,2,3,4]: polistrata_hisp =  9
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [5,6]: polistrata_hisp =  10
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [1,2,3,4]: polistrata_hisp =  11
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [5,6]: polistrata_hisp =  12
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [1,2,3,4]: polistrata_hisp =  13
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [5,6]: polistrata_hisp =  14
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  15
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  16
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  17
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  18
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >=65 and pdl.educ in [1,2,3,4]: polistrata_hisp =  19
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 2 and pdl.age >=65  and pdl.educ in [5,6]: polistrata_hisp =  20
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  21
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 1 and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  22
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [1,2,3,4]: polistrata_hisp =  23
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 ==  [3,4] and pdl.gender == 2 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [5,6]: polistrata_hisp =  24
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 ==  [3,4] and pdl.gender == 1 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [1,2,3,4]: polistrata_hisp =  25
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [5,6]: polistrata_hisp =  26
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [1,2,3,4]: polistrata_hisp =  27
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [5,6]: polistrata_hisp =  28
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [1,2,3,4]: polistrata_hisp =  29
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [5,6]: polistrata_hisp =  30
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  31
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  32
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  33
 elif pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  34
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >=65 and pdl.educ in [1,2,3,4]: polistrata_hisp =  35
 elif pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 2 and pdl.age >=65  and pdl.educ in [5,6]: polistrata_hisp =  36
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  37
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == [3,4] and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  38
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [1,2,3,4]: polistrata_hisp =  39
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 ==  2 and pdl.gender == 2 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [5,6]: polistrata_hisp =  40
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 ==  2 and pdl.gender == 1 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [1,2,3,4]: polistrata_hisp =  41
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >= 18 and pdl.age <30 and pdl.educ in [5,6]: polistrata_hisp =  42
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [1,2,3,4]: polistrata_hisp =  43
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [5,6]: polistrata_hisp =  44
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [1,2,3,4]: polistrata_hisp =  45
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >= 30 and pdl.age <= 44 and pdl.educ in [5,6]: polistrata_hisp =  46
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  47
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  48
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [1,2,3,4]: polistrata_hisp =  49
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >= 45 and pdl.age <= 64 and pdl.educ in [5,6]: polistrata_hisp =  50
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >=65 and pdl.educ in [1,2,3,4]: polistrata_hisp =  51
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 2 and pdl.age >=65  and pdl.educ in [5,6]: polistrata_hisp =  52
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >=65 and pdl.educ in [1,2,3,4]: polistrata_hisp =  53
 if pdl.race in [1,2,4,5,6,7,8] and pdl.e14_presvote12 == 2 and pdl.gender == 1 and pdl.age >=65 and pdl.educ in [5,6]: polistrata_hisp =  54
"""

# NOTE:
"""
if age > 15:
    if size == 3:
        test = 1
    if size == 4:
        test = 2

translates to:
'age > 15 and size == 3: test=1'
'age > 15 and size == 4: test=2'


the case of pdl.age and pdl.sample --> could be removed and assume
the user already know those vars exist and the default value should
cover the missing

Validation:
could be made by counting the number of assignments and compare to the response options map
"""


class FormulaParser(object):
    """
    This class takes a Definition getter as input and returns
    a valid JSON structure that declares a variable case
    statement in Crunch API

    Assumptions:
        - if/elif statements are one-liners
        - if/elif statements don't declare more than 1 variable
        - no nested conditionals for now
        - the value assigned to the variable declared in the if is the
          categorical value the Crunch variable will take
        - no else statements is supported at the moment

    Steps:
        - Remove 'pdl.' prefix
    """

    def __init__(self, formula):
        self.formula = formula
        self.map = defaultdict(list)
        self.parsed_map = defaultdict(list)
        self.unfolded_map = dict()

    def remove_pdl_prefix(self):
        self.formula = self.formula.replace('pdl.', '')

    def prepare(self):
        """
        Does some cleaning and converts the string
        into lines
        """
        lines = self.formula.split('\n')
        # remove spaces
        lines = [x.strip() for x in lines]
        # remove empty lines
        self.lines = filter(lambda x: not x == '', lines)

    def mappings(self):
        """
        splits formula lines by conditional and
        variable assignment and appends them to a
        map that is keyed by category
        """
        for line in self.lines:
            expr = line.split(':')[0]
            expr = expr.lstrip('if')
            expr = expr.lstrip('elif')
            expr = expr.strip()
            binding = line.split(':')[-1]
            category = binding.split('=')[-1].strip()
            self.map[category].append(expr)

    def parse_mappings(self):
        """
        Converts simple conditional statements into
        crunch conditional operations
        """
        for key, values in self.map.items():
            for val in values:
                parsed = parse_expr(val)
                self.parsed_map[key].append(parsed)

    def unfold_categories(self):
        """
        A category at the moment might have more than 1
        conditionals, we need to join them in a or operation
        """
        for key, value in self.parsed_map.items():
            if len(value) > 1:
                default = {
                    'function': 'or',
                    'args': value
                }
                self.unfolded_map[key] = default
            else:
                self.unfolded_map[key] = self.parsed_map[key][0]

    def run(self):
        self.remove_pdl_prefix()
        self.prepare()
        self.mappings()
        self.parse_mappings()
        self.unfold_categories()


if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    fp = FormulaParser(my_formula)
    fp.run()
    pp.pprint(fp.unfolded_map)
