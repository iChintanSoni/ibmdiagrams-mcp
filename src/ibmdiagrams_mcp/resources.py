"""
IBM Diagrams MCP Server - Resources
Contains all resource implementations for the MCP server.
"""


def quickstart_guide() -> str:
    """Quick-start guide for building IBM Cloud diagrams."""
    return """\
# IBM Cloud Diagrams — Quick Start

## Installation
The ibmdiagrams package must be available in your Python environment.

## Basic Pattern
```python
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet, AvailabilityZone
from ibmdiagrams.ibmcloud.compute import VirtualServer
from ibmdiagrams.ibmcloud.network import LoadBalancer

with IBMDiagram(name="My Diagram", output="/tmp"):
    with IBMCloud("IBM Cloud"):
        with VPC("prod-vpc", sublabel="10.0.0.0/16"):
            with AvailabilityZone("us-south-1"):
                with Subnet("app-subnet", sublabel="10.0.1.0/24"):
                    lb = LoadBalancer("app-lb")
                    vsi = VirtualServer("app-vsi")
    lb >> vsi
```

## Key Rules
1. Groups are Python context managers (`with Group(...): ...`)
2. Items are instantiated directly (`vsi = VirtualServer("name")`)
3. Connections use operators: `a - b`, `a >> b`, `a << b`
4. `output=` sets the directory for the .drawio file
5. `direction='LR'` (default) or `'TB'` controls layout direction

## Component Categories
- **groups_core**: IBMCloud, VPC, Subnet, Region, AvailabilityZone, ...
- **groups_control**: SecurityGroup, ResourceGroup, AccessGroup, ...
- **compute**: VirtualServer, BareMetalServer, PowerVirtualServer, ...
- **network**: LoadBalancer, TransitGateway, PublicGateway, FloatingIP, ...
- **storage**: ObjectStorage, BlockStorage, FileStorage, ...
- **data**: Db2, PostgreSQL, Redis, MongoDB, EventStreams, ...
- **security**: VPNGateway, KeyProtect, SecretsManager, BastionHost, ...
- **containers**: OpenShift, KubernetesService, ContainerRegistry, ...
- **ai**: watsonxAI, watsonxData, watsonxGovernance, WatsonStudio, ...
- **devops**: ContinuousDelivery, Toolchain, MQ, GitLab, ...
- **observability**: CloudLogs, FlowLogs, Monitoring
- **actors**: User, Users, Enterprise, Application, WebApplication

Use `list_components()` for a full catalog with import paths.
Use `get_example(name=...)` for ready-to-run examples.
Use `generate_diagram(code=...)` to produce a .drawio file.
"""


def terraform_guide() -> str:
    """Comprehensive guide for converting Terraform to IBM Cloud diagrams."""
    return """\
# Terraform to Diagram Guide

## Overview
Convert Terraform state files to IBM Cloud architecture diagrams automatically.
This feature analyzes your infrastructure-as-code and generates visual representations
following IBM Diagram Standards.

## Quick Start

### 1. Export Terraform State
```bash
# Export state to JSON format
terraform show -json > infrastructure.tfstate
```

### 2. Generate Diagram
Use the `generate_from_terraform` tool with the JSON content:
- **tfstate_content**: The JSON content from terraform show
- **label_type**: "custom" (detailed labels) or "general" (simplified)
- **output_dir**: Where to save the .drawio file (optional)

### 3. View Result
Open the generated .drawio file in draw.io desktop or web application.

## Label Types

### Custom Labels (Recommended)
- Shows detailed resource information
- Includes IDs, CIDR blocks, and configuration details
- Best for documentation and detailed architecture reviews
- Example: "my-vpc (vpc-123abc, 10.0.0.0/16)"

### General Labels
- Shows simplified, human-readable names
- Cleaner appearance for presentations
- Best for high-level architecture diagrams
- Example: "my-vpc"

## Supported Resources

### Networking
- **VPCs**: Virtual Private Clouds with CIDR blocks
- **Subnets**: Subnet configurations across availability zones
- **Load Balancers**: Application and Network Load Balancers
- **Public Gateways**: Internet connectivity for private subnets
- **Floating IPs**: Public IP addresses
- **VPN Gateways**: Site-to-site VPN connections
- **VPE Gateways**: Virtual Private Endpoints for private connectivity
- **Transit Gateways**: Multi-VPC connectivity
- **Security Groups**: Instance-level firewall rules
- **Network ACLs**: Subnet-level firewall rules

### Compute
- **Virtual Servers**: VPC virtual server instances
- **Bare Metal Servers**: Dedicated physical servers
- **Instance Groups**: Auto-scaling groups

### Storage
- **Block Storage**: Persistent block storage volumes
- **Object Storage**: Cloud Object Storage buckets
- **File Storage**: NFS file shares

### Containers
- **OpenShift Clusters**: Red Hat OpenShift on IBM Cloud
- **Kubernetes Clusters**: IBM Kubernetes Service

### Data & AI
- **Databases**: Managed database services (Db2, PostgreSQL, etc.)
- **Event Streams**: Apache Kafka service

## Best Practices

### 1. Clean State Files
Ensure your Terraform state is up-to-date:
```bash
terraform refresh
terraform show -json > current-state.tfstate
```

### 2. Multi-Region Architectures
If you have resources in multiple regions, generate separate diagrams
per region for clarity, or use a single diagram with Region groups.

### 3. Large Infrastructures
For complex infrastructures with many resources:
- Consider filtering by resource group or tags
- Generate multiple diagrams for different layers (network, compute, data)
- Use general labels for overview diagrams

### 4. Version Control
Store generated diagrams alongside your Terraform code:
```
infrastructure/
├── main.tf
├── variables.tf
├── terraform.tfstate
└── diagrams/
    ├── architecture.drawio
    └── architecture.png
```

## Example Workflow

```python
# 1. Read Terraform state
with open('infrastructure.tfstate', 'r') as f:
    tfstate_content = f.read()

# 2. Generate diagram with custom labels
result = generate_from_terraform(
    tfstate_content=tfstate_content,
    label_type="custom",
    output_dir="./diagrams"
)

# 3. Check result
print(result)  # Shows file path and resource summary
```

## Troubleshooting

### "No resources found"
- Verify the tfstate file contains resources
- Check that resources are supported types
- Ensure JSON format is valid

### "Missing VPC or Subnet"
- Terraform state must include VPC and at least one subnet
- These are required for diagram generation

### "Timeout error"
- Large infrastructures may take longer
- Consider breaking into smaller diagrams
- Increase timeout if needed

## Advanced Usage

### Combining with Python Code
After generating from Terraform, you can enhance the diagram:

1. Generate base diagram from Terraform
2. Use `validate_diagram_code` to check structure
3. Add additional components (monitoring, security layers)
4. Regenerate with enhanced code

### Integration with CI/CD
Automate diagram generation in your pipeline:
```yaml
- name: Generate Architecture Diagram
  run: |
    terraform show -json > state.tfstate
    python generate_diagram.py
```

## Related Tools
- `validate_diagram_code`: Validate Python diagram code
- `search_components`: Find specific IBM Cloud components
- `analyze_architecture`: Get recommendations for improvements
- `design_architecture`: Generate diagrams from descriptions

## Additional Resources
- IBM Cloud Terraform Provider: https://registry.terraform.io/providers/IBM-Cloud/ibm
- IBM Diagram Standards: https://www.ibm.com/design/language/infographics/technical-diagrams
- draw.io Desktop: https://www.diagrams.net/
"""


