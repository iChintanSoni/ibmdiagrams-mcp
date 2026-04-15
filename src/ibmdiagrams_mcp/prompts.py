"""
IBM Diagrams MCP Server - Prompts
Contains all prompt implementations for the MCP server.
"""

import ast


def design_architecture(description: str) -> str:
    """Generate a prompt for designing an IBM Cloud architecture diagram.

    Args:
        description: Natural language description of the architecture to diagram.
    """
    return f"""\
You are an IBM Cloud architecture expert. Generate Python code using the ibmdiagrams library
to create a draw.io diagram for the following architecture:

{description}

Steps:
1. Call list_components() to review available IBM Cloud components.
2. Design the hierarchy: IBM Cloud > Region > VPC > Subnet > services.
3. Write clean Python code using context managers for groups and direct instantiation for nodes.
4. Use operators (>>, <<, -) for connections between components.
5. Call generate_diagram(code=<your_code>, output_dir="/tmp") to produce the .drawio file.

Remember:
- Group shapes (VPC, Subnet, etc.) use `with Group(...):` syntax.
- Node shapes (VirtualServer, LoadBalancer, etc.) are instantiated directly.
- Always wrap everything in `with IBMDiagram(name="...", output="/tmp"):`
- Use sublabel="" for CIDR ranges, descriptions, or IDs.
"""


def analyze_terraform_state(description: str = "") -> str:
    """Analyze Terraform state and generate optimal IBM Cloud diagram with recommendations.

    This prompt guides the agent through analyzing a Terraform state file,
    generating a diagram, and providing architectural recommendations.

    Args:
        description: Optional context about the infrastructure (e.g., "production environment", "dev setup")
    """
    context = f"\n\nContext: {description}" if description else ""

    return f"""\
You are an IBM Cloud infrastructure expert specializing in Terraform and architecture diagrams.
Your task is to analyze a Terraform state file and create an optimal architecture diagram with recommendations.{context}

## Step-by-Step Process:

### 1. Obtain Terraform State
Ask the user to provide their Terraform state file content. They should run:
```bash
terraform show -json > infrastructure.tfstate
```
Then provide the JSON content.

### 2. Generate Initial Diagram
Use `generate_from_terraform` tool with:
- tfstate_content: The JSON content provided
- label_type: Start with "custom" for detailed view
- output_dir: Specify or use default

### 3. Analyze the Architecture
Review the generated diagram and Terraform resources for:

**Network Architecture:**
- Are resources distributed across multiple availability zones for HA?
- Is there proper subnet segmentation (public/private)?
- Are security groups and ACLs properly configured?

**Security Posture:**
- Is there a VPN Gateway or Direct Link for secure connectivity?
- Are VPE Gateways used for private service endpoints?
- Is encryption enabled (Key Protect/HPCS)?
- Are there bastion hosts for secure admin access?

**High Availability:**
- Are critical workloads replicated across zones?
- Are load balancers configured for distribution?
- Is there a backup and disaster recovery strategy?

**Cost Optimization:**
- Are resources right-sized?
- Are there unused or idle resources?
- Could reserved capacity reduce costs?

**Monitoring & Observability:**
- Are Flow Logs enabled for network monitoring?
- Is Cloud Logs configured for application logs?
- Are there monitoring and alerting services?

### 4. Provide Recommendations
Based on your analysis, provide:

1. **Critical Issues**: Security vulnerabilities or single points of failure
2. **Improvements**: Specific enhancements with code examples
3. **Best Practices**: IBM Cloud architecture patterns to follow
4. **Cost Savings**: Opportunities to optimize spending

### 5. Generate Enhanced Diagram (Optional)
If significant improvements are recommended, offer to:
- Generate Python code with the enhancements
- Create an improved diagram showing the target architecture
- Provide a migration plan

## Example Output Format:

```
## Terraform State Analysis

### Current Architecture
- 1 VPC in us-south region
- 3 subnets across 3 availability zones
- 6 virtual servers (2 per zone)
- 1 application load balancer
- 2 security groups

### Diagram Generated
✓ File: /tmp/infrastructure.drawio
✓ Label type: custom
✓ Resources visualized: 15

### Analysis Results

#### ✅ Strengths
- Multi-zone deployment for high availability
- Load balancer for traffic distribution
- Proper subnet segmentation

#### ⚠️ Recommendations

**HIGH PRIORITY:**
1. Add VPN Gateway for secure remote access
2. Implement VPE Gateways for private service connectivity
3. Enable Flow Logs for network monitoring

**MEDIUM PRIORITY:**
4. Add Key Protect for encryption key management
5. Configure Cloud Logs for centralized logging
6. Implement Network ACLs for subnet-level security

**COST OPTIMIZATION:**
7. Consider reserved capacity for virtual servers (potential 30% savings)
8. Review block storage volumes for unused capacity

### Next Steps
Would you like me to:
1. Generate enhanced Python code with security improvements?
2. Create a target architecture diagram?
3. Provide detailed implementation steps for recommendations?
```

## Tools to Use:
- `generate_from_terraform`: Convert Terraform state to diagram
- `search_components`: Find specific IBM Cloud components for recommendations
- `validate_diagram_code`: Validate any Python code you generate
- `list_components`: Browse available components for enhancements

Remember: Focus on actionable, specific recommendations that improve security,
reliability, and cost-effectiveness while following IBM Cloud best practices.
"""

