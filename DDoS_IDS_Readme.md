
# AI‑Driven DDoS Detection System — AWS Deployment Runbook

This README explains how to restart and run the entire system after shutdown, from EC2 boot → API → real traffic detection.

---

# 🧭 System Architecture

Internet Traffic  
→ AWS VPC Flow Logs  
→ CloudWatch Logs  
→ Flow Parser Script  
→ Flask ML API  
→ Random Forest Model  
→ Prediction / Alerts  

---

# 🔁 FULL RESTART PLAYBOOK

Follow these steps in order whenever the server is stopped or rebooted.

---

## 1️⃣ Start EC2 Instance

AWS Console → EC2 → Instances → Select Instance → **Start**

Wait until:

- Instance State → Running  
- Status Checks → 2/2 Passed  

---

## 2️⃣ SSH Into EC2

From PowerShell / Terminal:

```bash
cd Downloads
ssh -i Aarit.pem ubuntu@13.235.23.114
```

---

## 3️⃣ Activate Virtual Environment

```bash
source ddos-env/bin/activate
```

Prompt should change to:

```
(ddos-env) ubuntu@ip-xxx:~$
```

---

## 4️⃣ Verify Project Files

```bash
ls
```

You should see:

```
app.py
flow_parser.py
ddos_rf_model.pkl
scaler.pkl
ddos-env/
```

---

## 5️⃣ Start Flask IDS API

```bash
python app.py
```

Expected output:

```
Running on http://0.0.0.0:5000
```

Browser test:

```
http://13.235.23.114:5000
```

---

## 6️⃣ Start Real Traffic Parser (New Terminal)

Open second SSH session:

```bash
ssh -i Aarit.pem ubuntu@13.235.23.114
source ddos-env/bin/activate
python flow_parser.py
```

Now real AWS traffic is being analyzed.

---

# 🧪 TEST PREDICTION MANUALLY

```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"features":[0,0,0,...77 values]}'
```

---

# 📡 ENABLE REAL TRAFFIC LOGGING (ONE‑TIME SETUP)

1. AWS → VPC → Flow Logs → Create  
2. Filter → ALL  
3. Destination → CloudWatch  
4. Attach IAM Role → CloudWatchReadOnlyAccess  

---

# ⚙️ OPTIONAL — RUN IN BACKGROUND

```bash
nohup python app.py &
nohup python flow_parser.py &
```

---

# 🔌 STOP SYSTEM

```bash
CTRL + C
deactivate
exit
```

Then stop EC2 from console.

---

# 📊 PROJECT CAPABILITIES

✔ AI DDoS Detection  
✔ Cloud Deployment  
✔ REST API Inference  
✔ Real Traffic Monitoring  
✔ Scalable AWS Architecture  

---

# 🚀 FUTURE EXTENSIONS

- SNS Phone Alerts  
- Auto‑blocking IPs  
- Dashboard Visualization  
- Gunicorn + Nginx Production Server  
- WAF Integration  

---

**Author:** Aarit  
**Project:** AI‑Driven Cloud IDS on AWS