def best_practices_guide() -> str:
    """IBM Cloud architecture best practices guide."""
    return """\
# IBM Cloud Architecture Best Practices

## Network Design

### VPC Architecture
- **CIDR Planning**: Use non-overlapping CIDR blocks for VPCs (e.g., 10.0.0.0/16, 10.1.0.0/16)
- **Subnet Segmentation**: Separate public and private subnets
  - Public subnets: For load balancers, bastion hosts
  - Private subnets: For application servers, databases
- **Multi-Zone Deployment**: Deploy across 3 availability zones for maximum HA
- **Reserved IP Space**: Leave room for growth in each subnet

### Connectivity
- **VPN Gateway**: For secure site-to-site connectivity
- **Direct Link**: For dedicated, high-bandwidth connections
- **Transit Gateway**: For connecting multiple VPCs and on-premises networks
- **VPE Gateways**: For private connectivity to IBM Cloud services

## Security

### Defense in Depth
1. **Network Level**
   - Network ACLs for subnet-level filtering
   - Security Groups for instance-level filtering
   - Separate security groups by tier (web, app, data)

2. **Access Control**
   - Bastion Host for administrative access
   - VPN Gateway for remote user access
   - IAM policies following least privilege principle

3. **Data Protection**
   - Key Protect or HPCS for encryption key management
   - Secrets Manager for credentials and API keys
   - Encryption at rest and in transit

4. **Monitoring & Compliance**
   - Flow Logs for network traffic analysis
   - Cloud Logs for application and system logs
   - Security & Compliance Center for posture management

### Security Group Best Practices
- Create specific security groups per application tier
- Use descriptive names (e.g., "web-tier-sg", "app-tier-sg")
- Document rules with clear descriptions
- Follow principle of least privilege
- Regularly audit and remove unused rules

## High Availability

### Multi-Zone Architecture
```
Region (us-south)
├── Zone 1 (us-south-1)
│   ├── Subnet (10.0.1.0/24)
│   └── Virtual Servers (2)
├── Zone 2 (us-south-2)
│   ├── Subnet (10.0.2.0/24)
│   └── Virtual Servers (2)
└── Zone 3 (us-south-3)
    ├── Subnet (10.0.3.0/24)
    └── Virtual Servers (2)
```

### Load Balancing
- **Application Load Balancer**: For HTTP/HTTPS traffic
- **Network Load Balancer**: For TCP/UDP traffic
- **Global Load Balancer**: For multi-region deployments
- Configure health checks for automatic failover
- Distribute backend instances across zones

### Data Resilience
- Regular backups with retention policies
- Cross-region replication for critical data
- Point-in-time recovery capabilities
- Test disaster recovery procedures regularly

## Performance Optimization

### Compute
- Right-size virtual servers based on workload
- Use instance profiles optimized for workload type
- Consider reserved capacity for predictable workloads
- Implement auto-scaling for variable workloads

### Network
- Place resources close to users (multi-region if needed)
- Use CDN for static content delivery
- Optimize security group rules (fewer, broader rules perform better)
- Use VPE Gateways to avoid internet egress charges

### Storage
- Choose appropriate storage tier (hot, cool, cold)
- Use block storage for databases and applications
- Use object storage for backups and archives
- Implement lifecycle policies for cost optimization

## Cost Optimization

### Compute Savings
- **Reserved Capacity**: 20-30% savings for committed usage
- **Right-Sizing**: Monitor and adjust instance sizes
- **Auto-Scaling**: Scale down during low-demand periods
- **Spot Instances**: For fault-tolerant workloads

### Network Savings
- **VPE Gateways**: Avoid internet egress charges
- **Transit Gateway**: Consolidate inter-VPC traffic
- **Direct Link**: Lower cost for high-volume transfers
- **CDN**: Reduce origin server load and bandwidth

### Storage Savings
- **Lifecycle Policies**: Auto-transition to cheaper tiers
- **Compression**: Reduce storage footprint
- **Deduplication**: Eliminate redundant data
- **Regular Cleanup**: Remove unused volumes and snapshots

## Operational Excellence

### Monitoring & Observability
- **IBM Cloud Monitoring**: Metrics and dashboards
- **Cloud Logs**: Centralized log management
- **Flow Logs**: Network traffic analysis
- **Activity Tracker**: Audit trail for all actions

### Automation
- **Terraform**: Infrastructure as code
- **Ansible**: Configuration management
- **CI/CD Pipelines**: Automated deployments
- **Backup Automation**: Scheduled backups

### Documentation
- Maintain architecture diagrams (use ibmdiagrams!)
- Document security group rules and network flows
- Keep runbooks for common operations
- Track changes in version control

## Compliance & Governance

### Regulatory Requirements
- Understand data residency requirements
- Implement appropriate encryption standards
- Maintain audit logs for compliance
- Regular security assessments

### Resource Organization
- **Resource Groups**: Organize by environment or project
- **Tags**: For cost allocation and automation
- **Naming Conventions**: Consistent, descriptive names
- **Access Groups**: Role-based access control

## Common Anti-Patterns to Avoid

### ❌ Single Zone Deployment
**Problem**: No resilience to zone failures
**Solution**: Deploy across multiple zones

### ❌ Overly Permissive Security Groups
**Problem**: Increased attack surface
**Solution**: Follow least privilege principle

### ❌ No Monitoring or Logging
**Problem**: Blind to issues and security events
**Solution**: Implement comprehensive observability

### ❌ Hardcoded Credentials
**Problem**: Security risk, difficult to rotate
**Solution**: Use Secrets Manager

### ❌ No Backup Strategy
**Problem**: Data loss risk
**Solution**: Automated backups with tested recovery

### ❌ Ignoring Cost Optimization
**Problem**: Unnecessary cloud spend
**Solution**: Regular cost reviews and optimization

## Architecture Review Checklist

### Security ✓
- [ ] Security Groups configured
- [ ] Network ACLs implemented
- [ ] VPN or Direct Link for secure connectivity
- [ ] Encryption enabled (Key Protect/HPCS)
- [ ] Secrets Manager for credentials
- [ ] Bastion Host for admin access
- [ ] Flow Logs enabled
- [ ] Regular security audits

### High Availability ✓
- [ ] Multi-zone deployment (3 zones)
- [ ] Load balancer configured
- [ ] Health checks enabled
- [ ] Auto-scaling configured
- [ ] Backup and DR strategy
- [ ] Tested failover procedures

### Performance ✓
- [ ] Right-sized instances
- [ ] Appropriate storage tiers
- [ ] CDN for static content
- [ ] VPE Gateways for service access
- [ ] Monitoring and alerting

### Cost ✓
- [ ] Reserved capacity where applicable
- [ ] Auto-scaling to reduce waste
- [ ] Storage lifecycle policies
- [ ] Regular cost reviews
- [ ] Tagged resources for allocation

### Operations ✓
- [ ] Monitoring configured
- [ ] Centralized logging
- [ ] Automation in place
- [ ] Documentation current
- [ ] Runbooks available

## Additional Resources
- IBM Cloud Architecture Center: https://www.ibm.com/cloud/architecture
- IBM Cloud Security: https://www.ibm.com/cloud/security
- IBM Cloud Well-Architected Framework: https://www.ibm.com/cloud/architecture/architectures/
"""


