import asyncio
import json
import argparse
from datetime import datetime
from typing import Optional

import httpx

# API base URL (local for CLI, remote for production)
API_BASE = "http://localhost:10000"

async def query_system(query: str, depth: int = 3, api_key: Optional[str] = None):
    """Query the system"""
    async with httpx.AsyncClient() as client:
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        response = await client.post(
            f"{API_BASE}/api/query",
            json={"query": query, "depth": depth},
            headers=headers,
            timeout=30.0
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

async def get_metrics(api_key: Optional[str] = None):
    """Get system metrics"""
    async with httpx.AsyncClient() as client:
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        response = await client.get(
            f"{API_BASE}/api/metrics",
            headers=headers,
            timeout=10.0
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

async def run_optimization(cycles: int = 2, api_key: Optional[str] = None):
    """Run optimization cycles"""
    async with httpx.AsyncClient() as client:
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        response = await client.post(
            f"{API_BASE}/api/optimize",
            json={"cycles": cycles},
            headers=headers,
            timeout=60.0
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

def print_result(result: dict):
    """Print query result"""
    print("\n" + "="*60)
    print("🧠 ABSOLUTE INTELLIGENCE SYSTEM - RESULT")
    print("="*60)
    
    print(f"\n📝 Query: {result['query']}")
    print(f"🆔 ID: {result['id']}")
    print(f"⏱️  Time: {result['processing_time_ms']:.1f}ms")
    
    print(f"\n📊 Metrics:")
    metrics = result['metrics']
    print(f"   Λ_Total: {metrics.get('lambda', 0):.3f}")
    print(f"   Grounding: {metrics.get('grounding', 0):.3f}")
    print(f"   Emergence: {metrics.get('emergence', 0):.2f}")
    print(f"   Depth: {metrics.get('depth_used', 0)}")
    
    print(f"\n💡 Answer:")
    answer = result['result'].get('answer', 'No answer generated')
    print(f"   {answer}")
    
    print(f"\n🎯 Recommendations:")
    for rec in result['result'].get('recommendations', []):
        print(f"   • {rec}")
    
    print(f"\n✅ Safety: {'PASS' if all(result.get('safety_passes', [])) else 'FAIL'}")

def print_metrics(metrics: dict):
    """Print system metrics"""
    print("\n" + "="*60)
    print("📈 SYSTEM METRICS")
    print("="*60)
    
    print(f"\n🏆 Performance:")
    print(f"   Λ_Total: {metrics['lambda_total']:.3f}")
    print(f"   Queries: {metrics['queries_processed']}")
    print(f"   Grounding: {metrics['avg_grounding']:.3f}")
    print(f"   Emergence: {metrics['avg_emergence']:.2f}")
    
    print(f"\n⚙️  System:")
    print(f"   Uptime: {metrics['uptime_seconds']:.0f}s")
    print(f"   Memory: {metrics['memory_usage_mb']:.1f}MB")
    print(f"   R³ Cycles: {metrics['r3_cycles']}")
    
    print(f"\n🔄 Status: {'✅ OPERATIONAL' if metrics['lambda_total'] > 0 else '⚠️  DEGRADED'}")

async def main():
    parser = argparse.ArgumentParser(description="Absolute Intelligence System CLI")
    parser.add_argument("--query", "-q", help="Process a query")
    parser.add_argument("--depth", "-d", type=int, default=3, help="Reasoning depth")
    parser.add_argument("--metrics", "-m", action="store_true", help="Show system metrics")
    parser.add_argument("--optimize", "-o", action="store_true", help="Run optimization")
    parser.add_argument("--cycles", "-c", type=int, default=2, help="Optimization cycles")
    parser.add_argument("--api-key", "-k", help="API key for authentication")
    parser.add_argument("--server", "-s", default=API_BASE, help="Server URL")
    
    args = parser.parse_args()
    
    global API_BASE
    API_BASE = args.server
    
    print("⚡ Absolute Intelligence System CLI")
    print(f"📡 Connecting to: {API_BASE}")
    
    if args.query:
        print(f"\n📨 Sending query: {args.query}")
        result = await query_system(args.query, args.depth, args.api_key)
        if result:
            print_result(result)
    
    elif args.metrics:
        print("\n📊 Fetching system metrics...")
        metrics = await get_metrics(args.api_key)
        if metrics:
            print_metrics(metrics)
    
    elif args.optimize:
        print(f"\n🌀 Running {args.cycles} optimization cycles...")
        result = await run_optimization(args.cycles, args.api_key)
        if result:
            print(f"\n✅ Optimization complete")
            print(f"   Cycles: {result['cycles_completed']}")
            print(f"   New Λ: {result['new_lambda']:.3f}")
    
    else:
        # Interactive mode
        print("\n💭 Entering interactive mode (Ctrl+C to exit)")
        try:
            while True:
                query = input("\n🧠 Query: ").strip()
                if query.lower() in ['exit', 'quit', 'q']:
                    break
                
                if query:
                    result = await query_system(query, args.depth, args.api_key)
                    if result:
                        print_result(result)
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
    
    print("\n" + "="*60)
    print("✅ CLI Complete")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
