def test_decorator(fn):
    print('------')
    def wrapper(*args, **kwargs):
        print(args)
        print(kwargs)
        fn(*args, **kwargs)
    return wrapper


@test_decorator
def test_function(a, b, c=1, d=2):
    return (a, b, c, d)


print(test_function(1, 2))




# account not exist


# account exist
# user exist
# user password correct



###### can we pass arguments to decorator?