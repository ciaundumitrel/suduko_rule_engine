import rule_engine
import datetime

dataset = [
    {
        'row': 0,
        'col': 0,
        'value': 2,
    },
    {
        'row': 0,
        'col': 0,
        'value': 3,
    }
]

context = rule_engine.Context(type_resolver=rule_engine.type_resolver_from_dict({
    'col': rule_engine.DataType.FLOAT,
    'row': rule_engine.DataType.FLOAT,
    'value': rule_engine.DataType.FLOAT,
}))

rule = rule_engine.Rule(
    # match books published by DC
    'row == 0  and value == 2',
)

x = rule.filter(dataset)

for item in x:
    print(item)
