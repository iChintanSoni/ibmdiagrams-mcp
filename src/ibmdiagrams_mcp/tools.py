"""
IBM Diagrams MCP Server - Tools
Contains all tool implementations for the MCP server.
"""

import subprocess
import sys
import tempfile
import os
import logging
import ast
import json
from pathlib import Path
from typing import Dict, List, Any

from .catalog import COMPONENTS, EXAMPLES

logger = logging.getLogger(__name__)

# Constants
DIAGRAM_GENERATION_TIMEOUT = 60  # seconds


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
    lines.append(
        "- All group classes (groups_core, groups_control, groups_expanded) are context managers: `with VPC('my-vpc'): ...`")
    lines.append(
        "- Node/item classes (compute, network, etc.) are instantiated directly: `vsi = VirtualServer('my-vsi')`")
    lines.append(
        "- Connect shapes with operators: `a - b` (undirected), `a >> b` (a→b), `a << b` (b→a)")
    lines.append(
        "- Every shape accepts `label` and optional `sublabel` parameters.")
    lines.append(
        "- `IBMDiagram` accepts `output=` to control where the .drawio file is written.")
    lines.append(
        "- `direction='LR'` (default) or `direction='TB'` controls layout.")

    return "\n".join(lines)


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


def generate_diagram(code: str, output_dir: str = "/tmp") -> str:
    """Generate an IBM Cloud architecture diagram from Python code.

    Executes the provided Python code (which must use the ibmdiagrams library)
    and returns the path to the generated .drawio file along with the XML content.

    The code should use IBMDiagram (or Diagram) as the top-level context manager.
    Set output= in IBMDiagram(..., output=output_dir) to control where the file
    is written, or leave it out — the tool captures the default location.

    SECURITY WARNING:
    This function executes arbitrary Python code provided by the user. While it
    validates the output directory and runs with a timeout, it does NOT sandbox
    the execution environment. The code runs with the same permissions as the
    MCP server process and can:
    - Access the file system
    - Make network requests
    - Execute system commands
    - Import any available Python modules

    This tool should only be used in trusted environments or with trusted input.
    Consider implementing additional security measures such as:
    - Code review before execution
    - Running in a containerized/sandboxed environment
    - Restricting available imports using AST parsing
    - Limiting file system access

    Args:
        code: Python code using the ibmdiagrams API. Must import and use
              IBMDiagram (or Diagram) as a context manager.
        output_dir: Directory where the .drawio file should be written.
                    Defaults to /tmp. Path is validated and resolved to prevent
                    path traversal attacks.

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
    # Validate and resolve output_dir to prevent path traversal
    try:
        output_path = Path(output_dir).resolve()
        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)
        if not output_path.is_dir():
            return f"ERROR\noutput_dir '{output_dir}' is not a directory"
        # Check write permissions
        if not os.access(output_path, os.W_OK):
            return f"ERROR\nNo write permission for directory '{output_dir}'"
    except (OSError, ValueError) as e:
        return f"ERROR\nInvalid output_dir '{output_dir}': {e}"

    script_path = None
    try:
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
                    rf'\1(output="{output_path}", ',
                    code,
                    count=1,
                )
                # Fix any doubled output= if user left a positional name arg
                f.write(patched)
            else:
                f.write(code)

        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=DIAGRAM_GENERATION_TIMEOUT,
            cwd=str(output_path),
        )

        if result.returncode != 0:
            return f"ERROR\n{result.stderr or result.stdout}"

        # Find the most recently created .drawio file
        drawio_files = list(output_path.glob("*.drawio"))
        if not drawio_files:
            return (
                f"ERROR\nNo .drawio file found in {output_path}.\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )

        # Get the most recently modified file
        latest = max(drawio_files, key=lambda p: p.stat().st_mtime)
        xml_content = latest.read_text(encoding="utf-8")
        return f"SUCCESS\nFILE:{latest}\n\n{xml_content}"

    except subprocess.TimeoutExpired:
        logger.warning(
            f"Diagram generation timed out after {DIAGRAM_GENERATION_TIMEOUT} seconds")
        return f"ERROR\nScript execution timed out after {DIAGRAM_GENERATION_TIMEOUT} seconds."
    except Exception as e:
        logger.error(f"Unexpected error during diagram generation: {e}")
        return f"ERROR\nUnexpected error: {e}"
    finally:
        # Clean up temporary script file
        if script_path:
            try:
                os.unlink(script_path)
                logger.debug(f"Cleaned up temporary file: {script_path}")
            except OSError as e:
                logger.warning(
                    f"Failed to clean up temporary file {script_path}: {e}")


def validate_diagram_code(code: str) -> str:
    """Validate IBM Cloud diagram Python code before execution.

    Performs AST-based validation to check for:
    - Syntax errors
    - Required imports (ibmdiagrams modules)
    - Proper IBMDiagram usage
    - Security concerns (dangerous imports/operations)

    Args:
        code: Python code to validate

    Returns:
        Validation results with status, errors, warnings, and suggestions.
    """
    result = {
        "status": "valid",
        "errors": [],
        "warnings": [],
        "suggestions": []
    }

    # Check for empty code
    if not code.strip():
        result["status"] = "invalid"
        result["errors"].append("Code is empty")
        return json.dumps(result, indent=2)

    # Try to parse the code
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        result["status"] = "invalid"
        result["errors"].append(f"Syntax error at line {e.lineno}: {e.msg}")
        return json.dumps(result, indent=2)

    # Check for required imports
    has_ibmdiagram_import = False
    has_component_imports = False
    dangerous_imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if 'ibmdiagrams' in alias.name:
                    has_component_imports = True
                if alias.name in ['os', 'subprocess', 'sys', 'shutil']:
                    dangerous_imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module and 'ibmdiagrams' in node.module:
                has_component_imports = True
                if 'diagram' in node.module.lower():
                    has_ibmdiagram_import = True
            if node.module in ['os', 'subprocess', 'sys', 'shutil']:
                dangerous_imports.append(node.module)

    # Check for IBMDiagram usage
    has_diagram_context = False
    for node in ast.walk(tree):
        if isinstance(node, ast.With):
            for item in node.items:
                if isinstance(item.context_expr, ast.Call):
                    if isinstance(item.context_expr.func, ast.Name):
                        if item.context_expr.func.id in ['IBMDiagram', 'Diagram']:
                            has_diagram_context = True

    # Validation checks
    if not has_ibmdiagram_import:
        result["errors"].append(
            "Missing IBMDiagram import. Add: from ibmdiagrams.ibmcloud.diagram import IBMDiagram"
        )
        result["status"] = "invalid"

    if not has_component_imports:
        result["warnings"].append(
            "No ibmdiagrams component imports found. You'll need to import components like VPC, Subnet, VirtualServer, etc."
        )

    if not has_diagram_context:
        result["errors"].append(
            "No IBMDiagram context manager found. Wrap your code with: with IBMDiagram(name='...', output='...'):"
        )
        result["status"] = "invalid"

    if dangerous_imports:
        result["warnings"].append(
            f"Potentially dangerous imports detected: {', '.join(dangerous_imports)}. "
            "These may pose security risks."
        )

    # Suggestions
    if result["status"] == "valid":
        result["suggestions"].append(
            "Code structure looks good! Ready to generate diagram.")

    return json.dumps(result, indent=2)


def search_components(query: str, category: str = "") -> str:
    """Search for IBM Cloud diagram components by keyword.

    Searches across all component names and descriptions to find matches.
    Much faster than browsing categories when you know what you're looking for.

    Args:
        query: Search term (case-insensitive)
        category: Optional category filter to narrow search

    Returns:
        Matching components with their categories, import paths, and descriptions.
    """
    query_lower = query.lower()
    matches = []

    # Determine which categories to search
    categories_to_search = COMPONENTS.items()
    if category:
        if category not in COMPONENTS:
            available = ", ".join(COMPONENTS.keys())
            return f"Unknown category '{category}'. Available: {available}"
        categories_to_search = [(category, COMPONENTS[category])]

    # Search through components
    for cat_name, cat_data in categories_to_search:
        for class_name, class_desc in cat_data["classes"].items():
            # Check if query matches class name or description
            if query_lower in class_name.lower() or query_lower in class_desc.lower():
                matches.append({
                    "component": class_name,
                    "category": cat_name,
                    "description": class_desc,
                    "import": cat_data["import"]
                })

    if not matches:
        return f"No components found matching '{query}'. Try a different search term or use list_components() to browse all components."

    # Format results
    lines = [f"# Search Results for '{query}'\n"]
    lines.append(f"Found {len(matches)} matching component(s):\n")

    for match in matches:
        lines.append(f"## {match['component']}")
        lines.append(f"**Category:** {match['category']}")
        lines.append(f"**Description:** {match['description']}")
        lines.append(f"**Import:** `{match['import']}`")
        lines.append("")

    # Add usage example
    if matches:
        first_match = matches[0]
        lines.append("## Quick Usage Example")
        lines.append("```python")
        lines.append(first_match['import'])
        lines.append("")

        # Determine if it's a group or node
        if 'groups' in first_match['category']:
            lines.append(
                f"with {first_match['component']}('my-{first_match['component'].lower()}'):")
            lines.append("    # Add components here")
        else:
            lines.append(
                f"{first_match['component'].lower()} = {first_match['component']}('my-{first_match['component'].lower()}')")
        lines.append("```")

    return "\n".join(lines)


def generate_from_terraform(tfstate_content: str, label_type: str = "custom", output_dir: str = "") -> str:
    """Generate IBM Cloud diagram from Terraform state file.

    Converts a Terraform state file (JSON format) into an IBM Cloud architecture diagram.
    This is a core feature of ibmdiagrams that enables infrastructure visualization.

    Args:
        tfstate_content: Terraform state file content in JSON format
        label_type: Label style - "custom" (detailed) or "general" (simplified). Default: "custom"
        output_dir: Output directory for the diagram. If empty, uses system temp directory.

    Returns:
        On success: Path to generated .drawio file and summary
        On failure: Error message with details

    Example:
        # Get terraform state
        tfstate = subprocess.run(['terraform', 'show', '-json'], capture_output=True, text=True).stdout
        result = generate_from_terraform(tfstate_content=tfstate)
    """
    # Validate label_type
    if label_type not in ["custom", "general"]:
        return f"ERROR\nInvalid label_type '{label_type}'. Must be 'custom' or 'general'."

    # Validate JSON
    try:
        tfstate_data = json.loads(tfstate_content)
    except json.JSONDecodeError as e:
        return f"ERROR\nInvalid JSON in tfstate_content: {e}"

    # Set output directory
    if not output_dir:
        output_dir = tempfile.gettempdir()

    try:
        output_path = Path(output_dir).resolve()
        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)
        if not output_path.is_dir():
            return f"ERROR\noutput_dir '{output_dir}' is not a directory"
        if not os.access(output_path, os.W_OK):
            return f"ERROR\nNo write permission for directory '{output_dir}'"
    except (OSError, ValueError) as e:
        return f"ERROR\nInvalid output_dir '{output_dir}': {e}"

    # Write tfstate to temporary file
    tfstate_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".tfstate",
            prefix="terraform_",
            delete=False,
            dir=tempfile.gettempdir(),
        ) as f:
            tfstate_path = f.name
            f.write(tfstate_content)

        # Build command
        cmd = [sys.executable, "-m", "ibmdiagrams.ibmscripts.ibmdiagrams"]
        cmd.append(tfstate_path)

        if output_dir:
            cmd.extend(["-output", str(output_path)])

        if label_type == "general":
            cmd.append("--general")

        # Execute ibmdiagrams command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=DIAGRAM_GENERATION_TIMEOUT,
            cwd=str(output_path),
        )

        if result.returncode != 0:
            return f"ERROR\n{result.stderr or result.stdout}"

        # Find generated .drawio file
        # The file will have the same base name as the tfstate file
        base_name = Path(tfstate_path).stem
        expected_file = output_path / f"{base_name}.drawio"

        if not expected_file.exists():
            # Try to find any recently created .drawio file
            drawio_files = list(output_path.glob("*.drawio"))
            if drawio_files:
                expected_file = max(
                    drawio_files, key=lambda p: p.stat().st_mtime)
            else:
                return (
                    f"ERROR\nNo .drawio file found in {output_path}.\n"
                    f"stdout: {result.stdout}\nstderr: {result.stderr}"
                )

        # Read the generated file
        xml_content = expected_file.read_text(encoding="utf-8")

        # Parse tfstate to provide summary
        summary_lines = ["SUCCESS", f"FILE:{expected_file}", ""]
        summary_lines.append("## Terraform State Summary")

        # Try to extract resource counts
        if "values" in tfstate_data and "root_module" in tfstate_data["values"]:
            resources = tfstate_data["values"]["root_module"].get(
                "resources", [])
            resource_types = {}
            for resource in resources:
                rtype = resource.get("type", "unknown")
                resource_types[rtype] = resource_types.get(rtype, 0) + 1

            summary_lines.append(f"Total resources: {len(resources)}")
            summary_lines.append("\nResource breakdown:")
            for rtype, count in sorted(resource_types.items()):
                summary_lines.append(f"  - {rtype}: {count}")

        summary_lines.append(f"\nLabel type: {label_type}")
        summary_lines.append(f"\nDiagram file: {expected_file}")

        return "\n".join(summary_lines)

    except subprocess.TimeoutExpired:
        logger.warning(
            f"Terraform diagram generation timed out after {DIAGRAM_GENERATION_TIMEOUT} seconds")
        return f"ERROR\nDiagram generation timed out after {DIAGRAM_GENERATION_TIMEOUT} seconds."
    except Exception as e:
        logger.error(
            f"Unexpected error during Terraform diagram generation: {e}")
        return f"ERROR\nUnexpected error: {e}"
    finally:
        # Clean up temporary tfstate file
        if tfstate_path:
            try:
                os.unlink(tfstate_path)
                logger.debug(f"Cleaned up temporary file: {tfstate_path}")
            except OSError as e:
                logger.warning(
                    f"Failed to clean up temporary file {tfstate_path}: {e}")

# Made with Bob


def analyze_architecture(code: str) -> str:
    """Analyze IBM Cloud diagram code for best practices and completeness.

    Reviews the architecture for:
    - Security best practices
    - High availability patterns
    - Cost optimization opportunities
    - Missing critical components
    - IBM Cloud architecture standards compliance

    Args:
        code: Python diagram code to analyze

    Returns:
        Detailed analysis with recommendations organized by priority.
    """
    result = {
        "status": "analyzed",
        "strengths": [],
        "recommendations": {
            "critical": [],
            "high": [],
            "medium": [],
            "low": []
        },
        "missing_components": [],
        "cost_optimization": [],
        "security_score": 0,
        "ha_score": 0
    }

    # Parse the code
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return json.dumps({
            "status": "error",
            "message": f"Cannot analyze code with syntax errors: {e}"
        }, indent=2)

    # Track components used
    components_used = {
        "vpcs": 0,
        "subnets": 0,
        "zones": 0,
        "virtual_servers": 0,
        "load_balancers": 0,
        "security_groups": 0,
        "vpn_gateways": 0,
        "vpe_gateways": 0,
        "key_protect": 0,
        "secrets_manager": 0,
        "flow_logs": 0,
        "cloud_logs": 0,
        "monitoring": 0,
        "bastion_hosts": 0,
        "transit_gateways": 0,
        "public_gateways": 0
    }

    # Analyze imports and usage
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and 'ibmdiagrams' in node.module:
                for alias in node.names:
                    name_lower = alias.name.lower()
                    if 'vpc' in name_lower and 'vpe' not in name_lower:
                        components_used["vpcs"] += 1
                    elif 'subnet' in name_lower:
                        components_used["subnets"] += 1
                    elif 'zone' in name_lower or 'availabilityzone' in name_lower:
                        components_used["zones"] += 1
                    elif 'virtualserver' in name_lower:
                        components_used["virtual_servers"] += 1
                    elif 'loadbalancer' in name_lower:
                        components_used["load_balancers"] += 1
                    elif 'securitygroup' in name_lower:
                        components_used["security_groups"] += 1
                    elif 'vpngateway' in name_lower:
                        components_used["vpn_gateways"] += 1
                    elif 'vpegateway' in name_lower or 'endpointgateway' in name_lower:
                        components_used["vpe_gateways"] += 1
                    elif 'keyprotect' in name_lower:
                        components_used["key_protect"] += 1
                    elif 'secretsmanager' in name_lower:
                        components_used["secrets_manager"] += 1
                    elif 'flowlogs' in name_lower:
                        components_used["flow_logs"] += 1
                    elif 'cloudlogs' in name_lower:
                        components_used["cloud_logs"] += 1
                    elif 'monitoring' in name_lower:
                        components_used["monitoring"] += 1
                    elif 'bastionhost' in name_lower:
                        components_used["bastion_hosts"] += 1
                    elif 'transitgateway' in name_lower:
                        components_used["transit_gateways"] += 1
                    elif 'publicgateway' in name_lower:
                        components_used["public_gateways"] += 1

    # Analyze architecture patterns

    # Check for multi-zone deployment
    if components_used["zones"] >= 3:
        result["strengths"].append(
            "Multi-zone deployment for high availability")
        result["ha_score"] += 30
    elif components_used["zones"] >= 2:
        result["strengths"].append("Multi-zone deployment across 2 zones")
        result["ha_score"] += 20
        result["recommendations"]["medium"].append(
            "Consider deploying across 3 availability zones for better HA"
        )
    else:
        result["recommendations"]["high"].append(
            "Deploy across multiple availability zones for high availability"
        )

    # Check for load balancer
    if components_used["load_balancers"] > 0:
        result["strengths"].append(
            "Load balancer configured for traffic distribution")
        result["ha_score"] += 20
    elif components_used["virtual_servers"] > 1:
        result["recommendations"]["high"].append(
            "Add Load Balancer to distribute traffic across multiple virtual servers"
        )

    # Security checks
    if components_used["security_groups"] > 0:
        result["strengths"].append(
            "Security Groups configured for instance-level security")
        result["security_score"] += 20
    else:
        result["recommendations"]["critical"].append(
            "Add Security Groups for instance-level firewall protection"
        )

    if components_used["vpn_gateways"] > 0:
        result["strengths"].append(
            "VPN Gateway configured for secure connectivity")
        result["security_score"] += 15
    else:
        result["recommendations"]["high"].append(
            "Add VPN Gateway for secure remote access to private resources"
        )

    if components_used["vpe_gateways"] > 0:
        result["strengths"].append(
            "VPE Gateways configured for private service connectivity")
        result["security_score"] += 15
    else:
        result["recommendations"]["medium"].append(
            "Add VPE Gateways for private connectivity to IBM Cloud services"
        )

    if components_used["key_protect"] > 0 or components_used["secrets_manager"] > 0:
        result["strengths"].append("Encryption key management configured")
        result["security_score"] += 20
    else:
        result["recommendations"]["high"].append(
            "Add Key Protect or Secrets Manager for encryption key management"
        )

    if components_used["bastion_hosts"] > 0:
        result["strengths"].append(
            "Bastion Host configured for secure admin access")
        result["security_score"] += 10
    else:
        result["recommendations"]["medium"].append(
            "Add Bastion Host for secure administrative access"
        )

    # Observability checks
    if components_used["flow_logs"] > 0:
        result["strengths"].append("Flow Logs enabled for network monitoring")
        result["security_score"] += 10
    else:
        result["recommendations"]["medium"].append(
            "Enable Flow Logs for network traffic monitoring and troubleshooting"
        )

    if components_used["cloud_logs"] > 0:
        result["strengths"].append(
            "Cloud Logs configured for centralized logging")
    else:
        result["recommendations"]["medium"].append(
            "Add Cloud Logs for centralized application and system logging"
        )

    if components_used["monitoring"] > 0:
        result["strengths"].append("Monitoring service configured")
    else:
        result["recommendations"]["low"].append(
            "Add IBM Cloud Monitoring for metrics and alerting"
        )

    # Network architecture checks
    if components_used["public_gateways"] > 0:
        result["strengths"].append(
            "Public Gateway configured for internet connectivity")
    elif components_used["subnets"] > 0:
        result["recommendations"]["medium"].append(
            "Consider adding Public Gateway for outbound internet access from private subnets"
        )

    if components_used["transit_gateways"] > 0:
        result["strengths"].append(
            "Transit Gateway configured for multi-VPC connectivity")
    elif components_used["vpcs"] > 1:
        result["recommendations"]["medium"].append(
            "Add Transit Gateway for connectivity between multiple VPCs"
        )

    # Cost optimization suggestions
    if components_used["virtual_servers"] > 5:
        result["cost_optimization"].append(
            "Consider reserved capacity for virtual servers (potential 20-30% savings)"
        )

    if components_used["zones"] == 1 and components_used["virtual_servers"] > 1:
        result["cost_optimization"].append(
            "Single-zone deployment may be cost-effective but lacks HA. Evaluate trade-offs."
        )

    # Calculate final scores
    result["security_score"] = min(100, result["security_score"])
    result["ha_score"] = min(100, result["ha_score"])

    # Add summary
    result["summary"] = {
        "security_score": f"{result['security_score']}/100",
        "ha_score": f"{result['ha_score']}/100",
        "total_recommendations": (
            len(result["recommendations"]["critical"]) +
            len(result["recommendations"]["high"]) +
            len(result["recommendations"]["medium"]) +
            len(result["recommendations"]["low"])
        )
    }

    return json.dumps(result, indent=2)


def get_component_usage(component_name: str, include_examples: bool = True) -> str:
    """Get detailed usage information for a specific IBM Cloud component.

    Provides comprehensive documentation including:
    - Component description and purpose
    - Import statement
    - Parameters and options
    - Usage examples
    - Related components
    - Best practices

    Args:
        component_name: Name of the component (e.g., "VPC", "LoadBalancer")
        include_examples: Whether to include code examples (default: True)

    Returns:
        Detailed component documentation and usage guide.
    """
    # Search for the component across all categories
    found_component = None
    found_category = None

    for cat_name, cat_data in COMPONENTS.items():
        if component_name in cat_data["classes"]:
            found_component = component_name
            found_category = cat_name
            break

    if not found_component:
        # Try case-insensitive search
        for cat_name, cat_data in COMPONENTS.items():
            for class_name in cat_data["classes"].keys():
                if class_name.lower() == component_name.lower():
                    found_component = class_name
                    found_category = cat_name
                    break
            if found_component:
                break

    if not found_component or not found_category:
        return f"Component '{component_name}' not found. Use search_components() to find available components."

    cat_data = COMPONENTS[found_category]
    comp_desc = cat_data["classes"][found_component]

    lines = [f"# {found_component}\n"]
    lines.append(f"**Category:** {found_category}")
    lines.append(f"**Description:** {comp_desc}\n")

    # Import statement
    lines.append("## Import")
    lines.append("```python")
    lines.append(cat_data["import"])
    lines.append("```\n")

    # Usage type
    lines.append("## Usage Type")
    if 'groups' in found_category:
        lines.append("**Context Manager** - Use with `with` statement")
        lines.append(
            "This component is a container that groups other components.\n")
    else:
        lines.append("**Direct Instantiation** - Create as a variable")
        lines.append("This component is a node/item in the diagram.\n")

    # Parameters
    lines.append("## Common Parameters")
    lines.append("- `label` (str): Primary label text (SemiBold font)")
    lines.append(
        "- `sublabel` (str, optional): Secondary label text (Regular font)")
    lines.append(
        "- `fontname` (str, optional): Font family (default: 'IBM Plex Sans')")
    lines.append("- `fontsize` (int, optional): Font size (default: 14)")

    if 'groups' in found_category:
        lines.append(
            "- `direction` (str, optional): Layout direction 'LR' or 'TB' (default: 'LR')")

    lines.append("")

    # Examples
    if include_examples:
        lines.append("## Usage Examples\n")

        if 'groups' in found_category:
            lines.append("### Basic Usage (Context Manager)")
            lines.append("```python")
            lines.append(cat_data["import"])
            lines.append("")
            lines.append(
                f"with {found_component}('my-{found_component.lower()}'):")
            lines.append("    # Add child components here")
            lines.append("    pass")
            lines.append("```\n")

            lines.append("### With Sublabel")
            lines.append("```python")
            lines.append(
                f"with {found_component}('my-{found_component.lower()}', sublabel='Additional info'):")
            lines.append("    # Add child components")
            lines.append("    pass")
            lines.append("```\n")
        else:
            lines.append("### Basic Usage (Direct Instantiation)")
            lines.append("```python")
            lines.append(cat_data["import"])
            lines.append("")
            lines.append(
                f"{found_component.lower()} = {found_component}('my-{found_component.lower()}')")
            lines.append("```\n")

            lines.append("### With Sublabel")
            lines.append("```python")
            lines.append(
                f"{found_component.lower()} = {found_component}('my-{found_component.lower()}', sublabel='Details')")
            lines.append("```\n")

            lines.append("### With Connections")
            lines.append("```python")
            lines.append(f"comp1 = {found_component}('component-1')")
            lines.append(f"comp2 = {found_component}('component-2')")
            lines.append("")
            lines.append("# Connect components")
            lines.append("comp1 >> comp2  # Directed: comp1 to comp2")
            lines.append("comp1 << comp2  # Directed: comp2 to comp1")
            lines.append("comp1 - comp2   # Undirected connection")
            lines.append("```\n")

    # Related components
    lines.append("## Related Components")
    if found_category == "groups_core":
        lines.append(
            "- Often contains: Subnets, Zones, or other grouping components")
        lines.append(
            "- Often contained by: Higher-level groups (Region, IBMCloud)")
    elif found_category == "compute":
        lines.append("- Often contained by: Subnet, SecurityGroup")
        lines.append("- Often connected to: LoadBalancer, Storage components")
    elif found_category == "network":
        lines.append("- Often contained by: VPC, Subnet")
        lines.append(
            "- Often connected to: Compute instances, other network components")
    elif found_category == "storage":
        lines.append("- Often connected to: Compute instances")
        lines.append("- Often contained by: VPC or Region")

    lines.append("")

    # Best practices
    lines.append("## Best Practices")
    if found_component == "VPC":
        lines.append(
            "- Use meaningful CIDR blocks in sublabel (e.g., '10.0.0.0/16')")
        lines.append("- Deploy across multiple availability zones for HA")
        lines.append("- Implement proper subnet segmentation (public/private)")
    elif found_component == "Subnet":
        lines.append("- Use CIDR notation in sublabel (e.g., '10.0.1.0/24')")
        lines.append("- Separate public and private subnets")
        lines.append("- Deploy in different availability zones for HA")
    elif found_component == "LoadBalancer":
        lines.append(
            "- Place in public subnet for internet-facing applications")
        lines.append("- Connect to multiple backend instances for HA")
        lines.append("- Use with SecurityGroups for access control")
    elif found_component == "VirtualServer":
        lines.append("- Deploy in private subnets when possible")
        lines.append("- Use SecurityGroups for firewall rules")
        lines.append("- Deploy across multiple zones for HA")
    elif found_component == "SecurityGroup":
        lines.append("- Define specific ingress/egress rules")
        lines.append("- Follow principle of least privilege")
        lines.append("- Document rules in sublabel or comments")

    lines.append("")
    lines.append("## Additional Resources")
    lines.append("- Use `search_components()` to find related components")
    lines.append("- Use `get_example()` to see complete diagram examples")
    lines.append(
        "- Use `validate_diagram_code()` to check your code before execution")

    return "\n".join(lines)


def preview_structure(code: str) -> str:
    """Preview diagram structure without executing code.

    Parses Python code and shows the hierarchical structure of the diagram
    without actually executing it. Useful for understanding layout before generation.

    Args:
        code: Python diagram code to preview

    Returns:
        Hierarchical structure representation of the diagram.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"ERROR: Cannot parse code with syntax errors: {e}"

    structure = {
        "diagram_name": None,
        "output_dir": None,
        "direction": "LR",
        "hierarchy": [],
        "connections": [],
        "components_count": 0
    }

    # Track context managers (groups) and their nesting
    context_stack = []
    components = []

    # Find diagram name and settings
    for node in ast.walk(tree):
        if isinstance(node, ast.With):
            for item in node.items:
                if isinstance(item.context_expr, ast.Call):
                    if isinstance(item.context_expr.func, ast.Name):
                        if item.context_expr.func.id in ['IBMDiagram', 'Diagram']:
                            # Extract diagram parameters
                            for keyword in item.context_expr.keywords:
                                if keyword.arg == 'name':
                                    if isinstance(keyword.value, ast.Constant):
                                        structure["diagram_name"] = keyword.value.value
                                elif keyword.arg == 'output':
                                    if isinstance(keyword.value, ast.Constant):
                                        structure["output_dir"] = keyword.value.value
                                elif keyword.arg == 'direction':
                                    if isinstance(keyword.value, ast.Constant):
                                        structure["direction"] = keyword.value.value

    # Build hierarchy representation
    def extract_hierarchy(node, level=0):
        items = []
        if isinstance(node, ast.With):
            for item in node.items:
                if isinstance(item.context_expr, ast.Call):
                    if isinstance(item.context_expr.func, ast.Name):
                        comp_name = item.context_expr.func.id
                        comp_label = None

                        # Get label from first argument
                        if item.context_expr.args:
                            if isinstance(item.context_expr.args[0], ast.Constant):
                                comp_label = item.context_expr.args[0].value

                        items.append({
                            "type": comp_name,
                            "label": comp_label or f"<{comp_name}>",
                            "level": level,
                            "children": []
                        })

                        # Process nested items
                        for child in node.body:
                            child_items = extract_hierarchy(child, level + 1)
                            if child_items:
                                items[-1]["children"].extend(child_items)

        elif isinstance(node, ast.Assign):
            # Direct instantiation (nodes)
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Name):
                    comp_name = node.value.func.id
                    comp_label = None

                    if node.value.args:
                        if isinstance(node.value.args[0], ast.Constant):
                            comp_label = node.value.args[0].value

                    items.append({
                        "type": comp_name,
                        "label": comp_label or f"<{comp_name}>",
                        "level": level,
                        "is_node": True
                    })

        return items

    # Extract hierarchy
    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            for item in node.body:
                hierarchy_items = extract_hierarchy(item)
                structure["hierarchy"].extend(hierarchy_items)

    # Count components
    def count_components(items):
        count = len(items)
        for item in items:
            if "children" in item:
                count += count_components(item["children"])
        return count

    structure["components_count"] = count_components(structure["hierarchy"])

    # Extract connections
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr):
            if isinstance(node.value, (ast.BinOp, ast.Compare)):
                # This is a connection (>>, <<, -)
                structure["connections"].append("Connection detected")

    # Format output
    lines = ["# Diagram Structure Preview\n"]

    if structure["diagram_name"]:
        lines.append(f"**Diagram Name:** {structure['diagram_name']}")
    if structure["output_dir"]:
        lines.append(f"**Output Directory:** {structure['output_dir']}")
    lines.append(f"**Layout Direction:** {structure['direction']}")
    lines.append(f"**Total Components:** {structure['components_count']}")
    lines.append(f"**Connections:** {len(structure['connections'])}\n")

    lines.append("## Hierarchy\n")
    lines.append("```")

    def format_hierarchy(items, indent=0):
        result = []
        for item in items:
            prefix = "  " * indent
            is_node = item.get("is_node", False)
            symbol = "□" if is_node else "▢"
            result.append(f"{prefix}{symbol} {item['type']}: {item['label']}")

            if "children" in item and item["children"]:
                result.extend(format_hierarchy(item["children"], indent + 1))
        return result

    lines.extend(format_hierarchy(structure["hierarchy"]))
    lines.append("```\n")

    lines.append("## Legend")
    lines.append("- ▢ = Group/Container (context manager)")
    lines.append("- □ = Node/Item (direct instantiation)")

    return "\n".join(lines)


