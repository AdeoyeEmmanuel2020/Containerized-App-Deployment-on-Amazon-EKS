
## Enterprise Container Platform on Amazon EKS: Production Orchestration
**Role**: Solution Architect

**Status**: ✅ Architecture Designed, Deployed & Validated

### **Project Description**

*Architected and implemented a production-ready container orchestration platform on Amazon EKS, demonstrating end-to-end cloud-native deployment from Docker containerisation to Kubernetes orchestration with AWS managed services integration. Engineered for enterprise scalability, reliability, and cost optimisation with complete lifecycle management*

---

## Architecture Overview
<img width="800" height="500" alt="Architecture" src="https://github.com/user-attachments/assets/46a0cc02-8295-4e69-8b4c-01b3c7fb0192" />

---

## 🎬 Architecture Walkthrough & Live Deployment Video  

🚀 **Click the picture below to watch the full deployment on YouTube**

<a href="https://www.youtube.com/watch?v=imz9tSa3WVg" target="_blank">
  <img src="https://img.youtube.com/vi/imz9tSa3WVg/maxresdefault.jpg" 
       width="800" 
       height="500" 
       alt="Complete Kubernetes Deployment on AWS EKS (Production Ready)">
</a>

----


----
## Real-World Scenario: Troubleshooting ImagePullBackOff

### 🚨 Challenge Encountered
During deployment, Kubernetes reported: `ErrImagePull - Image not found`
- Pod status: `ImagePullBackOff`
- Error: Container image unavailable from ECR

### 🔍 Diagnostic Process
1. **Kubernetes State Analysis**: Identified `ImagePullBackOff` status
2. **AWS ECR Verification**: Checked repository existence and image availability
3. **Authentication Validation**: Verified IAM permissions and Docker credentials
4. **Network Connectivity**: Ensured EKS nodes could reach ECR

### 🛠️ Resolution Steps
- Re-authenticated Docker with ECR: `aws ecr get-login-password`
- Verified image tagging format
- Re-pushed Docker image to ECR
- Kubernetes automatically recovered pods (self-healing demonstrated)

### 🎯 Skills Demonstrated
- **Cross-Service Troubleshooting**: EKS ↔ ECR ↔ IAM integration issues
- **Production Incident Response**: Systematic diagnosis methodology
- **Cloud-Native Understanding**: AWS service dependencies and timing
- **Operational Excellence**: Health checks maintained throughout incident

### 💡 Key Learning
This "failure" scenario actually **enhances** the demonstration by showcasing:
- Real-world cloud deployment challenges
- Professional troubleshooting methodology
- The importance of understanding AWS service interactions
- That production systems require robust error handling

## 🔗 Full Documentation & Demo
📚 Complete Project Documentation: [[Notion Page Link]](https://www.notion.so/Enterprise-Container-Platform-on-Amazon-EKS-Production-Orchestration-2c5afa903f8a80f5b3fee9cb8aa946c0?source=copy_link)

🎥 Video Demonstration: [[Video Demo Link]](https://youtu.be/imz9tSa3WVg?si=orUGleOmmzUTz4ET)

💻 Source Code: [[GitHub Repository Link]](https://github.com/DOTWEB2020/Containerized-App-Deployment-on-Amazon-EKS)

## **👤** Author
**Adeoye Emmanuel** - Solution Architect

**Email:** Emmanuelofgrace@gmail.com

💼 LinkedIn: [[LinkedIn Profile]](www.linkedin.com/in/emmanuel-adeoye-29187bb7)

