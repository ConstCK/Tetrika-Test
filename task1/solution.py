def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        exception_msg = 'Аргумент {} должен быть {} а не {}'

        for n, i in enumerate(args):
            if list(annotations.values())[n] and not isinstance(i, list(annotations.values())[n]):
                raise TypeError(
                    exception_msg.format(
                        list(annotations.keys())[n],
                        list(annotations.values())[n].__name__,
                        type(i).__name__
                    )
                )

        for k, v in kwargs.items():
            if annotations.get(k) and not isinstance(v, annotations.get(k)):
                raise TypeError(
                    exception_msg.format(
                        k,
                        annotations.get(k).__name__,
                        type(v).__name__
                    )
                )
        return func(*args, **kwargs)

    return wrapper


