import os
import logging
from logging import Logger
from src.api.commons.services.llm import LLM
from src.commons.application_settings import ApplicationSettings
from src.api.workflow.faqs_workflow import FaqsWorkflow
# TODO: CREATE APLICATION SETTINGS AND IMPORT 
# TODO: CREATE LLM SERVICES TO IMPORT LLM
# TODO: IMPORT THE CLASS OF FAQS 




# CREATE CONTAINER
class DependencyContainer:

    _LOGGER_NAME = "logger"
    _application_settings: ApplicationSettings = None
    _llm: LLM = None

    # Initialize dependencies 
    @classmethod
    def initilize(cls) -> None:
        cls._initialize_application_settings()
        cls._initialize_logger()
        cls._initialize_llm_manager()

    # application setting to call the env variables
    @classmethod
    def get_application_settings(cls) -> ApplicationSettings:
        return cls._application_settings
    
    # logger
    @classmethod
    def get_logger(cls, module_name = None) -> Logger:

        logger_name = cls._LOGGER_NAME if module_name is None else f"{cls._LOGGER_NAME}.{module_name}"
       
        return logging.getLogger(logger_name)
    
    
    # initialize logger
    @classmethod 
    def _initialize_logger(cls) -> None:
        logger = cls.get_logger()
        logger.setLevel(logging.INFO)

        # console ouput 
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        # format information
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    @classmethod
    def _initialize_application_settings(cls) -> None:
        cls._application_settings = ApplicationSettings()
    
    @classmethod
    def _initialize_llm_manager(cls) -> None:
        cls._llm = LLM()
    

    @classmethod
    def faqs_workflow(cls):

        # Ensure that the application settings are initialized
        if cls._llm is None or cls._application_settings is None:
            raise ValueError("LLM or ApplicationSettings are not initialized")

        # llm 
        llm = cls._llm.get_llm(model_name="gpt-4o", model_api_key=cls._application_settings.openai_api_key)

        return FaqsWorkflow(
            llm=llm
        )
    

    

        