from langchain_groq import ChatGroq
from src.utils.settings import app_settings
from src.dto.ai_schema import BlogGeneratedResponse
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=app_settings.GROQ_API_KEY
)

structured_llm = llm.with_structured_output(BlogGeneratedResponse)
async def llm_invoke(request):
    prompt = f"""
    Generate a blog about:

    {request.topic}

    Requirements:
    - Keep the blog simple and concise.
    - Create a suitable SEO-friendly title.
    - Create a URL-friendly slug.
    - Write a short description.
    - Write the blog content in simple text format only.
    - Create an SEO meta title.
    - Create an SEO meta description.
    - Status should be "draft".
    """

    response = await structured_llm.ainvoke(prompt)
    return {
        "topic": request.topic,
        "content": response
    }