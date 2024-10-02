# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import json
import frappe
import requests
from frappe.model.document import Document

class ModbusRTUDevice(Document):
    def before_save(self):
        # Display all fields to check if they exist
        msg = "Device Info:\n"
        try:
            msg += f"Device Name: {getattr(self, 'device_name', 'N/A')}\n"
            msg += f"Com port: {getattr(self, 'com_port', 'N/A')}\n"
            msg += f"Baud Rate: {getattr(self, 'baud_rate', 'N/A')}\n"
            msg += f"Flow Control: {getattr(self, 'flow_control', 'N/A')}\n"
            msg += f"Parity: {getattr(self, 'parity', 'N/A')}\n"
            msg += f"Data Bit: {getattr(self, 'data_bit', 'N/A')}\n"
            msg += f"Stop Bit: {getattr(self, 'stop_bit', 'N/A')}\n" 
            msg += f"Polling Time: {getattr(self, 'polling_time', 'N/A')}\n"
            msg += f"Time Out: {getattr(self, 'time_out', 'N/A')}\n"
            msg += f"No of Retries: {getattr(self, 'no_of_retries', 'N/A')}\n"

            # Loop through child table entries
            child_table_data = getattr(self, 'rtu_table', [])  # Replace 'rtu_table' with your actual child table field name
            if child_table_data:
                for row in child_table_data:
                    msg += f"Slave Device Name: {getattr(row, 'slave_device_name', 'N/A')}\n"
                    msg += f"Slave ID: {getattr(row, 'slave_id', 'N/A')}\n"
                    msg += f"Starting Address: {getattr(row, 'starting_address', 'N/A')}\n"
                    msg += f"Length: {getattr(row, 'length', 'N/A')}\n"
                    msg += f"Datatype: {getattr(row, 'datatype', 'N/A')}\n"
                    msg += f"Function Code: {getattr(row, 'function_code', 'N/A')}\n"
                    msg += f"Tag Name: {getattr(row, 'tag_name', 'N/A')}\n"
                    msg += f"DataFormat: {getattr(row, 'data_format', 'N/A')}\n"
                    msg += f"Description: {getattr(row,'description','N/A')}\n"
                    msg += f"Event Report: {getattr(row,'event_report','N/A')}\n"
            else:
                msg += "No child table data found.\n"
        except AttributeError as e:
            frappe.msgprint(f"Error: {str(e)}")

        # Display message
        frappe.msgprint(msg)

        # Step 1: Collect data from fields
        device_info = {
            "Device Name": getattr(self, 'device_name', 'N/A'),
            "Com port": getattr(self, 'com_port', 'N/A'),
            "Baud Rate": getattr(self, 'baud_rate', 'N/A'),
            "Flow Control": getattr(self, 'flow_control', 'N/A'),
            "Parity": getattr(self, 'parity', 'N/A'),
            "Data Bit": getattr(self, 'data_bit', 'N/A'),
            "Stop Bit": getattr(self, 'stop_bit', 'N/A'),  
            "Polling Time": getattr(self, 'polling_time', 'N/A'),
            "Time Out": getattr(self, 'time_out', 'N/A'),
            "No of Retries": getattr(self, 'no_of_retries', 'N/A'),
            "SlaveData": []  # To store child table data
        }

        # Loop through child table entries and add them to the device_info dictionary
        if child_table_data:
            for row in child_table_data:
                child_data = {
                    "Slave Device Name": getattr(row, 'slave_device_name', 'N/A'),
                    "Slave ID": getattr(row, 'slave_id', 'N/A'),
                    "Starting Address": getattr(row, 'starting_address', 'N/A'),
                    "Length": getattr(row, 'length', 'N/A'),
                    "Datatype": getattr(row, 'datatype', 'N/A'),
                    "Function Code": getattr(row, 'function_code', 'N/A'),
                    "Tag Name": getattr(row, 'tag_name', 'N/A'),
                    "DataFormat": getattr(row, 'data_format', 'N/A'),
                    "Description":getattr(row,'description','N/A'),
                    "Event Report":getattr(row,'event_report','N/A')
                }
                device_info["SlaveData"].append(child_data)

        # Step 2: Convert the data to JSON
        json_data = json.dumps(device_info)

        # Step 3: Save the JSON string into the json_data field
        self.json_data = json_data
        frappe.msgprint(json_data)

    def onload(self):
        # Fetch data from URL when the document is refreshed
        if not getattr(self, 'json_data', None):
            # Define the URL outside of the try-except block
            url = "http://demo-site.in/mrrrest/api/v2/config/rtu"  # Replace with your desired URL

            try:
                headers = {
                    'Accept': 'application/json',  # Ensure the server returns JSON
                    'User-Agent': 'ModbusRTUClient/1.0'  # Optionally set a User-Agent header if needed
                }

                # Send the GET request with headers
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)

                # Process the response
                json_data = response.text

                # Save the JSON string into the json_data field
                self.json_data = json_data

                # Parse and update fields from the JSON data
                device_info = json.loads(json_data)

                # Rewrite fields from the JSON data
                setattr(self, 'device_name', device_info.get("Device Name", ''))
                setattr(self, 'com_port', device_info.get("Com port", ''))
                setattr(self, 'baud_rate', device_info.get("Baud Rate", ''))
                setattr(self, 'flow_control', device_info.get("Flow Control", ''))
                setattr(self, 'parity', device_info.get("Parity", ''))
                setattr(self, 'data_bit', device_info.get("Data Bit", ''))
                setattr(self, 'stop_bit', device_info.get("Stop Bit", ''))
                setattr(self, 'polling_time', device_info.get("Polling Time", ''))
                setattr(self, 'time_out', device_info.get("Time Out", ''))
                setattr(self, 'no_of_retries', device_info.get("No of Retries", ''))

                # Assuming 'rtu_table' is your child table field name
                child_table_data = device_info.get("SlaveData", [])
                if child_table_data:
                    # Clear existing child table entries
                    self.rtu_table = []

                    # Add new entries from JSON data
                    for entry in child_table_data:
                        row = self.append('rtu_table')
                        row.slave_device_name = entry.get("Slave Device Name",'')
                        row.slave_id = entry.get("Slave ID", '')
                        row.starting_address = entry.get("Starting Address", '')
                        row.length = entry.get("Length", '')
                        row.datatype = entry.get("Datatype", '')
                        row.function_code = entry.get("Function Code", '')
                        row.tag_name = entry.get("Tag Name", '')
                        row.data_format = entry.get("DataFormat", '')
                        row.description = entry.get("Description", '')
                        row.event_report = entry.get("Event Report", '')
                else:
                    self.rtu_table = []

                frappe.msgprint(f"Document refreshed with data from URL: {url}")

            except requests.RequestException as e:
                frappe.msgprint(f"Error fetching data from URL: {str(e)}")
            except json.JSONDecodeError as e:
                frappe.msgprint(f"Error parsing JSON data: {str(e)}")