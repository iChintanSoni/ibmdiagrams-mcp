# IBM Diagrams MCP Server

An MCP (Model Context Protocol) server that provides tools for generating IBM Cloud architecture diagrams using the `ibmdiagrams` library.

## Overview

This MCP server enables AI assistants and other MCP clients to:

- **Browse & Search**: Discover IBM Cloud diagram components by category or keyword
- **Validate**: Check diagram code before execution with AST-based validation
- **Generate**: Create diagrams from Python code, Terraform state, or JSON specifications
- **Preview**: Visualize diagram structure without execution
- **Analyze**: Get architectural recommendations, best practices, and cost optimization
- **Learn**: Access comprehensive guides, examples, patterns, and design prompts

## Prerequisites

- Python 3.13 or higher
- The `ibmdiagrams` package (must be installed separately)
- `mcp` package (installed automatically)

## Installation

### 1. Install the ibmdiagrams package

The `ibmdiagrams` package is a separate dependency that must be available on your system. Currently, it's referenced as a local package in `pyproject.toml`:

```toml
ibmdiagrams @ file:///Users/chintansoni/Github/ibmdiagrams
```

**Important:** You need to update this path to match your local setup:

1. Clone or obtain the `ibmdiagrams` package
2. Update the path in `pyproject.toml` to point to your local `ibmdiagrams` directory
3. Alternatively, use a relative path: `ibmdiagrams @ file:///../ibmdiagrams`

### 2. Install this MCP server

```bash
# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

## Usage

### Running the Server

```bash
ibmdiagrams-mcp
```

The server runs using the `streamable-http` transport protocol.

### Available Tools (10 Tools)

#### 1. `list_components` (Browse)

List available IBM Cloud diagram components organized by category.

**Parameters:**

- `category` (optional): Filter by category (diagram, groups_core, compute, network, storage, data, security, containers, ai, devops, observability, actors, connectors)

**Example:**

```python
list_components(category="compute")
```

#### 2. `search_components` (NEW - Search)

Search for IBM Cloud diagram components by keyword across all categories.

**Parameters:**

- `query` (required): Search term (case-insensitive)
- `category` (optional): Filter by specific category

**Example:**

```python
search_components(query="load balancer")
search_components(query="storage", category="storage")
```

**Why use this:** Much faster than browsing categories when you know what component you need.

#### 3. `get_example` (Examples)

Get example IBM Cloud diagram code.

**Parameters:**

- `name` (optional): Example name (vpc_basic, vpc_multi_zone, watsonx_architecture, openshift_on_vpc)

**Example:**

```python
get_example(name="vpc_basic")
```

#### 4. `validate_diagram_code` (NEW - Validation)

Validate IBM Cloud diagram Python code before execution using AST-based analysis.

**Parameters:**

- `code` (required): Python code to validate

**Returns:** JSON with validation status, errors, warnings, and suggestions

**Example:**

```python
code = """
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import VPC

with IBMDiagram(name="Test"):
    vpc = VPC("my-vpc")
"""
result = validate_diagram_code(code=code)
```

**Why use this:** Catch errors before execution, improve success rate, identify security concerns.

#### 5. `generate_diagram` (Generate from Python)

Generate an IBM Cloud architecture diagram from Python code.

**Parameters:**

- `code` (required): Python code using the ibmdiagrams API
- `output_dir` (optional): Directory for output file (default: /tmp)

**Security Warning:** This tool executes arbitrary Python code. Use only in trusted environments with trusted input. See security considerations below.

**Example:**

```python
code = """
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import IBMCloud, VPC, Subnet
from ibmdiagrams.ibmcloud.compute import VirtualServer

with IBMDiagram(name="My Diagram", output="/tmp"):
    with IBMCloud("IBM Cloud"):
        with VPC("my-vpc"):
            with Subnet("subnet-1"):
                VirtualServer("vsi-1")
"""
generate_diagram(code=code, output_dir="/tmp")
```

#### 6. `generate_from_terraform` (NEW - HIGH PRIORITY)

Generate IBM Cloud diagrams directly from Terraform state files.

**Parameters:**

- `tfstate_content` (required): Terraform state file content (JSON format from `terraform show -json`)
- `label_type` (optional): "custom" (detailed, default) or "general" (simplified)
- `output_dir` (optional): Output directory (default: system temp)

**Example:**

```python
# Get Terraform state
import subprocess
result = subprocess.run(['terraform', 'show', '-json'], capture_output=True, text=True)
tfstate = result.stdout

