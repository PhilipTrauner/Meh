from imp import load_source
from os.path import isfile
from sys import version

class OptionDuplicateError(IndexError):
	def __init__(self, name):
		super(IndexError, self).__init__("'%s' already exists" % name)	


class OptionNotFoundError(IndexError):
	def __init__(self, name):
		super(IndexError, self).__init__("'%s' does not exist" % name)	


class NameMustBeStringError(Exception):
	def __init__(self):
		super(Exception, self).__init__("option names have to be strings")


class ValidationError(Exception):
	def __init__(self, option):
		super(Exception, self).__init__("invalid value for option '%s'" % option)


class UnsupportedTypeError(TypeError):
	def __init__(self):
		super(TypeError, self).__init__("only list, tuple, dict, bytes, "
			"str, float, complex, int and bool are supported (same " 
			"thing applies to list, dict and tuple contents)")	


class ExceptionInConfigError(Exception):
	"""
	Raised if an exception occurs while importing a config file.

	IN: error (hint: error that occured on import)
	"""
	def __init__(self, error):
		self.error = error
		super(Exception, self).__init__("error occured during config import (%s)" % 
			error.__class__.__name__)

def validate_value(value):
	type_value = type(value)
	if type_value in (list, tuple):
		for element in value:
			if not validate_value(element):
				return False
	elif type_value is dict:
		return validate_value(tuple(value.keys())) and validate_value(tuple(value.values()))
	elif type_value in (bytes, str, float, complex, int, bool):
		return True
	else:
		return False
	return True

def make_value(value):
	if validate_value(value):
		if type(value) is str:
			value = '"%s"' % value
		elif type(value) in (list, tuple, dict):
			value = str(value)
		return value
	else:
		raise UnsupportedTypeError()


class _EditableConfig:
	"""
	Automatically created proxy class.

	HINTS: 
	_values: All options with their respective values
	_options: All Option instances that were originally added to 
		the Config instance
	_file: Path to the config file
	_validation_failed: Optional function that's called on a validation error
	_debug: Debug mode on/off (obviously)
	"""
	def __init__(self, values, options, file, validation_failed=None, debug=False):
		self._values = values
		self._options = options
		self._file = file
		self._validation_failed = validation_failed
		self._debug = debug


	def __getattr__(self, name):
		if name in self._values:
			return self._values[name]
		else:
			raise AttributeError("config no attribute '%s'" % name)


	def __setattr__(self, name, value):
		if name == "_values" or name not in self._values:
			self.__dict__[name] = value
		else:
			dump_required = False
			for option in self._options:
				if option.name == name:
					if validate_value(value):
						if option.validator != None:
							if option.validator(value):
								self._values[name] = value
								dump_required = True
							else:
								if self._validation_failed != None:
									self._validation_failed(option.name, value)
								else:
									raise ValidationError(option.name)
						else:
							self._values[name] = value
							dump_required = True
					else:
						raise UnsupportedTypeError()
			if dump_required:
				if self._debug: 
					print("Rewriting config because the value of '%s' changed." % name)
				open(self._file, "w").write(self._dumps())


	def _dumps(self):
		out = ""
		for option in self._options:
			value = make_value(self._values[option.name])
			out += "%s = %s%s\n" % (option.name, value, 
				(" # %s" % option.comment) if option.comment else "")
		return out.rstrip("\n")


	def __repr__(self):
		return self._dumps()


class Option:
	
	def __init__(self, name, default_value, validator=None, comment=""):
		if not type(name) is str:
			raise NameMustBeStringError()
		if name.startswith("__"):
			raise InvalidOptionName()
		self._name = name
		self.default_value = default_value
		self.validator = validator
		self.comment = comment


	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		if name.startswith("__"):
			raise InvalidOptionName()
		self._name = value		


	def __eq__(self, other):
		if other.__class__ == Option:
			return self.__dict__ == other.__dict__


	def __repr__(self):
		return "%s = %s" % (self.name, str(self.default_value)) 


