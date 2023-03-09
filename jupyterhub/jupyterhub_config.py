# Configuration file for Jupyter Hub
import os
import sys

c = get_config()

import logging
logging.basicConfig(level=logging.INFO)
#logging.debug("Example message")


c.Application.log_level = 'INFO'

c.Notebook.log_level = 'INFO'
c.SingleUserLabApp.log_level = 'INFO'

# Set the log level by value or name.
# c.JupyterHub.log_level = 'DEBUG'

# Enable debug-logging of the single-user server
# c.Spawner.debug = True

# Enable debug-logging of the single-user server
# c.DockerSpawner.debug = True

# Spawn with Docker
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Keep the spawn limit low
# c.JupyterHub.concurrent_spawn_limit = 20

# Spawn containers from this image
c.DockerSpawner.image = os.environ['DOCKER_SINGLEUSER_IMAGE']
c.DockerSpawner.prefix = 'jupyterhub-user'
# c.DockerSpawner.container_name="jupyterhub-user-{username}"
c.DockerSpawner.extra_create_kwargs = {'user': 'root'}
c.DockerSpawner.environment = {
  'GRANT_SUDO': '1',
  'UID': '0', # workaround https://github.com/jupyter/docker-stacks/pull/420
}

# c.JupyterHub.base_url='/jupyterhub'

# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
c.DockerSpawner.extra_create_kwargs.update({ 'command': "start-singleuser.sh --SingleUserNotebookApp.default_url=/lab" })
#c.DockerSpawner.extra_create_kwargs.update({ 'command': "start-singleuser.sh --log-level='INFO' --SingleUserNotebookApp.default_url=/lab" })
# Redirect to JupyterLab, instead of the plain Jupyter notebook
# It seems it is required in case the start-singleuser command before doesn't include the default_url configuration
# c.Spawner.default_url = '/lab'

# Connect containers to this Docker network
# network_name = 'jupyter_network'
network_name = os.environ['DOCKER_NETWORK_NAME']
logging.debug("Using network " + network_name)
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
# notebook_dir = '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
# Stored in /var/lib/docker/volumes/jupyterhub-shared or jupyterhub-user-{username}
c.DockerSpawner.volumes = { 
    'jupyterhub-user-{username}': notebook_dir, 
    'jupyterhub-shared': {"bind": '/home/jovyan/shared', "mode": "ro"}
}

# STATUS: NOT WORKING WHAT IS INCLUDED BELOW
# TODO: Try to set /root/project/shared/jupyterhub-user-{username}
# todo: otherwise it seems that things are stored under /var/lib/docker/volumes/jupyterhub-shared or jupyterhub-user-whatever
# c.DockerSpawner.volumes = { 
#     os.path.join('/root/project/shared', 'jupyterhub-user-{username}'): notebook_dir, 
#     os.path.join('/root/project/shared', 'jupyterhub-shared'): {"bind": '/home/jovyan/shared', "mode": "rw"}
# }
# def create_dir_hook(spawner):
#     """ Create directory """
#     username = spawner.user.name  # get the username
#     volume_path = os.path.join('/root/project/shared', 'jupyterhub-user-', username)
#     if not os.path.exists(volume_path):
#         os.makedirs(volume_path, mode=0o755, exist_ok = True)
# c.DockerSpawner.pre_spawn_hook = create_dir_hook


# There is an option to define volumes for read-only use. 
# You can also use the way above by setting "r"
# c.DockerSpawner.read_only_volumes = {}

# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = False
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# The docker instances need access to the Hub, so the default loopback port doesn't work:
# from jupyter_client.localinterfaces import public_ips
# c.JupyterHub.hub_ip = public_ips()[0]
# c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# IP Configurations
# The public facing IP of the whole JupyterHub application (specifically referred to as the proxy).
c.JupyterHub.ip = '0.0.0.0'
# The public facing port of the proxy.
c.JupyterHub.port = 8000
# The public facing URL of the whole JupyterHub application. This is the address on which the proxy will bind
c.JupyterHub.bind_url = 'http://127.0.0.1:8000'

# Other stuff
c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '2G'

c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m", "jupyterhub_idle_culler",
            "--timeout=3600",
        ],
        # "admin": True,
    },
    # {
    #     "name": "notebook", 
    #     'url': '/hub'
    # },
    # {
    #     "name": "admin-service",
    #     "api_token": "my-token",
    # }
]

c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
            # "admin:users", # if using --cull-users
        ],
        # assignment of role's permissions to:
        "services": ["jupyterhub-idle-culler-service"],
    },
    # {
    #     'name': 'server',
    #     'scopes': [
    #         'servers',
    #         'users:activity',
    #         'read:users:name',
    #         'read:servers',
    #         'delete:servers'
    #     ],
    #     'services': ['notebook']
    # },
    # {
    #     "name": "admin-service-role",
    #     "scopes": [
    #         # specify the permissions the token should have
    #         "admin:users",
    #         "admin-ui",
    #         "admin:servers",
    #         "proxy"
    #     ],
    #     "services": [
    #         # assign the service the above permissions
    #         "admin-service",
    #     ],
    # }
]

# Read userlist file to get allowed and admin users
# File format
# user1 admin
# user2 admin
# user3
# user4
whitelist = set()
admin = set()
try:
    here = os.path.dirname(__file__)
    with open(os.path.join(os.path.dirname(__file__), 'userlist')) as f:
        for line in f:
            if not line:
                continue
            parts = line.split()
            name = parts[0]
            whitelist.add(name)
            if len(parts) > 1 and parts[1] == 'admin':
                admin.add(name)
