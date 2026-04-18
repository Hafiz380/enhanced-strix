
import asyncio
import json
import logging
import time
import os
from pathlib import Path
from typing import List, Dict, Any

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Template

from strix.agents.StrixAgent.strix_agent import StrixAgent
from strix.llm.config import LLMConfig
from strix.telemetry.tracer import Tracer, set_global_tracer, get_global_tracer

# Global state for current session
current_vulnerabilities: Dict[str, Any] = {}
history_file = Path.home() / ".strix" / "web_history.json"
history_file.parent.mkdir(parents=True, exist_ok=True)

app = FastAPI()

# Enhanced Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("strix-web")

# Serve static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.get("/")
async def get():
    index_file = static_path / "index.html"
    if index_file.exists():
        return HTMLResponse(index_file.read_text())
    return HTMLResponse("<h1>Strix Web Interface</h1><p>Index file not found.</p>")

@app.get("/api/vulnerability/{vuln_id}")
async def get_vulnerability(vuln_id: str):
    vuln = current_vulnerabilities.get(vuln_id)
    if vuln:
        return JSONResponse(vuln)
    return JSONResponse({"error": "Vulnerability not found"}, status_code=404)

@app.get("/api/history")
async def get_history():
    if history_file.exists():
        try:
            return JSONResponse(json.loads(history_file.read_text()))
        except Exception:
            return JSONResponse([])
    return JSONResponse([])

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "command":
                instruction = message["content"]
                logger.info(f"Received web command: {instruction}")
                asyncio.create_task(run_ai_task(instruction))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

def save_to_history(scan_id: str, instruction: str, status: str, vulnerabilities: list):
    history = []
    if history_file.exists():
        try:
            history = json.loads(history_file.read_text())
        except Exception:
            history = []
    
    history.append({
        "id": scan_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "instruction": instruction,
        "status": status,
        "vulnerabilities_count": len(vulnerabilities)
    })
    
    # Keep last 100 scans
    if len(history) > 100:
        history = history[-100:]
        
    history_file.write_text(json.dumps(history, indent=2))

async def run_ai_task(instruction: str):
    """Executes the actual AI task using StrixAgent and broadcasts updates."""
    scan_id = f"web_{int(time.time())}"
    current_vulnerabilities.clear()
    
    try:
        # Initialize tracer if not exists
        run_name = f"web_run_{int(time.time())}"
        tracer = Tracer(run_name)
        set_global_tracer(tracer)
        
        logger.info(f"Starting Scan [{scan_id}] with instruction: {instruction}")

        # 1. Setup scan config
        scan_config = {
            "targets": [{"type": "web_application", "details": {"target_url": "http://localhost"}, "original": "Web Interface Instruction"}],
            "user_instructions": instruction,
            "scan_id": scan_id,
            "scan_mode": "standard",
            "run_name": tracer.run_name
        }

        # 2. Add vulnerability callback to tracer
        async def on_vuln_found(vuln):
            vuln_id = vuln["id"]
            current_vulnerabilities[vuln_id] = vuln
            logger.info(f"Vulnerability Discovered: {vuln['title']} ({vuln['severity']})")
            await manager.broadcast({
                "type": "vulnerability",
                "id": vuln_id,
                "title": vuln["title"],
                "severity": vuln["severity"],
                "target": vuln.get("target", "N/A"),
                "description": vuln.get("description", "No description provided.")
            })
        
        def vuln_callback_wrapper(vuln):
            asyncio.create_task(on_vuln_found(vuln))
            
        tracer.vulnerability_found_callback = vuln_callback_wrapper

        # 3. Hook into tool execution
        original_log_start = tracer.log_tool_execution_start
        def hooked_log_start(agent_id, tool_name, args):
            exec_id = original_log_start(agent_id, tool_name, args)
            logger.info(f"AI using tool: {tool_name} with args: {args}")
            asyncio.create_task(manager.broadcast({
                "type": "tool_usage",
                "agent_id": agent_id,
                "tool": tool_name,
                "logic": f"Executing {tool_name} to solve the problem."
            }))
            return exec_id
        
        tracer.log_tool_execution_start = hooked_log_start

        # 4. Initialize Agent
        agent = StrixAgent({"state": None})
        
        # 5. Hook into LLM streaming
        original_generate = agent.llm.generate
        async def hooked_generate(history):
            async for response in original_generate(history):
                if response.thinking_blocks:
                    thinking_text = "".join([b.get("text", "") for b in response.thinking_blocks if b.get("type") == "thinking"])
                    if thinking_text:
                        await manager.broadcast({"type": "thinking", "content": thinking_text})
                
                if response.content:
                    await manager.broadcast({"type": "console", "content": response.content, "style": "white"})
                
                yield response

        agent.llm.generate = hooked_generate

        await manager.broadcast({"type": "console", "content": f"[SYSTEM] Starting task: {instruction}", "style": "bold green"})
        
        # Execute the scan
        result = await agent.execute_scan(scan_config)
        
        save_to_history(scan_id, instruction, "Completed", list(current_vulnerabilities.values()))
        
        await manager.broadcast({"type": "console", "content": f"[SUCCESS] Task Finished", "style": "bold cyan"})
        await manager.broadcast({"type": "action", "content": "Idle"})
        await manager.broadcast({"type": "thinking", "content": "Task finished successfully."})
        logger.info(f"Scan [{scan_id}] completed successfully.")

    except Exception as e:
        logger.error(f"Error in Scan [{scan_id}]: {e}", exc_info=True)
        save_to_history(scan_id, instruction, "Failed", [])
        await manager.broadcast({"type": "console", "content": f"[ERROR] {str(e)}", "style": "bold red"})
        await manager.broadcast({"type": "action", "content": "Error"})

def start_web_gui(host: str = "0.0.0.0", port: int = 8000):
    logger.info(f"Starting Strix Web GUI at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