# Made with Bob


def enhance_security(existing_code: str) -> str:
    """Add security components to existing diagram.

    Args:
        existing_code: Current diagram Python code
    """
    return f"""\
You are an IBM Cloud security expert. Enhance this diagram with comprehensive security best practices:

{existing_code}

## Security Enhancements to Add:

### 1. Network Security
- **Security Groups**: Add per-tier security groups (web-sg, app-sg, db-sg)
  - Web tier: Allow 80/443 from internet
  - App tier: Allow app ports from web tier only
  - DB tier: Allow DB ports from app tier only
- **Network ACLs**: Add subnet-level filtering for defense in depth

### 2. Access Control
- **VPN Gateway**: For secure remote access to private resources
- **Bastion Host**: For secure administrative access (jump server)
- **IAM Policies**: Document required access policies

### 3. Data Protection
- **Key Protect**: For encryption key management
- **Secrets Manager**: For storing credentials and API keys
- **Encryption**: Enable at-rest and in-transit encryption

### 4. Monitoring & Compliance
- **Flow Logs**: For network traffic monitoring
- **Cloud Logs**: For centralized logging
- **Activity Tracker**: For audit trail
- **Security & Compliance Center**: For posture management

### 5. Additional Security Measures
- **VPE Gateways**: For private connectivity to IBM Cloud services
- **Private Endpoints**: Avoid public internet exposure
- **DDoS Protection**: Via Cloud Internet Services

## Implementation Steps:

1. **Analyze Current Architecture**
   - Identify existing components
   - Determine security gaps
   - Plan security layer additions

2. **Add Security Components**
   - Import required security modules
   - Add Security Groups around compute resources
   - Add VPN Gateway for remote access
   - Add Bastion Host in public subnet
   - Add Key Protect for encryption
   - Add Flow Logs for monitoring

3. **Update Connections**
   - Show security group associations
   - Document allowed traffic flows
   - Add VPN connections

4. **Generate Enhanced Diagram**
   - Use `validate_diagram_code()` to check
   - Use `generate_diagram()` to create
   - Compare with original

## Example Security Enhancement:

```python
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet, SecurityGroup
from ibmdiagrams.ibmcloud.compute import VirtualServer
from ibmdiagrams.ibmcloud.security import VPNGateway, KeyProtect, BastionHost
from ibmdiagrams.ibmcloud.observability import FlowLogs

with IBMDiagram(name="Secure Architecture", output="/tmp"):
    with IBMCloud("IBM Cloud"):
        with VPC("secure-vpc"):
            # Public subnet with bastion
            with Subnet("public-subnet"):
                bastion = BastionHost("bastion")
                vpn = VPNGateway("vpn-gw")
            
            # Private subnet with security groups
            with Subnet("private-subnet"):
                with SecurityGroup("app-sg"):
                    app = VirtualServer("app-server")
            
            # Security services
            kp = KeyProtect("key-protect")
            fl = FlowLogs("flow-logs")
    
    # Secure access path
    vpn >> bastion >> app
    kp >> app  # Encryption
    fl >> app  # Monitoring
```

## Deliverables:

1. **Enhanced Python Code**: Complete code with all security components
2. **Security Documentation**: List of added security measures
3. **Compliance Notes**: How enhancements address security standards
4. **Implementation Guide**: Steps to deploy security enhancements

Remember: Security is layered. Implement multiple controls for defense in depth.
"""