class Config:
	"""
	The central element of Meh (TM).
	IN: 
		options=[] (type: list, hint: a list of options)
		validation_failed=None (type: function, hint: function accepting two 
			parameters that's called when a validation fails)
	
	Example usage:
	from Meh import Config, Option
	config = Config()
	config.add(Option("number", 42, validator=lambda x: type(x) is int))

	CONFIG_PATH = "awesome_config.cfg"
	try:
		config = config.load(CONFIG_PATH)
	except IOError:
		config.dump(CONFIG_PATH)
		config = config.load(CONFIG_PATH)

	print(config.number)
	"""
	def __init__(self, options=[], validation_failed=None, debug=False):
		if type(options) in (list, tuple):
			for option in options:
				if not option.__class__ == Option:
					raise TypeError("all options must be of type Option")
		else:
			raise TypeError("options must be a list or tuple containing options of type Option")
		self.options = options
		self.validation_failed = validation_failed
		self.debug = debug
		self._iterator_index = 0


	def __iter__(self):
		return self


	def __next__(self):
		if self._iterator_index < len(self.options):
			self._iterator_index += 1
			return self.options[self._iterator_index - 1]
		self._iterator_index = 0
		raise StopIteration


	def load(self, file):
		"""
		Returns the actual read- and editable config
		IN: file (type: str, hint: should be a valid path)
		"""
		if isfile(file):
			try:
				config = load_source("config", file)
			except Exception as e:
				raise ExceptionInConfigError(e)
			option_missing = False
			values = {}
			for option in self.options:
				# Make sure all options are avaliable (validators aren't run in this case
				# because there are no values defined)
				if option.name not in dir(config):
					values[option.name] = option.default_value
					option_missing = True
				else:
					# Retrieve the option value
					value = getattr(config, option.name)
					# Make sure validator passes
					if option.validator != None:	
						# If validation doesn't pass
						if not option.validator(value):
							# Resort to default value
							values[option.name] = option.default_value
							if self.validation_failed != None:
								self.validation_failed(option.name, value)
							else:
								raise ValidationError(option.name)
							option_missing = True
						# If validation passes
						else:
							values[option.name] = value
					else:
						values[option.name] = value
				if option_missing:
					self.dump(file)
			return _EditableConfig(values, self.options, file, 
				validation_failed=self.validation_failed, debug=self.debug)
		else:
			error = "'%s' not found" % file
			raise FileNotFoundError(error) if version.startswith("3") else IOError(error)


	def __add__(self, other):
		try:
			self.add(other)
		except TypeError:
			return NotImplemented
		return self


	def __sub__(self, other):
		try:
			self.remove(other)
		except TypeError:
			return NotImplemented
		return self


	def add(self, option):
		"""
		Adds an option to a Config instance
		IN: option (type: Option)
		"""		
		if option.__class__ == Option:
			for _option in self.options:
				if option.name == _option.name:
					raise OptionDuplicateError(_option.name)
			self.options.append(option)
		else:
			raise TypeError("invalid type supplied")


	def remove(self, option):
		"""
		Removes an option from a Config instance
		IN: option (type: Option)
		"""
		if option.__class__ == Option:
			if option in self.options:
				del self.options[self.options.index(option)]
			else:
				raise OptionNotFoundError(option.name)
		else:
			raise TypeError("invalid type supplied")


	def dump(self, file):
		"""
		Writes output of dumps() to the path provided
		IN: file (type: str, hint: should be a valid path)
		"""
		open(file, "w").write(self.dumps())


	def dumps(self):
		"""
		Returns contents of config file as string
		OUT: out (type: str, hint: config content)
		"""
		out = ""
		for option in self.options:
			value = make_value(option.default_value)
			out += "%s = %s%s\n" % (option.name, value, 
				(" # %s" % option.comment) if option.comment else "")
		return out.rstrip("\n")


	def __repr__(self):
		return self.dumps()
