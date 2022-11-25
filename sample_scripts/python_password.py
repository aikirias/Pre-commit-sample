import pulsar
import pyodbc
client = pulsar.Client("pulsar://localhost:6650")
consumer = client.subscribe(topic="customerID_2", subscription_name="hydrate-test3")
def hydrate_customers_ID(customers_id):
    conn = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=ReportDB01.dev.pposervices.local;"
        "Database=ASIDb;"
        "uid=p1Pulsar01;"
        "pwd=Csr)72WcNPVYxkn#r;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    cursor = conn.cursor()
    query = "[ASIDb].[dbo].[dbsp_GetGenericUserProfileDataProfile_2] '{}' ".format(
        customers_id
    )
    cursor.execute(query)
    for i in cursor:
        print(i)
    conn.close()
while True:
    msg = consumer.receive()
    try:
        customers_id = msg.data().decode("utf-8")
        hydrate_customers_ID(customers_id)
        consumer.acknowledge(msg)
    except:
        consumer.negative_acknowledge(msg)
client.close()