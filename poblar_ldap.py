import getpass
from ldap3 import Server, Connection, ALL

dom = 'dc=gonzalonazareno,dc=org'

server = Server('172.22.200.121')

user = input('Usuario: ')
pwd = getpass.getpass('Contraseña: ')

c = Connection(server, 'cn={},{}'.format(user, dom), pwd, auto_bind = True)

with open('../usuarios.csv', 'r') as f:
	fichero = f.readlines()

usuarios = []
fichero.pop(0)

for i in fichero:
	usuarios.append(i.strip('\n').split(':'))

for i in usuarios:
	c.add('uid={},ou=People,dc=gonzalonazareno,dc=org'.format(i[3]), \
		  attributes = {'objectClass': ['top', 'posixAccount', 'inetOrgPerson', 'ldapPublicKey'],\
		  'givenName': i[0], 'sn': i[1], 'cn': '{} {}'.format(i[0], i[1]), \
	 	  'uid': i[3], 'mail': i[2], 'uidNumber': str(2000), 'gidNumber': str(2000), \
	  	  'homeDirectory': '/home/{}'.format(i[3]), 'loginShell': '/bin/bash', \
	  	  'sshPublicKey': i[4]})
	c.unbind()