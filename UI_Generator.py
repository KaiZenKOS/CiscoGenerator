import os
import datetime
import customtkinter as ctk
from tkinter import messagebox, simpledialog
import ConfigGenerator


class ConfigApp:
    """Classe principale pour l'application de génération de configuration Cisco."""

    def __init__(self):
        """Initialise l'interface utilisateur et les variables."""
        ctk.set_appearance_mode("System")  # Thème clair, sombre ou système
        ctk.set_default_color_theme("blue")  # Thème de couleur : blue, green, dark-blue

        self.root = ctk.CTk()
        self.root.title("Générateur de Configuration Cisco")
        self.root.geometry("1000x700")
        self.initialize_variables()
        self.create_widgets()
        self.root.mainloop()

    def initialize_variables(self):
        """Initialise les variables de l'application."""
        self.device = {}
        self.vlan_list = []
        self.interface_list = []
        self.routing_protocols = []
        self.acls = []

    def create_widgets(self):
        """Crée les widgets principaux de l'interface utilisateur."""
        # Création des onglets
        self.notebook = ctk.CTkTabview(self.root, width=1000, height=700)
        self.notebook.pack(expand=True, fill="both")

        # Création des onglets
        self.notebook.add("Informations Appareil")
        self.notebook.add("VLANs")
        self.notebook.add("Interfaces")
        self.notebook.add("Routage")
        self.notebook.add("ACLs")

        self.create_device_info_tab()
        self.create_vlans_tab()
        self.create_interfaces_tab()
        self.create_routing_tab()
        self.create_acls_tab()

        # Boutons de génération et de sortie
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)

        generate_button = ctk.CTkButton(button_frame, text="Générer la configuration", command=self.generate_configuration)
        generate_button.pack(side="left", padx=10)

        quit_button = ctk.CTkButton(button_frame, text="Quitter", command=self.root.quit)
        quit_button.pack(side="left", padx=10)

    def create_device_info_tab(self):
        """Crée l'onglet pour les informations de l'appareil."""
        frame = self.notebook.tab("Informations Appareil")

        ctk.CTkLabel(frame, text="Nom d'hôte:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.hostname_entry = ctk.CTkEntry(frame, placeholder_text="Entrez le nom d'hôte")
        self.hostname_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Bannière:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.banner_entry = ctk.CTkEntry(frame, placeholder_text="Entrez une bannière")
        self.banner_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Enable Secret:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.enable_secret_entry = ctk.CTkEntry(frame, placeholder_text="Entrez le secret", show="*")
        self.enable_secret_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Mot de passe des lignes:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.line_password_entry = ctk.CTkEntry(frame, placeholder_text="Entrez le mot de passe", show="*")
        self.line_password_entry.grid(row=3, column=1, padx=10, pady=5)

    def create_vlans_tab(self):
        """Crée l'onglet pour gérer les VLANs."""
        frame = self.notebook.tab("VLANs")
        ctk.CTkLabel(frame, text="Liste des VLANs configurés").pack(pady=10)

        self.vlan_listbox = ctk.CTkTextbox(frame, width=600, height=300)
        self.vlan_listbox.pack(pady=5)

        add_vlan_button = ctk.CTkButton(frame, text="Ajouter VLAN", command=self.add_vlan)
        add_vlan_button.pack(pady=5)

    def add_vlan(self):
        """Ajoute un VLAN."""
        vlan_id = simpledialog.askinteger("ID VLAN", "Entrez l'ID VLAN:", parent=self.root)
        vlan_name = simpledialog.askstring("Nom VLAN", "Entrez un nom de VLAN:", parent=self.root)
        if vlan_id and vlan_name:
            self.vlan_list.append({"id": vlan_id, "name": vlan_name})
            self.vlan_listbox.insert("end", f"VLAN {vlan_id}: {vlan_name}\n")

    def create_interfaces_tab(self):
        """Crée l'onglet pour gérer les interfaces."""
        frame = self.notebook.tab("Interfaces")
        ctk.CTkLabel(frame, text="Liste des interfaces configurées").pack(pady=10)

        self.interface_listbox = ctk.CTkTextbox(frame, width=600, height=300)
        self.interface_listbox.pack(pady=5)

        add_interface_button = ctk.CTkButton(frame, text="Ajouter Interface", command=self.add_interface)
        add_interface_button.pack(pady=5)

    def add_interface(self):
        """Ajoute une interface."""
        interface_name = simpledialog.askstring("Nom Interface", "Entrez le nom de l'interface (ex. GigabitEthernet0/1):", parent=self.root)
        description = simpledialog.askstring("Description", "Entrez une description pour l'interface:", parent=self.root)
        mode = simpledialog.askstring("Mode", "Entrez le mode (access/trunk/routed):", parent=self.root)
        interface = {"name": interface_name, "description": description, "mode": mode}

        if mode == "access":
            vlan_id = simpledialog.askinteger("VLAN ID", "Entrez l'ID du VLAN pour le mode access:", parent=self.root)
            interface["access_vlan"] = vlan_id
        elif mode == "trunk":
            allowed_vlans = simpledialog.askstring("VLANs autorisés", "Entrez les VLANs autorisés (ex. 10,20,30):", parent=self.root)
            interface["allowed_vlans"] = allowed_vlans
        elif mode == "routed":
            ip_address = simpledialog.askstring("Adresse IP", "Entrez l'adresse IP:", parent=self.root)
            subnet_mask = simpledialog.askstring("Masque de sous-réseau", "Entrez le masque de sous-réseau:", parent=self.root)
            interface["ip_address"] = ip_address
            interface["subnet_mask"] = subnet_mask

        self.interface_list.append(interface)
        self.interface_listbox.insert("end", f"Interface {interface_name}: {description}, Mode: {mode}\n")

    def create_routing_tab(self):
        """Crée l'onglet pour gérer le routage."""
        frame = self.notebook.tab("Routage")
        ctk.CTkLabel(frame, text="Configuration des Protocoles de Routage").pack(pady=10)

        self.routing_listbox = ctk.CTkTextbox(frame, width=600, height=300)
        self.routing_listbox.pack(pady=5)

        add_routing_button = ctk.CTkButton(frame, text="Ajouter Routage", command=self.add_routing)
        add_routing_button.pack(pady=5)

    def add_routing(self):
        """Ajoute une configuration de routage."""
        protocol = simpledialog.askstring("Protocole", "Entrez le protocole (ospf/rip/eigrp):", parent=self.root)
        if protocol == "ospf":
            process_id = simpledialog.askinteger("Process ID", "Entrez le Process ID pour OSPF:", parent=self.root)
            networks = []
            while True:
                add_network = messagebox.askyesno("Réseau OSPF", "Voulez-vous ajouter un réseau OSPF ?", parent=self.root)
                if not add_network:
                    break
                network = simpledialog.askstring("Réseau", "Entrez le réseau (ex. 192.168.1.0):", parent=self.root)
                wildcard = simpledialog.askstring("Wildcard", "Entrez le masque wildcard (ex. 0.0.0.255):", parent=self.root)
                area = simpledialog.askstring("Zone", "Entrez la zone OSPF:", parent=self.root)
                networks.append({"network": network, "wildcard": wildcard, "area": area})

            self.routing_protocols.append({"protocol": protocol, "process_id": process_id, "networks": networks})
            self.routing_listbox.insert("end", f"OSPF: Process ID {process_id}, Réseaux: {len(networks)}\n")

    def create_acls_tab(self):
        """Crée l'onglet pour gérer les ACLs."""
        frame = self.notebook.tab("ACLs")
        ctk.CTkLabel(frame, text="Liste des ACLs configurées").pack(pady=10)

        self.acl_listbox = ctk.CTkTextbox(frame, width=600, height=300)
        self.acl_listbox.pack(pady=5)

        add_acl_button = ctk.CTkButton(frame, text="Ajouter ACL", command=self.add_acl)
        add_acl_button.pack(pady=5)

    def add_acl(self):
        """Ajoute une ACL."""
        acl_number = simpledialog.askinteger("Numéro ACL", "Entrez le numéro de l'ACL:", parent=self.root)
        entries = []
        while True:
            add_entry = messagebox.askyesno("Entrée ACL", "Voulez-vous ajouter une entrée ACL ?", parent=self.root)
            if not add_entry:
                break
            action = simpledialog.askstring("Action", "Entrez l'action (permit/deny):", parent=self.root)
            protocol = simpledialog.askstring("Protocole", "Entrez le protocole (ip/tcp/udp):", parent=self.root)
            source = simpledialog.askstring("Source", "Entrez la source (ex. any, host 192.168.1.1):", parent=self.root)
            destination = simpledialog.askstring("Destination", "Entrez la destination (ex. any, host 192.168.1.2):", parent=self.root)
            entries.append({"action": action, "protocol": protocol, "source": source, "destination": destination})

        self.acls.append({"number": acl_number, "entries": entries})
        self.acl_listbox.insert("end", f"ACL {acl_number}: {len(entries)} entrées\n")

    def generate_configuration(self):
        """Génère la configuration complète."""
        if not self.hostname_entry.get():
            messagebox.showerror("Erreur", "Le nom d'hôte est obligatoire.")
            return
        self.device["hostname"] = self.hostname_entry.get()
        self.device["vlans"] = self.vlan_list
        self.device["interfaces"] = self.interface_list
        self.device["routing_protocols"] = self.routing_protocols
        self.device["acls"] = self.acls

        config_generator = ConfigGenerator.ConfigGenerator(self.device)
        config = config_generator.generate_configuration()
        self.save_configuration(config)

    def save_configuration(self, config):
        """Enregistre la configuration générée."""
        documents_folder = os.path.expanduser("~/Documents")
        config_folder = os.path.join(documents_folder, "ConfigurationsCisco")
        os.makedirs(config_folder, exist_ok=True)
        filename = os.path.join(config_folder, f"{self.device['hostname']}_config.txt")
        with open(filename, "w") as f:
            f.write(config)
        messagebox.showinfo("Succès", f"Configuration sauvegardée dans {filename}")


