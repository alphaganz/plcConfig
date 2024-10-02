# # Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# # For license information, please see license.txt

import json
import frappe
import requests
from frappe.model.document import Document

class ModbusTCPDevice(Document):
    def before_save(self):
        # Display all fields to check if they exist
        msg = "Device Info:\n"
        try:
            msg += f"Device Name: {getattr(self, 'device_name', 'N/A')}\n"
            msg += f"Polling Time: {getattr(self, 'polling_time', 'N/A')}\n"
            msg += f"Time Out: {getattr(self, 'time_out', 'N/A')}\n"
            msg += f"No of Retries: {getattr(self, 'no_of_retries', 'N/A')}\n"

            # Loop through child table entries
            child_table_data = getattr(self, 'tcp_table', [])
            if child_table_data:
                msg += "Child Table Data:\n"
                for row in child_table_data:
                    msg += f"Slave Device Name: {getattr(row, 'slave_device_name', 'N/A')}\n"
                    msg += f"IP Address: {getattr(row, 'ip_address', 'N/A')}\n"
                    msg += f"Port Number: {getattr(row, 'port_number', 'N/A')}\n"
                    msg += f"Unit ID: {getattr(row, 'unit_id', 'N/A')}\n"
                    msg += f"Starting Address: {getattr(row, 'starting_address', 'N/A')}\n"
                    msg += f"Length: {getattr(row, 'length', 'N/A')}\n"
                    msg += f"Datatype: {getattr(row, 'datatype', 'N/A')}\n"
                    msg += f"Function Code: {getattr(row, 'function_code', 'N/A')}\n"
                    msg += f"Tag Name: {getattr(row, 'tag_name', 'N/A')}\n"
                    msg += f"DataFormat: {getattr(row, 'data_format', 'N/A')}\n"
                    msg += f"Description: {getattr(row, 'description', 'N/A')}\n"
                    msg += f"Event Report: {getattr(row, 'event_report', 'N/A')}\n"
            else:
                msg += "No child table data found.\n"
        except AttributeError as e:
            frappe.msgprint(f"Error: {str(e)}")

        # Display the collected message
        frappe.msgprint(msg)

        # Step 1: Collect data from fields
        device_info = {
            "Device Name": getattr(self, 'device_name', 'N/A'),
            "Polling Time": getattr(self, 'polling_time', 'N/A'),
            "Time Out": getattr(self, 'time_out', 'N/A'),
            "No of Retries": getattr(self, 'no_of_retries', 'N/A'),
            "Child Table Data": []  # Corrected line to store child table data
        }

        # Loop through child table entries and add them to the device_info dictionary
        if child_table_data:
            for row in child_table_data:
                child_data = {
                    "Slave Device Name": getattr(row, 'slave_device_name', 'N/A'),
                    "IP Address": getattr(row, 'ip_address', 'N/A'),
                    "Port Number": getattr(row, 'port_number', 'N/A'),
                    "Unit ID": getattr(row, 'unit_id', 'N/A'),
                    "Starting Address": getattr(row, 'starting_address', 'N/A'),
                    "Length": getattr(row, 'length', 'N/A'),
                    "Datatype": getattr(row, 'datatype', 'N/A'),
                    "Function Code": getattr(row, 'function_code', 'N/A'),
                    "Tag Name": getattr(row, 'tag_name', 'N/A'),
                    "DataFormat": getattr(row, 'data_format', 'N/A'),
                    "Description": getattr(row, 'description', 'N/A'),
                    "Event Report": getattr(row, 'event_report', 'N/A')
                }
                device_info["Child Table Data"].append(child_data)

        # Step 2: Convert the data to JSON
        try:
            json_data = json.dumps(device_info)
            # Step 3: Save the JSON string into the json_data field
            self.json_data = json_data
            frappe.msgprint(f"JSON generated successfully: {json_data}")
        except Exception as e:
            frappe.msgprint(f"Error generating JSON: {str(e)}")

        # Step 4: Send JSON data to the external API
        try:
            url = "http://localhost/api/v2/config/store.php"
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(url, data=json_data, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                frappe.msgprint("Data sent successfully to the external API.")
            else:
                frappe.msgprint(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            frappe.msgprint(f"Error sending data to API: {str(e)}")


    # def onload(self):
    #     # Fetch data from URL when the document is refreshed
    #     if not getattr(self, 'json_data', None):
    #         url = "http://demo-site.in/mrrrest/api/v2/config/tcp"  # Replace with your desired URL

    #         try:
    #             headers = {
    #                 'Accept': 'application/json',  
    #                 'User-Agent': 'Frappe Client'  
    #             }
    #             response = requests.get(url, headers=headers)
    #             response.raise_for_status()  

    #             json_data = response.text

    #             # Save the JSON string into the json_data field
    #             self.json_data = json_data

    #             # Update fields from JSON data
    #             device_info = json.loads(json_data)

    #             # Rewrite fields from the JSON data
    #             setattr(self, 'device_name', device_info.get("Device Name", ''))
    #             setattr(self, 'polling_time', device_info.get("Polling Time", ''))
    #             setattr(self, 'time_out', device_info.get("Time Out", ''))
    #             setattr(self, 'no_of_retries', device_info.get("No of Retries", ''))

    #             # Assuming 'tcp_table' is your child table field name
    #             child_table_data = device_info.get("Child Table Data", [])
    #             if child_table_data:
    #                 # Clear existing child table entries
    #                 self.tcp_table = []

    #                 # Add new entries from JSON data
    #                 for entry in child_table_data:
    #                     row = self.append('tcp_table')
    #                     row.slave_device_name = entry.get("Slave Device Name",'')
    #                     row.ip_address = entry.get("IP Address", '')
    #                     row.port_number = entry.get("Port Number", '')
    #                     row.unit_id = entry.get("Unit ID", '')
    #                     row.starting_address = entry.get("Starting Address", '')
    #                     row.length = entry.get("Length", '')
    #                     row.datatype = entry.get("Datatype", '')
    #                     row.function_code = entry.get("Function Code", '')
    #                     row.tag_name = entry.get("Tag Name", '')
    #                     row.data_format = entry.get("DataFormat", '')
    #                     row.description = entry.get("Description", '')
    #                     row.event_report = entry.get("Event Report", '')
    #             else:
    #                 self.tcp_table = []

    #             frappe.msgprint(f"Document refreshed with data from URL: {url}")

    #         except requests.RequestException as e:
    #             frappe.msgprint(f"Error fetching data from URL: {str(e)}")
    #         except json.JSONDecodeError as e:
    #             frappe.msgprint(f"Error parsing JSON data: {str(e)}")
