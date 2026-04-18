# 🔑 API Configuration & Failover Setup

Enhanced Strix supports multiple LLM providers with automatic failover, performance-based routing, and secure credential management.

## 📁 Configuration File Location
You can manage your API settings using the human-readable configuration file located at:
`[project-root]/.config/api-config.yaml`

## 🛠️ How to Add a New Provider
To add a new API endpoint, open the `api-config.yaml` file and add a new entry under the `endpoints` list:

```yaml
endpoints:
  - name: "my-custom-provider"
    model: "openai/gpt-4o"
    api_key: "${MY_API_KEY}" # Uses environment variable for security
    api_base: "https://my-proxy.com/v1"
    priority: 1
```

### Fields Description:
- **name**: A unique identifier for this connection.
- **model**: The model identifier (Strix uses LiteLLM format, e.g., `anthropic/claude-3-5-sonnet`).
- **api_key**: Your secret API key. Use `${ENV_VAR}` syntax to keep keys secure.
- **api_base** (Optional): Custom endpoint URL if you are using a proxy or local model (Ollama/vLLM).
- **priority**: Lower numbers mean higher priority. Strix will try providers with priority 1 before priority 2.

## 🛡️ Security & Environment Variables
For security reasons, it is **highly recommended** not to hardcode API keys directly in the YAML file. Instead, set them as environment variables and reference them:

1. Set the variable in your terminal:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```
2. Reference it in `api-config.yaml`:
   ```yaml
   api_key: "${OPENAI_API_KEY}"
   ```

## 🔄 Automatic Failover Logic
Strix uses a smart routing algorithm:
1. **Priority**: It first attempts connections with the lowest `priority` value.
2. **Success Rate**: If a provider fails 3 consecutive times, it is temporarily disabled.
3. **Latency**: Among providers with the same priority, Strix picks the one with the lowest average response time.

## 🧪 Validation
You can verify your configuration by running:
```bash
strix stats
```
This will show you which providers are currently active and their historical performance.