# Generate diagram
diagram_result = generate_from_terraform(
    tfstate_content=tfstate,
    label_type="custom",
    output_dir="./diagrams"
)
```

**Why use this:** Core ibmdiagrams feature - visualize your infrastructure-as-code automatically. Supports VPCs, subnets, virtual servers, load balancers, storage, security groups, and more.

#### 7. `analyze_architecture` (NEW - Architecture Analysis)

Analyze IBM Cloud diagram code for best practices, security, high availability, and cost optimization.

**Parameters:**

- `code` (required): Python diagram code to analyze

**Returns:** Detailed analysis with:

- Security score and recommendations
- High availability score and suggestions
- Missing critical components
- Best practices violations
- Prioritized action items

**Example:**

```python
code = """
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import VPC, Subnet
from ibmdiagrams.ibmcloud.compute import VirtualServer

with IBMDiagram("Production App"):
    with VPC("prod-vpc"):
        with Subnet("app-subnet"):
            VirtualServer("app-server")
"""
result = analyze_architecture(code=code)
```

**Why use this:** Get expert architectural feedback before deployment. Identifies security gaps, HA issues, and optimization opportunities.

#### 8. `get_component_usage` (NEW - Component Documentation)

Get detailed usage information for any IBM Cloud component.

**Parameters:**

- `component_name` (required): Name of the component (e.g., "VPC", "LoadBalancer")
- `include_examples` (optional): Include code examples (default: True)

**Returns:** Comprehensive documentation including:

- Description and purpose
- Import statement
- Parameters and options
- Usage examples
- Related components
- Best practices

**Example:**

```python
result = get_component_usage(component_name="LoadBalancer", include_examples=True)
```

**Why use this:** Quick reference for any component without leaving your workflow.

#### 9. `preview_structure` (NEW - Structure Preview)

Preview diagram structure without executing code. Parses Python code and shows hierarchical layout.

**Parameters:**

- `code` (required): Python diagram code to preview

**Returns:** Hierarchical structure showing:

- Diagram name and settings
- Component hierarchy with nesting
- Total component count
- Connection count
- Layout direction

**Example:**

```python
code = """
from ibmdiagrams.ibmcloud.diagram import IBMDiagram
from ibmdiagrams.ibmcloud.groups import VPC, Subnet
from ibmdiagrams.ibmcloud.compute import VirtualServer

with IBMDiagram("Test", direction="TB"):
    with VPC("my-vpc"):
        with Subnet("subnet-1"):
            VirtualServer("web-1")
"""
result = preview_structure(code=code)
```

**Why use this:** Understand diagram layout before generation. Useful for complex architectures.

#### 10. `generate_from_json` (NEW - JSON to Diagram)

Generate IBM Cloud diagrams from JSON infrastructure specifications.

**Parameters:**

- `json_content` (required): JSON infrastructure specification
- `output_dir` (optional): Output directory (default: system temp)

**JSON Format:**

```json
{
  "vpcs": [{ "name": "prod-vpc", "cidr": "10.0.0.0/16" }],
  "subnets": [
    { "name": "web-subnet", "vpc": "prod-vpc", "cidr": "10.0.1.0/24" }
  ],
  "instances": [{ "name": "web-1", "subnet": "web-subnet" }]
}
```

**Example:**

```python
json_spec = '''
{
  "vpcs": [{"name": "production", "cidr": "10.0.0.0/16"}],
  "subnets": [{"name": "public", "vpc": "production", "cidr": "10.0.1.0/24"}],
  "instances": [{"name": "web-server", "subnet": "public"}]
}
'''
result = generate_from_json(json_content=json_spec, output_dir="./diagrams")
```

**Why use this:** Programmatic diagram generation from structured data. Useful for automation and integration.

### Available Resources (6 Resources)

#### 1. `resource://ibmdiagrams/quickstart`

