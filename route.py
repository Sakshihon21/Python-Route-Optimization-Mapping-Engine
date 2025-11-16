import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
import folium

# Speed improvements (DO NOT change logic)
ox.settings.use_cache = True
ox.settings.log_console = False

geolocator = Nominatim(user_agent="route_optimizer")

print("Enter Source Location: ", end="")
source_name = input().strip()

print("Enter Destination Location: ", end="")
dest_name = input().strip()

# Geocode user input
source = geolocator.geocode(source_name)
dest = geolocator.geocode(dest_name)

if source is None:
    print("❌ Invalid Source Address")
    exit()
if dest is None:
    print("❌ Invalid Destination Address")
    exit()

# Get bbox automatically based on both locations
north = max(source.latitude, dest.latitude) + 0.02
south = min(source.latitude, dest.latitude) - 0.02
east = max(source.longitude, dest.longitude) + 0.02
west = min(source.longitude, dest.longitude) - 0.02

print("📦 Fetching road network...")
print(f"North={north}, South={south}, East={east}, West={west}")

# Fetch map using bounding box (same as your logic)
G = ox.graph_from_bbox(north, south, east, west, network_type="drive")

print("🔍 Finding nearest nodes...")
orig_node = ox.nearest_nodes(G, source.longitude, source.latitude)
dest_node = ox.nearest_nodes(G, dest.longitude, dest.latitude)

print("🚀 Calculating shortest path...")
try:
    # Try weighted shortest path first
    route = nx.shortest_path(G, orig_node, dest_node, weight="length")
except:
    print("⚠️ Direct path not found. Trying fallback...")
    try:
        route = nx.shortest_path(G, orig_node, dest_node)
    except:
        print("❌ No route found between these locations.")
        exit()

# Create map and plot route
print("🗺 Creating map...")
m = folium.Map(location=[source.latitude, source.longitude], zoom_start=12)
ox.plot_route_folium(G, route, route_map=m)

m.save("route_map.html")
print("✅ Route saved as route_map.html")
