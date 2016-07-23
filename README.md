# Meh

![](http://content.philip-trauner.me/meh.png)

***Meh*** is a **Python configuration utility**. I know there are already quite a few good ones out there but trust me, ***Meh*** is different.
Instead of relying on some kind of **data format** like JSON it uses something which I can't believe nobody has thought of yet: **Python**. 


## Usage
```python
from Meh import Config, Option

config = Config()
config.add(Option("food", ["Steak", "Pizza", "Burgers"], 
	validator=lambda x: type(x) is list))
config.add(Option("ages", {"@snoato" : 18, "@PhilipTrauner" : 16}, 
	validator=lambda x: type(x) is dict))
config.add(Option("bytestring", b"test"))
config += Option("another_number", 42.0, comment="hihi")
config -= Option("another_number", 42.0, comment="hihi")
config += Option("another_number", 42.0, comment="hihi")

CONFIG_PATH = "awesome_config.cfg"

try:
	config = config.load(CONFIG_PATH)
except IOError:
	config.dump(CONFIG_PATH)
	config = config.load(CONFIG_PATH)

print(config.food)
print(config.ages)
print(config.bytestring)
print(config.another_number)

# Changing values during runtime
config.food = ["Baked Beans", "Ramen"]
print(config.food)
```
**Outputs**:

```
['Baked Beans', 'Ramen']
{'@PhilipTrauner': 16, '@snoato': 18}
test
42.0
['Baked Beans', 'Ramen']
```
**Creates**:

```python
food = ['Baked Beans', 'Ramen']
ages = {'@PhilipTrauner': 16, '@snoato': 18}
bytestring = "test"
another_number = 42.0 # hihi
```


## Tidbits
`Config(options=[], validation_failed=None)`

* `options`: Provide a list of options instead of calling `add` for all of them.
* `validation_failed`: Provide a function accepting two parameters (name and value) that's called when a validation fails (returns nothing). (Otherwise a ValidationError will be raised)

`Option(name, default_value, validator=None, comment="")`

* `validator`: Provide a function accepting one parameter which checks if a value is correct (returns a boolean).
* `comment`: A comment appended to the variable declaration in the config file itself.