Quick-start guide for building IBM Cloud diagrams with Python code.

#### 2. `resource://ibmdiagrams/terraform-guide` (NEW)

Comprehensive guide for converting Terraform state files to diagrams, including:

- Step-by-step workflow
- Label type explanations
- Supported resources list
- Best practices for large infrastructures
- Troubleshooting common issues
- CI/CD integration examples

#### 3. `resource://ibmdiagrams/best-practices` (NEW)

IBM Cloud architecture best practices guide covering:

- Security best practices (defense in depth, encryption, access control)
- High availability patterns (multi-zone, load balancing, auto-scaling)
- Cost optimization strategies
- Performance optimization
- Disaster recovery planning
- Compliance and governance
- Network design principles
- Storage best practices

#### 4. `resource://ibmdiagrams/architecture-patterns` (NEW)

Common IBM Cloud architecture patterns catalog with complete code templates:

1. **Three-Tier Web Application** - Classic web app with LB, app servers, database
2. **Microservices Architecture** - Kubernetes-based microservices with service mesh
3. **Data Lake Architecture** - Object storage, analytics, and data processing
4. **Hybrid Cloud Setup** - On-premises to cloud connectivity
5. **High Availability Multi-Zone** - Redundant infrastructure across zones
6. **Serverless Event-Driven** - Cloud Functions with event triggers
7. **AI/ML Platform** - Watson services with data pipeline

Each pattern includes:

- Complete working code
- Architecture diagram description
- Use cases and benefits
- Implementation notes

#### 5. `resource://ibmdiagrams/component-reference` (NEW)

Complete IBM Cloud component reference guide with:

- All 14 component categories
- Detailed documentation for each component
- Usage examples and parameters
- Common use cases
- Best practices per component
- Quick reference tables
- Common patterns

#### 6. `resource://ibmdiagrams/troubleshooting` (NEW)

Comprehensive troubleshooting guide covering:

- Installation issues
- Import errors
- Diagram generation failures
- Layout problems
- Component issues
- Connection problems
- File output issues
- Performance issues
- Validation errors
- Common error messages reference

### Available Prompts (5 Prompts)

#### 1. `design_architecture`

Generate a prompt for designing an IBM Cloud architecture diagram based on a natural language description.

**Parameters:**

- `description` (required): Natural language description of the architecture

**Example:** "Design a three-tier web application with load balancer, app servers, and database"

#### 2. `analyze_terraform_state` (NEW)

Analyze Terraform state and generate optimal diagrams with architectural recommendations.

**Parameters:**

- `description` (optional): Context about the infrastructure (e.g., "production environment")

**What it does:**

1. Guides through Terraform state analysis
2. Generates initial diagram
3. Analyzes for security, HA, cost optimization
4. Provides specific recommendations
5. Offers to generate enhanced architecture

**Example use case:** "Analyze my production infrastructure and suggest improvements for high availability"

#### 3. `enhance_security` (NEW)

Add security components and best practices to existing diagrams.

**Parameters:**

- `existing_code` (required): Current diagram Python code

**What it does:**

1. Analyzes current security posture
2. Identifies missing security components
3. Suggests security enhancements
4. Generates updated code with security layers
5. Provides implementation guidance

**Example use case:** "Add security best practices to my web application diagram"

#### 4. `make_highly_available` (NEW)

Transform single-zone architecture to multi-zone high availability setup.

**Parameters:**

- `existing_code` (required): Current diagram Python code

**What it does:**

