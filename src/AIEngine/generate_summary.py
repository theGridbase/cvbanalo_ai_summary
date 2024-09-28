from groq import Groq
from .prompts import PreDefinedPrompts

class RAGPrompting:
    def __init__(self, model="mixtral-8x7b-32768"):
        """
        Initialize the RAG/Prompting class with the Groq API.

        :param api_key: API key for authenticating with the Groq service.
        :param model: The model to be used for completion (default is mixtral-8x7b-32768).
        """
        self.client = Groq()
        self.model = model
        self.prompt_messages = []

    def create_prompt(self, 
                      job_title, 
                      experience, 
                      technical_skills=[], 
                      soft_skills=[], 
                      character_limit=300, 
                      tone="formal"):
        """
        Create a tailored prompt based on the user's job description and profile.

        :param job_title: Title of the job.
        :param experience: Years of experience in the field.
        :param education: Educational background (optional).
        :param technical_skills: List of technical skills.
        :param soft_skills: List of soft skills.
        :param tone: Tone of the summary (default is "formal").
        :return: List of prompts for system and user roles.
        """
        system_content = PreDefinedPrompts.system_content(tone, character_limit)
        user_content = PreDefinedPrompts.summary_user_content(job_title, experience, technical_skills, soft_skills)

        self.prompt_messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

        return self.prompt_messages

    def generate_summary(self, temperature=1, max_tokens=300, top_p=0.95, is_stream=True, stop=None):
        """
        Generate a CV summary based on the provided prompts and parameters.

        :param temperature: Sampling temperature (higher means more creative output).
        :param max_tokens: Maximum number of tokens to generate.
        :param top_p: Controls diversity via nucleus sampling.
        :param is_stream: Whether to stream results (default is True).
        :param stop: Optional stop condition.
        :return: Chat object with generated summary.
        """
        if not self.prompt_messages:
            raise ValueError("Prompt messages have not been created. Use create_prompt() first.")

        # Generate the completion
        chat_object = self.client.chat.completions.create(
            model=self.model,
            messages=self.prompt_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=is_stream,
            stop=stop
        )

        summary = ""
        for chunk in chat_object:
            content = chunk.choices[0].delta.content
            if content:
                yield content


if __name__ == "__main__":
    rag_prompting = RAGPrompting()
    print(rag_prompting.create_prompt(
        job_title="Software Engineer",
        experience="5",
        technical_skills=["Python", "Java", "SQL"],
        soft_skills=["Communication", "Problem-solving"],
        character_limit=500,
        tone="formal"
    )
    )

    generated_summary = rag_prompting.generate_summary(temperature=0.7, max_tokens=1024)
    
    summary_text = ""
    for summary_chunk in generated_summary:
        if summary_chunk:
            summary_text += summary_chunk
    
    print(summary_text)
    
    # Example of historical prompt usage
    user_input = "I would like to emphasize my experience in machine learning."
    rag_prompting.prompt_messages.append({"role": "assistant", "content": summary_text})
    rag_prompting.prompt_messages.append({"role": "user", "content": user_input})
    refined_summary = rag_prompting.generate_summary(temperature=0.7, max_tokens=1024)
    
    summary_text = ""
    for summary_chunk in refined_summary:
        if summary_chunk:
            summary_text += summary_chunk
        
    print(summary_text)