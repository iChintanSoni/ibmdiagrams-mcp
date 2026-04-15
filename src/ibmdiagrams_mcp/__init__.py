import subprocess
import sys
import tempfile
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ibmdiagrams")

# ---------------------------------------------------------------------------
# Component catalog — all available IBM Cloud diagram elements
# ---------------------------------------------------------------------------

COMPONENTS = {
    "diagram": {
        "description": "Top-level diagram context manager. Use as 'with IBMDiagram(name, output=...) as d:'",
        "import": "from ibmdiagrams.ibmcloud.diagram import IBMDiagram",
        "classes": {
            "IBMDiagram": "Top-level diagram. Params: name, filename='', output='', font='IBM Plex Sans', direction='LR'|'TB'",
        },
    },
    "groups_core": {
        "description": "Core grouping shapes (container=1). These represent 'deployedOn' relationships. Use as context managers with 'with Group(...) as g:'",
        "import": "from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet, Region, EnterpriseNetwork, PublicNetwork, CloudServices, InternetServices, OverlayNetwork, PowerWorkspace, ZSystem, Internet, VLAN, ClassicVLAN, ClassicInfrastructure, OpenShift, KubernetesServices, ZContainers, watsonx, watsonxCodeAssistant, AuthorizationBoundary, PointOfPresence",
        "classes": {
            "IBMCloud": "IBM Cloud top-level group",
            "VPC": "Virtual Private Cloud group",
            "Subnet": "Subnet group",
            "Region": "IBM Cloud Region group",
            "EnterpriseNetwork": "Enterprise Network group (alias: Enterprise)",
            "PublicNetwork": "Public Network group (alias: Public)",
            "CloudServices": "Cloud Services group",
            "InternetServices": "Internet Services group",
            "OverlayNetwork": "Overlay Network group",
            "PowerWorkspace": "Power Workspace group",
            "ZSystem": "Z System group",
            "Internet": "Internet group",
            "VLAN": "VLAN group",
            "ClassicVLAN": "Classic VLAN group",
            "ClassicInfrastructure": "Classic Infrastructure group",
            "OpenShift": "OpenShift container platform group",
            "KubernetesServices": "Kubernetes Services group",
            "ZContainers": "Z Containers group",
            "watsonx": "watsonx AI platform group",
            "watsonxCodeAssistant": "watsonx Code Assistant group",
            "AuthorizationBoundary": "Authorization Boundary group",
            "PointOfPresence": "Point of Presence group (alias: PoP)",
        },
    },
    "groups_control": {
        "description": "Control/zone shapes (container=0). These represent 'deployedTo' relationships (e.g. security groups, availability zones). Use as context managers.",
        "import": "from ibmdiagrams.ibmcloud.groups import AccessGroup, AccountGroup, InstanceGroup, PlacementGroup, ResourceGroup, SecurityGroup, AvailabilityZone",
        "classes": {
            "AccessGroup": "Access Group control zone",
            "AccountGroup": "Account Group control zone",
            "InstanceGroup": "Instance Group control zone",
            "PlacementGroup": "Placement Group control zone",
            "ResourceGroup": "Resource Group control zone",
            "SecurityGroup": "Security Group control zone",
            "AvailabilityZone": "Availability Zone control zone (alias: Zone)",
        },
    },
    "groups_expanded": {
        "description": "Expanded node shapes — represent a service with child items inside.",
        "import": "from ibmdiagrams.ibmcloud.groups import ExpandedVirtualServer, ExpandedPowerVirtualServer, ExpandedClassicVirtualServer, ExpandedBareMetalServer, ExpandedClassicBareMetalServer, ExpandedApplication, ExpandedMicroservice",
        "classes": {
            "ExpandedVirtualServer": "Virtual Server expanded node",
            "ExpandedPowerVirtualServer": "Power Virtual Server expanded node",
            "ExpandedClassicVirtualServer": "Classic Virtual Server expanded node",
            "ExpandedBareMetalServer": "Bare Metal Server expanded node",
            "ExpandedClassicBareMetalServer": "Classic Bare Metal Server expanded node",
            "ExpandedApplication": "Application expanded node",
            "ExpandedMicroservice": "Microservice expanded node",
        },
    },
    "compute": {
        "description": "Compute service nodes (collapsed Item shapes).",
        "import": "from ibmdiagrams.ibmcloud.compute import VirtualServer, PowerVirtualServer, ClassicVirtualServer, BareMetalServer, ClassicBareMetalServer, DedicatedHost, ImageService, Satellite",
        "classes": {
            "VirtualServer": "Virtual Server instance",
            "PowerVirtualServer": "Power Virtual Server",
            "ClassicVirtualServer": "Classic Virtual Server",
            "BareMetalServer": "Bare Metal Server",
            "ClassicBareMetalServer": "Classic Bare Metal Server",
            "DedicatedHost": "Dedicated Host",
            "ImageService": "Image Service",
            "Satellite": "IBM Satellite",
        },
    },
    "network": {
        "description": "Network service nodes.",
        "import": "from ibmdiagrams.ibmcloud.network import LoadBalancer, ApplicationLoadBalancer, NetworkLoadBalancer, GlobalLoadBalancer, ClassicLoadBalancer, FloatingIP, NetworkInterface, EndpointGateway, PublicGateway, TransitGateway, DirectLinkConnect, DirectLinkDedicated, DNSServices, InternetServices, Internet, Bridge, Router, VLAN, ClassicVLAN, ProxyServer, L2Switch, L3Switch",
        "classes": {
            "LoadBalancer": "Load Balancer (alias: LB)",
            "ApplicationLoadBalancer": "Application Load Balancer",
            "NetworkLoadBalancer": "Network Load Balancer",
            "GlobalLoadBalancer": "Global Load Balancer (alias: GLB)",
            "ClassicLoadBalancer": "Classic Load Balancer",
            "FloatingIP": "Floating IP (alias: FIP)",
            "NetworkInterface": "Network Interface",
            "EndpointGateway": "Endpoint Gateway / VPE (alias: VPE)",
            "PublicGateway": "Public Gateway",
            "TransitGateway": "Transit Gateway (alias: TGW)",
            "DirectLinkConnect": "Direct Link Connect",
            "DirectLinkDedicated": "Direct Link Dedicated",
            "DNSServices": "DNS Services (alias: DNS)",
            "InternetServices": "Internet Services",
            "Internet": "Internet node",
            "Bridge": "Network Bridge",
            "Router": "Router",
            "VLAN": "VLAN node",
            "ClassicVLAN": "Classic VLAN node",
            "ProxyServer": "Proxy Server",
            "L2Switch": "Layer 2 Switch",
            "L3Switch": "Layer 3 Switch",
        },
    },
    "storage": {
        "description": "Storage service nodes.",
        "import": "from ibmdiagrams.ibmcloud.storage import BlockStorage, BlockStorageSnapshots, FileStorage, ObjectStorage, CloudBackup",
        "classes": {
            "BlockStorage": "Block Storage",
            "BlockStorageSnapshots": "Block Storage Snapshots",
            "FileStorage": "File Storage",
            "ObjectStorage": "Object Storage (COS)",
            "CloudBackup": "Cloud Backup",
        },
    },
    "data": {
        "description": "Data and database service nodes.",
        "import": "from ibmdiagrams.ibmcloud.data import Db2, Db2Warehouse, Cloudant, DataStax, Elasticsearch, MongoDB, MySQL, PostgreSQL, Rabbit, Redis, Database, EventStreams, DataPak",
        "classes": {
            "Db2": "IBM Db2",
            "Db2Warehouse": "IBM Db2 Warehouse",
            "Cloudant": "IBM Cloudant",
            "DataStax": "DataStax (alias: Ds)",
            "Elasticsearch": "Elasticsearch (alias: Es)",
            "MongoDB": "MongoDB (alias: Mg)",
            "MySQL": "MySQL (alias: My)",
            "PostgreSQL": "PostgreSQL",
            "Rabbit": "RabbitMQ (alias: Ra)",
            "Redis": "Redis (alias: Rd)",
            "Database": "Generic Database (alias: DB)",
            "EventStreams": "IBM Event Streams (Kafka)",
            "DataPak": "Data Pak",
        },
    },
    "security": {
        "description": "Security service nodes.",
        "import": "from ibmdiagrams.ibmcloud.security import AppID, KeyProtect, SecretsManager, SecurityComplianceCenter, SSHKey, VPNGateway, VPNConnection, BastionHost, ACLRules, SecurityPak",
        "classes": {
            "AppID": "App ID",
            "KeyProtect": "Key Protect",
            "SecretsManager": "Secrets Manager",
            "SecurityComplianceCenter": "Security & Compliance Center (alias: SCC)",
            "SSHKey": "SSH Key",
            "VPNGateway": "VPN Gateway (alias: VPN)",
            "VPNConnection": "VPN Connection",
            "BastionHost": "Bastion Host",
            "ACLRules": "ACL Rules",
            "SecurityPak": "Security Pak",
        },
    },
    "containers": {
        "description": "Container platform nodes.",
        "import": "from ibmdiagrams.ibmcloud.containers import OpenShift, KubernetesService, ZContainers, ContainerRegistry",
        "classes": {
            "OpenShift": "Red Hat OpenShift on IBM Cloud",
            "KubernetesService": "IBM Kubernetes Service",
            "ZContainers": "Z Containers",
            "ContainerRegistry": "Container Registry",
        },
    },
    "ai": {
        "description": "AI and Watson service nodes.",
        "import": "from ibmdiagrams.ibmcloud.ai import watsonx, watsonxAI, watsonxData, watsonxGovernance, watsonxOrchestrate, watsonxAssistant, watsonxCodeAssistant, watsonxZCodeAssistant, WatsonDiscovery, WatsonMachineLearning, WatsonStudio",
        "classes": {
            "watsonx": "watsonx platform",
            "watsonxAI": "watsonx.ai",
            "watsonxData": "watsonx.data",
            "watsonxGovernance": "watsonx.governance",
            "watsonxOrchestrate": "watsonx Orchestrate",
            "watsonxAssistant": "watsonx Assistant",
            "watsonxCodeAssistant": "watsonx Code Assistant",
            "watsonxZCodeAssistant": "watsonx Z Code Assistant",
            "WatsonDiscovery": "Watson Discovery",
            "WatsonMachineLearning": "Watson Machine Learning",
            "WatsonStudio": "Watson Studio",
        },
    },
    "devops": {
        "description": "DevOps and integration service nodes.",
        "import": "from ibmdiagrams.ibmcloud.devops import ContinuousDelivery, ContinuousIntegration, SourceCodeRepository, Toolchain, MQ, Ansible, GitLab, IntegrationPak",
        "classes": {
            "ContinuousDelivery": "Continuous Delivery",
            "ContinuousIntegration": "Continuous Integration",
            "SourceCodeRepository": "Source Code Repository",
            "Toolchain": "Toolchain",
            "MQ": "IBM MQ",
            "Ansible": "Ansible",
            "GitLab": "GitLab",
            "IntegrationPak": "Integration Pak",
        },
    },
    "observability": {
        "description": "Observability and monitoring service nodes.",
        "import": "from ibmdiagrams.ibmcloud.observability import CloudLogs, FlowLogs, Monitoring",
        "classes": {
            "CloudLogs": "IBM Cloud Logs",
            "FlowLogs": "Flow Logs",
            "Monitoring": "IBM Cloud Monitoring",
        },
    },
    "actors": {
        "description": "Actor shapes (round icons) for users, applications, and external entities.",
        "import": "from ibmdiagrams.ibmcloud.actors import User, Users, Enterprise, Application, WebApplication, Microservice",
        "classes": {
            "User": "User actor",
            "Users": "Multiple Users actor",
            "Enterprise": "Enterprise actor",
            "Application": "Application actor (alias: App)",
            "WebApplication": "Web Application actor (alias: WebApp)",
            "Microservice": "Microservice actor",
        },
    },
    "connectors": {
        "description": "Connector/edge types for linking shapes. Use operators: a - b (undirected), a >> b (a to b), a << b (b to a). Or instantiate explicitly with sourceid/targetid.",
        "import": "from ibmdiagrams.ibmcloud.connectors import SolidEdge, PrivateSolidEdge, PublicSolidEdge, DashedEdge, DottedEdge, DoubleEdge, TunnelEdge",
        "classes": {
            "SolidEdge": "Solid black edge",
            "PrivateSolidEdge": "Solid green edge (private network)",
            "PublicSolidEdge": "Solid blue edge (public network)",
            "DashedEdge": "Dashed black edge",
            "DottedEdge": "Dotted black edge",
            "DoubleEdge": "Double black edge",
            "TunnelEdge": "Tunnel edge",
        },
    },
}