1. Analyzes current architecture
2. Identifies single points of failure
3. Designs multi-zone redundancy
4. Adds load balancing and failover
5. Generates HA-ready code

**Example use case:** "Make my application highly available across multiple zones"

#### 5. `optimize_costs` (NEW)

Analyze architecture and provide cost optimization recommendations.

**Parameters:**

- `diagram_code` (required): Python diagram code to analyze
- `budget_constraint` (optional): Monthly budget in USD (e.g., "5000")
- `optimization_priority` (optional): "cost" (minimize costs), "performance" (balance), or "reliability" (maintain reliability)

**What it does:**

1. Analyzes component usage and costs
2. Identifies cost optimization opportunities
3. Provides estimated savings per recommendation
4. Prioritizes by impact (High/Medium/Low)
5. Suggests implementation steps
6. Includes budget analysis if provided

**Returns:**

- Total estimated monthly savings
- Prioritized recommendations by category
- Quick wins (high-impact items)
- Implementation guidance
- Cost management best practices

**Example use case:** "Optimize my architecture for cost while maintaining performance"

## Key Features

### 🔍 Smart Search & Discovery

- **Category browsing**: Organized by compute, network, storage, security, etc.
- **Keyword search**: Find components quickly across all categories
- **Detailed documentation**: Import paths, parameters, and usage examples

### ✅ Code Validation

- **AST-based analysis**: Parse code without execution
- **Security checks**: Detect dangerous imports and operations
- **Structure validation**: Ensure proper IBMDiagram usage
- **Helpful suggestions**: Get actionable feedback before generation

### 🏗️ Multiple Input Methods

- **Python code**: Full programmatic control with ibmdiagrams API
- **Terraform state**: Automatic visualization of infrastructure-as-code
- **JSON specifications**: Programmatic diagram generation from structured data

### 🎯 Intelligent Assistance

- **Architecture analysis**: Get recommendations for security, HA, and cost optimization
- **Best practices**: Built-in IBM Cloud architecture patterns and guidelines
- **Design prompts**: Guided diagram creation from natural language descriptions
- **Component documentation**: Instant access to detailed usage information
- **Structure preview**: Visualize layout before generation

### 💰 Cost Optimization

- **Cost analysis**: Identify optimization opportunities across all components
- **Estimated savings**: Get specific savings estimates per recommendation
- **Priority-based**: Recommendations sorted by impact (High/Medium/Low)
- **Budget tracking**: Compare against budget constraints
- **Quick wins**: Identify high-impact, easy-to-implement optimizations

### 🔒 Security & Compliance

- **Security scoring**: Automated security posture assessment
- **Best practices**: Built-in security recommendations
- **Enhancement prompts**: Add security layers to existing architectures
- **Compliance guidance**: Follow IBM Cloud security standards

## Component Categories

The server provides access to the following IBM Cloud component categories:

- **diagram**: Top-level diagram context manager
- **groups_core**: Core grouping shapes (IBMCloud, VPC, Subnet, Region, etc.)
- **groups_control**: Control/zone shapes (SecurityGroup, ResourceGroup, etc.)
- **groups_expanded**: Expanded node shapes
- **compute**: Compute services (VirtualServer, BareMetalServer, etc.)
- **network**: Network services (LoadBalancer, TransitGateway, etc.)
- **storage**: Storage services (ObjectStorage, BlockStorage, etc.)
- **data**: Data and database services (Db2, PostgreSQL, Redis, etc.)
- **security**: Security services (VPNGateway, KeyProtect, etc.)
- **containers**: Container platforms (OpenShift, KubernetesService, etc.)
- **ai**: AI and Watson services (watsonx, WatsonStudio, etc.)
- **devops**: DevOps services (ContinuousDelivery, Toolchain, etc.)
- **observability**: Monitoring services (CloudLogs, Monitoring, etc.)
- **actors**: Actor shapes (User, Application, etc.)
- **connectors**: Edge types for linking shapes

