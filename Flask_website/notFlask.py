class NotFlask():
    def __init__(self):
        self.routes = []

    # Here's our build_route_pattern we made earlier
    @staticmethod
    def build_route_pattern(route):
        route_regex = re.sub(r'(<\w+>)', r'(?P\1.+)', route)
        return re.compile("^{}$".format(route_regex))

    def route(self, route_str):
        def decorator(f):
            # Instead of inserting into a dictionary,
            # We'll append the tuple to our route list
            route_pattern = self.build_route_pattern(route_str)
            self.routes.append((route_pattern, f))

            return f

        return decorator

    def get_route_match(path):
    for route_pattern, view_function in self.routes:
        m = route_pattern.match(path)
        if m:
           return m.groupdict(), view_function

    return None
