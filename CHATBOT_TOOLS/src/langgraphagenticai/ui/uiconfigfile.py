from configparser import ConfigParser

class Config:
    def __init__(self, config_file='./src/langgraphagenticai/ui/configfile.ini'):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_llm_options(self):
        return self.config["Default"].get("LLM_OPTIONS").split(", ")
    
    def get_usecase_options(self):
        return self.config["Default"].get("USECASE_OPTIONS").split(", ")
    
    def get_groq_model_options(self):
        return self.config["Default"].get("GROQ_MODEL_OPTIONS").split(",")
    
    def get_page_title(self):
        return self.config["Default"].get("PAGE_TITLE")