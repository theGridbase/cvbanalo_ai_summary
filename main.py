import asyncio 
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from src import RAGPrompting
from src.Session.redis import RedisSessionManager
from src.Schema.request_params import CVRequest, StreamCVRequest, RepromptRequest

app = FastAPI()
session_manager = RedisSessionManager()

@app.post("/create-summary/")
def generate_cv_summary(cv_request: CVRequest):
    try:
        rag_prompting = RAGPrompting()

        # Create the prompt using the incoming request data
        rag_prompting.create_prompt(
            job_title=cv_request.job_title,
            experience=cv_request.experience,
            technical_skills=cv_request.technical_skills,
            soft_skills=cv_request.soft_skills
        )

        # Generate summary
        generated_summary = rag_prompting.generate_summary(temperature=0.7, max_tokens=300)
        summary_text = ''.join(generated_summary)

        # Create a session for the user on the first attempt
        session_data = {
            "job_title": cv_request.job_title,
            "experience": cv_request.experience,
            "technical_skills": cv_request.technical_skills,
            "soft_skills": cv_request.soft_skills,
            "summary": summary_text,
            "messages": [{"role": "user", "content": summary_text}]  # Initialize messages with the summary
        }
        session_id = session_manager.create_session(session_data)

        return {
            "session_id": session_id,
            "generated_summary": summary_text
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refine-summary/")
async def re_prompt(session_request: RepromptRequest):
    try:
        session_data = session_manager.get_session(session_request.session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found.")

        rag_prompting = RAGPrompting()
        
        # Load existing messages
        rag_prompting.prompt_messages = session_data["messages"]

        # Append new user input to the historical messages
        rag_prompting.prompt_messages.append({"role": "user", "content": session_request.user_input})

        # Generate refined summary based on updated messages
        refined_summary = rag_prompting.generate_summary(temperature=0.7, max_tokens=1024)
        refined_summary_text = ''.join(refined_summary)

        # Update session in the session manager
        session_data["summary"] = refined_summary_text
        session_data["messages"] = rag_prompting.prompt_messages
        session_manager.update_session(session_request.session_id, session_data)

        return {
            "session_id": session_request.session_id,
            "refined_summary": refined_summary_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stream-summary/")
async def generate_stream_summary(cv_request: StreamCVRequest):
    try:
        rag_prompting = RAGPrompting()
        
        # Create the prompt using the incoming request data
        rag_prompting.create_prompt(
            job_title=cv_request.job_title,
            experience=cv_request.experience,
            technical_skills=cv_request.technical_skills,
            soft_skills=cv_request.soft_skills,
            character_limit=cv_request.character_limit,
            tone=cv_request.tone
        )

        # Asynchronous generator function to stream chunks
        async def stream_chunks():
            try:
                # Generate summary with streaming enabled
                generated_summary = rag_prompting.generate_summary(temperature=0.7, max_tokens=1024)

                # Stream the generated text chunks
                for summary_chunk in generated_summary:
                    if summary_chunk:
                        # Send each chunk as it is generated
                        yield summary_chunk
                        await asyncio.sleep(0.1)

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        # Return the stream as a plain text response
        return StreamingResponse(stream_chunks(), media_type="text/plain")

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-session/{session_id}")
def get_session(session_id: str):
    session_data = session_manager.get_session(session_id)
    if session_data is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_data

@app.get("/get-all-sessions")
def get_all_sessions():
    return session_manager.get_all_sessions()

@app.get("/clear-sessions")
def clear_sessions():
    session_manager.clear_sessions()
    return {"message": "Sessions cleared"}

@app.delete("/delete-session/{session_id}")
def delete_session(session_id: str):
    session_manager.delete_session(session_id)
    return {"message": "Session deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
