""" Various setup
"""
try:
    import Products.LDAPUserFolder
except ImportError:
    LDAP_INSTALLED = False
else:
    LDAP_INSTALLED = True


def setupVarious(context):
    """ Do some various setup.
    """
    if context.readDataFile('eeaplonebuildout.txt') is None:
        return

    # LDAP support is not available
    if not LDAP_INSTALLED:
        return

    # Setup eionet ldap user authentication
    acl_users = context.getSite().acl_users
    acl_users.manage_addProduct['LDAPMultiPlugins'].manage_addLDAPMultiPlugin(
        id='EIONETLDAP',
        title='EIONET LDAP',
        LDAP_server='ldap2.eionet.europa.eu',
        login_attr='uid',
        uid_attr='uid',
        users_base="ou=Users,o=EIONET,l=Europe",
        users_scope=2,
        roles=["Anonymous"],
        groups_base="ou=groups,o=EIONET,l=Europe",
        groups_scope=2,
        binduid='',
        bindpwd="",
        binduid_usage=0,
        rdn_attr='uid',
        local_groups=1,
        use_ssl=0,
        encryption='SHA',
        read_only=0,
        REQUEST=None
    )

    luf = acl_users['EIONETLDAP']['acl_users']
    luf.manage_deleteServers([0])
    luf.manage_addServer('ldap2.eionet.europa.eu', op_timeout=10)
    luf.manage_addServer('ldap3.eionet.europa.eu', op_timeout=10)
    luf.setSchemaConfig(
                           { 'cn' : { 'ldap_name' : 'cn'
                                    , 'friendly_name' : 'Full Name'
                                    , 'multivalued' : False
                                    , 'public_name' : 'fullname'
                                    , 'binary' : False
                                    }
                           , 'sn' : { 'ldap_name' : 'sn'
                                    , 'friendly_name' : 'Last Name'
                                    , 'multivalued' : False
                                    , 'public_name' : ''
                                    , 'binary' : False
                                    }
                           , 'mail' : { 'ldap_name' : 'mail'
                                    , 'friendly_name' : 'email'
                                    , 'multivalued' : False
                                    , 'public_name' : 'email'
                                    , 'binary' : False
                                    }
                           , 'uid' : { 'ldap_name' : 'uid'
                                    , 'friendly_name' : 'uid'
                                    , 'multivalued' : False
                                    , 'public_name' : ''
                                    , 'binary' : False
                                    }
                           }
    )

    acl_users['EIONETLDAP'].manage_activateInterfaces([
                                    'IAuthenticationPlugin',
                                    'IPropertiesPlugin',
                                    'IUserEnumerationPlugin'])
