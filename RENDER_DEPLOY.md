# 🚀 Render.com Deployment Configuration for Jotica Bible

## 📋 Pre-deployment Checklist

### 1. Environment Variables (Set in Render Dashboard)
- `OPENAI_API_KEY` - Your OpenAI API key for embeddings
- `SUPABASE_URL` - Your Supabase project URL  
- `SUPABASE_SERVICE_ROLE` - Your Supabase service role key

### 2. Render Service Configuration
- **Type**: Web Service
- **Environment**: Docker 
- **Region**: Oregon (recommended for GPU availability)
- **Plan**: Starter (for API) / Standard (for training worker)
- **Branch**: main

### 3. Build & Deploy Commands
```bash
# Build Command (automatically handled by Docker)
# No custom build command needed

# Start Command (set in render.yaml)
python -m src.api.server
```

### 4. Health Check
- **Path**: `/health`
- **Protocol**: HTTP
- **Port**: 8000 (default)

## 🔧 Service Endpoints

Once deployed, your Jotica API will be available at:

- **Root**: `https://your-app.onrender.com/` - Service information
- **Health**: `https://your-app.onrender.com/health` - Health check
- **Docs**: `https://your-app.onrender.com/docs` - Interactive API documentation  
- **Generate**: `https://your-app.onrender.com/generate` - Text generation endpoint
- **Models**: `https://your-app.onrender.com/models` - Available models

## 📡 API Usage Examples

### Generate Biblical Response
```bash
curl -X POST "https://your-app.onrender.com/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Explica Juan 1:1 con citas bíblicas", "max_tokens": 512}'
```

### Check Available Models
```bash
curl "https://your-app.onrender.com/models"
```

## 🔄 Deployment Steps

1. **Connect Repository**: Link your GitHub repo to Render
2. **Set Environment Variables**: Add API keys in Render dashboard
3. **Configure Service**: Use the settings from `render.yaml`
4. **Deploy**: Render will automatically build and deploy
5. **Monitor**: Check logs and health endpoint

## 📊 Resource Requirements

### API Service
- **CPU**: 1-2 cores
- **RAM**: 2-4 GB
- **Storage**: 10 GB (for model caching)
- **Network**: Standard

### Training Worker  
- **CPU**: 2-4 cores (or GPU if available)
- **RAM**: 8-16 GB
- **Storage**: 20-50 GB
- **Network**: High bandwidth for model downloads

## 🛠️ Troubleshooting

### Common Issues
- **Build Timeout**: Increase build timeout in Render settings
- **Memory Errors**: Reduce model size or batch size
- **API Errors**: Check environment variables and logs
- **Model Loading**: Ensure sufficient disk space

### Debug Commands
```bash
# Check service status
curl https://your-app.onrender.com/health

# View logs in Render dashboard
# Logs -> Service Logs

# Test locally with Docker
docker build -t jotica .
docker run -p 8000:8000 jotica
```

## 📈 Scaling Options

### Horizontal Scaling
- Add more web service instances
- Use Redis for job queuing
- Load balance with Render's built-in LB

### Vertical Scaling  
- Upgrade to higher tier plans
- Use GPU instances for training
- Increase memory allocation

## 🔒 Security Considerations

- All API keys set as environment variables (not in code)
- CORS configured for web access
- Health checks for monitoring
- Secure HTTPS endpoints

## 💰 Cost Optimization

### Development
- Use Starter plan for API testing
- Suspend services when not needed
- Monitor usage in dashboard

### Production
- Standard/Pro plans for reliability
- Auto-scaling based on traffic
- Background workers for training jobs

---

**Ready to deploy?** Push to main branch and let Render handle the rest! 🚀