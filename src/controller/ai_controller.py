from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

from src.utils.settings import app_settings
from src.dto.ai_schema import BlogGeneratedResponse

llm = ChatGroq(model="openai/gpt-oss-120b", api_key=app_settings.GROQ_API_KEY)

structured_llm = llm.with_structured_output(BlogGeneratedResponse,method="json_schema")


SYSTEM_PROMPT = """
You are an AI blog content generator for a minimalist blog management system.

Your job is to generate useful, accurate, concise, and readable blog content
based strictly on the user's topic.

Rules:

1. Write for humans first, SEO second.
2. Every sentence must provide useful information.
3. Do not add filler, repetition, or generic statements.
4. Do not invent facts, statistics, studies, quotes, sources, or claims.
5. Stay focused on the requested topic.
6. Do not introduce unrelated topics.
7. Prefer clarity and practical explanations.
8. Keep the article concise.
9. Do not use marketing hype or exaggerated claims.
10. body_content MUST be plain text only.
11. Do NOT use Markdown.
12. Do NOT use HTML.
13. Do NOT use JSON inside body_content.
14. Do NOT use emojis or decorative symbols.
15. Use normal paragraphs and simple section headings where useful.
16. Do not put the title inside body_content.
17. status must always be "draft".

Return only useful content relevant to the requested topic.
"""


async def llm_invoke(request):

    prompt = f"""
Generate a blog post about:

Topic: {request.topic}

Requirements:

- Create a clear and SEO-friendly title.
- Create a lowercase URL-friendly slug using only letters, numbers, and hyphens.
- Write a concise description explaining what the reader will learn.
- Write useful and focused body content.
- Keep body_content in plain text only.
- Do not use Markdown or HTML.
- Use paragraphs and simple section headings where appropriate.
- Keep the article concise.
- Avoid unnecessary sections and repetition.
- Create a meta title of 60 characters or fewer.
- Create a meta description of 160 characters or fewer.
- Set status to "draft".
- Do not generate filler just to make the article longer.
"""

    response = await structured_llm.ainvoke(
        [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)]
    )

    return {"topic": request.topic, "content": response}
