import sys, os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hyper_resource_py.settings") # HARDCODED
django.setup()

from user_management.models import HyperUser, HyperUserGroup

NO_COMMAND_ERROR_MESSAGE = """
command:
    createadmingroup
    createsuperuser
"""

def prepare_create_super_user_command():
    user_name = input("User name: ")
    password = input("Password: ")

    #try:
    create_super_user(user_name, password)
    return True
    #except:
    #    return False

def prepare_create_group_command():
    try:
        name = input("Group name: ")
        read = bool(input("Read permission? [ True | False ]: "))
        create = bool(input("Read permission? [ True | False ]: "))
        update = bool(input("Read permission? [ True | False ]: "))
        delete = bool(input("Read permission? [ True | False ]: "))
        create_group(name, read, create, update, delete)
        return True
    except:
        return False

def prepare_create_admin_group():
    #try:
    create_admin_group( input("Admin group name: ") )
    #except:
    #    return False

COMMAND_LINE_INTERFACE_OPERATIONS = {
    "createsuperuser": prepare_create_super_user_command,
    "creategroup": prepare_create_group_command,
    "createadmingroup": prepare_create_admin_group
}

def create_super_user(user_name, password, name='', email=None, description='', avatar='', active=True, boss=None, group=1):
    HyperUser.objects.create(**{
        "user_name": user_name,
        "password": password,
        "name": name,
        "email": email,
        "description": description,
        "avatar": avatar,
        "active": active,
        "boss": boss,
        "group": HyperUserGroup.objects.get(pk=group),
    })

def create_admin_group(name):
    HyperUserGroup.objects.create(**{
        "type": 1,
        "name": name,
        "read": True,
        "create": True,
        "update": True,
        "delete": True,
    })

def create_group(name, read=True, create=False, update=False, delete=False):
    HyperUserGroup.objects.create()

def main(argv):

    size_of_arguments = len(argv)
    if size_of_arguments < 2:
        print('Usage: python hyper_config.py <command>')
        print(NO_COMMAND_ERROR_MESSAGE)
        exit()
    #else:
    #    print('-------------------------------------------------------------------------------------------------------')
    #    print('Changing models.py and generating files: urls.py,views.py, serializers.py e contexts.py')
    #    print('-------------------------------------------------------------------------------------------------------')

    command = argv[1]
    result = COMMAND_LINE_INTERFACE_OPERATIONS[command]()
    if result:
        print("Success")
    else:
        print("Error")

    #if size_of_arguments > 3:
    #    has_to_generate_views = ast.literal_eval(argv[3])


if __name__ == "__main__":
    main(sys.argv)