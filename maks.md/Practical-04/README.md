# Practical 4 — Kafka Schema Registry — Backward Compatibility

Based on the uploaded **BD Practical Journal**. The source text below is kept for reference; the separate code files were extracted from that journal.

## Files

- `schemas/patient-v1.avsc`
- `schemas/patient-v2.avsc`
- `schemas/patient-v3.avsc`

## Step-by-step execution (Windows PowerShell)

1. Start Kafka and Schema Registry using Docker Compose (journal environment configuration must be supplied separately).
2. Create topic `patient-records` and schema files in `schemas/`.
3. Register `schemas/patient-v1.avsc` with the Schema Registry subject.
4. Set `BACKWARD` compatibility for `patient-records-value`.
5. Register `schemas/patient-v2.avsc`, adding `blood_pressure` with default `Unknown`.
6. Try registering `schemas/patient-v3.avsc` (new mandatory field without default) and observe incompatibility.
7. Use the PowerShell commands in the source reference below for REST requests.

## Expected result

V2 accepted; incompatible V3 rejected with error 409.

## Important note

The journal has extensive PowerShell commands and schema content, but not a complete local Docker Compose file.

## Original journal text (reference)

This section preserves the text extracted from the uploaded document. Screenshots/figures are not embedded here.

```text
Practical 4

Q.1 Schema Evolution: Use Kafka Schema Registry to demonstrate a "Backward
Compatible" schema change.




In Kafka Schema Registry, backward compatibility means:
A new schema can be used to read data that was produced using the older schema.
Hospital Patient System
       |
       | Patient data

       ↓
       Kafka
       |

       ↓
 Schema Registry
       |

       ┌────┴────┐

       ↓       ↓
Schema V1 Schema V2
       |       |
Patient        Patient
ID     ID
Name           Name
Age            Age
HeartRate HeartRate
       BP


We can use Patient Records / Hospital Monitoring Data.
Real-world scenario
Suppose a hospital initially sends patient information to Kafka like this:
Version 1
Patient ID
Patient Name
Age
Heart Rate


Later, the hospital wants to add:


Version 2
Patient ID
Patient Name
Age
Heart Rate
Blood Pressure


The flow will be:
Hospital Patient System
       |
       | Patient data

       ↓
       Kafka
          |

          ↓
    Schema Registry
          |

          ┌────┴────┐

          ↓       ↓
Schema V1 Schema V2
          |       |
Patient           Patient
ID        ID
Name              Name
Age               Age
HeartRate HeartRate
          BP
What we will actually demonstrate
V1 — Original patient schema
{
    "patient_id": 101,
    "patient_name": "Amit",
    "age": 45,
    "heart_rate": 78
}
Then the hospital changes its system.
V2 — New patient schema
{
    "patient_id": 101,
    "patient_name": "Amit",
    "age": 45,
    "heart_rate": 78,
    "blood_pressure": "120/80"
}
The important part is:
{
    "name": "blood_pressure",
    "type": "string",
    "default": "Unknown"
}
Practical sequence
      1. Create hospital Kafka environment using Docker




      2. Start Kafka




      3. Start Schema Registry




           docker exec practical4-kafka kafka-topics --bootstrap-server localhost:9092 --create --
           topic patient-records --partitions 1 --replication-factor 1

           docker exec practical4-kafka kafka-topics --bootstrap-server localhost:9092 --list




      4. Create patient-v1.avsc
         Code:
         {
           "type": "record",
           "name": "Patient",
           "namespace": "hospital",
           "fields": [
           {
             "name": "patient_id",
             "type": "int"
           },
           {
             "name": "patient_name",
             "type": "string"
           },
           {
             "name": "age",
             "type": "int"
           },
           {
             "name": "heart_rate",
             "type": "int"
           }
       ]
   }

5. Register V1

    $schema = Get-Content -Raw .\schemas\patient-v1.avsc
   PS C:\Users\Admin\Desktop\practical4> $escapedSchema = $schema.Replace('\','\
   \').Replace('"','\"').Replace("`r",'').Replace("`n",'\n')
   PS C:\Users\Admin\Desktop\practical4> $body = '{"schema":"' + $escapedSchema + '"}'
   PS C:\Users\Admin\Desktop\practical4> $body
   {"schema":"{\n \"type\": \"record\",\n \"name\": \"Patient\",\n \"namespace\": \"hospital\",
   \n \"fields\": [\n {\n      \"name\": \"patient_id\",\n       \"type\": \"int\"\n },\n {\n
   \"name\": \"patient_name\",\n          \"type\": \"string\"\n },\n {\n         \"name\": \"age\",\n
   \"type\": \"int\"\n },\n {\n       \"name\": \"heart_rate\",\n        \"type\": \"int\"\n }\n ]\n}"}
   PS C:\Users\Admin\Desktop\practical4> Invoke-RestMethod `
   >> -Uri "http://localhost:8081/subjects/patient-records-value/versions" `
   >> -Method Post `
   >> -ContentType "application/vnd.schemaregistry.v1+json" `
   >> -Body $body
6. Set compatibility to BACKWARD
   PS C:\Users\Admin\Desktop\practical4> curl.exe -X PUT `
   >> -H "Content-Type: application/json" `
   >> --data '{\"compatibility\":\"BACKWARD\"}' `
   >> http://localhost:8081/config/patient-records-value
   {"compatibility":"BACKWARD"}
   PS C:\Users\Admin\Desktop\practical4> curl.exe http://localhost:8081/config/patient-
   records-value
   {"compatibilityLevel":"BACKWARD"}




