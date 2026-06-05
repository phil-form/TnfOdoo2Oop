def argsFunction(*args):
    print(args)
    for a in args:
        print(a)

argsFunction("coucou", "tu", "vas", "bien?")

def kwargsFunction(**kwargs):
    print(kwargs)

kwargsFunction(test="coucou", tu="tu", vas="vas", bienm="bien?")

def findBy(**kwargs):
    query = f"SELECT * FROM table WHERE "
    for k,v in kwargs.items():
        query += f"{k} = {v} "
    print(query)

findBy(test="1234", userid = 5)

def my_function(test="testdefault", userid=0, username="usernamedefault"):
    print(test, userid, username)

my_function("testval", 1, "usrename")

my_function(userid=5, username="test")
my_function(userid=5, username="test", test="new test val")

def ex_print(*args, sep=" ", end="\n"):
    print(sep=sep, end=end, *args)

