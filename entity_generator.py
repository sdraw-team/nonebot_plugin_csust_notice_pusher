def main(pstr: str, defaults: dict):
    properties = pstr.rsplit(',')
    result = ''

    arg_init_head = """    def __init__(self, {}):\n"""
    arg_init_line = """        self.__{0} = {0}\n"""
    noarg_init_head = """    def __init__(self):\n"""
    noarg_init_line = """        self.__{0} = {1}\n"""
    getter = """    @property
    def {0}(self):
        return self.__{0}
"""
    setter = """    @{0}.setter
    def {0}(self, value):
        if value == None:
            self.__{0} = ''
        self.__{0} = value
"""

    # 有参构造器
    result += arg_init_head.format(', '.join(properties))
    for p in properties:
        result += arg_init_line.format(p)

    # 无参构造器
    result += '\n'
    result += noarg_init_head
    for p in properties:
        if p in defaults:
            default = str(defaults[p])
        else:
            default = "''"
        result += noarg_init_line.format(p, default)
        
    # property
    for p in properties:
        result += '\n'
        result += getter.format(p)
        result += '\n'
        result += setter.format(p)
    
    # get_properties()
    result += '\n'
    result += '    def get_properties(self) -> list:\n'
    _ret = list(map(lambda x: 'self.' + x, properties))
    _ret = ', '.join(_ret)
    result += '        return {}'.format(_ret)
    
    # tostring()
        

    print(result)


if __name__ == '__main__':
    properties = 'id,url,title,content_review,publish_date,content,source'
    defaults = {'publish_date': None, 'id': 0}
    main(properties, defaults)
