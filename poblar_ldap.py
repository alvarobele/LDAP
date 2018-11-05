import getpass, ldap3
from ldap3 import Server, Connection, ALL

dom = 'dc=gonzalonazareno,dc=org'

server = Server('172.22.200.121')

user = input('Usuario: ')
pwd = getpass.getpass('Contraseña: ')

with open('../usuarios.csv', 'r') as f:
	fichero = f.readlines()

usuarios = []
fichero.pop(0)

for i in fichero:
	usuarios.append(i.strip('\n').split(':'))

try:
	for i in usuarios:
		c = Connection(server, 'cn={},{}'.format(user, dom), pwd, auto_bind = True, raise_exceptions = True)
		nombre = i[0]
		apellidos = i[1]
		if all(ord(char) < 128 for char in nombre):
			nombre = nombre
		else:
			nombre = str(base64.b64encode(nombre.encode())).lstrip("b'").rstrip("'")
		c.add('uid={},ou=People,dc=gonzalonazareno,dc=org'.format(i[3]), \
		  attributes = {'objectClass': ['top', 'posixAccount', 'inetOrgPerson', 'ldapPublicKey'],\
		  'givenName': nombre, 'sn': apellidos, 'cn': '{} {}'.format(nombre, apellidos), \
	 	  'uid': i[3], 'mail': i[2], 'uidNumber': str(2000), 'gidNumber': str(2000), \
	  	  'homeDirectory': '/home/{}'.format(i[3]), 'loginShell': '/bin/bash', \
	  	  'sshPublicKey': i[4]})
		c.unbind()
except ldap3.core.exceptions.LDAPInvalidCredentialsResult:
	print('No se pudo llevar a cabo la conexión: Credenciales incorrectas.')