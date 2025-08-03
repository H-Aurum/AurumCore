# AurumCore - IA de Moderação para Streamers

![AurumCore Logo](https://via.placeholder.com/150/000000/FFFFFF?text=AurumCore)

AurumCore é um sistema de inteligência artificial para moderação e assistência em transmissões ao vivo, integrado com OBS Studio e plataformas de streaming.

## Recursos Principais
- Moderação inteligente de chat em tempo real
- Integração com OBS Studio via WebSocket
- Controle por interface web (tablet/smartphone)
- Respostas a comandos de voz
- Aprendizado adaptativo ao estilo do streamer

## Instalação no Windows 11

1. **Pré-requisitos**:
   - OBS Studio instalado
   - Conta na Twitch/YouTube

2. **Instalação**:
   ```powershell
   git clone https://github.com/seuusuario/AurumCore.git
   cd AurumCore
   scripts\install_windows.bat
   ```

3. **Configuração**:
   - Edite o arquivo `.env` com suas credenciais
   - Configure o OBS WebSocket:
     - Abra OBS > Ferramentas > WebSocket Server Settings
     - Porta: 4444, Senha: aurum2024 (ou altere no .env)

4. **Execução**:
   ```powershell
   start.bat
   ```

5. **Acesso à interface web**:
   - Abra no navegador: `http://localhost:5000`
   - Ou em outro dispositivo: `http://<IP-DO-PC>:5000`

## Uso Básico

1. **Moderação automática**:
   - O sistema analisa automaticamente as mensagens do chat
   - Mensagens tóxicas são filtradas com base nas preferências

2. **Controle do OBS**:
   - Na interface web:
     - Mude de cenas
     - Ative/desative fontes
     - Controle áudio
   - Por comando de voz:
     - "Aurum, mudar para cena gameplay"
     - "Aurum, desativar microfone"

3. **Configuração da IA**:
   - Acesse `http://localhost:5000/settings`
   - Ajuste o nível de moderação
   - Personalize respostas

## Desenvolvimento

Para contribuir:

```bash
git clone https://github.com/seuusuario/AurumCore.git
cd AurumCore
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m aurumcore.core
```

## Licença
Este projeto está licenciado sob a GNU GPLv3. Veja [LICENSE](LICENSE) para detalhes.
