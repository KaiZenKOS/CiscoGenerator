class ConfigGenerator:
    """Classe pour générer la configuration Cisco basée sur les données fournies."""

    def __init__(self, device):
        """Initialise le générateur avec les informations de l'appareil."""
        self.device = device

    def generate_banner_config(self):
        """Génère la configuration de la bannière."""
        banner = self.device.get('banner', '')
        return f'banner motd #{banner}#'

    def generate_line_password_config(self):
        """Génère la configuration des mots de passe des lignes."""
        line_password = self.device.get('line_password', '')
        return f'''
line con 0
 password {line_password}
 login
line vty 0 4
 password {line_password}
 login
'''

    def generate_stp_config(self):
        """Génère la configuration STP."""
        stp_mode = self.device.get('stp_mode', '')
        stp_priorities = self.device.get('stp_priorities', {})
        if not stp_mode:
            return ''
        stp_config_str = f'spanning-tree mode {stp_mode}\n'
        for vlan_id, priority in stp_priorities.items():
            stp_config_str += f'spanning-tree vlan {vlan_id} priority {priority}\n'
        return stp_config_str

    def generate_vlan_config(self):
        """Génère la configuration des VLANs."""
        vlans = self.device.get('vlans', [])
        vlan_config_str = ''
        for vlan in vlans:
            vlan_config_str += f'''
vlan {vlan['id']}
 name {vlan['name']}
'''
        return vlan_config_str

    def generate_interface_configs(self):
        """Génère la configuration des interfaces."""
        interfaces = self.device.get('interfaces', [])
        interface_config_str = ''
        for interface in interfaces:
            interface_config_str += f'''
interface {interface['name']}
 description {interface['description']}
'''
            if 'ip_address' in interface and 'subnet_mask' in interface:
                interface_config_str += f' ip address {interface["ip_address"]} {interface["subnet_mask"]}\n'
            if interface.get('mode') == 'access':
                interface_config_str += f'''
 switchport mode access
 switchport access vlan {interface['access_vlan']}
 spanning-tree portfast
'''
            elif interface.get('mode') == 'trunk':
                interface_config_str += f'''
 switchport mode trunk
 switchport trunk allowed vlan {interface['allowed_vlans']}
'''
            interface_config_str += ' no shutdown\n'
        return interface_config_str

    def generate_routing_config(self):
        """Génère la configuration du routage."""
        routing = self.device.get('routing', False)
        routing_protocols = self.device.get('routing_protocols', [])
        if not routing:
            return ''
        routing_config_str = 'ip routing\n'
        for protocol in routing_protocols:
            if protocol['protocol'] == 'ospf':
                routing_config_str += f'router ospf {protocol["process_id"]}\n'
                for network in protocol['networks']:
                    routing_config_str += f' network {network["network"]} {network["wildcard"]} area {network["area"]}\n'
        return routing_config_str

    def generate_acl_config(self):
        """Génère la configuration des ACLs."""
        acls = self.device.get('acls', [])
        acl_config_str = ''
        for acl in acls:
            for entry in acl['entries']:
                acl_config_str += f'access-list {acl["number"]} {entry["action"]} {entry["protocol"]} {entry["source"]} {entry["destination"]}\n'
        return acl_config_str

    def generate_configuration(self):
        """Génère la configuration complète."""
        config_template = '''
hostname {hostname}
!
{banner_config}
!
enable secret {enable_secret}
!
{line_password_config}
!
{stp_config}
!
{vlan_config}
!
{interface_configs}
!
{routing_config}
!
{acl_config}
'''
        config = config_template.format(
            hostname=self.device.get('hostname', 'Device'),
            banner_config=self.generate_banner_config(),
            enable_secret=self.device.get('enable_secret', 'cisco'),
            line_password_config=self.generate_line_password_config(),
            stp_config=self.generate_stp_config(),
            vlan_config=self.generate_vlan_config(),
            interface_configs=self.generate_interface_configs(),
            routing_config=self.generate_routing_config(),
            acl_config=self.generate_acl_config()
        )
        return config
