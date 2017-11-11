from os import remove
from os.path import isfile
from sys import path
from os.path import abspath
from sys import argv

path.append(abspath("."))

from meh import Config, Option, UnsupportedTypeError, ExceptionInConfigError

CONFIG_PATH = "data_types.cfg"

config = Config()
config.add(Option("list", [1, 2, 3]))
config.add(Option("tuple", (1, 2, 3)))
config.add(Option("dict", {"foo" : "baz", "test" : 123}))
config.add(Option("bytes", b"test"))
config.add(Option("string", "test"))
config.add(Option("float", 42.0))
config.add(Option("complex", (1+2j)))
config.add(Option("int", 42))
config.add(Option("boolean", False))

try:
	config = config.load(CONFIG_PATH)
except (IOError, ExceptionInConfigError):
	config.dump(CONFIG_PATH)
	config = config.load(CONFIG_PATH)

print(config.list)
print(config.tuple)
print(config.dict)
print(config.bytes)
print(config.string)
print(config.float)
print(config.complex)
print(config.int)
print(config.boolean)

config.list = [1, 2, 3, 4]
config.tuple = ("1", "2", "3")
config.dict = {"foo" : 123, "test" : 124.0, "foo1" : "bar"}
config.bytes = b"bytes"
config.string = "string"
config.float = 10.0
config.complex = (2+2j)
config.int = 43
config.boolean = True

try:
	config.list = [1, 2, 3, [lambda x: True]]
except UnsupportedTypeError:
	print("Value validatation succeeded for list")

try:
	config.tuple = ("1", "2", (lambda x: True, ))
except UnsupportedTypeError:
	print("Value validatation succeeded for tuple")

try:
	config.dict = {"foo" : lambda x: True, "test" : 124.0, "foo1" : "bar"}
except UnsupportedTypeError:
	print("Value validatation succeeded for dict")

print("File contents:")
print(config._dumps())

if not (len(argv) == 2 and argv[1] == "keep"):
	remove(CONFIG_PATH)
	if isfile(CONFIG_PATH + "c"):
		remove(CONFIG_PATH + "c")
	