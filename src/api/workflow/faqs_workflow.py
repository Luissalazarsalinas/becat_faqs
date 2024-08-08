import logging
from langchain.base_language import BaseLanguageModel
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
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

    def ai_faqs(self, question:str) -> str:

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


        