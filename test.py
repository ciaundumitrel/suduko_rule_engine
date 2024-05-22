import rule_engine
import datetime

# define the custom context with two symbols
dataset = [
    {
        'row': 0,
        'col': 0,
        'value': 2,
    },
    {
        'row': 0,
        'col': 1,
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
    'row == 0  and col == 0',
)

x = rule.filter(dataset)
for _ in x:
    dataset.remove(_)
dataset.append({'row': 0, 'col': 0, 'value': 2})
print(dataset)