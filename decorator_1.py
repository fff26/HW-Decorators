import datetime
import os


def logger(old_function):

    def new_function(*args, **kwargs):
        now = datetime.datetime.now()
        name = old_function.__name__
        args_str = ', '.join(map(str, args))
        kwargs_str = ', '.join(f'{k}={v}' for k, v in kwargs.items())
        arguments = ', '.join([args_str, kwargs_str]) if args_str and kwargs_str else args_str or kwargs_str

        with open('main.log', 'a') as f:
            f.write(f'{now} - {name} - {arguments}\n')

        result = old_function(*args, **kwargs)
        
        with open('main.log', 'a') as f:
            f.write(f'Result: {result}\n')

        return result

    return new_function

def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world()
    result = summator(2, 2)
    assert isinstance(result, int)
    assert result == 4
    result = div(6, 2)
    assert result == 3
    
    assert os.path.exists(path)

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content


if __name__ == '__main__':
    test_1()