
def toStr(val):
	if val is None:
		return 'null'
	if isinstance(val, bool) or isinstance(val, int):
		return str(val)
	return val