def architecture_patterns_guide() -> str:
    """Common IBM Cloud architecture patterns catalog."""
    return """\
# IBM Cloud Architecture Patterns

## 1. Three-Tier Web Application

### Description
Classic web application with presentation, application, and data tiers.

### Components
- **Load Balancer**: Distributes traffic to web tier
- **Web Tier**: Frontend servers in public subnets
- **App Tier**: Application servers in private subnets
- **Data Tier**: Managed database service
- **Security**: Security groups per tier, VPN for admin access

### Use Cases
- E-commerce websites
- Content management systems
- Business applications

### Code Template
```python
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet, AvailabilityZone, SecurityGroup
from ibmdiagrams.ibmcloud.compute import VirtualServer
from ibmdiagrams.ibmcloud.network import LoadBalancer
from ibmdiagrams.ibmcloud.data import PostgreSQL

with IBMDiagram(name="Three-Tier App", output="/tmp"):
    with IBMCloud("IBM Cloud"):
        with VPC("app-vpc", sublabel="10.0.0.0/16"):
            with AvailabilityZone("us-south-1"):
                with Subnet("web-subnet", sublabel="10.0.1.0/24"):
                    with SecurityGroup("web-sg"):
                        lb = LoadBalancer("app-lb")
                        web1 = VirtualServer("web-1")
                with Subnet("app-subnet", sublabel="10.0.2.0/24"):
                    with SecurityGroup("app-sg"):
                        app1 = VirtualServer("app-1")
                with Subnet("data-subnet", sublabel="10.0.3.0/24"):
                    with SecurityGroup("db-sg"):
                        db = PostgreSQL("app-db")
    
    lb >> web1 >> app1 >> db
```

## 2. Microservices on OpenShift

### Description
Container-based microservices architecture using Red Hat OpenShift.

### Components
- **OpenShift Cluster**: Container orchestration platform
- **Container Registry**: Private image registry
- **CI/CD Pipeline**: Automated build and deployment
- **Service Mesh**: Inter-service communication
- **Monitoring**: Observability stack

### Use Cases
- Cloud-native applications
- API-driven architectures
- DevOps environments

### Code Template
```python
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet, OpenShift as OpenShiftGroup
from ibmdiagrams.ibmcloud.containers import OpenShift, ContainerRegistry
from ibmdiagrams.ibmcloud.devops import ContinuousDelivery, Toolchain
from ibmdiagrams.ibmcloud.network import LoadBalancer
from ibmdiagrams.ibmcloud.observability import Monitoring, CloudLogs

with IBMDiagram(name="Microservices", output="/tmp"):
    with IBMCloud("IBM Cloud"):
        with VPC("ocp-vpc"):
            with Subnet("worker-subnet"):
                with OpenShiftGroup("OpenShift Cluster"):
                    ocp = OpenShift("ROKS")
                    lb = LoadBalancer("ingress-lb")
        cr = ContainerRegistry("icr")
        cd = ContinuousDelivery("cd-service")
        tc = Toolchain("pipeline")
        mon = Monitoring("monitoring")
        logs = CloudLogs("logs")
    
    tc >> cr >> ocp
    ocp >> mon
    ocp >> logs
```

## 3. Data Lake Architecture

### Description
Scalable data analytics platform with data ingestion, storage, and processing.

### Components
- **Object Storage**: Data lake storage
- **watsonx.data**: Analytics engine
- **Event Streams**: Real-time data ingestion
- **Data Governance**: watsonx.governance
- **Security**: Encryption and access control

### Use Cases
- Big data analytics
- Machine learning pipelines
- Business intelligence

### Code Template
```python
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, watsonx
from ibmdiagrams.ibmcloud.ai import watsonxData, watsonxGovernance
from ibmdiagrams.ibmcloud.storage import ObjectStorage
from ibmdiagrams.ibmcloud.data import EventStreams
from ibmdiagrams.ibmcloud.security import KeyProtect

with IBMDiagram(name="Data Lake", output="/tmp"):
    with IBMCloud("IBM Cloud"):
        with watsonx("watsonx Platform"):
            wx_data = watsonxData("watsonx.data")
            wx_gov = watsonxGovernance("watsonx.governance")
        cos = ObjectStorage("data-lake")
        es = EventStreams("event-streams")
        kp = KeyProtect("key-protect")
    
    es >> cos >> wx_data
    wx_data >> wx_gov
    kp >> cos
```

## 4. Hybrid Cloud with VPN

### Description
Secure connection between on-premises infrastructure and IBM Cloud.

### Components
- **VPN Gateway**: Secure tunnel to on-premises
- **Transit Gateway**: Multi-VPC connectivity
- **Direct Link**: High-bandwidth alternative
- **Hybrid Workloads**: Distributed applications

### Use Cases
- Cloud migration
- Hybrid applications
- Disaster recovery

### Code Template
```python
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, EnterpriseNetwork
from ibmdiagrams.ibmcloud.security import VPNGateway
from ibmdiagrams.ibmcloud.network import TransitGateway
from ibmdiagrams.ibmcloud.compute import VirtualServer

with IBMDiagram(name="Hybrid Cloud", output="/tmp"):
    with IBMCloud("IBM Cloud"):
        with VPC("cloud-vpc"):
            vpn = VPNGateway("vpn-gw")
            vsi = VirtualServer("cloud-app")
        tgw = TransitGateway("transit-gw")
    
    with EnterpriseNetwork("On-Premises"):
        onprem = VirtualServer("onprem-app")
    
    onprem >> vpn >> tgw >> vsi
```

## 5. High Availability Multi-Zone

### Description
Resilient architecture distributed across multiple availability zones.

### Components
- **3 Availability Zones**: Maximum resilience
- **Load Balancer**: Traffic distribution
- **Auto-Scaling**: Dynamic capacity
- **Shared Storage**: Cross-zone data access

### Use Cases
- Mission-critical applications
- 24/7 services
- High-traffic websites

### Code Template
```python
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet, AvailabilityZone
from ibmdiagrams.ibmcloud.compute import VirtualServer
from ibmdiagrams.ibmcloud.network import LoadBalancer
from ibmdiagrams.ibmcloud.storage import FileStorage

with IBMDiagram(name="HA Multi-Zone", output="/tmp"):
    with IBMCloud("IBM Cloud"):
        with VPC("ha-vpc"):
            lb = LoadBalancer("global-lb")
            
            with AvailabilityZone("us-south-1"):
                with Subnet("subnet-1"):
                    vsi1 = VirtualServer("app-1")
            
            with AvailabilityZone("us-south-2"):
                with Subnet("subnet-2"):
                    vsi2 = VirtualServer("app-2")
            
            with AvailabilityZone("us-south-3"):
                with Subnet("subnet-3"):
                    vsi3 = VirtualServer("app-3")
            
            storage = FileStorage("shared-storage")
    
    lb >> vsi1
    lb >> vsi2
    lb >> vsi3
    vsi1 >> storage
    vsi2 >> storage
    vsi3 >> storage
```

## 6. Serverless Architecture

### Description
Event-driven architecture using IBM Cloud Functions.

### Components
- **Cloud Functions**: Serverless compute
- **API Gateway**: REST API management
- **Object Storage**: Event triggers
- **Event Streams**: Message queue

### Use Cases
- Event processing
- API backends
- Scheduled tasks

## 7. AI/ML Platform

### Description
Machine learning platform with training and inference capabilities.

### Components
- **watsonx.ai**: ML model training
- **Watson Studio**: Development environment
- **GPU Instances**: Training acceleration
- **Model Serving**: Inference endpoints

### Use Cases
- Machine learning projects
- AI application development
- Model training and deployment

## Pattern Selection Guide

### Choose Three-Tier When:
- Traditional web application
- Clear separation of concerns needed
- Moderate scalability requirements

### Choose Microservices When:
- Cloud-native development
- Independent service scaling needed
- DevOps culture in place

### Choose Data Lake When:
- Large-scale data analytics
- Multiple data sources
- Advanced analytics requirements

### Choose Hybrid Cloud When:
- Gradual cloud migration
- On-premises integration needed
- Regulatory requirements

### Choose HA Multi-Zone When:
- High availability critical
- Zero downtime required
- Mission-critical workloads

## Combining Patterns

Patterns can be combined for complex architectures:
- **Three-Tier + HA Multi-Zone**: Resilient web applications
- **Microservices + Data Lake**: Analytics-driven microservices
- **Hybrid Cloud + HA Multi-Zone**: Resilient hybrid applications

## Next Steps

1. Choose a pattern that matches your requirements
2. Customize the template for your specific needs
3. Use `validate_diagram_code()` to check your code
4. Use `analyze_architecture()` for recommendations
5. Generate and review your diagram
"""


