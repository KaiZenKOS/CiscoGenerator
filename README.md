# Cisco Configuration Generator Application

This project provides a graphical user interface (GUI) tool to assist in generating Cisco router and switch configurations. The application, developed in Python, allows users to define key networking parameters, including VLANs, interfaces, routing protocols, access control lists (ACLs), and more, making it easier to produce accurate Cisco configuration scripts.

## Features

- **Graphical User Interface (GUI)**:
  - Built with `customtkinter`, this tool provides a user-friendly interface to configure Cisco devices.
  - Users can easily navigate tabs dedicated to different aspects of the configuration: Device Information, VLANs, Interfaces, Routing, and ACLs.

- **Flexible Configuration Options**:
  - Define **basic settings** like hostname, enable secret, and banner.
  - Configure **VLANs**, **interfaces** (access, trunk, or routed modes), and **routing protocols** such as OSPF.
  - Create **Access Control Lists (ACLs)** to control packet flows.

- **Complete Configuration Generation**:
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

### Installation

- Clone the repository.
- Make sure you have Python 3 and install the required packages using:

  ```sh
  pip install customtkinter
