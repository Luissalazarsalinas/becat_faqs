from fastapi import APIRouter, status
from src.api.commons.dependency_container import DependencyContainer
from src.api.workflow.utils.schemas import FaqsRequest

# api router
router = APIRouter(
    prefix='/FAQs',
    tags=['FAQs']
) 


# Create faqs enpoint
@router.post('/IA_FAQs', status_code= status.HTTP_201_CREATED)
async def ia_faqs(request: FaqsRequest):

    results = DependencyContainer.faqs_workflow().ai_faqs(request.question)

    return results
