import asyncio
import json
import socket
import websockets
import websockets.exceptions

latest = {"ax": 0.0, "ay": 0.0}

# ! WEBSOCKET DO NOT TOUCH IT WORKS AND I DONT KNOW WHY IT DOES IT JST DOES

async def handler(websocket):
    addr = websocket.remote_address
    print(f"[CONNECTED]    {addr[0]}:{addr[1]}")
    try:
        async for raw in websocket:
            try:
                data = json.loads(raw)
                latest["ax"] = float(data["ax"])
                latest["ay"] = float(data["ay"])
                print(
                    f"  ax={latest['ax']:+.3f}  ay={latest['ay']:+.3f}   ",
                    end="\r",
                    flush=True,
                )
            except (json.JSONDecodeError, KeyError, ValueError):
                pass  # drop awful frames
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        print(f"\n[DISCONNECTED] {addr[0]}:{addr[1]}")

# LAN IP (you can change things now)

def local_ips() -> list[str]:
    """Return all local IPv4 addresses, hotspot address first."""
    seen: set[str] = set()
    ips: list[str] = []
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip: str = info[4][0]
            if ip not in seen and not ip.startswith("127."):
                seen.add(ip)
                ips.append(ip)
    except Exception:
        pass
    ips.sort(key=lambda x: (0 if x.startswith("192.168.137.") else 1))
    return ips

# entry

async def main() -> None:
    PORT = 8765
    ips = local_ips()

    print("=" * 52)
    print("  Motion Cue — WebSocket Server")
    print("=" * 52)
    print(f"  Binding to  0.0.0.0:{PORT}  (all interfaces)")
    print()
    if ips:
        print("  Enter one of these into html:")
        for ip in ips:
            tag = "  ◀ Windows hotspot default" if ip.startswith("192.168.137.") else ""
            print(f"    {ip}{tag}")
    else:
        print("  Could not detect LAN IPs — check network adapter.")
    print()
    print("  Waiting for phone connection…")
    print("-" * 52)

    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()  # run until force or rage quit

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n ha ha rage quit.")
