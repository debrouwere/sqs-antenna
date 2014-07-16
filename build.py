import inspect
import antenna

with open('README', 'w') as readme:
    docs = inspect.getdoc(antenna)
    readme.write(docs)