from obswebsocket import obsws, requests
import logging

class OBSController:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.client = None
        self.connected = False
        self.logger = logging.getLogger('obs_integration')
        
    def connect(self):
        try:
            self.client = obsws(self.host, self.port, self.password)
            self.client.connect()
            self.connected = True
            self.logger.info("Connected to OBS WebSocket")
            return True
        except Exception as e:
            self.logger.error(f"OBS connection error: {str(e)}")
            self.connected = False
            return False
            
    def disconnect(self):
        if self.connected:
            try:
                self.client.disconnect()
                self.connected = False
                return True
            except:
                pass
        return False
            
    def switch_scene(self, scene_name):
        if not self.connected:
            return False
            
        try:
            self.client.call(requests.SetCurrentProgramScene(sceneName=scene_name))
            self.logger.info(f"Switched to scene: {scene_name}")
            return True
        except Exception as e:
            self.logger.error(f"Scene switch error: {str(e)}")
            return False
            
    def toggle_source(self, source_name, visible=None):
        if not self.connected:
            return False
            
        try:
            current_visibility = self.client.call(
                requests.GetSceneItemEnabled(
                    sceneName=self.client.call(requests.GetCurrentProgramScene()).getName(),
                    sceneItemId=self.get_source_id(source_name)
                )
            ).isEnabled()
            
            new_visibility = not current_visibility if visible is None else visible
            
            self.client.call(
                requests.SetSceneItemEnabled(
                    sceneName=self.client.call(requests.GetCurrentProgramScene()).getName(),
                    sceneItemId=self.get_source_id(source_name),
                    sceneItemEnabled=new_visibility
                )
            )
            
            self.logger.info(f"Source '{source_name}' visibility set to {new_visibility}")
            return True
        except Exception as e:
            self.logger.error(f"Source toggle error: {str(e)}")
            return False
            
    def get_source_id(self, source_name):
        try:
            scene = self.client.call(requests.GetCurrentProgramScene()).getName()
            items = self.client.call(requests.GetSceneItemList(sceneName=scene)).getSceneItems()
            for item in items:
                if item['sourceName'] == source_name:
                    return item['sceneItemId']
            return None
        except:
            return None
            
    def show_overlay(self, message, duration=3):
        if not self.connected:
            return False
            
        try:
            # Implementação simplificada para demonstração
            # Em produção, usar fonte de texto no OBS
            self.logger.info(f"Showing overlay: {message}")
            return True
        except Exception as e:
            self.logger.error(f"Overlay error: {str(e)}")
            return False