def component_reference_guide() -> str:
    """Complete IBM Cloud component reference guide.

    Returns:
        Comprehensive reference documentation for all IBM Cloud components.
    """
    return """# IBM Cloud Component Reference Guide

Complete reference for all IBM Cloud components available in ibmdiagrams.

## Table of Contents

1. [Compute Components](#compute)
2. [Storage Components](#storage)
3. [Network Components](#network)
4. [Security Components](#security)
5. [Database Components](#database)
6. [Analytics Components](#analytics)
7. [AI/ML Components](#ai-ml)
8. [Integration Components](#integration)
9. [DevOps Components](#devops)
10. [Management Components](#management)
11. [Blockchain Components](#blockchain)
12. [IoT Components](#iot)
13. [Mobile Components](#mobile)
14. [Web Components](#web)

---

## Compute

### VirtualServer
**Purpose:** Virtual machine instances in IBM Cloud
**Usage:**
```python
from ibmdiagrams.ibm.compute import VirtualServer

with IBMDiagram("Compute Example"):
    vm = VirtualServer("Web Server")
```
**Common Use Cases:** Application hosting, development environments, batch processing
**Best Practices:** Use appropriate instance sizes, enable monitoring, configure auto-scaling

### BareMetalServer
**Purpose:** Dedicated physical servers
**Usage:**
```python
from ibmdiagrams.ibm.compute import BareMetalServer

server = BareMetalServer("Database Server")
```
**Common Use Cases:** High-performance workloads, compliance requirements, database hosting
**Best Practices:** Plan capacity carefully, implement backup strategies

### ContainerRegistry
**Purpose:** Private container image registry
**Usage:**
```python
from ibmdiagrams.ibm.compute import ContainerRegistry

registry = ContainerRegistry("Image Registry")
```
**Common Use Cases:** Store Docker images, CI/CD pipelines, microservices
**Best Practices:** Scan images for vulnerabilities, use namespaces, implement retention policies

### KubernetesService
**Purpose:** Managed Kubernetes clusters
**Usage:**
```python
from ibmdiagrams.ibm.compute import KubernetesService

k8s = KubernetesService("Production Cluster")
```
**Common Use Cases:** Container orchestration, microservices, cloud-native applications
**Best Practices:** Use multiple worker nodes, enable logging/monitoring, implement RBAC

### RedHatOpenShift
**Purpose:** Enterprise Kubernetes platform
**Usage:**
```python
from ibmdiagrams.ibm.compute import RedHatOpenShift

openshift = RedHatOpenShift("OpenShift Cluster")
```
**Common Use Cases:** Enterprise applications, hybrid cloud, developer platforms
**Best Practices:** Leverage built-in CI/CD, use projects for isolation, implement security policies

### CodeEngine
**Purpose:** Serverless container platform
**Usage:**
```python
from ibmdiagrams.ibm.compute import CodeEngine

ce = CodeEngine("Serverless App")
```
**Common Use Cases:** Event-driven applications, batch jobs, APIs
**Best Practices:** Optimize cold starts, use appropriate scaling settings, monitor costs

### CloudFunctions
**Purpose:** Function-as-a-Service (FaaS)
**Usage:**
```python
from ibmdiagrams.ibm.compute import CloudFunctions

func = CloudFunctions("API Handler")
```
**Common Use Cases:** Event processing, webhooks, microservices, scheduled tasks
**Best Practices:** Keep functions small, use environment variables, implement error handling

---

## Storage

### BlockStorage
**Purpose:** Block-level storage volumes
**Usage:**
```python
from ibmdiagrams.ibm.storage import BlockStorage

storage = BlockStorage("Data Volume")
```
**Common Use Cases:** Database storage, application data, boot volumes
**Best Practices:** Choose appropriate IOPS, enable encryption, implement snapshots

### ObjectStorage
**Purpose:** Scalable object storage (Cloud Object Storage)
**Usage:**
```python
from ibmdiagrams.ibm.storage import ObjectStorage

cos = ObjectStorage("Media Storage")
```
**Common Use Cases:** Backups, media files, data lakes, archives
**Best Practices:** Use lifecycle policies, enable versioning, implement access controls

### FileStorage
**Purpose:** NFS-based file storage
**Usage:**
```python
from ibmdiagrams.ibm.storage import FileStorage

nfs = FileStorage("Shared Files")
```
**Common Use Cases:** Shared application data, content management, home directories
**Best Practices:** Configure appropriate size/IOPS, use security groups, enable snapshots

---

## Network

### VPC
**Purpose:** Virtual Private Cloud network isolation
**Usage:**
```python
from ibmdiagrams.ibm.network import VPC

with VPC("Production VPC"):
    # Resources here
```
**Common Use Cases:** Network isolation, multi-tier applications, hybrid cloud
**Best Practices:** Use multiple zones, implement proper CIDR planning, enable flow logs

### Subnet
**Purpose:** Network segments within VPC
**Usage:**
```python
from ibmdiagrams.ibm.network import Subnet

with Subnet("Web Tier"):
    # Resources here
```
**Common Use Cases:** Tier separation, security zones, availability zones
**Best Practices:** Use /24 or larger, distribute across zones, implement NACLs

### LoadBalancer
**Purpose:** Application and network load balancing
**Usage:**
```python
from ibmdiagrams.ibm.network import LoadBalancer

lb = LoadBalancer("App LB")
```
**Common Use Cases:** High availability, traffic distribution, SSL termination
**Best Practices:** Use health checks, enable logging, configure timeouts

### VPN
**Purpose:** Virtual Private Network connectivity
**Usage:**
```python
from ibmdiagrams.ibm.network import VPN

vpn = VPN("Site-to-Site VPN")
```
**Common Use Cases:** Hybrid cloud, remote access, site-to-site connectivity
**Best Practices:** Use strong encryption, implement redundancy, monitor connections

### DirectLink
**Purpose:** Dedicated network connection to IBM Cloud
**Usage:**
```python
from ibmdiagrams.ibm.network import DirectLink

dl = DirectLink("Direct Connect")
```
**Common Use Cases:** High-bandwidth requirements, low latency, hybrid cloud
**Best Practices:** Plan capacity, implement redundancy, use BGP properly

### TransitGateway
**Purpose:** Connect multiple VPCs and on-premises networks
**Usage:**
```python
from ibmdiagrams.ibm.network import TransitGateway

tgw = TransitGateway("Central Hub")
```
**Common Use Cases:** Hub-and-spoke topology, multi-VPC connectivity, centralized routing
**Best Practices:** Plan routing carefully, use prefix filters, monitor bandwidth

### PublicGateway
**Purpose:** Provide internet access for private subnets
**Usage:**
```python
from ibmdiagrams.ibm.network import PublicGateway

pgw = PublicGateway("NAT Gateway")
```
**Common Use Cases:** Outbound internet access, software updates, API calls
**Best Practices:** One per zone, monitor usage, implement security groups

### FloatingIP
**Purpose:** Static public IP addresses
**Usage:**
```python
from ibmdiagrams.ibm.network import FloatingIP

fip = FloatingIP("Public IP")
```
**Common Use Cases:** Public-facing services, remote access, DNS records
**Best Practices:** Use sparingly, document assignments, implement security

---

## Security

### KeyProtect
**Purpose:** Key management service
**Usage:**
```python
from ibmdiagrams.ibm.security import KeyProtect

kp = KeyProtect("Encryption Keys")
```
**Common Use Cases:** Encryption key management, BYOK, compliance
**Best Practices:** Rotate keys regularly, use separate keys per service, enable logging

### SecretsManager
**Purpose:** Centralized secrets management
**Usage:**
```python
from ibmdiagrams.ibm.security import SecretsManager

sm = SecretsManager("App Secrets")
```
**Common Use Cases:** API keys, passwords, certificates, credentials
**Best Practices:** Rotate secrets, use IAM policies, enable notifications

### SecurityGroups
**Purpose:** Virtual firewall rules
**Usage:**
```python
from ibmdiagrams.ibm.security import SecurityGroups

sg = SecurityGroups("Web SG")
```
**Common Use Cases:** Instance-level firewall, access control, security zones
**Best Practices:** Principle of least privilege, document rules, use descriptive names

### IAM
**Purpose:** Identity and Access Management
**Usage:**
```python
from ibmdiagrams.ibm.security import IAM

iam = IAM("Access Control")
```
**Common Use Cases:** User management, service authentication, access policies
**Best Practices:** Use service IDs, implement MFA, regular access reviews

---

## Database

### Db2
**Purpose:** Relational database service
**Usage:**
```python
from ibmdiagrams.ibm.database import Db2

db = Db2("Application DB")
```
**Common Use Cases:** Transactional applications, data warehousing, analytics
**Best Practices:** Enable high availability, implement backups, monitor performance

### Cloudant
**Purpose:** NoSQL JSON document database
**Usage:**
```python
from ibmdiagrams.ibm.database import Cloudant

cloudant = Cloudant("Document Store")
```
**Common Use Cases:** Mobile apps, web applications, IoT data
**Best Practices:** Design for replication, use indexes, implement partitioning

### PostgreSQL
**Purpose:** Open-source relational database
**Usage:**
```python
from ibmdiagrams.ibm.database import PostgreSQL

pg = PostgreSQL("User Database")
```
**Common Use Cases:** Web applications, geospatial data, JSON storage
**Best Practices:** Use connection pooling, enable SSL, regular vacuuming

### MongoDB
**Purpose:** NoSQL document database
**Usage:**
```python
from ibmdiagrams.ibm.database import MongoDB

mongo = MongoDB("Content DB")
```
**Common Use Cases:** Content management, catalogs, real-time analytics
**Best Practices:** Use replica sets, implement sharding, create indexes

### Redis
**Purpose:** In-memory data store and cache
**Usage:**
```python
from ibmdiagrams.ibm.database import Redis

redis = Redis("Session Cache")
```
**Common Use Cases:** Caching, session storage, pub/sub, queues
**Best Practices:** Set eviction policies, use persistence, monitor memory

---

## Analytics

### DataStage
**Purpose:** ETL and data integration
**Usage:**
```python
from ibmdiagrams.ibm.analytics import DataStage

etl = DataStage("Data Pipeline")
```
**Common Use Cases:** Data warehousing, data migration, transformation
**Best Practices:** Optimize job design, use parallel processing, implement error handling

### Cognos
**Purpose:** Business intelligence and reporting
**Usage:**
```python
from ibmdiagrams.ibm.analytics import Cognos

bi = Cognos("Analytics Dashboard")
```
**Common Use Cases:** Reporting, dashboards, data visualization
**Best Practices:** Optimize queries, use caching, implement security

### StreamingAnalytics
**Purpose:** Real-time data processing
**Usage:**
```python
from ibmdiagrams.ibm.analytics import StreamingAnalytics

stream = StreamingAnalytics("Event Processing")
```
**Common Use Cases:** IoT data, log analysis, real-time monitoring
**Best Practices:** Design for scalability, implement checkpointing, monitor latency

---

## AI/ML

### WatsonStudio
**Purpose:** Data science and ML platform
**Usage:**
```python
from ibmdiagrams.ibm.ai import WatsonStudio

studio = WatsonStudio("ML Platform")
```
**Common Use Cases:** Model development, data preparation, collaboration
**Best Practices:** Use version control, implement MLOps, document experiments

### WatsonMachineLearning
**Purpose:** Model deployment and serving
**Usage:**
```python
from ibmdiagrams.ibm.ai import WatsonMachineLearning

wml = WatsonMachineLearning("Model Serving")
```
**Common Use Cases:** Model deployment, batch scoring, online predictions
**Best Practices:** Monitor model performance, implement A/B testing, version models

### WatsonAssistant
**Purpose:** Conversational AI chatbots
**Usage:**
```python
from ibmdiagrams.ibm.ai import WatsonAssistant

assistant = WatsonAssistant("Customer Support Bot")
```
**Common Use Cases:** Customer service, virtual agents, FAQ automation
**Best Practices:** Train with diverse data, implement fallback, monitor conversations

---

## Integration

### AppConnect
**Purpose:** Application and data integration
**Usage:**
```python
from ibmdiagrams.ibm.integration import AppConnect

integration = AppConnect("API Integration")
```
**Common Use Cases:** SaaS integration, API management, data synchronization
**Best Practices:** Use error handling, implement retry logic, monitor flows

### EventStreams
**Purpose:** Apache Kafka messaging service
**Usage:**
```python
from ibmdiagrams.ibm.integration import EventStreams

kafka = EventStreams("Event Bus")
```
**Common Use Cases:** Event streaming, microservices communication, log aggregation
**Best Practices:** Design topic structure, use consumer groups, monitor lag

### MQ
**Purpose:** Enterprise messaging
**Usage:**
```python
from ibmdiagrams.ibm.integration import MQ

mq = MQ("Message Queue")
```
**Common Use Cases:** Reliable messaging, transaction processing, legacy integration
**Best Practices:** Use persistent messages, implement dead letter queues, monitor depth

---

## DevOps

### ContinuousDelivery
**Purpose:** CI/CD pipeline automation
**Usage:**
```python
from ibmdiagrams.ibm.devops import ContinuousDelivery

cd = ContinuousDelivery("CI/CD Pipeline")
```
**Common Use Cases:** Automated deployments, testing, release management
**Best Practices:** Implement automated testing, use GitOps, enable notifications

### Monitoring
**Purpose:** Application and infrastructure monitoring
**Usage:**
```python
from ibmdiagrams.ibm.devops import Monitoring

monitor = Monitoring("Observability")
```
**Common Use Cases:** Performance monitoring, alerting, troubleshooting
**Best Practices:** Set meaningful alerts, use dashboards, implement SLOs

### LogAnalysis
**Purpose:** Centralized log management
**Usage:**
```python
from ibmdiagrams.ibm.devops import LogAnalysis

logs = LogAnalysis("Log Aggregation")
```
**Common Use Cases:** Log aggregation, troubleshooting, compliance
**Best Practices:** Structure logs, set retention policies, use log levels

---

## Quick Reference Tables

### Component Categories

| Category | Component Count | Common Use Cases |
|----------|----------------|------------------|
| Compute | 7 | VMs, containers, serverless |
| Storage | 3 | Block, object, file storage |
| Network | 8 | VPC, load balancing, connectivity |
| Security | 4 | Encryption, secrets, access control |
| Database | 5 | SQL, NoSQL, caching |
| Analytics | 3 | ETL, BI, streaming |
| AI/ML | 3 | Model training, deployment, chatbots |
| Integration | 3 | Messaging, events, APIs |
| DevOps | 3 | CI/CD, monitoring, logging |

### Common Patterns

1. **Three-Tier Web App:** VPC → Subnet → LoadBalancer → VirtualServer → Database
2. **Microservices:** VPC → KubernetesService → ContainerRegistry → EventStreams
3. **Data Lake:** ObjectStorage → DataStage → Db2 → Cognos
4. **Serverless API:** CloudFunctions → APIGateway → Cloudant
5. **Hybrid Cloud:** DirectLink → TransitGateway → VPC → VPN

### Security Best Practices

- Always use KeyProtect or SecretsManager for sensitive data
- Implement SecurityGroups with least privilege
- Enable encryption at rest and in transit
- Use IAM for fine-grained access control
- Enable audit logging for compliance

### Performance Optimization

- Use LoadBalancer for high availability
- Implement Redis for caching
- Use ObjectStorage for static content
- Enable auto-scaling for compute resources
- Use DirectLink for high-bandwidth requirements

---

For more examples and patterns, see the architecture-patterns resource.
"""


