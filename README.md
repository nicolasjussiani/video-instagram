# Automação de cenas do OBS para Reels

Scripts Python para controlar o OBS Studio pelo WebSocket local e preparar uma cena vertical de rosto e jogo.

## Uso

Requer Windows, Python 3, OBS Studio com o servidor WebSocket habilitado e o plugin `obs-backgroundremoval` instalado separadamente. Instale a biblioteca cliente:

```powershell
python -m pip install websocket-client
python obs_control.py setup-scene.json
```

O script lê a porta e a senha da configuração local do OBS em `%APPDATA%/obs-studio/plugin_config/obs-websocket/config.json`. Esses dados não são distribuídos. A sequência espera uma cena inicial chamada `Cena`; adapte os nomes ao seu OBS. `configure_browser.py` ajusta uma fonte de captura do Edge já existente, chamada `Jogo no navegador`.

Backups pessoais, senhas, capturas da câmera, binários e trechos de referência do plugin foram excluídos. Estes scripts alteram cenas do OBS; faça seu próprio backup antes de executá-los.
