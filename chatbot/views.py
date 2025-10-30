from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import json
import os

# ✅ Configure Gemini API (make sure GOOGLE_API_KEY is set in your environment)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"reply": "Please enter a message."}, status=400)

            # ✅ Use the latest stable Gemini model
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
            except Exception:
                # fallback if the model name ever changes or is unavailable
                model = genai.GenerativeModel("gemini-2.5-pro")

            # ✅ Generate the assistant response
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
