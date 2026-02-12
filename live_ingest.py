# ==========================================
# Live CloudWatch → DDoS Detection Pipeline
# ==========================================

import boto3
import joblib
import numpy as np
import time

# -------------------------------
# Config
# -------------------------------
LOG_GROUP = "/aws/vpc/ddos-flowlogs"
MODEL_PATH = "ddos_model.pkl"

# -------------------------------
# Load Model
# -------------------------------
model = joblib.load(MODEL_PATH)
print("Model loaded")

# -------------------------------
# CloudWatch Client
# -------------------------------
client = boto3.client("logs", region_name="ap-south-1")

# -------------------------------
# Get Log Streams
# -------------------------------
streams = client.describe_log_streams(
    logGroupName=LOG_GROUP,
    orderBy="LastEventTime",
    descending=True,
    limit=1
)

log_stream = streams["logStreams"][0]["logStreamName"]

print("Monitoring stream:", log_stream)

# -------------------------------
# Poll Logs Continuously
# -------------------------------
while True:

    response = client.get_log_events(
        logGroupName=LOG_GROUP,
        logStreamName=log_stream,
        startFromHead=False
    )

    for event in response["events"]:

        message = event["message"]

        # Parse log line
        fields = message.split()

        if len(fields) < 14:
            continue

        # Extract features
        packets = int(fields[9])
        bytes_ = int(fields[10])
        protocol = int(fields[8])

        if packets == 0:
            packets = 1

        byte_per_packet = bytes_ / packets

        is_tcp  = 1 if protocol == 6 else 0
        is_udp  = 1 if protocol == 17 else 0
        is_icmp = 1 if protocol == 1 else 0

        features = np.array([[
            packets,
            bytes_,
            byte_per_packet,
            is_tcp,
            is_udp,
            is_icmp
        ]])

        prediction = model.predict(features)[0]

        if prediction == 1:
            print("🚨 DDoS ATTACK DETECTED 🚨")
        else:
            print("Normal traffic")

    time.sleep(10)  # Poll every 10 sec