def make_highly_available(existing_code: str) -> str:
    """Transform single-zone to multi-zone HA architecture.

    Args:
        existing_code: Current diagram Python code
    """
    return f"""\
You are an IBM Cloud HA expert. Transform this single-zone architecture into a highly available multi-zone deployment:

{existing_code}

## High Availability Transformation:

### 1. Multi-Zone Distribution
- **Deploy Across 3 Zones**: us-south-1, us-south-2, us-south-3
- **Replicate Resources**: Duplicate compute and storage across zones
- **Zone Isolation**: Each zone operates independently

### 2. Load Balancing
- **Application Load Balancer**: Distribute HTTP/HTTPS traffic
- **Network Load Balancer**: For TCP/UDP traffic
- **Health Checks**: Automatic failover on instance failure
- **Session Persistence**: Maintain user sessions

### 3. Data Resilience
- **Shared Storage**: File Storage accessible from all zones
- **Database Replication**: Multi-zone database deployment
- **Backup Strategy**: Cross-zone backups
- **Point-in-Time Recovery**: For data protection

### 4. Network Redundancy
- **Multiple Subnets**: One per zone
- **Public Gateways**: Per zone for internet access
- **Transit Gateway**: For multi-VPC connectivity
- **Redundant VPN**: Multiple VPN gateways

### 5. Auto-Scaling
- **Instance Groups**: Auto-scale based on demand
- **Scaling Policies**: CPU, memory, or custom metrics
- **Min/Max Instances**: Per zone capacity limits

## Transformation Steps:

1. **Analyze Current Architecture**
   - Identify single points of failure
   - Determine replication requirements
   - Plan zone distribution

2. **Design Multi-Zone Layout**
   ```
   Region (us-south)
   ├── Zone 1 (us-south-1)
   │   ├── Subnet (10.0.1.0/24)
   │   ├── Virtual Servers (2)
   │   └── Public Gateway
   ├── Zone 2 (us-south-2)
   │   ├── Subnet (10.0.2.0/24)
   │   ├── Virtual Servers (2)
   │   └── Public Gateway
   └── Zone 3 (us-south-3)
       ├── Subnet (10.0.3.0/24)
       ├── Virtual Servers (2)
       └── Public Gateway
   ```

3. **Add HA Components**
   - Import AvailabilityZone from groups
   - Create 3 zone contexts
   - Replicate subnets and instances
   - Add Load Balancer
   - Add shared storage

4. **Configure Connections**
   - Load Balancer to all instances
   - Instances to shared storage
   - Cross-zone connectivity

## Example HA Transformation:

### Before (Single Zone):
```python
with VPC("app-vpc"):
    with Subnet("app-subnet"):
        vsi = VirtualServer("app-server")
```

### After (Multi-Zone HA):
```python
from ibmdiagrams.ibmcloud.groups import AvailabilityZone
from ibmdiagrams.ibmcloud.network import LoadBalancer
from ibmdiagrams.ibmcloud.storage import FileStorage

with VPC("app-vpc"):
    lb = LoadBalancer("app-lb")
    
    with AvailabilityZone("us-south-1"):
        with Subnet("app-subnet-1", sublabel="10.0.1.0/24"):
            vsi1 = VirtualServer("app-server-1")
    
    with AvailabilityZone("us-south-2"):
        with Subnet("app-subnet-2", sublabel="10.0.2.0/24"):
            vsi2 = VirtualServer("app-server-2")
    
    with AvailabilityZone("us-south-3"):
        with Subnet("app-subnet-3", sublabel="10.0.3.0/24"):
            vsi3 = VirtualServer("app-server-3")
    
    storage = FileStorage("shared-storage")

# HA connections
lb >> vsi1
lb >> vsi2
lb >> vsi3
vsi1 >> storage
vsi2 >> storage
vsi3 >> storage
```

## HA Checklist:

### Infrastructure ✓
- [ ] 3 availability zones configured
- [ ] Resources replicated across zones
- [ ] Load balancer distributing traffic
- [ ] Health checks enabled
- [ ] Auto-scaling configured

### Data ✓
- [ ] Shared storage or replication
- [ ] Database multi-zone deployment
- [ ] Backup strategy implemented
- [ ] Recovery procedures tested

### Network ✓
- [ ] Redundant network paths
- [ ] Public gateways per zone
- [ ] VPN redundancy (if applicable)
- [ ] DNS failover configured

### Monitoring ✓
- [ ] Health monitoring per zone
- [ ] Alerting on zone failures
- [ ] Performance metrics tracked
- [ ] Failover testing scheduled

## Deliverables:

1. **HA Python Code**: Complete multi-zone architecture
2. **Architecture Diagram**: Visual representation
3. **Failover Documentation**: How failover works
4. **Cost Analysis**: HA vs single-zone costs
5. **Implementation Plan**: Migration steps

## Expected Outcomes:

- **99.99% Availability**: With 3-zone deployment
- **Zero Downtime**: During zone failures
- **Automatic Failover**: No manual intervention
- **Scalability**: Handle traffic spikes
- **Disaster Recovery**: Quick recovery from failures

Remember: HA requires testing. Regularly test failover scenarios to ensure reliability.
"""


