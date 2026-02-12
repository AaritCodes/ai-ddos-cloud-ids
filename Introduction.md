# AI-Driven Real-Time DDoS Detection System (AWS + Machine Learning)

## 📌 Project Overview

This project implements an **AI-powered real-time DDoS detection system** using AWS cloud network telemetry and machine learning.

The system ingests live VPC traffic logs, converts them into structured datasets, trains a classification model, and deploys it to detect anomalous traffic patterns in real time.

It demonstrates the integration of:

* Cloud Security Monitoring
* Network Traffic Analysis
* Machine Learning Classification
* Real-Time Log Ingestion
* Detection & Alerting Pipelines

---

## 🧠 Problem Statement

Distributed Denial of Service (DDoS) attacks overwhelm cloud infrastructure by flooding network resources.

Traditional detection approaches rely on static thresholds or signature-based IDS systems.

This project explores:

> How machine learning can detect anomalous traffic behavior using cloud flow telemetry in real time.

---

## 🏗️ System Architecture

```
AWS VPC Traffic
        ↓
VPC Flow Logs
        ↓
CloudWatch Log Groups
        ↓
Live Ingestion Script (boto3)
        ↓
Feature Extraction Engine
        ↓
ML Model (Random Forest)
        ↓
Prediction Output
        ↓
Alert System (Email/SNS – Optional)
```

---

## ⚙️ Technology Stack

| Layer             | Tools / Services              |
| ----------------- | ----------------------------- |
| Cloud             | AWS VPC, CloudWatch, EC2, IAM |
| Data Processing   | Python, Pandas, NumPy         |
| Machine Learning  | Scikit-learn                  |
| Deployment        | Flask API, EC2                |
| Ingestion         | boto3                         |
| Serialization     | Joblib                        |
| Training Platform | Kaggle Notebooks              |

---

## 📊 Dataset Source

Dataset was engineered from **AWS VPC Flow Logs**, which contain network telemetry such as:

* Source / Destination IP
* Ports
* Protocol
* Packet count
* Byte count
* Traffic action

Unlike static public datasets, this project uses **real cloud traffic data**.

---

## 🛠️ Project Pipeline

### 1️⃣ Log Collection

* Enabled VPC Flow Logs
* Configured delivery to CloudWatch
* Exported historical logs to S3 for training

---

### 2️⃣ Log Parsing & Dataset Creation

Script: `convert_logs.py`

Converts raw AWS flow logs → structured CSV dataset.

Key tasks:

* Line parsing
* Column mapping
* Data structuring
* CSV generation

Output:

```
dataset.csv
```

---

### 3️⃣ Data Preprocessing

Performed:

* Missing value handling (`-`)
* Type conversion
* Feature selection
* Traffic aggregation

Engineered features include:

* Packets
* Bytes
* Ports
* Protocol
* Duration

---

### 4️⃣ Label Engineering

Traffic labeled based on behavioral thresholds.

Example logic:

```
High packet bursts → Attack
Normal volume → Benign
```

---

### 5️⃣ Model Training (Kaggle)

Notebook trained using:

```
RandomForestClassifier
```

Steps:

* Train/Test split
* Feature scaling
* Model fitting
* Evaluation metrics

Evaluation included:

* Accuracy
* Precision
* Recall
* F1-Score
* Confusion Matrix

---

### 6️⃣ Model Serialization

Exported trained artifacts:

```
ddos_model.pkl
scaler.pkl
```

This enables inference without retraining.

---

### 7️⃣ Flask API Deployment

File: `app.py`

Provides REST inference endpoint.

Endpoint:

```
POST /predict
```

Input:

```json
{
  "features": [packets, bytes, srcport, dstport, protocol]
}
```

Output:

```json
{
  "prediction": 0,
  "probability": [0.98, 0.02]
}
```

---

### 8️⃣ Real-Time Log Ingestion

Script: `live_ingest.py`

Capabilities:

* Connects to CloudWatch via boto3
* Streams live flow logs
* Extracts features
* Runs ML inference
* Outputs detection results

Example console output:

```
Monitoring stream: eni-xxxx
Normal traffic
```

---

### 9️⃣ Cloud Deployment (EC2)

Deployed ingestion engine on AWS EC2:

Steps:

* Instance provisioning
* SSH access
* SCP project transfer
* Virtual environment setup
* Dependency installation
* Continuous monitoring execution

This enables **24×7 real-time detection**.

---

## 🚨 Alerting System (In Progress / Optional)

Detection triggers alerts via:

* Email (SMTP)
* AWS SNS
* Webhooks (future)

Example trigger:

```
If prediction == Attack → Send alert
```

---

## 📁 Project Structure

```
project/
│
├── dataset.csv
├── convert_logs.py
├── model_training.py
├── live_ingest.py
├── app.py
│
├── models/
│   ├── ddos_model.pkl
│   └── scaler.pkl
│
├── src/
│   ├── api/
│   ├── parser/
│   └── training/
│
└── README.md
```

---

## ▶️ How To Run

### 1️⃣ Clone Repo

```bash
git clone <repo_url>
cd project
```

---

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install boto3 pandas numpy scikit-learn flask joblib
```

---

### 4️⃣ Train Model

```bash
python model_training.py
```

---

### 5️⃣ Run API

```bash
python app.py
```

---

### 6️⃣ Run Live Ingestion

```bash
python live_ingest.py
```

---

## 📈 Results

* Successfully classified live VPC traffic
* Achieved high accuracy on test data
* Real-time inference operational
* Cloud deployment validated

---

## ⚠️ Limitations

* Dataset imbalance (few attack samples)
* Flow-level detection (not packet payload)
* No automated mitigation yet

---

## 🚀 Future Enhancements

Planned upgrades:

* Balanced dataset via attack simulation
* Auto IP blocking via Security Groups
* AWS WAF integration
* SNS / Slack alerting
* SOC dashboard visualization
* Packet-level IDS integration

---

## 🎓 Learning Outcomes

This project demonstrates applied skills in:

* Cloud security monitoring
* Network traffic analysis
* Machine learning deployment
* Real-time log ingestion
* AWS infrastructure engineering

---

## 📜 License

MIT License — free to use for academic and research purposes.

---

## 👤 Author

**Aarit Haldar**
B.Tech Cyber Security Engineering

---

## ⭐ Acknowledgment

Built as an academic research & cybersecurity engineering project exploring AI-driven threat detection in cloud environments.

---