EXAMPLES = {
    "vpc_basic": {
        "description": "Basic VPC with a subnet and virtual server instances",
        "code": """\
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet, AvailabilityZone, SecurityGroup
from ibmdiagrams.ibmcloud.compute import VirtualServer
from ibmdiagrams.ibmcloud.network import LoadBalancer, PublicGateway, FloatingIP

with IBMDiagram(name="Basic VPC", output="/tmp"):
    with IBMCloud("IBM Cloud"):
        with VPC("my-vpc", sublabel="10.0.0.0/16"):
            with AvailabilityZone("us-south-1"):
                with Subnet("web-subnet", sublabel="10.0.1.0/24"):
                    with SecurityGroup("web-sg"):
                        lb = LoadBalancer("web-lb")
                        vsi1 = VirtualServer("web-vsi-1")
                        vsi2 = VirtualServer("web-vsi-2")
                pgw = PublicGateway("pgw-1")

    lb >> vsi1
    lb >> vsi2
""",
    },
    "vpc_multi_zone": {
        "description": "Multi-zone VPC with availability zones, subnets, and a transit gateway",
        "code": """\
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet, AvailabilityZone, Region
from ibmdiagrams.ibmcloud.compute import VirtualServer
from ibmdiagrams.ibmcloud.network import LoadBalancer, TransitGateway, PublicGateway
from ibmdiagrams.ibmcloud.security import VPNGateway

with IBMDiagram(name="Multi-Zone VPC", output="/tmp"):
    with IBMCloud("IBM Cloud"):
        with Region("us-south"):
            with VPC("production-vpc"):
                with AvailabilityZone("us-south-1"):
                    with Subnet("app-subnet-1", sublabel="10.0.1.0/24"):
                        vsi1 = VirtualServer("app-vsi-1")
                with AvailabilityZone("us-south-2"):
                    with Subnet("app-subnet-2", sublabel="10.0.2.0/24"):
                        vsi2 = VirtualServer("app-vsi-2")
                with AvailabilityZone("us-south-3"):
                    with Subnet("app-subnet-3", sublabel="10.0.3.0/24"):
                        vsi3 = VirtualServer("app-vsi-3")
            tgw = TransitGateway("transit-gw")
            lb = LoadBalancer("global-lb")

    lb >> vsi1
    lb >> vsi2
    lb >> vsi3
    tgw - vsi1
""",
    },
    "watsonx_architecture": {
        "description": "watsonx AI architecture with data services",
        "code": """\
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet, watsonx, ResourceGroup
from ibmdiagrams.ibmcloud.ai import watsonxAI, watsonxData, watsonxGovernance
from ibmdiagrams.ibmcloud.data import ObjectStorage, Db2
from ibmdiagrams.ibmcloud.actors import User
from ibmdiagrams.ibmcloud.security import KeyProtect

with IBMDiagram(name="watsonx Architecture", output="/tmp"):
    with IBMCloud("IBM Cloud"):
        with ResourceGroup("ai-rg"):
            with watsonx("watsonx Platform"):
                wx_ai = watsonxAI("watsonx.ai")
                wx_data = watsonxData("watsonx.data")
                wx_gov = watsonxGovernance("watsonx.governance")
            cos = ObjectStorage("model-data-cos")
            db = Db2("metadata-db2")
            kp = KeyProtect("key-protect")

    u = User("Data Scientist")
    u >> wx_ai
    wx_ai >> wx_data
    wx_data >> cos
    wx_ai >> wx_gov
    wx_data >> db
""",
    },
    "openshift_on_vpc": {
        "description": "Red Hat OpenShift cluster on VPC with container registry and CI/CD",
        "code": """\
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet, AvailabilityZone, OpenShift as OpenShiftGroup
from ibmdiagrams.ibmcloud.containers import OpenShift, ContainerRegistry
from ibmdiagrams.ibmcloud.devops import ContinuousDelivery, Toolchain
from ibmdiagrams.ibmcloud.storage import ObjectStorage
from ibmdiagrams.ibmcloud.actors import WebApplication
from ibmdiagrams.ibmcloud.network import LoadBalancer
from ibmdiagrams.ibmcloud.observability import Monitoring, CloudLogs

with IBMDiagram(name="OpenShift on VPC", output="/tmp"):
    with IBMCloud("IBM Cloud"):
        with VPC("ocp-vpc"):
            with AvailabilityZone("us-south-1"):
                with Subnet("worker-subnet-1"):
                    with OpenShiftGroup("OpenShift Cluster"):
                        ocp = OpenShift("ROKS")
                        lb = LoadBalancer("router-lb")
        cr = ContainerRegistry("icr")
        cd = ContinuousDelivery("cd-service")
        tc = Toolchain("pipeline")
        mon = Monitoring("monitoring")
        logs = CloudLogs("cloud-logs")
        cos = ObjectStorage("image-registry-cos")

    app = WebApplication("Developer")
    app >> tc
    tc >> cr
    cr >> ocp
    ocp >> lb
    ocp >> mon
    ocp >> logs
""",
    },
}


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_components(category: str = "") -> str:
    """List available IBM Cloud diagram components organized by category.

    Args:
        category: Optional category filter. One of: diagram, groups_core,
                  groups_control, groups_expanded, compute, network, storage,
                  data, security, containers, ai, devops, observability,
                  actors, connectors. Leave empty to list all categories.

    Returns:
        A formatted catalog of components with their import paths and descriptions.
    """
    if category and category not in COMPONENTS:
        available = ", ".join(COMPONENTS.keys())
        return f"Unknown category '{category}'. Available: {available}"

    cats = {category: COMPONENTS[category]} if category else COMPONENTS

    lines = ["# IBM Cloud Diagram Components\n"]
    for cat_name, cat in cats.items():
        lines.append(f"## {cat_name}")
        lines.append(f"{cat['description']}\n")
        lines.append(f"**Import:** `{cat['import']}`\n")
        lines.append("**Classes:**")
        for cls, desc in cat["classes"].items():
            lines.append(f"  - `{cls}` — {desc}")
        lines.append("")

    lines.append("---")
    lines.append("## Usage Notes")
    lines.append("- All group classes (groups_core, groups_control, groups_expanded) are context managers: `with VPC('my-vpc'): ...`")
    lines.append("- Node/item classes (compute, network, etc.) are instantiated directly: `vsi = VirtualServer('my-vsi')`")
    lines.append("- Connect shapes with operators: `a - b` (undirected), `a >> b` (a→b), `a << b` (b→a)")
    lines.append("- Every shape accepts `label` and optional `sublabel` parameters.")
    lines.append("- `IBMDiagram` accepts `output=` to control where the .drawio file is written.")
    lines.append("- `direction='LR'` (default) or `direction='TB'` controls layout.")

    return "\n".join(lines)