except FileNotFoundError:
    logging.info("File userlist not found. Not applying access restrictions.")


# whitelist = set()
# admin = set()

c.Authenticator.blocked_users = {'root'}
c.Authenticator.allowed_users = whitelist
c.Authenticator.admin_users = admin

# https://github.com/jupyterhub/nativeauthenticator
# https://native-authenticator.readthedocs.io/en/stable/
if (os.environ['AUTH_MODE'].lower() == 'native'):
    import nativeauthenticator
    c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
    c.JupyterHub.template_paths = [f"{os.path.dirname(nativeauthenticator.__file__)}/templates/"]

    # Make sure nobody can create an account with the name root or login as root
    # c.Authenticator.blocked_users = {'root'}
    # c.Authenticator.allowed_users = whitelist
    # c.Authenticator.admin_users = admin

    # Password Strength
    c.NativeAuthenticator.check_common_password = False
    c.NativeAuthenticator.minimum_password_length = 10
    # Block users after failed logins
    c.NativeAuthenticator.allowed_failed_logins = 3
    c.NativeAuthenticator.seconds_before_next_try = 600
    # Disable SignUp
    # !IMPORTANT: If no account was created, it is impossible to register new accounts
    # c.NativeAuthenticator.enable_signup = False

    # ! IMPORTANT: 
    # Request additional user information
    # TODO: still to be checked to include mail address
    c.NativeAuthenticator.ask_email_on_signup = True

    # Add two factor authentication obligatory for users
    c.NativeAuthenticator.allow_2fa = True

# https://github.com/jupyterhub/ldapauthenticator
if (os.environ['AUTH_MODE'].lower() == 'ldap'):
    # TODO: This is another option, but seems to be not updated
    # https://github.com/hansohn/jupyterhub-ldap-authenticator

    c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
    c.LDAPAuthenticator.log_level = 'DEBUG'
    c.LDAPAuthenticator.server_address = os.environ['LDAP_server_address']
    c.LDAPAuthenticator.use_ssl = True
    c.LDAPAuthenticator.server_port = int(os.environ['LDAP_server_port'])

    # LDAP not bind
    c.LDAPAuthenticator.lookup_dn = False
    # c.LDAPAuthenticator.bind_dn_template = [
    #     'CN={username},CN=Users,DC=alumnos,DC=unican,DC=es',
    #     'CN={username},OU=Cuentas Servicios,DC=alumnos,DC=unican,DC=es',
    # ]
    c.LDAPAuthenticator.bind_dn_template = os.environ['LDAP_bind_dn_template'].split(';')
    c.LDAPAuthenticator.valid_username_regex = '^[a-zA-Z][.a-zA-Z0-9_-]*$'
    c.LDAPAuthenticator.escape_userdn = False

    # Make sure nobody can create an account with the name root or login as root
    # c.Authenticator.blocked_users = {'root'}
    # c.Authenticator.allowed_users = whitelist
    # c.Authenticator.admin_users = admin

    # LDAP Bind
    # c.LDAPAuthenticator.lookup_dn = True
    # c.LDAPAuthenticator.lookup_dn_search_user = os.environ['LDAP_lookup_dn_search_user']
    # c.LDAPAuthenticator.lookup_dn_search_password = os.environ['LDAP_lookup_dn_search_password']

    # logging.debug(c.LDAPAuthenticator.lookup_dn_search_password)

    # c.LDAPAuthenticator.lookup_dn_search_filter = '(&(objectclass=user)(sAMAccountName={login}))'
    # #c.LDAPAuthenticator.lookup_dn_search_filter = '({login_attr}={login})'

    # logging.debug(c.LDAPAuthenticator.lookup_dn_search_filter)

    # # Active directory
    # c.LDAPAuthenticator.user_attribute = 'sAMAccountName'
    # c.LDAPAuthenticator.lookup_dn_user_dn_attribute = 'cn'
    # c.LDAPAuthenticator.bind_dn_template = '{username}'
    # c.LDAPAuthenticator.user_search_base = 'OU=Cuentas Servicios,DC=alumnos,DC=unican,DC=es'
    # c.LDAPAuthenticator.user_search_base = 'CN=Users,DC=alumnos,DC=unican,DC=es'
    # c.LDAPAuthenticator.escape_userdn = False
    # c.LDAPAuthenticator.valid_username_regex = '^[a-zA-Z][.a-zA-Z0-9_-]*$'


if (os.environ['AUTH_MODE'].lower() == 'lti'):
    # /hub/lti/launch
    c.JupyterHub.authenticator_class = "ltiauthenticator.LTIAuthenticator"
    # Add the LTI 1.1 consumer key and shared secret. Note the use of
    # `LTI11Authenticator` vs the legacy `LTIAuthenticator`.
    # c.LTI11Authenticator.consumers = {
    c.LTI11Authenticator.consumers = {
        os.environ["LTI_CLIENT_KEY"]: os.environ["LTI_SHARED_SECRET"]
    }

    # Use an LTI 1.1 parameter to set the username.
    # c.LTIAuthenticator.username_key = "lis_person_name_full"
    # Set the user's email as their user id
    c.LTI11Authenticator.username_key = os.environ["LTI_USERNAME_KEY"]
    
