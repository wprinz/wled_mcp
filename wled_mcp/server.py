"""WLED MCP Server implementation."""

import argparse
import json
import os
from typing import Any, Dict, Optional
import logging

from mcp.server.mcpserver import MCPServer
from .wled_client import WLEDClient

# Configure logging to stderr
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = MCPServer("WLED Controller")

def get_wled_client(host: Optional[str] = None) -> WLEDClient:
    """Get WLED client instance."""
    if not host:
        host = os.getenv("WLED_HOST")
        if not host:
            raise ValueError("WLED host must be provided or set via WLED_HOST environment variable")
    return WLEDClient(host)


@mcp.tool()
async def wled_get_info(host: Optional[str] = None) -> str:
    """Get WLED device information including version, LED count, and capabilities.
    
    Args:
        host: WLED device IP address or hostname (optional if WLED_HOST env var is set)
    
    Returns:
        JSON string with device information
    """
    try:
        client = get_wled_client(host)
        info = await client.get_info()
        return json.dumps(info, indent=2)
    except Exception as e:
        logger.error(f"Error getting WLED info: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def wled_get_state(host: Optional[str] = None) -> str:
    """Get current WLED device state including power, brightness, colors, and effects.
    
    Args:
        host: WLED device IP address or hostname (optional if WLED_HOST env var is set)
    
    Returns:
        JSON string with current device state
    """
    try:
        client = get_wled_client(host)
        state = await client.get_state()
        return json.dumps(state, indent=2)
    except Exception as e:
        logger.error(f"Error getting WLED state: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def wled_set_power(on: bool, host: Optional[str] = None) -> str:
    """Turn WLED device on or off.
    
    Args:
        on: True to turn on, False to turn off
        host: WLED device IP address or hostname (optional if WLED_HOST env var is set)
    
    Returns:
        JSON string with updated device state
    """
    try:
        client = get_wled_client(host)
        result = await client.set_power(on)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error setting WLED power: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def wled_set_brightness(brightness: int, host: Optional[str] = None) -> str:
    """Set WLED device brightness.
    
    Args:
        brightness: Brightness level (0-255)
        host: WLED device IP address or hostname (optional if WLED_HOST env var is set)
    
    Returns:
        JSON string with updated device state
    """
    try:
        client = get_wled_client(host)
        result = await client.set_brightness(brightness)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error setting WLED brightness: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def wled_set_color(r: int, g: int, b: int, host: Optional[str] = None) -> str:
    """Set WLED device color using RGB values.
    
    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)
        host: WLED device IP address or hostname (optional if WLED_HOST env var is set)
    
    Returns:
        JSON string with updated device state
    """
    try:
        client = get_wled_client(host)
        result = await client.set_color(r, g, b)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error setting WLED color: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def wled_set_effect(effect_id: int, speed: Optional[int] = None, 
                         intensity: Optional[int] = None, host: Optional[str] = None) -> str:
    """Set WLED lighting effect.
    
    Args:
        effect_id: Effect ID number (0 for solid color, 1+ for various effects)
        speed: Effect speed (0-255, optional)
        intensity: Effect intensity (0-255, optional)
        host: WLED device IP address or hostname (optional if WLED_HOST env var is set)
    
    Returns:
        JSON string with updated device state
    """
    try:
        client = get_wled_client(host)
        result = await client.set_effect(effect_id, speed, intensity)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error setting WLED effect: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def wled_get_effects(host: Optional[str] = None) -> str:
    """Get list of available WLED effects.
    
    Args:
        host: WLED device IP address or hostname (optional if WLED_HOST env var is set)
    
    Returns:
        JSON string with available effects and their IDs
    """
    try:
        client = get_wled_client(host)
        effects = await client.get_effects()
        return json.dumps(effects, indent=2)
    except Exception as e:
        logger.error(f"Error getting WLED effects: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def wled_get_palettes(host: Optional[str] = None) -> str:
    """Get list of available WLED color palettes.
    
    Args:
        host: WLED device IP address or hostname (optional if WLED_HOST env var is set)
    
    Returns:
        JSON string with available color palettes
    """
    try:
        client = get_wled_client(host)
        palettes = await client.get_palettes()
        return json.dumps(palettes, indent=2)
    except Exception as e:
        logger.error(f"Error getting WLED palettes: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def wled_get_presets(host: Optional[str] = None) -> str:
    """Get list of available WLED presets.
    
    Args:
        host: WLED device IP address or hostname (optional if WLED_HOST env var is set)
    
    Returns:
        JSON string with available presets and their names/IDs
    """
    try:
        client = get_wled_client(host)
        presets = await client.get_presets()
        return json.dumps(presets, indent=2)
    except Exception as e:
        logger.error(f"Error getting WLED presets: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def wled_activate_preset(preset_id: int, host: Optional[str] = None) -> str:
    """Activate a WLED preset by ID.
    
    Args:
        preset_id: Preset ID to activate (1-250)
        host: WLED device IP address or hostname (optional if WLED_HOST env var is set)
    
    Returns:
        JSON string with updated device state
    """
    try:
        client = get_wled_client(host)
        result = await client.activate_preset(preset_id)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error activating WLED preset: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def wled_set_state(state_json: str, host: Optional[str] = None) -> str:
    """Set WLED device state using raw JSON state object for advanced control.
    
    Args:
        state_json: JSON string representing the state to set
        host: WLED device IP address or hostname (optional if WLED_HOST env var is set)
    
    Returns:
        JSON string with updated device state
    """
    try:
        client = get_wled_client(host)
        state = json.loads(state_json)
        result = await client.set_state(state)
        return json.dumps(result, indent=2)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in state_json: {e}")
        return f"Error: Invalid JSON - {str(e)}"
    except Exception as e:
        logger.error(f"Error setting WLED state: {e}")
        return f"Error: {str(e)}"


def main(argv: Optional[list] = None) -> None:
    """Run the WLED MCP server (stdio by default, or over HTTP)."""
    parser = argparse.ArgumentParser(description="WLED MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default=os.getenv("MCP_TRANSPORT", "stdio"),
        help="Transport (default: stdio, env MCP_TRANSPORT)",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("MCP_HOST", "127.0.0.1"),
        help="Bind address for HTTP transports; use 0.0.0.0 to listen on all interfaces (env MCP_HOST)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("MCP_PORT", "8000")),
        help="Port for HTTP transports (env MCP_PORT)",
    )
    parser.add_argument(
        "--path",
        default=os.getenv("MCP_PATH", "/mcp"),
        help="URL path of the streamable-http endpoint (env MCP_PATH)",
    )
    args = parser.parse_args(argv)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        logger.info("Serving MCP on http://%s:%s%s", args.host, args.port, args.path)
        mcp.run(
            transport="streamable-http",
            host=args.host,
            port=args.port,
            streamable_http_path=args.path,
            transport_security=_transport_security(args.host),
        )
    else:
        logger.info("Serving MCP (SSE) on http://%s:%s", args.host, args.port)
        mcp.run(transport="sse", host=args.host, port=args.port)


def _transport_security(host: str):
    """Allow remote Host headers when bound to a non-loopback address.

    The SDK's DNS-rebinding protection only accepts localhost Host headers by
    default, which would reject requests from other machines.
    """
    if host in ("127.0.0.1", "localhost", "::1"):
        return None
    from mcp.server.transport_security import TransportSecuritySettings

    extra = [h for h in os.getenv("MCP_ALLOWED_HOSTS", "").split(",") if h.strip()]
    if not extra:
        # No allow-list configured: disable Host check (use a firewall/proxy).
        return TransportSecuritySettings(enable_dns_rebinding_protection=False)
    return TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[h.strip() for h in extra],
        allowed_origins=[],
    )


if __name__ == "__main__":
    main()
