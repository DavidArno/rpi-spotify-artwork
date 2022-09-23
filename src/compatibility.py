running_as_cpython = True

try:
    import micropython # type: ignore
    running_as_cpython = False    
except: pass

running_as_micropython = not running_as_cpython