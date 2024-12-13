import logging
from langchain.base_language import BaseLanguageModel
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from tenacity import retry, wait_exponential, retry_if_exception_type, retry_if_exception_message, stop_after_attempt
from src.api.workflow.utils.faqs_extract import FAQsExtract
from src.api.workflow.utils.prompts import Prompts

# logging 
logger = logging.getLogger(__name__)

class FaqsWorkflow:

    # faqs web scraping
    get_faqs = FAQsExtract()

    # General task
    _task = "Genera una respuesta con la FAQ(de #BeCaT) adecuada, a una consulta realizada."

    def __init__(self, llm:BaseLanguageModel):

        self.llm = llm

    def __chain(self, llm:BaseLanguageModel, system_prompt:str) -> Runnable:

        # prompt
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    system_prompt
                ),
                MessagesPlaceholder(variable_name='messages')
            ]
        )

        chain = prompt | llm

        return chain
    
    @retry(
            stop= stop_after_attempt(3), # intenta maximo tres veces si ocurre algun fallo
            wait= wait_exponential(multiplier=1, min=4, max=10), # espera minimo 4 segundos y maximo 10 segundos
            retry= retry_if_exception_message(match=".*"), # los reintentos se activan con cualquier mensaje de error
    )
    def ai_faqs(self, question:str) -> str:

        try:
            # Get faqs from  becat
            faqs:str = self.get_faqs.get_faqs()
            logger.info("FAQs were obtained with a successful")

            # format the system prompt 
            system_prompt:str = Prompts.prompt(faqs=faqs, question=question)
            # TODO: add a logging message

            # chain
            chain = self.__chain(
                llm=self.llm,
                system_prompt=system_prompt
            )

            # run chain
            logger.debug(f"Processing query: {question}")
            results = chain.invoke({"messages": [HumanMessage(content=self._task)]})
            logger.info("The query was processed with a successful")

            return results.content
        except Exception as e:
            print(f"Any error has ocurred: {e}")
            raise 

        