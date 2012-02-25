from fabric.api import *

ROOT_PATH = '.'
DEPLOY_PATH = './deploy'
# REPO used for synchronisation between development workstations
REPO = '/home/hubert/Entwicklung/hyde/opa'
# PROD production releases go here
PROD = '/var/www/opa'
# We use UNISON primary to be able to sync REPO and because it works on Windows boxes
UFLAGS = "-batch -perms 0"
env.hosts = ['netbeer.org']
user = 'hubert'

REMOTE = "ssh://{0}@{1}/".format(user, env.hosts[0])

def list():
    run('ls -al {0} {1}'.format(REPO, PROD))
    local('ls -al', capture = False)

def clean():
    local('rm -rf ./deploy')

def regen():
    clean()
    local('hyde.py -g -s .')

def serve():
    local('hyde.py -w -p 8000 -s .')

def reserve():
    regen()
    serve()

def commit():
    local('unison {source} {dest} -force {source} {uflags}'.format(
            source = ROOT_PATH,
            dest = REMOTE + REPO,
            uflags = UFLAGS),
        capture = False)

def checkout():
    local('unison {source} {dest} -force {source} {uflags}'.format(
            source = REMOTE + REPO,
            dest = ROOT_PATH,
            uflags = UFLAGS),
        capture = False)

def sync():
    local('unison {source} {dest} {uflags}'.format(
            source = ROOT_PATH,
            dest = REMOTE + REPO,
            uflags = UFLAGS),
        capture = False)

def publish():
    local('unison {source} {dest} -force {source} {uflags}'.format(
            source = DEPLOY_PATH,
            dest = REMOTE + PROD,
            uflags = UFLAGS),
        capture = False)