## Security Considerations

### Code Execution Risk

The `generate_diagram` tool executes arbitrary Python code provided by users. This poses significant security risks:

- **File System Access**: Code can read/write files with server process permissions
- **Network Access**: Code can make arbitrary network requests
- **System Commands**: Code can execute system commands
- **Module Imports**: Code can import any available Python modules

### Recommended Security Measures

1. **Trusted Environments Only**: Only deploy in trusted environments
2. **Input Validation**: Review code before execution when possible
3. **Sandboxing**: Consider running in containers or VMs with limited permissions
4. **Network Isolation**: Restrict network access for the server process
5. **File System Restrictions**: Use chroot or similar to limit file system access
6. **Monitoring**: Log and monitor all diagram generation requests

### Built-in Protections

The server includes some basic protections:

- Output directory validation and path traversal prevention
- Execution timeout (60 seconds default)
- Temporary file cleanup
- Error logging

However, these do NOT provide complete security against malicious code.

## Configuration

### Timeout Configuration

The diagram generation timeout is set to 60 seconds by default. To modify:

1. Edit `src/ibmdiagrams_mcp/__init__.py`
2. Change the `DIAGRAM_GENERATION_TIMEOUT` constant

### Logging

Logging is configured at the INFO level by default. To adjust:

```python
import logging
logging.basicConfig(level=logging.DEBUG)  # or WARNING, ERROR, etc.
```

## Development

### Project Structure

```
ibmdiagrams-mcp/
├── src/
│   └── ibmdiagrams_mcp/
│       ├── __init__.py      # Main server with tool/resource/prompt registration
│       ├── tools.py         # All tool implementations (10 tools)
│       ├── resources.py     # All resource implementations (6 resources)
│       ├── prompts.py       # All prompt implementations (5 prompts)
│       └── catalog.py       # Component and example definitions
├── pyproject.toml           # Project configuration
├── README.md               # This file
└── .gitignore
```

### Feature Summary

**Phase 1 - Foundation (Completed):**

- Core tools: list_components, get_example, generate_diagram
- Validation: validate_diagram_code with AST analysis
- Terraform: generate_from_terraform with comprehensive support
- Search: search_components for quick discovery
- Resources: quickstart_guide, terraform_guide
- Prompts: design_architecture, analyze_terraform_state

**Phase 2 - Enhancement (Completed):**

- Code refactoring: Separated into tools.py, resources.py, prompts.py
- Architecture analysis: analyze_architecture with security/HA scoring
- Component docs: get_component_usage with detailed information
- Best practices: best_practices_guide resource
- Patterns: architecture_patterns_guide with 7 common patterns
- Security: enhance_security prompt
- High availability: make_highly_available prompt

**Phase 3 - Completion (Completed):**

- Structure preview: preview_structure tool
- JSON support: generate_from_json tool
- Component reference: component_reference_guide resource
- Troubleshooting: troubleshooting_guide resource
- Cost optimization: optimize_costs prompt with detailed analysis

### Making the Project Portable

To make this project work on other systems:

1. **Option A: Use Relative Path**

   ```toml
   ibmdiagrams @ file:///../ibmdiagrams
   ```

2. **Option B: Use Environment Variable**

   ```toml
   ibmdiagrams @ file:///${IBMDIAGRAMS_PATH}
   ```

3. **Option C: Publish to PyPI**
   Publish the `ibmdiagrams` package to PyPI and reference it normally:
   ```toml
   ibmdiagrams = "^1.0.0"
   ```

## Troubleshooting

### ImportError: ibmdiagrams package not found

**Solution:** Ensure the `ibmdiagrams` package is installed and the path in `pyproject.toml` is correct.

### Permission Denied when writing diagrams

**Solution:** Ensure the output directory has write permissions for the server process.

### Diagram generation timeout

**Solution:** Increase `DIAGRAM_GENERATION_TIMEOUT` or optimize your diagram code.

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

[Add support contact information here]
