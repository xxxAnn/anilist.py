class Scheme:
    def __init__(self, t=None):
        self._layers = []

    def __getattr__(self, k):
        self._layers.append(k)
        return self
    
def construct_query(schs: list[Scheme]):
    temp = {}

    for sch in schs:
        sch = sch._layers
        if not sch[0] in temp:
            temp[sch[0]] = {}
        for i in range(1, len(sch)):
            if not sch[i] in get_nest_list(get_numbers_up_to(i), temp, i, sch):
                get_nest_list(get_numbers_up_to(i), temp, i, sch)[sch[i]] = {}
    
    return temp

def construct_query_as_string(d, ss=""):
    print(d)
    if type(d) != dict:
        return str(d)
    s = ""
    for k, v in d.items():
        if v == {}:
            s = f"{s}{ss}{k}\n"
        else:
            t = construct_query_as_string(v, f'{ss}  ')
            t = t[0:-1]
            s = f"{s}{ss}{k} {{\n{t}\n{ss}}}\n"
    
    return s

def get_numbers_up_to(i):
    l = []
    n = i
    while n > 0:
        l.append(n)
        n -= 1
    
    return l

def get_nest_list(n, l, m, sch):
    prev = l
    for i in n:
        prev = prev[sch[m-i]]
    return prev
    
    # a b e
    # a d v
class MediaScheme(Scheme):
    def __init__(self):
        super().__init__(None)
        self._layers.append("media")