def troubleshooting_guide() -> str:
    """Common issues and solutions for IBM Cloud diagrams.

    Returns:
        Troubleshooting guide with solutions to common problems.
    """
    return """# IBM Cloud Diagrams Troubleshooting Guide

Solutions to common issues when creating IBM Cloud architecture diagrams.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Import Errors](#import-errors)
3. [Diagram Generation Failures](#diagram-generation-failures)
4. [Layout Problems](#layout-problems)
5. [Component Issues](#component-issues)
6. [Connection Problems](#connection-problems)
7. [File Output Issues](#file-output-issues)
8. [Performance Issues](#performance-issues)
9. [Validation Errors](#validation-errors)
10. [Best Practices](#best-practices)

---

## Installation Issues

### Problem: Package not found
**Error:** `ModuleNotFoundError: No module named 'ibmdiagrams'`

**Solution:**
```bash
# Install from local path
pip install -e /path/to/ibmdiagrams

# Or if using uv
uv pip install -e /path/to/ibmdiagrams
```

### Problem: Dependency conflicts
**Error:** `ERROR: pip's dependency resolver does not currently take into account...`

**Solution:**
```bash
# Create fresh virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install --upgrade pip
pip install -e /path/to/ibmdiagrams
```

---

## Import Errors

### Problem: Cannot import specific component
**Error:** `ImportError: cannot import name 'ComponentName' from 'ibmdiagrams.ibm.category'`

**Solution:**
1. Check component name spelling and capitalization
2. Verify component exists in catalog:
```python
# Use list_components tool to see available components
```
3. Check import path matches component category

**Example:**
```python
# Correct
from ibmdiagrams.ibm.compute import VirtualServer

# Incorrect
from ibmdiagrams.ibm.compute import VirtualMachine  # Wrong name
```

### Problem: Circular import errors
**Error:** `ImportError: cannot import name 'X' from partially initialized module`

**Solution:**
- Move imports inside functions if needed
- Avoid importing at module level in complex scenarios
- Use `from ibmdiagrams import IBMDiagram` first

---

## Diagram Generation Failures

### Problem: No output file created
**Error:** Diagram code runs but no .drawio file appears

**Solution:**
1. Check output directory exists and is writable:
```python
import os
output_dir = "./diagrams"
os.makedirs(output_dir, exist_ok=True)

with IBMDiagram("My Diagram", output=output_dir):
    # diagram code
```

2. Verify no exceptions were silently caught
3. Check file permissions on output directory

### Problem: Diagram generation timeout
**Error:** `TimeoutExpired: Command timed out after 30 seconds`

**Solution:**
- Simplify complex diagrams
- Break into multiple smaller diagrams
- Reduce number of components
- Check for infinite loops in code

### Problem: Invalid diagram code
**Error:** `SyntaxError` or `NameError` in diagram code

**Solution:**
Use the validate_diagram_code tool before generation:
```python
# Validate first
result = validate_diagram_code(code)
if "ERROR" in result:
    print(result)
else:
    # Generate diagram
```

---

## Layout Problems

### Problem: Components overlapping
**Issue:** Components render on top of each other

**Solution:**
1. Use proper grouping with context managers:
```python
with IBMDiagram("Proper Layout"):
    with VPC("Production"):
        with Subnet("Web Tier"):
            web = VirtualServer("Web")
        with Subnet("App Tier"):
            app = VirtualServer("App")
```

2. Adjust direction parameter:
```python
# Try different directions
with IBMDiagram("My Diagram", direction="TB"):  # Top to Bottom
with IBMDiagram("My Diagram", direction="LR"):  # Left to Right
```

### Problem: Connections not visible
**Issue:** Arrows between components don't show

**Solution:**
1. Ensure components are properly instantiated:
```python
# Correct
web = VirtualServer("Web")
db = Db2("Database")
web >> db  # Connection visible

# Incorrect
VirtualServer("Web") >> Db2("Database")  # Components not stored
```

2. Check components are in same diagram context

### Problem: Poor automatic layout
**Issue:** Diagram layout is messy or unclear

**Solution:**
1. Use explicit grouping to control layout:
```python
with IBMDiagram("Better Layout"):
    with VPC("VPC"):
        # Group related components
        with Subnet("Public"):
            lb = LoadBalancer("LB")
        
        with Subnet("Private"):
            app1 = VirtualServer("App1")
            app2 = VirtualServer("App2")
        
        lb >> [app1, app2]
```

2. Consider manual positioning in draw.io after generation

---

## Component Issues

### Problem: Component not rendering
**Issue:** Component appears in code but not in diagram

**Solution:**
1. Verify component is within diagram context:
```python
# Correct
with IBMDiagram("My Diagram"):
    vm = VirtualServer("Web")

# Incorrect
vm = VirtualServer("Web")  # Outside diagram context
with IBMDiagram("My Diagram"):
    pass
```

2. Check component is used in connections or groups

### Problem: Wrong component icon
**Issue:** Component shows generic icon instead of specific one

**Solution:**
- Verify you're using the correct component class
- Check component name matches catalog
- Update ibmdiagrams package to latest version

### Problem: Component label too long
**Issue:** Label text is truncated or wraps poorly

**Solution:**
```python
# Use shorter, clearer labels
# Instead of:
vm = VirtualServer("Production Web Server Instance 1")

# Use:
vm = VirtualServer("Web-1")
```

---

## Connection Problems

### Problem: Connection syntax error
**Error:** `TypeError: unsupported operand type(s) for >>`

**Solution:**
```python
# Correct connection syntax
web >> app  # Single connection
web >> [app1, app2]  # Multiple connections
[web1, web2] >> app  # Multiple sources

# Incorrect
web > app  # Wrong operator
web -> app  # Wrong operator
```

### Problem: Bidirectional connections
**Issue:** Need to show two-way communication

**Solution:**
```python
# Use both directions
web >> db  # Web to DB
db >> web  # DB to Web

# Or use Edge with custom properties (if supported)
```

### Problem: Connection labels
**Issue:** Want to label connections

**Solution:**
Currently, connection labels are not directly supported. Workarounds:
1. Use component labels to indicate relationship
2. Add text annotations in draw.io after generation
3. Use descriptive component names

---

## File Output Issues

### Problem: Permission denied
**Error:** `PermissionError: [Errno 13] Permission denied`

**Solution:**
```python
# Check directory permissions
import os
output_dir = "./diagrams"
if not os.access(output_dir, os.W_OK):
    print(f"No write permission for {output_dir}")
    
# Use absolute path
output_dir = os.path.abspath("./diagrams")
```

### Problem: File already exists
**Issue:** Want to overwrite existing diagram

**Solution:**
```python
import os
output_file = "./diagrams/my_diagram.drawio"

# Remove existing file
if os.path.exists(output_file):
    os.remove(output_file)

# Then generate diagram
```

### Problem: Cannot open .drawio file
**Issue:** Generated file won't open in draw.io

**Solution:**
1. Verify file was completely written (check file size > 0)
2. Check for errors during generation
3. Try opening in different draw.io viewer (web vs desktop)
4. Validate XML structure if needed

---

## Performance Issues

### Problem: Slow diagram generation
**Issue:** Large diagrams take too long to generate

**Solution:**
1. Break into multiple smaller diagrams:
```python
# Instead of one large diagram
with IBMDiagram("Complete Architecture"):
    # 100+ components
    
# Create multiple focused diagrams
with IBMDiagram("Network Layer"):
    # Network components only
    
with IBMDiagram("Application Layer"):
    # Application components only
```

2. Reduce component count
3. Simplify connections
4. Use preview_structure tool to check before generation

### Problem: Memory issues
**Error:** `MemoryError` or system slowdown

**Solution:**
- Close other applications
- Increase available memory
- Simplify diagram
- Generate diagrams sequentially, not in parallel

---

## Validation Errors

### Problem: Dangerous imports detected
**Error:** `SECURITY WARNING: Dangerous imports detected`

**Solution:**
```python
# Remove dangerous imports
# Avoid:
import os
import subprocess
import sys

# Use only:
from ibmdiagrams import IBMDiagram
from ibmdiagrams.ibm.compute import VirtualServer
# etc.
```

### Problem: Syntax errors in code
**Error:** Various Python syntax errors

**Solution:**
Use validate_diagram_code tool before execution:
```python
code = '''
from ibmdiagrams import IBMDiagram
from ibmdiagrams.ibm.compute import VirtualServer

with IBMDiagram("Test"):
    vm = VirtualServer("Web")
'''

result = validate_diagram_code(code)
print(result)  # Check for errors
```

---

## Best Practices

### 1. Always Validate First
```python
# Validate before generating
result = validate_diagram_code(code)
if "SUCCESS" in result:
    generate_diagram(code)
```

### 2. Use Descriptive Names
```python
# Good
web_server = VirtualServer("Web-Prod-1")
app_server = VirtualServer("App-Prod-1")

# Avoid
vm1 = VirtualServer("VM1")
vm2 = VirtualServer("VM2")
```

### 3. Group Related Components
```python
with IBMDiagram("Architecture"):
    with VPC("Production"):
        with Subnet("Public"):
            # Public components
        with Subnet("Private"):
            # Private components
```

### 4. Test Incrementally
```python
# Build diagram step by step
# Test after each major addition
# Don't write entire diagram at once
```

### 5. Use Tools Effectively
- `list_components` - Discover available components
- `search_components` - Find specific components
- `validate_diagram_code` - Check before generation
- `preview_structure` - Verify layout before generation
- `analyze_architecture` - Get best practices feedback

### 6. Handle Errors Gracefully
```python
try:
    with IBMDiagram("My Diagram"):
        # diagram code
except Exception as e:
    print(f"Error generating diagram: {e}")
```

### 7. Document Your Diagrams
```python
# Add comments explaining architecture decisions
with IBMDiagram("Production Architecture"):
    # Public subnet for load balancer
    with Subnet("Public"):
        lb = LoadBalancer("Main LB")
    
    # Private subnet for application servers
    with Subnet("Private"):
        app = VirtualServer("App Server")
```

---

## Getting Help

If you continue to experience issues:

1. **Check the documentation:**
   - Use `quickstart_guide` resource
   - Review `component_reference` resource
   - Check `architecture_patterns` resource

2. **Use diagnostic tools:**
   - `validate_diagram_code` - Check code validity
   - `preview_structure` - Verify structure
   - `analyze_architecture` - Get recommendations

3. **Simplify and isolate:**
   - Create minimal reproduction case
   - Test with simple diagram first
   - Add complexity gradually

4. **Check environment:**
   - Verify Python version (3.8+)
   - Check package versions
   - Ensure dependencies installed

---

## Common Error Messages Reference

| Error Message | Likely Cause | Solution |
|--------------|--------------|----------|
| `ModuleNotFoundError` | Package not installed | Install ibmdiagrams |
| `ImportError` | Wrong component name | Check catalog |
| `SyntaxError` | Invalid Python code | Validate code |
| `PermissionError` | No write access | Check permissions |
| `TimeoutExpired` | Diagram too complex | Simplify diagram |
| `NameError` | Undefined variable | Check variable names |
| `TypeError` | Wrong operator | Use >> for connections |
| `FileNotFoundError` | Invalid path | Check file paths |

---

For more information, see the quickstart guide and component reference.
"""
