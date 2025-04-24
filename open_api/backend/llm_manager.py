from config import settings
import openai, asyncio

# ─── OpenAI ────────────────────────────────────────────────────────────────────
openai.api_key = settings.OPENAI_API_KEY


# ─── Gemini (Google Generative AI) ────────────────────────────────────────────
genai = None
if settings.ACTIVE_LLM == "gemini" or settings.ACTIVE_LLM != "openai":
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
    except ImportError:
        # Library not installed; we’ll catch this later
        pass


# ─── Public API ───────────────────────────────────────────────────────────────
async def generate_response(message: str) -> str:
    """
    Route the request to the ACTIVE_LLM.  
    Falls back → Gemini if OpenAI fails, then returns a friendly error.
    """
    try:
        if settings.ACTIVE_LLM == "openai":
            return await _generate_openai(message)
        elif settings.ACTIVE_LLM == "gemini":
            return await _generate_gemini(message)
        elif settings.ACTIVE_LLM == "claude":
            return await _generate_claude(message)
        else:
            raise ValueError(f"Unsupported ACTIVE_LLM: {settings.ACTIVE_LLM}")
    except Exception as primary_error:
        print(f"Primary LLM ({settings.ACTIVE_LLM}) failed ▶︎ {primary_error}")
        return await _fallback_gemini(message, primary_error)


# ─── Fallback helpers ─────────────────────────────────────────────────────────
async def _fallback_gemini(message: str, original_error: Exception) -> str:
    if settings.ACTIVE_LLM != "gemini" and genai:
        print("⚠️  Falling back to Gemini…")
        try:
            return await _generate_gemini(message)
        except Exception as ge:
            print(f"Gemini fallback failed ▶︎ {ge}")
    # If we reached here, both services failed:
    return (
        "All AI services are currently unavailable "
        "(OpenAI error + Gemini error). Please try again later."
    )


# ─── Concrete providers ───────────────────────────────────────────────────────
async def _generate_openai(message: str) -> str:
    loop = asyncio.get_event_loop()
    try:
        # run_sync because openai’s Python SDK is blocking
        resp = await loop.run_in_executor(
            None,
            lambda: openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}],
            ),
        )
        return resp.choices[0].message["content"].strip()
    except Exception as e:
        raise RuntimeError(f"OpenAI error: {e}") from e


async def _generate_gemini(message: str) -> str:
    if genai is None:
        raise RuntimeError(
            "Gemini requested but google‑generativeai library is not installed."
        )

    try:
        model = genai.GenerativeModel("models/gemini-pro")  # full ID avoids 404
        # Gemini SDK is synchronous → off‑load to thread to keep FastAPI non‑blocking
        loop = asyncio.get_event_loop()
        resp = await loop.run_in_executor(None, lambda: model.generate_content(message))

        # New SDK versions: resp.text ; older: resp.candidates[0].content.parts[0].text
        return getattr(resp, "text", None) or resp.candidates[0].content.parts[0].text
    except Exception as e:
        # Surface 404 hints clearly
        if "404" in str(e):
            raise RuntimeError(
                "Gemini 404: check model ID ('models/gemini-pro'), API version "
                "('v1beta'), and that Generative Language API is enabled for your key."
            ) from e
        raise RuntimeError(f"Gemini error: {e}") from e


async def _generate_claude(message: str) -> str:
    return "Claude integration not implemented yet."