def optimize_costs_prompt() -> dict:
    """Prompt for analyzing and optimizing IBM Cloud architecture costs.

    Returns:
        Prompt configuration for cost optimization analysis.
    """
    return {
        "name": "optimize_costs",
        "description": "Analyze IBM Cloud architecture and provide cost optimization recommendations",
        "arguments": [
            {
                "name": "diagram_code",
                "description": "Python code for the IBM Cloud diagram to analyze for cost optimization",
                "required": True,
            },
            {
                "name": "budget_constraint",
                "description": "Optional monthly budget constraint in USD (e.g., '5000')",
                "required": False,
            },
            {
                "name": "optimization_priority",
                "description": "Optimization priority: 'cost' (minimize costs), 'performance' (balance cost/performance), or 'reliability' (maintain reliability while reducing costs)",
                "required": False,
            },
        ],
    }


def optimize_costs_handler(diagram_code: str, budget_constraint: str = "", optimization_priority: str = "cost") -> str:
    """Analyze architecture and provide cost optimization recommendations.

    Args:
        diagram_code: Python diagram code to analyze
        budget_constraint: Optional monthly budget in USD
        optimization_priority: Optimization approach (cost/performance/reliability)

    Returns:
        Detailed cost optimization recommendations with estimated savings.
    """
    # Validate priority
    valid_priorities = ["cost", "performance", "reliability"]
    if optimization_priority not in valid_priorities:
        optimization_priority = "cost"

    # Parse budget if provided
    budget = None
    if budget_constraint:
        try:
            budget = float(budget_constraint.replace("$", "").replace(",", ""))
        except ValueError:
            budget = None

    # Parse the diagram code
    try:
        tree = ast.parse(diagram_code)
    except SyntaxError as e:
        return f"ERROR: Cannot parse diagram code: {e}"

    # Extract components
    components = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                comp_name = node.func.id
                comp_label = ""
                if node.args and isinstance(node.args[0], ast.Constant):
                    comp_label = node.args[0].value
                components.append({"type": comp_name, "label": comp_label})

    if not components:
        return "ERROR: No components found in diagram code"

    # Cost optimization analysis
    recommendations = []
    estimated_savings = 0

    # Component-specific recommendations
    component_counts = {}
    for comp in components:
        comp_type = comp["type"]
        component_counts[comp_type] = component_counts.get(comp_type, 0) + 1

    # 1. Compute optimization
    if "VirtualServer" in component_counts:
        count = component_counts["VirtualServer"]
        if count > 3:
            recommendations.append({
                "category": "Compute",
                "issue": f"Using {count} Virtual Servers",
                "recommendation": "Consider containerization with Kubernetes Service or Code Engine for better resource utilization",
                "priority": "High",
                "estimated_savings": f"${count * 50}-${count * 150}/month",
                "implementation": "Migrate to KubernetesService with auto-scaling to reduce idle capacity costs"
            })
            estimated_savings += count * 75

    if "BareMetalServer" in component_counts:
        count = component_counts["BareMetalServer"]
        recommendations.append({
            "category": "Compute",
            "issue": f"Using {count} Bare Metal Server(s)",
            "recommendation": "Evaluate if workload can run on Virtual Servers or Reserved Instances",
            "priority": "High",
            "estimated_savings": f"${count * 200}-${count * 500}/month",
            "implementation": "Test workload on Virtual Servers with appropriate sizing; use Reserved Instances for predictable workloads"
        })
        estimated_savings += count * 300

    if "CloudFunctions" in component_counts and "VirtualServer" in component_counts:
        recommendations.append({
            "category": "Compute",
            "issue": "Mixed serverless and server-based architecture",
            "recommendation": "Maximize serverless usage for event-driven workloads",
            "priority": "Medium",
            "estimated_savings": "$100-$300/month",
            "implementation": "Move sporadic workloads to Cloud Functions; keep only persistent services on Virtual Servers"
        })
        estimated_savings += 150

    # 2. Storage optimization
    if "BlockStorage" in component_counts:
        count = component_counts["BlockStorage"]
        if count > 2:
            recommendations.append({
                "category": "Storage",
                "issue": f"Using {count} Block Storage volumes",
                "recommendation": "Audit storage usage and delete unused volumes; consider lower IOPS tiers for non-critical data",
                "priority": "Medium",
                "estimated_savings": f"${count * 20}-${count * 50}/month",
                "implementation": "Review storage metrics, downgrade IOPS where possible, implement lifecycle policies"
            })
            estimated_savings += count * 30

    if "ObjectStorage" in component_counts:
        recommendations.append({
            "category": "Storage",
            "issue": "Using Object Storage",
            "recommendation": "Implement lifecycle policies to move infrequently accessed data to cheaper storage classes",
            "priority": "Medium",
            "estimated_savings": "$50-$200/month",
            "implementation": "Configure lifecycle rules: move to cold storage after 90 days, archive after 180 days"
        })
        estimated_savings += 100

    # 3. Database optimization
    db_components = ["Db2", "PostgreSQL", "MongoDB", "Cloudant", "Redis"]
    db_count = sum(component_counts.get(db, 0) for db in db_components)

    if db_count > 2:
        recommendations.append({
            "category": "Database",
            "issue": f"Using {db_count} separate database instances",
            "recommendation": "Consolidate databases where possible; use multi-tenant approach",
            "priority": "High",
            "estimated_savings": f"${db_count * 100}-${db_count * 200}/month",
            "implementation": "Evaluate if multiple databases can be consolidated; use schemas/databases within single instance"
        })
        estimated_savings += db_count * 120

    if "Redis" in component_counts and optimization_priority == "cost":
        recommendations.append({
            "category": "Database",
            "issue": "Using Redis for caching",
            "recommendation": "Consider application-level caching or smaller Redis instance",
            "priority": "Low",
            "estimated_savings": "$30-$80/month",
            "implementation": "Implement in-memory caching in application; use Redis only for shared cache"
        })
        estimated_savings += 50

    # 4. Network optimization
    if "LoadBalancer" in component_counts:
        count = component_counts["LoadBalancer"]
        if count > 2:
            recommendations.append({
                "category": "Network",
                "issue": f"Using {count} Load Balancers",
                "recommendation": "Consolidate load balancers using path-based routing",
                "priority": "Medium",
                "estimated_savings": f"${(count-1) * 50}-${(count-1) * 100}/month",
                "implementation": "Use single Application Load Balancer with multiple target groups"
            })
            estimated_savings += (count - 1) * 65

    if "DirectLink" in component_counts and optimization_priority == "cost":
        recommendations.append({
            "category": "Network",
            "issue": "Using Direct Link",
            "recommendation": "Evaluate if VPN Gateway can meet requirements at lower cost",
            "priority": "Medium",
            "estimated_savings": "$200-$500/month",
            "implementation": "Test VPN performance; migrate if latency/bandwidth requirements are met"
        })
        estimated_savings += 300

    if "FloatingIP" in component_counts:
        count = component_counts["FloatingIP"]
        if count > 3:
            recommendations.append({
                "category": "Network",
                "issue": f"Using {count} Floating IPs",
                "recommendation": "Release unused Floating IPs; use Load Balancer for public access",
                "priority": "Low",
                "estimated_savings": f"${count * 5}-${count * 10}/month",
                "implementation": "Audit IP usage, release unused IPs, use LB DNS instead of direct IPs"
            })
            estimated_savings += count * 7

    # 5. High Availability vs Cost trade-offs
    if "TransitGateway" in component_counts and optimization_priority == "cost":
        recommendations.append({
            "category": "Network",
            "issue": "Using Transit Gateway",
            "recommendation": "Evaluate if VPC peering can meet connectivity needs",
            "priority": "Low",
            "estimated_savings": "$50-$150/month",
            "implementation": "For simple VPC-to-VPC connectivity, use VPC peering instead"
        })
        estimated_savings += 80

    # 6. Monitoring and observability
    if "Monitoring" in component_counts or "LogAnalysis" in component_counts:
        recommendations.append({
            "category": "Observability",
            "issue": "Using monitoring and logging services",
            "recommendation": "Optimize log retention and metrics collection frequency",
            "priority": "Low",
            "estimated_savings": "$30-$100/month",
            "implementation": "Reduce log retention to 30 days, sample metrics at lower frequency for non-critical resources"
        })
        estimated_savings += 50

    # 7. Reserved capacity recommendations
    if optimization_priority in ["performance", "reliability"]:
        if "VirtualServer" in component_counts or "Db2" in component_counts:
            recommendations.append({
                "category": "Commitment",
                "issue": "Using on-demand pricing",
                "recommendation": "Purchase Reserved Instances for predictable workloads (1-3 year commitment)",
                "priority": "High",
                "estimated_savings": "$200-$800/month (30-50% discount)",
                "implementation": "Analyze usage patterns, commit to reserved capacity for baseline load"
            })
            estimated_savings += 400

    # 8. Serverless opportunities
    if "VirtualServer" in component_counts and "CloudFunctions" not in component_counts:
        recommendations.append({
            "category": "Architecture",
            "issue": "No serverless components detected",
            "recommendation": "Identify workloads suitable for serverless (APIs, batch jobs, event processing)",
            "priority": "Medium",
            "estimated_savings": "$100-$400/month",
            "implementation": "Move sporadic workloads to Cloud Functions or Code Engine"
        })
        estimated_savings += 200

    # 9. Auto-scaling recommendations
    if "KubernetesService" in component_counts or "VirtualServer" in component_counts:
        recommendations.append({
            "category": "Optimization",
            "issue": "Static resource allocation",
            "recommendation": "Implement auto-scaling to match demand",
            "priority": "High",
            "estimated_savings": "$150-$500/month",
            "implementation": "Configure horizontal pod autoscaling (HPA) for Kubernetes or instance auto-scaling groups"
        })
        estimated_savings += 250

    # 10. Development/staging environment optimization
    recommendations.append({
        "category": "Environment",
        "issue": "Production-grade resources for all environments",
        "recommendation": "Use smaller instances for dev/test; implement auto-shutdown schedules",
        "priority": "Medium",
        "estimated_savings": "$200-$600/month",
        "implementation": "Downsize non-prod environments, schedule shutdown during off-hours (nights/weekends)"
    })
    estimated_savings += 350

    # Sort by priority
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    recommendations.sort(key=lambda x: priority_order[x["priority"]])

    # Build response
    lines = ["# Cost Optimization Analysis\n"]

    lines.append(f"**Optimization Priority:** {optimization_priority.title()}")
    if budget:
        lines.append(f"**Budget Constraint:** ${budget:,.2f}/month")
    lines.append(
        f"**Total Estimated Savings:** ${estimated_savings:,.2f}/month\n")

    lines.append("## Architecture Summary\n")
    lines.append(f"**Total Components:** {len(components)}")
    lines.append(f"**Unique Component Types:** {len(component_counts)}\n")

    lines.append("### Component Breakdown\n")
    for comp_type, count in sorted(component_counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"- {comp_type}: {count}")

    lines.append("\n## Cost Optimization Recommendations\n")

    if not recommendations:
        lines.append(
            "✅ No major cost optimization opportunities identified. Architecture appears cost-efficient.\n")
    else:
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"### {i}. {rec['category']}: {rec['issue']}\n")
            lines.append(f"**Priority:** {rec['priority']}")
            lines.append(f"**Estimated Savings:** {rec['estimated_savings']}")
            lines.append(f"**Recommendation:** {rec['recommendation']}")
            lines.append(f"**Implementation:** {rec['implementation']}\n")

    # Priority-specific guidance
    lines.append("## Implementation Guidance\n")

    if optimization_priority == "cost":
        lines.append("**Cost-First Approach:**")
        lines.append("1. Start with High priority items for maximum savings")
        lines.append("2. Accept some performance trade-offs")
        lines.append("3. Focus on eliminating waste and over-provisioning")
        lines.append("4. Consider reserved capacity for predictable workloads")
        lines.append("5. Implement aggressive auto-scaling policies\n")

    elif optimization_priority == "performance":
        lines.append("**Balanced Approach:**")
        lines.append("1. Optimize without impacting user experience")
        lines.append("2. Use reserved instances for baseline capacity")
        lines.append("3. Implement smart caching strategies")
        lines.append("4. Right-size resources based on actual usage")
        lines.append("5. Keep redundancy for critical components\n")

    else:  # reliability
        lines.append("**Reliability-First Approach:**")
        lines.append("1. Maintain all redundancy and failover capabilities")
        lines.append("2. Optimize non-critical components only")
        lines.append("3. Use reserved capacity for cost predictability")
        lines.append("4. Focus on operational efficiency improvements")
        lines.append("5. Implement monitoring to catch issues early\n")

    # Quick wins
    lines.append("## Quick Wins (Implement First)\n")
    quick_wins = [r for r in recommendations if r["priority"] == "High"][:3]
    if quick_wins:
        for i, rec in enumerate(quick_wins, 1):
            lines.append(
                f"{i}. **{rec['category']}:** {rec['recommendation']}")
            lines.append(f"   - Savings: {rec['estimated_savings']}\n")
    else:
        lines.append("No high-priority quick wins identified.\n")

    # Budget analysis
    if budget:
        lines.append(f"## Budget Analysis\n")
        lines.append(f"**Monthly Budget:** ${budget:,.2f}")
        lines.append(f"**Potential Savings:** ${estimated_savings:,.2f}")
        lines.append(
            f"**Optimized Budget:** ${max(0, budget - estimated_savings):,.2f}")

        if estimated_savings > budget * 0.3:
            lines.append(
                f"\n✅ Significant savings potential ({(estimated_savings/budget)*100:.1f}% of budget)")
        elif estimated_savings > budget * 0.1:
            lines.append(
                f"\n✓ Moderate savings potential ({(estimated_savings/budget)*100:.1f}% of budget)")
        else:
            lines.append(
                f"\n→ Limited savings potential ({(estimated_savings/budget)*100:.1f}% of budget)")

    # Additional recommendations
    lines.append("\n## Additional Cost Management Best Practices\n")
    lines.append(
        "1. **Tagging Strategy:** Implement comprehensive resource tagging for cost allocation")
    lines.append(
        "2. **Budget Alerts:** Set up billing alerts at 50%, 75%, and 90% of budget")
    lines.append(
        "3. **Regular Reviews:** Conduct monthly cost reviews and optimization sessions")
    lines.append(
        "4. **Rightsizing:** Continuously monitor and adjust resource sizes based on actual usage")
    lines.append(
        "5. **Unused Resources:** Implement automated detection and cleanup of unused resources")
    lines.append(
        "6. **Cost Allocation:** Use resource groups and tags to track costs by team/project")
    lines.append(
        "7. **Reserved Capacity:** Commit to 1-3 year terms for predictable workloads (30-50% savings)")
    lines.append(
        "8. **Spot Instances:** Use for fault-tolerant workloads (up to 90% savings)")
    lines.append(
        "9. **Data Transfer:** Minimize cross-region data transfer; use CDN for static content")
    lines.append(
        "10. **Development Environments:** Implement auto-shutdown schedules for non-production resources")

    lines.append("\n## Monitoring Recommendations\n")
    lines.append("- Set up IBM Cloud Cost and Usage reports")
    lines.append("- Enable detailed billing with resource-level breakdown")
    lines.append("- Create custom dashboards for cost tracking")
    lines.append("- Implement anomaly detection for unexpected cost spikes")
    lines.append("- Review cost trends weekly and adjust as needed")

    return "\n".join(lines)
