from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("MyFirstServer", host="127.0.0.1", port=8000)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get the current real weather for a city."""
    async with httpx.AsyncClient() as client:
        # Step 1: Convert city name to latitude/longitude
        geo_response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}
        )
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return f"Could not find location: {city}"

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        found_name = location["name"]
        country = location.get("country", "")

        # Step 2: Get current weather for that location
        weather_response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True}
        )
        weather_data = weather_response.json()
        current = weather_data["current_weather"]

        temp = current["temperature"]
        windspeed = current["windspeed"]

        return f"Weather in {found_name}, {country}: {temp}°C, wind speed {windspeed} km/h."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")