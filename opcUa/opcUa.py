from opcua import Client

# Connect to OPC UA server
client = Client("opc.tcp://192.168.1.1:62520/AggregationServer")
try:
    client.connect()
    print("Connected to OPC UA server")
    # Access nodes
    root = client.get_root_node()
    objects = client.get_objects_node()
    print("Root node: ", root)
    print("Objects node: ", objects)
    # Now you can access the nodes and read/write data as needed
finally:
    # Disconnect from server
    client.disconnect()
    print("Disconnected from OPC UA server")

