# Practical 4: register backward-compatible Kafka schemas through the REST API.
# Needs Kafka Schema Registry at http://localhost:8081 (journal Docker setup).
# Requires: pip install requests
import json, copy, requests

url = "http://localhost:8081"
subject = "patient-data-value"
v1 = {"type":"record", "name":"Patient", "fields":[
    {"name":name, "type":kind} for name,kind in [
        ("patient_id","int"), ("patient_name","string"),
        ("age","int"), ("heart_rate","int")]]}
v2 = copy.deepcopy(v1)
v2["fields"].append({"name":"blood_pressure", "type":"string", "default":"Unknown"})

# New schema can read old records because the added field has a default.
def register(schema):
    r = requests.post(f"{url}/subjects/{subject}/versions",
                      json={"schema":json.dumps(schema)}, timeout=10)
    print("Register:", r.status_code, r.text)
    return r

register(v1)
r = requests.put(f"{url}/config/{subject}",
                 json={"compatibility":"BACKWARD"}, timeout=10)
print("Compatibility:", r.status_code, r.text)
register(v2)
v3 = copy.deepcopy(v2)
v3["fields"].append({"name":"emergency_contact", "type":"string"})
register(v3)  # Expected HTTP 409: missing default for a new field.
