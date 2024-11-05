# Manlingua API (FastAPI) Setup Tutorial
## IMPORTANT NOTES
### About Ollama
Pastiin kalian udah install Ollama. Kalo belom, bisa install dari homebrew dengan command:
```
brew install ollama
```
Atau bisa langsung install secara manual dari websitenya. https://ollama.com/

### Install base LLM model
Setelah Ollama di install, kalian bisa install model LLM yang akan kita pake di terminal. Run command berikut
```
ollama pull qwen2.5
```
**DISCLAIMER: Ini lumayan makan waktu karena donlot model. Intinya jangan pake kuota :)**

Kalo mau testing apakah modelnya dah ke install apa belom, bisa run command ini.
```
ollama run qwen2.5
```
terus untuk quitnya bisa type '/bye' atau Ctrl+D.

### Install custom model buat ollama
Kalau kalian liat ada manlingua2.yaml, itu buat install custom model untuk Ollama.
```
ollama create manlingua-ai -f manlingua2.yaml
```
Disarankan nama modelnya pake 'manlingua-ai' karena di model.py model yg di define itu manlingua-ai. Setelah ini, kalian bisa lanjut ke tahap selanjutnya.

---
## Clone Project
```
git clone https://github.com/paullmich28/Manlingua_PhotoChallengeModel.git
```

## Install Custom Python Environment
```
python -m venv manlingua_api
```
*Notes : Pastiin namanya manlingua_api, karena di gitignorenya kedetectnya itu. Kalo yg lain, nanti pas push ke githubnya takutnya ngikut library2 yg ke install*

## Install Library yg dibutuhin
```
pip install fastapi ultralytics pillow langchain langchain_ollama uvicorn
```

Done, itu aja yg dibutuhin. Happy Coding :)