7. Create patient-v2.avsc(Add blood_pressure)
   CODE:
   {
     "type": "record",
     "name": "Patient",
     "namespace": "hospital",
     "fields": [
       {
         "name": "patient_id",
         "type": "int"
       },
       {
         "name": "patient_name",
         "type": "string"
       },
       {
         "name": "age",
         "type": "int"
       },
       {
         "name": "heart_rate",
         "type": "int"
       },
       {
         "name": "blood_pressure",
         "type": "string",
         "default": "Unknown"
       }
     ]
   }
8. Register V2
   PS C:\Users\Admin\Desktop\practical4> $schema = Get-Content -Raw .
   \schemas\patient-v2.avsc
   PS C:\Users\Admin\Desktop\practical4> $escapedSchema = $schema.Replace('\','\
   \').Replace('"','\"').Replace("`r",'').Replace("`n",'\n')
   PS C:\Users\Admin\Desktop\practical4> $body = '{"schema":"' + $escapedSchema + '"}'
   PS C:\Users\Admin\Desktop\practical4> Invoke-RestMethod `
   >> -Uri "http://localhost:8081/subjects/patient-records-value/versions" `
   >> -Method Post `
   >> -ContentType "application/vnd.schemaregistry.v1+json" `
   >> -Body $body
   id
   --
    2




9. Verify that V2 is accepted


10. Produce patient data using the new schema
    PS C:\Users\Admin\Desktop\practical4> curl.exe http://localhost:8081/subjects/patient-
    records-value/versions/1
    {"subject":"patient-records-value","version":1,"id":1,"schema":"{\"type\":\"record\",
    \"name\":\"Patient\",\"namespace\":\"hospital\",\"fields\":[{\"name\":\"patient_id\",\"type\":
    \"int\"},{\"name\":\"patient_name\",\"type\":\"string\"},{\"name\":\"age\",\"type\":\"int\"},
    {\"name\":\"heart_rate\",\"type\":\"int\"}]}"}
    PS C:\Users\Admin\Desktop\practical4> curl.exe http://localhost:8081/subjects/patient-
    records-value/versions/2
    {"subject":"patient-records-value","version":2,"id":2,"schema":"{\"type\":\"record\",
    \"name\":\"Patient\",\"namespace\":\"hospital\",\"fields\":[{\"name\":\"patient_id\",\"type\":
    \"int\"},{\"name\":\"patient_name\",\"type\":\"string\"},{\"name\":\"age\",\"type\":\"int\"},
    {\"name\":\"heart_rate\",\"type\":\"int\"},{\"name\":\"blood_pressure\",\"type\":\"string\",
    \"default\":\"Unknown\"}]}"}
    PS C:\Users\Admin\Desktop\practical4> docker exec -it practical4-kafka kafka-console-
    producer --bootstrap-server localhost:9092 --topic patient-records
    >{"patient_id":101,"patient_name":"Amit","age":45,"heart_rate":78,"blood_pressure":"120
    /80"}
    >^C
11. Create an incompatible V3
    CODE FOR patient-v3.ASVC:
    {
      "type": "record",
      "name": "Patient",
      "namespace": "hospital",
      "fields": [
        {"name": "patient_id", "type": "int"},
        {"name": "patient_name", "type": "string"},
        {"name": "age", "type": "int"},
        {"name": "heart_rate", "type": "int"},
        {"name": "blood_pressure", "type": "string", "default": "Unknown"},
        {"name": "emergency_contact", "type": "string"}
      ]
    }

12. Try registering V3
13. Observe Schema Registry rejecting V3
    PS C:\Users\Admin\Desktop\practical4> $schema = Get-Content -Raw .
    \schemas\patient-v3.avsc
    >> $escapedSchema = $schema.Replace('\','\
    \').Replace('"','\"').Replace("`r",'').Replace("`n",'\n')
    >> $body = '{"schema":"' + $escapedSchema + '"}'
    >> Invoke-RestMethod -Uri
    "http://localhost:8081/subjects/patient-records-value/versions" -Method Post
    -ContentType "application/vnd.schemaregistry.v1+json" -Body $body
    Invoke-RestMethod :
    {"error_code":409,"message":"Schema being
    registered is incompatible with an earlier schema
    for subject \"patient-records-value\", details:
    [{errorType:'READER_FIELD_MISSING_DEFAULT_VALUE',
    description:'The field 'emergency_contact' at path
    '/fields/5' in the new schema has no default value
    and is missing in the old schema',
    additionalInfo:'emergency_contact'},
    {oldSchemaVersion: 5}, {oldSchema: '{\"type\":\"reco
    rd\",\"name\":\"Patient\",\"namespace\":\"hospital\"
      ,\"fields\":[{\"name\":\"patient_id\",\"type\":\"int
      \"},{\"name\":\"patient_name\",\"type\":\"string\"},
      {\"name\":\"age\",\"type\":\"int\"},{\"name\":\"hear
      t_rate\",\"type\":\"int\"},{\"name\":\"blood_pressur
      e\",\"type\":\"string\",\"default\":\"Unknown\"}]}'}
      , {validateFields: 'false', compatibility:
      'BACKWARD'}]"}
      At line:4 char:1
      + Invoke-RestMethod -Uri
      "http://localhost:8081/subjects/patient-record ...
      + ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      ~~~~~~~~~~~~~~~~~~~
          + CategoryInfo           : InvalidOperation: (Sy
         stem.Net.HttpWebRequest:HttpWebRequest) [Invoke
        -RestMethod], WebException
          + FullyQualifiedErrorId : WebCmdletWebResponseE
         xception,Microsoft.PowerShell.Commands.InvokeRe
        stMethodCommand




   14. Verify all schema versions
```
