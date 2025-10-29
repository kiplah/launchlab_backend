from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@csrf_exempt
def chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Launchlab's AI assistant, an expert in web design, branding, and software development."},
                {"role": "user", "content": user_message}
            ]
        )

        answer = response.choices[0].message.content
        return JsonResponse({"reply": answer})
    return JsonResponse({"error": "Invalid request"}, status=400)
