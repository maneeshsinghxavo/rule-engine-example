import json
import yaml
import rule_engine
import re

re_flags = re.IGNORECASE | re.MULTILINE
context = rule_engine.Context(default_value=None, regex_flags=re_flags)


def log_violations():
    f = open('compiler_data.json')
    results = json.load(f)

    with open('rules.yml', 'r') as file_h:
        rules = yaml.load(file_h, Loader=yaml.FullLoader)

    for violation in rules['rules']:
        try:
            rule = rule_engine.Rule(violation['rule'], context=context)
        except rule_engine.RuleSyntaxError as error:
            print(error.message)

        matches = rule.filter(results)
        if not matches:
            continue

        for match in matches:
            target_name = match['name']
            print('{} {} violation'.format(target_name, violation['description']))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    log_violations()

