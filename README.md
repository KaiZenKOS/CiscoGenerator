# Cisco Configuration Generator Application

This project provides a graphical user interface (GUI) tool to assist in generating Cisco router and switch configurations. The application, developed in Python, allows users to define key networking parameters, including VLANs, interfaces, routing protocols, access control lists (ACLs), and more, making it easier to produce accurate Cisco configuration scripts.

## Features

1. **Graphical User Interface (GUI)**:
   - Built with `customtkinter`, this tool provides a user-friendly interface to configure Cisco devices.
   - Users can easily navigate tabs dedicated to different aspects of the configuration: Device Information, VLANs, Interfaces, Routing, and ACLs.

2. **Flexible Configuration Options**:
   - Define **basic settings** like hostname, enable secret, and banner.
   - Configure **VLANs**, **interfaces** (access, trunk, or routed modes), and **routing protocols** such as OSPF.
   - Create **Access Control Lists (ACLs)** to control packet flows.

3. **Complete Configuration Generation**:
   - Generates a full Cisco IOS configuration script based on user inputs.
   - Supports customization of VLAN, STP, interface settings, line passwords, and routing protocols.
   - Exports the configuration to a `.txt` file for easy deployment.

## Structure

The project is structured into three main Python files:

1. **`ConfigGenerator.py`**:
   - This module contains the `ConfigGenerator` class which handles the logic to convert user inputs into Cisco configuration commands.
   - Generates different configuration parts such as banner, line password, VLAN, STP, interface settings, routing, and ACLs.
   - Provides a complete formatted Cisco configuration script from the gathered data.

2. **`UI_Generator.py`**:
   - Defines the `ConfigApp` class, responsible for the GUI interface.
   - Uses `customtkinter` to create different tabs where users can input the necessary device configuration details.
   - Collects user inputs from GUI components and passes them to the `ConfigGenerator` to generate the final configuration.
   - Saves the generated configuration into a file within the user's Documents directory.

3. **`main.py`**:
   - Serves as the entry point of the application.
   - Initializes and starts the GUI application.

## How to Use

1. **Installation**:
   - Clone the repository.
   - Make sure you have Python 3 and install the required packages using:
     ```sh
     pip install customtkinter
     ```

2. **Run the Application**:
   - Simply execute the `main.py` file:
     ```sh
     python main.py
     ```
   - This will start the GUI application.

3. **Input Configuration**:
   - Use the provided tabs to input details like:
     - **Device Info**: Hostname, enable secret, banner, etc.
     - **VLANs**: Create and list all VLANs.
     - **Interfaces**: Configure interfaces, including access/trunk modes, VLANs, and routed interfaces.
     - **Routing**: Add routing configurations (currently supports OSPF).
     - **ACLs**: Create Access Control Lists with multiple entries.

4. **Generate and Save Configuration**:
   - After entering all the details, click on "Generate Configuration".
   - The configuration will be saved in a folder named `ConfigurationsCisco` inside the Documents directory.

## Code Overview

- **`ConfigGenerator` Class**:
  - Methods like `generate_banner_config()`, `generate_vlan_config()`, and others are used to generate specific parts of the Cisco configuration.
  - The complete configuration is assembled in `generate_configuration()` and formatted to Cisco's standards.

- **`ConfigApp` Class (UI)**:
  - Provides a tabbed interface where users can enter configuration details.
  - Collects all information into a dictionary (`self.device`) and passes it to `ConfigGenerator`.

## Example Usage

Once you start the application, follow these steps:

1. Fill in device details such as hostname and enable password.
2. Add VLANs and interfaces as needed.
3. Configure OSPF routing if applicable.
4. Define ACLs to enforce network security policies.
5. Click "Generate Configuration" to produce the Cisco config script.

The configuration output will resemble:

```sh
hostname MyDevice
!
banner motd #Welcome to the network#
!
enable secret mySecretPassword
!
line con 0
 password consolePassword
 login
line vty 0 4
 password vtyPassword
 login
!
spanning-tree mode rapid-pvst
!
vlan 10
 name Sales
!
interface GigabitEthernet0/1
 description Connection to Switch
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
!
router ospf 1
 network 192.168.1.0 0.0.0.255 area 0
!
access-list 10 permit ip any any