@mcp.tool()
def get_example(name: str = "") -> str:
    """Get example IBM Cloud diagram code.

    Args:
        name: Example name. One of: vpc_basic, vpc_multi_zone,
              watsonx_architecture, openshift_on_vpc.
              Leave empty to list all available examples.

    Returns:
        Example Python code ready to use with ibmdiagrams.
    """
    if not name:
        lines = ["# Available IBM Cloud Diagram Examples\n"]
        for ex_name, ex in EXAMPLES.items():
            lines.append(f"- **{ex_name}**: {ex['description']}")
        lines.append("\nCall get_example(name='<name>') to get the code.")
        return "\n".join(lines)

    if name not in EXAMPLES:
        available = ", ".join(EXAMPLES.keys())
        return f"Unknown example '{name}'. Available: {available}"

    ex = EXAMPLES[name]
    return f"# {ex['description']}\n\n```python\n{ex['code']}\n```"


@mcp.tool()
def generate_diagram(code: str, output_dir: str = "/tmp") -> str:
    """Generate an IBM Cloud architecture diagram from Python code.

    Executes the provided Python code (which must use the ibmdiagrams library)
    and returns the path to the generated .drawio file along with the XML content.

    The code should use IBMDiagram (or Diagram) as the top-level context manager.
    Set output= in IBMDiagram(..., output=output_dir) to control where the file
    is written, or leave it out — the tool captures the default location.

    Args:
        code: Python code using the ibmdiagrams API. Must import and use
              IBMDiagram (or Diagram) as a context manager.
        output_dir: Directory where the .drawio file should be written.
                    Defaults to /tmp.

    Returns:
        On success: "SUCCESS\nFILE:<path>\n\n<xml content>"
        On failure: "ERROR\n<stderr output>"

    Example code:
        from ibmdiagrams.ibmcloud.diagram import IBMDiagram
        from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet
        from ibmdiagrams.ibmcloud.compute import VirtualServer

        with IBMDiagram(name="My Diagram", output="/tmp"):
            with IBMCloud("IBM Cloud"):
                with VPC("my-vpc"):
                    with Subnet("subnet-1"):
                        VirtualServer("vsi-1")
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write user code to a temp file
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        prefix="ibmdiagram_",
        delete=False,
        dir=tempfile.gettempdir(),
    ) as f:
        script_path = f.name
        # Inject output_dir into code if no output= is specified
        if "output=" not in code and "output =" not in code:
            # Replace IBMDiagram( or Diagram( calls to inject output_dir
            import re
            patched = re.sub(
                r'\b(IBMDiagram|Diagram)\s*\(',
                rf'\1(output="{output_dir}", ',
                code,
                count=1,
            )
            # Fix any doubled output= if user left a positional name arg
            f.write(patched)
        else:
            f.write(code)

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=output_dir,
        )

        if result.returncode != 0:
            return f"ERROR\n{result.stderr or result.stdout}"

        # Find the .drawio file(s) created in output_dir
        drawio_files = sorted(
            Path(output_dir).glob("*.drawio"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        if not drawio_files:
            return (
                f"ERROR\nNo .drawio file found in {output_dir}.\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )

        latest = drawio_files[0]
        xml_content = latest.read_text(encoding="utf-8")
        return f"SUCCESS\nFILE:{latest}\n\n{xml_content}"

    except subprocess.TimeoutExpired:
        return "ERROR\nScript execution timed out after 60 seconds."
    finally:
        try:
            os.unlink(script_path)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------

@mcp.resource("resource://ibmdiagrams/quickstart")
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


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

@mcp.prompt()
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


def main() -> None:
    mcp.run()
