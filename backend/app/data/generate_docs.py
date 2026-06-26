import os
import json

# Ensure directories exist
os.makedirs("c:/Users/adars/OneDrive/Desktop/AI-Crisis-War-Room/backend/app/data/documents", exist_ok=True)

CATEGORIES = {
    "Cybersecurity": [
        "Ransomware Infection response playbook: Isolate affected hosts, block SMB traffic, verify backups, identify strain, prepare decryptor, establish operations checkpoint.",
        "Phishing Attack response checklist: Scan mail server logs, reset compromised credentials, configure MFA rules, run email containment scripts, notify users.",
        "SQL Injection exploit remediation: Review application logs, identify vulnerable endpoints, sanitize queries using parameterized parameters, patch database permissions.",
        "DDoS Attack mitigation: Route traffic through scrubbers, configure rate limits, block malicious IPs, coordinate with upstream ISPs, implement CDN caching.",
        "Insider Threat containment guidelines: Revoke account access keys, review active sessions, audit file access logs, coordinate with HR and legal counsel.",
        "API Security Exploit response: Revoke compromised API keys, rate limit endpoint, implement JWT validation checks, audit recent requests for data leakage.",
        "Supply Chain Software exploit: Identify vendor dependency, verify file checksums, rollback to last secure version, audit internal build pipelines.",
        "Zero-day Exploit emergency patch: Configure Web Application Firewall (WAF) rule to block payload, contact software vendor, isolate impacted systems.",
        "Unauthorized Server Access response: Revoke SSH keys, analyze system auth logs, reinstall compromised system images, audit administrative access routes.",
        "Session Hijacking mitigation: Shorten session token lifetimes, force token resets, implement user-agent validation, audit cookie configuration flags.",
        "Malware outbreak playbook: Run endpoint detection and response (EDR) scans, quarantine infected assets, inspect network traffic for command and control (C2).",
        "Key/Secret Exposure response: Rotate leaked credentials on cloud services, audit cloud trail logs for unauthorized actions, update configuration variables.",
        "Brute Force attack defense: Implement account lockout policy, set up IP-based rate limiting, configure CAPTCHA, notify targeted users of login attempts.",
        "Logic Bomb investigation: Review source code commits, verify author credentials, isolate system containing suspicious code, run rollback scripts.",
        "Domain Hijacking recovery: Contact domain registrar, verify DNS records, reset registrar account credentials, activate registry lock services.",
        "Cloud Storage Bucket Exposure response: Set bucket permissions to private, review bucket access logs for downloads, check search indexes for leaks.",
        "SSL/TLS Certificate Expiration recovery: Generate new certificate signing request (CSR), deploy cert to load balancers, audit certificate expiry monitoring.",
        "Router/Switch Compromise guide: Reset device admin credentials, load last verified firmware image, review routing tables, inspect device syslog.",
        "Credential Stuffing incident response: Force password reset for impacted user accounts, block automated traffic, send security notification emails.",
        "Man-in-the-Middle attack mitigation: Force HTTPS encryption, check local network ARP tables for spoofing, install corporate network monitoring tools."
    ],
    "Data_Breach": [
        "Customer PII Exposure guidelines: Conduct forensic investigation, assess number of records leaked, prepare database containment, notify regulatory bodies.",
        "Credit Card Data Leak protocol: Notify merchant processor, engage PCI forensic investigator, rotate encryption keys, inform affected consumers.",
        "Health Records Exposure response: Verify HIPAA disclosure requirements, report leak to HHS within required timeline, establish toll-free customer hotline.",
        "Employee SSN Leaked document: Isolate HR database, offer identity theft protection services, issue formal notice letter, audit internal HR database access.",
        "Source Code Theft playbook: Audit GitHub repository access, rotate all hardcoded API keys, scan code for intellectual property markers.",
        "Tax Records Exposure guidelines: Audit payroll systems, notify state/federal tax agencies, offer tax fraud protection monitoring to affected employees.",
        "CRM System Breach response: Audit Salesforce logs, review export histories, revoke unauthorized integration tokens, notify account managers.",
        "Password Database Leak action plan: Force password reset for all users, update password hashing algorithm to bcrypt, write client warning notification.",
        "Marketing Email List Leak guidelines: Review marketing system access logs, verify unsubscribe lists, notify subscribers of email spoofing risk.",
        "Lost Physical Backup Drive protocol: Verify encryption status of disk, identify file categories on drive, report loss to compliance officer.",
        "Dark Web Database Dump verification: Fetch sample dump, compare schemas with live database, identify leak timeframe, audit database write logs.",
        "Client Billing Information Leak response: Mask bank account digits, revoke administrative tokens, inform corporate clients, review payment service logs.",
        "Proprietary Business Secret Theft guidelines: Revoke employee permissions, audit document access logs, coordinate with litigation legal counsel.",
        "Executive Payroll Data exposure response: Lock HR software, notify impacted executives, review executive login histories, check payroll export rules.",
        "Vendor Data Exposure notification process: Identify which third-party systems were compromised, review data sharing contracts, request vendor security audit.",
        "Data Sanitization failure response: Identify disposed hardware, review drive wiping logs, audit hardware disposal contracts, check data privacy regulations.",
        "Web Form Data Leak remediation: Inspect web server logs, fix HTML form parameters, sanitize public server variables, alert affected users.",
        "Mobile App Log Leak guidelines: Review logging configurations, release urgent app store patch, force update on app clients, audit logs for PII.",
        "API Response Data Leaks audit: Check JSON output sanitization rules, filter nested schemas, implement fields level access control keys.",
        "Contract Database Exposure protocol: Seal sharepoint site permissions, review contract download counts, check external file sharing settings."
    ],
    "Service_Outage": [
        "DNS Resolution Failure playbook: Switch to secondary provider, flush local DNS caches, verify zone files, monitor TTL expiration cycles.",
        "Primary Database Crash response: Verify replication lag, promote read-replica to primary, restart database instances, run file system consistency check.",
        "Cloud Provider Region Outage: Trigger DNS failover to backup region, verify multi-region database replication, start standby app servers.",
        "ISP Datacenter Network Outage: Route network traffic through alternate fiber line, coordinate with BGP routing provider, monitor latency stats.",
        "Power Outage in Datacenter protocol: Verify generator fuel levels, inspect UPS battery systems, shut down non-critical servers, monitor temperature.",
        "Content Delivery Network (CDN) Outage: Update DNS to bypass CDN, route requests directly to origin servers, implement client rate limits.",
        "Message Queue Consumer Lock recovery: Clear dead letter queue, restart queue consumer worker nodes, scale up consumer instances.",
        "Caching Server Memory Leak fix: Flush Redis cache, allocate more memory resources, restart cache instances, optimize cache eviction policy.",
        "Storage Cluster Disk Corruption: Run storage repair script, replace failed NVMe drives, rebuild RAID array, verify backup snapshot integrity.",
        "Load Balancer Crash response: Re-route traffic to secondary load balancer, check load balancer health checks, review active connection count.",
        "Auto-Scale Failure recovery: Manually provision server instances, audit cloud provider quota limit, review auto-scaling CPU metric thresholds.",
        "Third-Party Authentication API Down: Enable fallback local logins, display downtime banner, retry auth requests with backoff.",
        "Server CPU Overload incident: Terminate runaway processes, scale up server specs, restrict heavy API endpoints, review application profiling.",
        "Microservices Latency Storm fix: Enable circuit breaker rules, configure query timeouts, scale slow service instances, profile network calls.",
        "Database Connection Pool Exhaustion: Increase pool size limits, close idle connections, implement query pagination, verify query indexes.",
        "Payment Gateway API Outage: Queue checkout transactions, display payment alert message, retry transactions asynchronously.",
        "Storage Bucket Access Denied incident: Review AWS IAM policy rules, verify bucket resource policy, refresh API access credentials.",
        "SMTP Email Server Down response: Queue notification emails, switch to fallback email vendor, monitor email delivery backlog.",
        "Container Orchestrator Cluster Down: Restart Kubernetes control plane, check node status, redeploy deployment configs, audit cluster logs.",
        "Search Index Failure response: Rebuild Elasticsearch index, route search requests to database, limit query complex filters."
    ],
    "PR_Reputation": [
        "CEO Social Media controversy response: Draft executive statement, brief public relations agency, restrict corporate media posts.",
        "Executive Fraud Charges playbook: Stand up crisis comms committee, coordinate with legal counsel, prepare statement, assign interim leader.",
        "Product Safety Recall procedure: Identify batch numbers, publish recall warning page, notify distributors, establish refund portal.",
        "Activist Boycott coordination: Monitor social media sentiment, draft stakeholder letter, organize roundtable discussion.",
        "Insider Trading Rumors statement: Formulate official denial statement, cooperate with regulatory audit, review internal trading rules.",
        "Toxic Work Culture Expose response: Initiate independent HR investigation, draft employee address letter, outline workplace changes.",
        "Greenwashing Accusations strategy: Publish sustainability audit report, update carbon footprint data, issue clarifying press release.",
        "SLA Breach Lawsuit communications: Restrict internal discussions, draft holding statement, brief customer account managers.",
        "Negative Viral Review mitigation: Contact reviewer, investigate complaint details, post public response, implement product fix.",
        "Product Defect Scandal response: Halt product shipments, investigate QA testing logs, issue replacement warranty statement.",
        "Supply Chain Labor Dispute response: Audit supplier facility, issue corporate vendor code statement, update press statement.",
        "Executive Resignation Scandal protocol: Prepare press release, outline transition plan, brief institutional investors.",
        "Financial Misstatement rumors response: Issue audited balance sheet, schedule press briefing, brief institutional investors.",
        "Customer Service Outrage response: Apologize to users, explain root cause, issue service credits, post technical post-mortem.",
        "Marketing Campaign Backlash response: Withdraw ad materials, publish public apology, review future marketing assets.",
        "Partnership termination scandal: Issue joint termination statement, address supply chain impact, reassure major customers.",
        "Competitor Hostile Attack response: Fact check claims, draft customer support document, monitor industry forum boards.",
        "Regulatory Fine public response: Draft compliance correction plan, publish statement, outline governance enhancements.",
        "Security Disclosure public announcement: Draft vulnerability report, release software patch details, credit security researcher.",
        "Systemic Service Outage apology: Send CEO email apology, offer SLA service refunds, publish full technical post-mortem."
    ],
    "Frameworks_Guidelines": [
        "NIST SP 800-61 incident handler: Incident response phases: Preparation, Detection, Containment, Eradication, Recovery, Post-Incident.",
        "ISO 22301 Business Continuity Standard: Establish business impact analysis, identify critical assets, set recovery time objectives.",
        "Disaster Recovery Planning template: Outline recovery teams, define failover triggers, detail data restore steps, test schedules.",
        "Incident Command System roles: Incident Commander, Public Information Officer, Safety Officer, Operations Section Chief.",
        "Crisis Communications Playbook: Establish media contact list, write template statements, set approval flow, review social media.",
        "Post-Mortem Review template: Document root cause, timeline of events, containment time, corrective actions, prevention plan.",
        "Board Briefing guidelines: Summarize incident, outline business impact, list mitigation steps, present legal/reputational risks.",
        "Regulator Notification rules: GDPR 72-hour reporting rule, identify data types leaked, complete regulatory forms.",
        "Litigation Hold Notice template: Instruct staff to preserve emails, log files, backups, and physical documents.",
        "Emergency Communication tree: Define cascade rules, maintain phone directories, configure SMS alert broadcasts.",
        "Incident Triage Matrix: Define P0 to P3 priority levels based on business impact, system downtime, and data loss severity.",
        "Third-party Vendor Audits checklist: Verify SOC2 compliance, check data encryption at rest, audit network access rules.",
        "Tabletop Crisis Exercise guide: Scenario injects, role play assignments, post-exercise review, update crisis playbooks.",
        "Business Impact Analysis (BIA) guide: Identify revenue loss per hour, estimate regulatory fines, evaluate brand damage.",
        "Eradication and Recovery phase details: Delete malware binaries, rebuild OS from golden image, restore database backup.",
        "Stakeholder Notification timelines: Customers within 48h, board within 4h, media within 12h, insurers within 24h.",
        "Incident Response Team Training plan: Run monthly workshops, practice phishing triage, review latest CVE exploits.",
        "Evidence Preservation standard: Write MD5 hashes of log files, create disk sector images, maintain chain of custody.",
        "Disaster Recovery Test Schedule: Run quarterly failovers to standby datacenter, measure recovery point objectives (RPO).",
        "Public Relations Holding Statements: Standard templates for cyber attacks, outages, recalls, executive changes."
    ]
}

# Write 100 files
doc_index = 1
for category, docs in CATEGORIES.items():
    for doc in docs:
        file_path = f"c:/Users/adars/OneDrive/Desktop/AI-Crisis-War-Room/backend/app/data/documents/doc_{doc_index:03d}.txt"
        content = {
            "title": f"Playbook Document {doc_index:03d}: {category} Guide",
            "category": category,
            "id": f"doc_{doc_index:03d}",
            "text": doc
        }
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"Title: {content['title']}\n")
            f.write(f"Category: {content['category']}\n")
            f.write(f"Document ID: {content['id']}\n")
            f.write(f"Content: {content['text']}\n")
        doc_index += 1

print(f"Generated {doc_index-1} crisis document files successfully.")
