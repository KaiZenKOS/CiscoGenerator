# Générateur de Configuration Cisco

Ce projet fournit un outil avec une interface graphique (GUI) pour aider à générer des configurations pour les routeurs et commutateurs Cisco. L'application, développée en Python, permet aux utilisateurs de définir les principaux paramètres réseau, notamment les VLAN, les interfaces, les protocoles de routage, les listes de contrôle d'accès (ACL), etc., ce qui facilite la production de scripts de configuration Cisco précis.

## Fonctionnalités

1. **Interface Graphique (GUI)** :
   - Construit avec `customtkinter`, cet outil offre une interface conviviale pour configurer les appareils Cisco.
   - Les utilisateurs peuvent facilement naviguer entre les onglets dédiés aux différents aspects de la configuration : Informations de l'appareil, VLANs, Interfaces, Routage, et ACLs.

2. **Options de Configuration Flexibles** :
   - Définir des **paramètres de base** tels que le nom d'hôte, le mot de passe secret d'activation, et la bannière.
   - Configurer des **VLANs**, des **interfaces** (modes access, trunk, ou routé), et des **protocoles de routage** comme OSPF.
   - Créer des **Listes de Contrôle d'Accès (ACLs)** pour contrôler les flux de paquets.

3. **Génération Complète de la Configuration** :
   - Génère un script de configuration Cisco IOS complet basé sur les entrées de l'utilisateur.
   - Supporte la personnalisation des VLAN, STP, des paramètres d'interface, des mots de passe de ligne, et des protocoles de routage.
   - Exporte la configuration dans un fichier `.txt` pour une mise en œuvre facile.

## Structure

Le projet est structuré en trois fichiers Python principaux :

1. **`ConfigGenerator.py`** :
   - Ce module contient la classe `ConfigGenerator` qui gère la logique pour convertir les entrées des utilisateurs en commandes de configuration Cisco.
   - Génère différentes parties de la configuration telles que la bannière, le mot de passe de ligne, les VLAN, le STP, les paramètres d'interface, le routage, et les ACL.
   - Fournit un script de configuration Cisco formaté complet basé sur les données collectées.

2. **`UI_Generator.py`** :
   - Définit la classe `ConfigApp`, responsable de l'interface utilisateur.
   - Utilise `customtkinter` pour créer différents onglets où les utilisateurs peuvent saisir les détails nécessaires à la configuration de l'appareil.
   - Collecte les entrées des utilisateurs à partir des composants GUI et les transmet au `ConfigGenerator` pour générer la configuration finale.
   - Enregistre la configuration générée dans un fichier situé dans le répertoire Documents de l'utilisateur.

3. **`main.py`** :
   - Sert de point d'entrée à l'application.
   - Initialise et démarre l'application GUI.

## Comment Utiliser

1. **Installation** :
   - Clonez le dépôt.
   - Assurez-vous d'avoir Python 3 et installez les packages requis en utilisant :
     ```sh
     pip install customtkinter
     ```

2. **Lancer l'Application** :
   - Exécutez simplement le fichier `main.py` :
     ```sh
     python main.py
     ```
   - Cela démarrera l'application GUI.

3. **Saisir la Configuration** :
   - Utilisez les onglets fournis pour saisir les détails tels que :
     - **Informations sur l'appareil** : Nom d'hôte, mot de passe secret d'activation, bannière, etc.
     - **VLANs** : Créer et lister tous les VLANs.
     - **Interfaces** : Configurer les interfaces, y compris les modes access/trunk, les VLANs, et les interfaces routées.
     - **Routage** : Ajouter des configurations de routage (actuellement, prend en charge OSPF).
     - **ACLs** : Créer des listes de contrôle d'accès avec plusieurs entrées.

4. **Générer et Enregistrer la Configuration** :
   - Après avoir saisi tous les détails, cliquez sur "Générer la configuration".
   - La configuration sera enregistrée dans un dossier nommé `ConfigurationsCisco` dans le répertoire Documents.

## Créer un Exécutable avec PyInstaller

Vous pouvez créer un exécutable pour que votre application soit utilisable sans avoir besoin de Python installé sur le système. Voici comment procéder pour macOS et Linux :

1. **Installer PyInstaller** :
   - Si PyInstaller n'est pas encore installé, vous pouvez l'installer avec la commande suivante :
     ```sh
     pip install pyinstaller
     ```

2. **Créer l'Exécutable** :
   - Depuis la racine de votre projet, exécutez la commande suivante pour créer un exécutable :
     ```sh
     pyinstaller --onefile --windowed main.py
     ```
   - Voici une explication des options :
     - `--onefile` : Crée un fichier exécutable unique.
     - `--windowed` : Sur macOS, cette option permet de cacher la console lors de l'exécution (utile pour les applications GUI).

3. **Trouver l'Exécutable** :
   - Après l'exécution de PyInstaller, l'exécutable sera situé dans le dossier `dist/`.
   - Pour macOS et Linux, vous pourrez trouver un fichier nommé `main` (ou similaire). Vous pouvez déplacer ce fichier vers l'endroit souhaité pour une distribution facile.

4. **Utilisation sur macOS et Linux** :
   - L'exécutable généré peut être utilisé directement sur les systèmes macOS et Linux compatibles.
   - Assurez-vous de donner les permissions d'exécution sur l'exécutable si nécessaire :
     ```sh
     chmod +x dist/main
     ```

## Aperçu du Code

- **Classe `ConfigGenerator`** :
  - Des méthodes comme `generate_banner_config()`, `generate_vlan_config()`, et d'autres sont utilisées pour générer des parties spécifiques de la configuration Cisco.
  - La configuration complète est assemblée dans `generate_configuration()` et formatée selon les normes de Cisco.

- **Classe `ConfigApp` (Interface Utilisateur)** :
  - Fournit une interface avec des onglets où les utilisateurs peuvent entrer les détails de la configuration.
  - Collecte toutes les informations dans un dictionnaire (`self.device`) et les transmet au `ConfigGenerator`.

## Exemple d'Utilisation

Une fois que vous démarrez l'application, suivez ces étapes :

1. Renseignez les détails de l'appareil tels que le nom d'hôte et le mot de passe d'activation.
2. Ajoutez les VLANs et les interfaces selon les besoins.
3. Configurez le routage OSPF si nécessaire.
4. Définissez les ACLs pour appliquer des politiques de sécurité réseau.
5. Cliquez sur "Générer la configuration" pour produire le script de configuration Cisco.

La sortie de la configuration ressemblera à ceci :

```sh
hostname MonAppareil
!
banner motd #Bienvenue sur le réseau#
!
enable secret monMotDePasseSecret
!
line con 0
 password motDePasseConsole
 login
line vty 0 4
 password motDePasseVty
 login
!
spanning-tree mode rapid-pvst
!
vlan 10
 name Ventes
!
interface GigabitEthernet0/1
 description Connexion au Commutateur
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
!
router ospf 1
 network 192.168.1.0 0.0.0.255 area 0
!
access-list 10 permit ip any any
