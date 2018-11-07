import getpass, ldap3, sys
from ldap3 import Server, Connection, ALL

# Tratamiento del fichero de configuración 
with open('../conf.csv', 'r') as conf:
    cfg = conf.readlines()

cfg.pop(0)

dom = cfg[0].strip('\n').split(':')[0]
uid = int(cfg[0].strip('\n').split(':')[1])
gid = int(cfg[0].strip('\n').split(':')[2])
cont = 0

server = Server(cfg[0].strip('\n').split(':')[3])

user = input('Usuario: ')
pwd = getpass.getpass('Contraseña: ')

with open('../usuarios.csv', 'r') as f:
    fichero = f.readlines()

usuarios = []
fichero.pop(0)

try:
    c = Connection(server, 'cn={},{}'.format(user, dom), pwd, auto_bind = True, raise_exceptions = True)
except ldap3.core.exceptions.LDAPInvalidCredentialsResult:
	print('No se pudo llevar a cabo la conexión: Credenciales incorrectas.')
	sys.exit(1)

# Tratamiento del fichero de usuarios
for i in fichero:
    usuarios.append(i.strip('\n').split(':'))

for i in usuarios:
    print('Añadiendo al usuario {}...'.format(i[3]))

    c.add('uid={},ou=People,dc=gonzalonazareno,dc=org'.format(i[3]),
            attributes = {'objectClass': ['top',
                                        'posixAccount',
                                        'inetOrgPerson',
                                        'ldapPublicKey'],
                        'givenName': i[0],
                        'sn': i[1],
                        'cn': '{} {}'.format(i[0], i[1]),
                        'uid': i[3],
                        'mail': i[2],
                        'uidNumber': str(uid),
                        'gidNumber': str(gid),
                        'homeDirectory': '/home/{}'.format(i[3]),
                        'loginShell': '/bin/bash',
                        'sshPublicKey': str(i[4])})

    uid += 1
    cont += 1

c.unbind()

if cont == 1:
    print('Añadido 1 registro')
else:
    print('Añadidos {} registros'.format(cont))
