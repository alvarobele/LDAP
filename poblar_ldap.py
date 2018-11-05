import getpass
from ldap3 import Server, Connection, ALL

dom = 'dc=gonzalonazareno,dc=org'

server = Server('172.22.200.121')

user = input('Usuario: ')
pwd = getpass.getpass('Contraseña: ')

c = Connection(server, 'cn={},{}'.format(user, dom))