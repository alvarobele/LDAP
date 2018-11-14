import getpass, ldap3, sys
from ldap3 import Server, Connection, ALL

# Tratamiento de los ficheros de configuración
with open('conf.csv', 'r') as conf:
    cfg = conf.readlines()

with open('usuarios.csv', 'r') as f:
    fich_us = f.readlines()

with open('equipos.csv', 'r') as e:
    fich_eq = e.readlines()

# Quitamos la primera línea de los ficheros
cfg.pop(0)
fich_us.pop(0)
fich_eq.pop(0)

dom = cfg[0].strip('\n').split(':')[0]
uid = int(cfg[0].strip('\n').split(':')[1])
gid = int(cfg[0].strip('\n').split(':')[2])
cont = 0

server = Server(cfg[0].strip('\n').split(':')[3])

user = input('Usuario: ')
pwd = getpass.getpass('Contraseña: ')

# Se intenta establecer conexión. Si falla, salta una excepción.
try:
    c = Connection(server, 'cn={},{}'.format(user, dom), pwd, auto_bind = True, raise_exceptions = True)
except ldap3.core.exceptions.LDAPInvalidCredentialsResult:
	print('No se pudo llevar a cabo la conexión: Credenciales incorrectas.')
	sys.exit(1)

# Tratamiento del fichero de usuarios
usuarios = []

for i in fich_us:
    usuarios.append(i.strip('\n').split(':'))

# Añadimos los usuarios
for i in usuarios:
    print('Añadiendo al usuario {}...'.format(i[3]))

    c.add('uid={},ou=People,{}'.format(i[3], dom),
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

# Tratamiento del fichero de equipos
equipos = []

for i in fich_eq:
    equipos.append(i.strip('\n').split(':'))

# Añadimos los equipos
for i in equipos:
    print('Añadiendo el equipo con IP {}'.format(i[1]))

    c.add('uid={},ou=Equipos,{}'.format(i[1], dom),
           attributes = {'objectClass': ['top',
                                        'device',
                                        'ipHost',
                                        'ldapPublicKey'],
                         'cn': i[0],
                         'ipHostNumber': i[1],
                         'sshPublicKey': i[2]})
    cont +=1

c.unbind()

if cont == 1:
    print('Añadido 1 registro')
else:
    print('Añadidos {} registros'.format(cont))
