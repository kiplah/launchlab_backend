from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FAQ
from .serializers import FAQSerializer
import google.generativeai as genai
import json
import os

# ✅ Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ==============================
# 💬 CHATBOT ENDPOINT
# ==============================
@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"reply": "Please enter a message."}, status=400)

            try:
                # ✅ Use Gemini model
                model = genai.GenerativeModel("gemini-2.5-flash")
            except Exception:
                model = genai.GenerativeModel("gemini-2.5-pro")

            prompt = (
                "You are LaunchLab's AI assistant, an expert in website design, "
                "development, and branding. Respond helpfully and professionally.\n\n"
                f"User: {user_message}"
            )

            response = model.generate_content(prompt)
            answer = response.text or "Sorry, I couldn’t generate a response."

            return JsonResponse({"reply": answer})

        except Exception as e:
            return JsonResponse({"reply": f"⚠️ Gemini error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


# ==============================
# 📚 FAQ ENDPOINT
# ==============================
@api_view(['GET'])
def get_faqs(request):
    """
    Returns all frequently asked questions.
    You can manage these via Django Admin or API.
    """
    faqs = FAQ.objects.all().order_by('id')
    serializer = FAQSerializer(faqs, many=True)
    return Response(serializer.data)
