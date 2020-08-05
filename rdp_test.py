# recusive decent json parser test

import json



# from https://stackoverflow.com/questions/12507206/how-to-completely-traverse-a-complex-dictionary-of-unknown-depth
def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]



def dict_generator_w_num(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value,  pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for k,v in enumerate(value):
                    for d in dict_generator(v, pre + [key] + [k]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield indict




# json_test = "u'body': [{u'declarations': [{u'id': {u'name': u'i',
#                                        u'type': u'Identifier'},
#                                u'init': {u'type': u'Literal', u'value': 2},
#                                u'type': u'VariableDeclarator'}],
#             u'kind': u'var',
#             u'type': u'VariableDeclaration'},
#            {u'declarations': [{u'id': {u'name': u'j',
#                                        u'type': u'Identifier'},
#                                u'init': {u'type': u'Literal', u'value': 4},
#                                u'type': u'VariableDeclarator'}],
#             u'kind': u'var',
#             u'type': u'VariableDeclaration'},
#            {u'declarations': [{u'id': {u'name': u'answer',
#                                        u'type': u'Identifier'},
#                                u'init': {u'left': {u'name': u'i',
#                                                    u'type': u'Identifier'},
#                                          u'operator': u'*',
#                                          u'right': {u'name': u'j',
#                                                     u'type': u'Identifier'},
#                                          u'type': u'BinaryExpression'},
#                                u'type': u'VariableDeclarator'}],
#             u'kind': u'var',
#             u'type': u'VariableDeclaration'}],
#  u'type': u'Program'}"
 

x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}
#for result in dict_generator(x):
#    print(result)
x =  '{ "name":"John", "age":30, "city":"New York"}'
y = json.loads(x)
# print(mydict)
print('y[name] =',y['name'])