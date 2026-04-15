"""
IBM Diagrams MCP Server
An MCP server for generating IBM Cloud architecture diagrams.
"""

from . import prompts
from . import resources
from . import tools
import logging

from mcp.server.fastmcp import FastMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import catalog data
try:
    from .catalog import COMPONENTS, EXAMPLES
except ImportError as e:
    logger.error(f"Failed to import catalog: {e}")
    raise ImportError(
        "Failed to import catalog module. Ensure the package is properly installed."
    ) from e

# Verify ibmdiagrams package is available
try:
    import ibmdiagrams
    logger.info("ibmdiagrams package successfully imported")
except ImportError as e:
    logger.error(
        "ibmdiagrams package not found. Please install it or check the path in pyproject.toml"
    )
    raise ImportError(
        "The ibmdiagrams package is required but not found. "
        "Please ensure it's installed and accessible. "
        "Check the dependency path in pyproject.toml: "
        "ibmdiagrams @ file:///path/to/ibmdiagrams"
    ) from e

# Import tools, resources, and prompts

# Initialize FastMCP server
mcp = FastMCP("ibmdiagrams")

# ---------------------------------------------------------------------------
# Register Tools
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
    return tools.list_components(category)


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
    return tools.get_example(name)


@mcp.tool()
def generate_diagram(code: str, output_dir: str = "/tmp") -> str:
    """Generate an IBM Cloud architecture diagram from Python code.

    Executes the provided Python code (which must use the ibmdiagrams library)
    and returns the path to the generated .drawio file along with the XML content.

    SECURITY WARNING:
    This function executes arbitrary Python code. Use only in trusted environments.

    Args:
        code: Python code using the ibmdiagrams API
        output_dir: Directory for output file (default: /tmp)

    Returns:
        On success: "SUCCESS\nFILE:<path>\n\n<xml content>"
        On failure: "ERROR\n<stderr output>"
    """
    return tools.generate_diagram(code, output_dir)


@mcp.tool()
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
    return tools.validate_diagram_code(code)


@mcp.tool()
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
    return tools.search_components(query, category)


@mcp.tool()
def generate_from_terraform(tfstate_content: str, label_type: str = "custom", output_dir: str = "") -> str:
    """Generate IBM Cloud diagram from Terraform state file.

    Converts a Terraform state file (JSON format) into an IBM Cloud architecture diagram.
    This is a core feature of ibmdiagrams that enables infrastructure visualization.

    Args:
        tfstate_content: Terraform state file content in JSON format
        label_type: Label style - "custom" (detailed) or "general" (simplified)
        output_dir: Output directory for the diagram

    Returns:
        On success: Path to generated .drawio file and summary
        On failure: Error message with details
    """
    return tools.generate_from_terraform(tfstate_content, label_type, output_dir)


@mcp.tool()
def analyze_architecture(code: str) -> str:
    """Analyze IBM Cloud diagram code for best practices and completeness.

    Reviews architecture for security, HA, cost optimization, and missing components.

    Args:
        code: Python diagram code to analyze

    Returns:
        Detailed analysis with recommendations organized by priority.
    """
    return tools.analyze_architecture(code)


@mcp.tool()
def get_component_usage(component_name: str, include_examples: bool = True) -> str:
    """Get detailed usage information for a specific IBM Cloud component.

    Provides comprehensive documentation including description, import statement,
    parameters, usage examples, related components, and best practices.

    Args:
        component_name: Name of the component (e.g., "VPC", "LoadBalancer")
        include_examples: Whether to include code examples (default: True)

    Returns:
        Detailed component documentation and usage guide.
    """
    return tools.get_component_usage(component_name, include_examples)


@mcp.tool()
def preview_structure(code: str) -> str:
    """Preview diagram structure without executing code.

    Parses Python code and shows the hierarchical structure of the diagram
    without actually executing it. Useful for understanding layout before generation.

    Args:
        code: Python diagram code to preview

    Returns:
        Hierarchical structure representation of the diagram.
    """
    return tools.preview_structure(code)


@mcp.tool()
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
    """
    return tools.generate_from_json(json_content, output_dir)


# ---------------------------------------------------------------------------
# Register Resources
# ---------------------------------------------------------------------------

@mcp.resource("resource://ibmdiagrams/quickstart")
def quickstart_guide() -> str:
    """Quick-start guide for building IBM Cloud diagrams."""
    return resources.quickstart_guide()


@mcp.resource("resource://ibmdiagrams/terraform-guide")
def terraform_guide() -> str:
    """Comprehensive guide for converting Terraform to IBM Cloud diagrams."""
    return resources.terraform_guide()


@mcp.resource("resource://ibmdiagrams/best-practices")
def best_practices_guide() -> str:
    """IBM Cloud architecture best practices guide."""
    return resources.best_practices_guide()


@mcp.resource("resource://ibmdiagrams/architecture-patterns")
def architecture_patterns_guide() -> str:
    """Common IBM Cloud architecture patterns catalog."""
    return resources.architecture_patterns_guide()


@mcp.resource("resource://ibmdiagrams/component-reference")
def component_reference_guide() -> str:
    """Complete IBM Cloud component reference guide."""
    return resources.component_reference_guide()


@mcp.resource("resource://ibmdiagrams/troubleshooting")
def troubleshooting_guide() -> str:
    """Common issues and solutions for IBM Cloud diagrams."""
    return resources.troubleshooting_guide()


# ---------------------------------------------------------------------------
# Register Prompts
# ---------------------------------------------------------------------------

@mcp.prompt()
def design_architecture(description: str) -> str:
    """Generate a prompt for designing an IBM Cloud architecture diagram.

    Args:
        description: Natural language description of the architecture to diagram.
    """
    return prompts.design_architecture(description)


@mcp.prompt()
def analyze_terraform_state(description: str = "") -> str:
    """Analyze Terraform state and generate optimal IBM Cloud diagram with recommendations.

    Args:
        description: Optional context about the infrastructure
    """
    return prompts.analyze_terraform_state(description)


@mcp.prompt()
def enhance_security(existing_code: str) -> str:
    """Add security components to existing diagram.

    Args:
        existing_code: Current diagram Python code
    """
    return prompts.enhance_security(existing_code)


@mcp.prompt()
def make_highly_available(existing_code: str) -> str:
    """Transform single-zone to multi-zone HA architecture.

    Args:
        existing_code: Current diagram Python code
    """
    return prompts.make_highly_available(existing_code)


@mcp.prompt()
def optimize_costs(diagram_code: str, budget_constraint: str = "", optimization_priority: str = "cost") -> list:
    """Analyze architecture and provide cost optimization recommendations.

    Args:
        diagram_code: Python diagram code to analyze
        budget_constraint: Optional monthly budget in USD
        optimization_priority: Optimization approach (cost/performance/reliability)
    """
    prompt_config = prompts.optimize_costs_prompt()
    result = prompts.optimize_costs_handler(
        diagram_code, budget_constraint, optimization_priority)
    return [{"type": "text", "text": result}]


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the MCP server."""
    mcp.run(transport="streamable-http")


# Made with Bob