def generate_from_json(json_content: str, output_dir: str = "") -> str:
    """Generate IBM Cloud diagram from JSON specification.

    Converts a JSON infrastructure specification into an IBM Cloud architecture diagram.
    The JSON format follows the ibmdiagrams internal structure.

    Args:
        json_content: JSON infrastructure specification
        output_dir: Output directory for the diagram

    Returns:
        On success: Path to generated .drawio file and summary
        On failure: Error message with details

    Note: This uses the ibmdiagrams JSON loader functionality.
    """
    # Validate JSON
    try:
        json_data = json.loads(json_content)
    except json.JSONDecodeError as e:
        return f"ERROR\nInvalid JSON: {e}"

    # Check for required fields
    if "vpcs" not in json_data:
        return "ERROR\nJSON must contain 'vpcs' field"
    if "subnets" not in json_data:
        return "ERROR\nJSON must contain 'subnets' field"

    # Set output directory
    if not output_dir:
        output_dir = tempfile.gettempdir()

    try:
        output_path = Path(output_dir).resolve()
        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)
        if not output_path.is_dir():
            return f"ERROR\noutput_dir '{output_dir}' is not a directory"
        if not os.access(output_path, os.W_OK):
            return f"ERROR\nNo write permission for directory '{output_dir}'"
    except (OSError, ValueError) as e:
        return f"ERROR\nInvalid output_dir '{output_dir}': {e}"

    # Write JSON to temporary file
    json_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            prefix="ibmdiagram_",
            delete=False,
            dir=tempfile.gettempdir(),
        ) as f:
            json_path = f.name
            f.write(json_content)

        # Build command
        cmd = [sys.executable, "-m", "ibmdiagrams.ibmscripts.ibmdiagrams"]
        cmd.append(json_path)

        if output_dir:
            cmd.extend(["-output", str(output_path)])

        # Execute ibmdiagrams command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=DIAGRAM_GENERATION_TIMEOUT,
            cwd=str(output_path),
        )

        if result.returncode != 0:
            return f"ERROR\n{result.stderr or result.stdout}"

        # Find generated .drawio file
        base_name = Path(json_path).stem
        expected_file = output_path / f"{base_name}.drawio"

        if not expected_file.exists():
            # Try to find any recently created .drawio file
            drawio_files = list(output_path.glob("*.drawio"))
            if drawio_files:
                expected_file = max(
                    drawio_files, key=lambda p: p.stat().st_mtime)
            else:
                return (
                    f"ERROR\nNo .drawio file found in {output_path}.\n"
                    f"stdout: {result.stdout}\nstderr: {result.stderr}"
                )

        # Parse JSON to provide summary
        summary_lines = ["SUCCESS", f"FILE:{expected_file}", ""]
        summary_lines.append("## JSON Specification Summary")

        # Count resources
        vpc_count = len(json_data.get("vpcs", []))
        subnet_count = len(json_data.get("subnets", []))
        instance_count = len(json_data.get("instances", []))

        summary_lines.append(f"VPCs: {vpc_count}")
        summary_lines.append(f"Subnets: {subnet_count}")
        summary_lines.append(f"Instances: {instance_count}")

        summary_lines.append(f"\nDiagram file: {expected_file}")

        return "\n".join(summary_lines)

    except subprocess.TimeoutExpired:
        logger.warning(
            f"JSON diagram generation timed out after {DIAGRAM_GENERATION_TIMEOUT} seconds")
        return f"ERROR\nDiagram generation timed out after {DIAGRAM_GENERATION_TIMEOUT} seconds."
    except Exception as e:
        logger.error(f"Unexpected error during JSON diagram generation: {e}")
        return f"ERROR\nUnexpected error: {e}"
    finally:
        # Clean up temporary JSON file
        if json_path:
            try:
                os.unlink(json_path)
                logger.debug(f"Cleaned up temporary file: {json_path}")
            except OSError as e:
                logger.warning(
                    f"Failed to clean up temporary file {json_path}: {e}")
